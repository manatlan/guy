#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os,sys,re,traceback
# #############################################################################
#    Copyright (C) 2019 manatlan manatlan[at]gmail(dot)com
#
# MIT licence
#
# https://github.com/manatlan/guy
# #############################################################################

#python3 -m pytest --cov-report html --cov=guy .



#TODO:
# cookiejar

__version__="0.3"
"""
changelog 0.3:
    - on android : save the cfg in a persistant storage (can reinstall without loose)
    - runner accept a log parameter, default to False
    - manage ctrl-c
    - better runner detection in android/kivy
    - .server(port=8000) : can set a specific port in server mode, else 8000
    - refacto ws.on_message
    - evil script dict
    - no more "guy.use"
    - introduce self (current guy instance), js side !
    - self != guy !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    - no more guy.EXIT()
changelog 0.2:
    - fetch ssl bypass
    - guy.EXIT()
"""
from threading import Thread
import tornado.web
import tornado.websocket
import tornado.platform.asyncio
import tornado.autoreload

import platform
import json
import asyncio
import time
import socket
from datetime import datetime,date
import tempfile
import subprocess
import webbrowser
import concurrent
import inspect
import uuid

class FULLSCREEN: pass
ISANDROID = "android" in sys.executable
LOG=None

GETPATH=os.getcwd
if hasattr(sys, "_MEIPASS"):  # when freezed with pyinstaller ;-)
    GETPATH=lambda: sys._MEIPASS

def isFree(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((ip,port))
    return not (result == 0)


def log(*a):
    if LOG:
        print(" ".join([str(i) for i in a]))

def serialize(obj):
    def toJSDate(d):
        assert type(d) in [datetime, date]
        d = datetime(d.year, d.month, d.day, 0, 0, 0, 0) if type(d) == date else d
        return d.isoformat() + "Z"

    if isinstance(obj, (datetime, date)):
        return toJSDate(obj)
    if isinstance(obj, bytes):
        return str(obj, "utf8")
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    else:
        return str(obj)


def unserialize(obj):
    if type(obj) == str:
        if re.search(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+Z$", obj):
            return datetime.strptime(obj, "%Y-%m-%dT%H:%M:%S.%fZ")
        elif re.search(r"^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ$", obj):
            return datetime.strptime(obj, "%Y-%m-%dT%H:%M:%SZ")
    elif type(obj) == list:
        return [unserialize(i) for i in obj]
    return obj


def jDumps(obj):
    return json.dumps(obj, default=serialize)


def jLoads(s):
    return unserialize(
        json.loads(s, object_pairs_hook=lambda obj: {k: unserialize(v) for k, v in obj})
    )


class JDict:
    def __init__(self, f: str):
        self.__f = f
        try:
            with open(self.__f, "r+") as fid:
                self.__d = (
                    json.load(
                        fid,
                        object_pairs_hook=lambda obj: {
                            k: unserialize(v) for k, v in obj
                        },
                    )
                    or {}
                )
        except FileNotFoundError as e:
            self.__d = {}

    def set(self, k: str, v):
        self.__d[k] = v
        self.__save()

    def get(self, k: str = None):
        return self.__d.get(k, None) if k else self.__d

    def __save(self):
        with open(self.__f, "w+") as fid:
            json.dump(self.__d, fid, indent=4, sort_keys=True, default=serialize)




class GuyJSHandler(tornado.web.RequestHandler):
    def initialize(self, instance):
        self.instance=instance
    async def get(self):
        self.write(self.instance._renderJs())

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, instance):
        self.instance=instance
    #~ async def get(self,page):
    async def get(self):
        self.write(self.instance._render( GETPATH() ))

class ProxyHandler(tornado.web.RequestHandler):
    def initialize(self, instance):
        self.instance=instance
    async def get(self,**kwargs):
        await self._do("GET",None,kwargs)
    async def post(self,**kwargs):
        await self._do("POST",self.request.body,kwargs)
    async def put(self,**kwargs):
        await self._do("PUT",self.request.body,kwargs)
    async def delete(self,**kwargs):
        await self._do("DELETE",self.request.body,kwargs)

    async def _do(self,method,body,qargs):
        url = qargs.get('url')
        if self.request.query:
            url = url + "?" + self.request.query
        headers = {k[4:]: v for k, v in self.request.headers.items() if k.lower().startswith("set-")}

        http_client = tornado.httpclient.AsyncHTTPClient()
        log("PROXY FETCH",method,url,headers,body)
        try:
            response = await http_client.fetch(url, method=method,body=body,headers=headers,validate_cert = False)
            self.set_status(response.code)
            for k, v in response.headers.items():
                if k.lower() in ["content-type", "date", "expires", "cache-control"]:
                    self.set_header(k,v)
            log("PROXY FETCH",response.code,"size=",len(response.body))
            self.write(response.body)
        except Exception as e:
            log("PROXY FETCH ERROR",e,"return 0")
            self.set_status(0)
            self.write(str(e))


async def sockwrite(wsock, **kwargs ):
    try:
        await wsock.write_message(jDumps(kwargs))
    except Exception as e:
        print("Socket write : can't")


async def wsBroadcast(event,args):
    log(">>> Emit ALL:",event,args)
    for i in WebSocketHandler.clients:
        await sockwrite(i,event=event,args=args)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients=[]

    def initialize(self, instance):
        self.instance=instance

    def open(self):
        WebSocketHandler.clients.append(self)

        if hasattr(self.instance,"init"):
            self.instance.init(self.instance)

    def on_close(self):
        WebSocketHandler.clients.remove(self)

    async def on_message(self, message):

        o = jLoads(message)
        log("WS RECEPT:",o)
        method,args,uuid = o["command"],o["args"],o["uuid"]

        if method == "emit":
            event, *args = args
            await wsBroadcast( event=event, args=args )
        else:
            async def execution(function, uuid,mode):
                log("Execute (%s)"%mode,method,args)
                try:
                    ret = await function()
                    ##############################################################
                    if type(ret)==dict and "script" in ret: #evil mode
                        s=ret["script"]
                        del ret["script"]
                        r = dict(result=ret,script=s, uuid=uuid) #evil mode
                    else:
                    ##############################################################
                        r = dict(result=ret, uuid=uuid)
                except concurrent.futures._base.CancelledError as e:
                    r = dict(error="task cancelled", uuid=uuid)
                except Exception as e:
                    r = dict(error=str(e), uuid=uuid)
                    print("=" * 40, "in ", method, mode)
                    print(traceback.format_exc().strip())
                    print("=" * 40)
                log(">>> (%s)"%mode,r)
                await sockwrite(self,**r)

            fct=self.instance._getRoutage(method)

            if asyncio.iscoroutinefunction( fct ):

                async def function():
                    return await self.instance(self,method,*args)

                asyncio.create_task( execution( function, uuid, "ASYNC") )

            else:
                async def function():
                    return self.instance(self,method,*args)

                await execution( function, uuid, "SYNC" )




    def check_origin(self, origin):
        return True



# the webserver is ran on a separated thread
class WebServer(Thread):
    port = 39000
    def __init__(self,instance,host="localhost",port=None):
        super(WebServer, self).__init__()
        self.instance=instance
        self.host=host

        if port is not None:
            self.port = port

        while not isFree("localhost", self.port):
            self.port += 1

    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        tornado.platform.asyncio.AsyncIOMainLoop().install()
        #~ tornado.autoreload.start()
        #~ tornado.autoreload.watch( sys.argv[0] )

        app=tornado.web.Application([
            (r'/ws',            WebSocketHandler,dict(instance=self.instance)),
            (r'/guy.js',        GuyJSHandler,dict(instance=self.instance)),
            (r'/_/(?P<url>.+)', ProxyHandler,dict(instance=self.instance)),
            #~ (r'/(?P<page>.*)',  MainHandler,dict(instance=self.instance)),
            (r'/',  MainHandler,dict(instance=self.instance)),
            (r'/(.*)',          tornado.web.StaticFileHandler, {'path': GETPATH()+"/static/"})
        ])
        app.listen(self.port,address=self.host)

        self.loop=asyncio.get_event_loop()

        async def _waitExit():
            while self._exit==False:
                await asyncio.sleep(0.1)

        self._exit=False
        self.loop.run_until_complete(_waitExit())

        # gracefull death
        tasks = asyncio.all_tasks(self.loop)
        for task in tasks: task.cancel()
        try:
            self.loop.run_until_complete(asyncio.gather(*tasks))
        except concurrent.futures._base.CancelledError:
            pass

    def exit(self):
        self._exit=True

    @property
    def startPage(self):
        return "http://localhost:%s/#%s" % (self.port,self.instance._name) #anchor is important ! (to uniqify ressource in webbrowser)


class ChromeApp:
    def __init__(self, url, size=None, chromeArgs=[]):
        self.__instance = None

        def find_chrome_win():
            import winreg  # TODO: pip3 install winreg

            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
            for install_type in winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE:
                try:
                    with winreg.OpenKey(install_type, reg_path, 0, winreg.KEY_READ) as reg_key:
                        return winreg.QueryValue(reg_key, None)
                except WindowsError:
                    pass

        def find_chrome_mac():
            default_dir = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            if os.path.exists(default_dir):
                return default_dir


        if sys.platform[:3] == "win":
            exe = find_chrome_win()
        elif sys.platform == "darwin":
            exe = find_chrome_mac()
        else:
            for i in ["chromium-browser", "chromium", "google-chrome", "chrome"]:
                try:
                    exe = webbrowser.get(i).name
                    break
                except webbrowser.Error:
                    exe = None

        if exe:
            args = [exe, "--app=" + url] + chromeArgs
            if size == FULLSCREEN:
                args.append("--start-fullscreen")
            if tempfile.gettempdir():
                args.append(
                    "--user-data-dir=%s"
                    % os.path.join(tempfile.gettempdir(), ".guyapp_"+re.sub(r"[^\w\d]","_",url))
                )
            log("CHROME APP-MODE:",args)
            self.__instance = subprocess.Popen(args)
        else:
            raise Exception("no chrome browser, no app-mode !")

    def wait(self):
        self.__instance.wait()

    def exit(self):
        self.__instance.kill()


class ChromeAppCef:
    def __init__(self, url, size=None, chromeArgs=None):  # chromeArgs is not used
        import pkgutil

        assert pkgutil.find_loader("cefpython3"), "cefpython3 not available"

        def cefbrowser():
            from cefpython3 import cefpython as cef
            import ctypes

            isWin = platform.system() == "Windows"

            windowInfo = cef.WindowInfo()
            windowInfo.windowName = "Guy-CefPython3"
            if type(size) == tuple:
                w, h = size[0], size[1]
                windowInfo.SetAsChild(0, [0, 0, w, h])  # not win
            else:
                w, h = None, None

            sys.excepthook = cef.ExceptHook

            settings = {
                "product_version": "Wuy/%s" % __version__,
                "user_agent": "Wuy/%s (%s)" % (__version__, platform.system()),
                "context_menu": dict(
                    enabled=True,
                    navigation=False,
                    print=False,
                    view_source=False,
                    external_browser=False,
                    devtools=True,
                ),
            }
            cef.Initialize(settings, {})
            b = cef.CreateBrowserSync(windowInfo, url=url)

            if isWin and w and h:
                window_handle = b.GetOuterWindowHandle()
                SWP_NOMOVE = 0x0002  # X,Y ignored with SWP_NOMOVE flag
                ctypes.windll.user32.SetWindowPos(
                    window_handle, 0, 0, 0, w, h, SWP_NOMOVE
                )

            # ===---
            def wuyInit(width, height):
                if size == FULLSCREEN:
                    if isWin:
                        b.ToggleFullscreen()  # win only
                    else:
                        b.SetBounds(0, 0, width, height)  # not win

            bindings = cef.JavascriptBindings()
            bindings.SetFunction("wuyInit", wuyInit)
            b.SetJavascriptBindings(bindings)

            b.ExecuteJavascript("wuyInit(window.screen.width,window.screen.height)")
            # ===---

            class WuyClientHandler(object):
                def OnLoadEnd(self, browser, **_):
                    pass  # could serve in the future (?)

            class WuyDisplayHandler(object):
                def OnTitleChange(self, browser, title):
                    try:
                        cef.WindowUtils.SetTitle(browser, title)
                    except AttributeError:
                        print(
                            "**WARNING** : title changed '%s' not work on linux" % title
                        )

            b.SetClientHandler(WuyClientHandler())
            b.SetClientHandler(WuyDisplayHandler())
            log("CEFPYTHON :",url)
            return cef

        self.__instance=cefbrowser()

    def wait(self):
        self.__instance.MessageLoop()

    def exit(self):
        self.__instance.Shutdown()

class Guy:
    _children={}
    size=None
    def __init__(self,*a,**k):
        self._name = self.__class__.__name__
        self._id=self._name+"-"+uuid.uuid4().hex
        self.callbackExit=None      #public callback when "exit"
        self._routes = {
            n: v
            for n, v in inspect.getmembers(self, inspect.ismethod) if not n.startswith("_")
            #~ if not v.__func__.__qualname__.startswith(("Window."))
        }
        for kw in ["init","cfg","fetch","run","runCef","server","on","log","emit","emitMe","exit","parent"]:
            if kw in self._routes: del self._routes[kw]

        #~ self._routes["_cfg_get"]=self._cfg_get
        #~ self._routes["_cfg_set"]=self._cfg_set
        self._routes["exit"]=self.exit

    def run(self,log=False):
        """ Run the guy's app in a windowed env (one client)"""
        global LOG
        LOG=log
        if ISANDROID: #TODO: add executable for kivy/iOs mac/apple
            runAndroid(self)
        else:
            os.chdir( os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0]))) )

            ws=WebServer( self )
            ws.start()

            app=ChromeApp(ws.startPage,self.size)

            def exit():
                ws.exit()
                app.exit()

            self.callbackExit = exit
            try:
                app.wait() # block
            except KeyboardInterrupt:
                print("-Process stopped")

            ws.exit()
            ws.join()

        return self

    def runCef(self,log=False):
        """ Run the guy's app in a windowed cefpython3 (one client)"""
        global LOG
        LOG=log

        os.chdir( os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0]))) )
        ws=WebServer( self )
        ws.start()

        app=ChromeAppCef(ws.startPage,self.size)
        self.callbackExit = app.exit
        try:
            app.wait() # block
        except KeyboardInterrupt:
            print("-Process stopped")
        ws.exit()
        ws.join()
        return self


    def server(self,port=8000,log=False):
        """ Run the guy's app for multiple clients (web mode) """
        global LOG
        LOG=log

        os.chdir( os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0]))) )
        ws=WebServer( self ,"0.0.0.0",port=port )
        ws.start()

        def exit():
            ws.exit()

        self.callbackExit = exit
        print("Running", ws.startPage )

        try:
            import webbrowser
            webbrowser.open_new_tab(ws.startPage)
        except:
            pass

        try:
            ws.join() #important !
        except KeyboardInterrupt:
            print("-Process stopped")
        ws.exit()
        return self

    def exit(self):
        if self.callbackExit: self.callbackExit()

    def cfg_set(self, key, value): setattr(self.cfg,key,value)
    def cfg_get(self, key=None):   return getattr(self.cfg,key)

    @property
    def cfg(self):
        class Proxy:
            def __init__(self):
                if ISANDROID:
                    self.__o=JDict(os.path.join( os.getcwd(),"..","config.json"))
                else:
                    self.__o=JDict(os.path.join( os.getcwd(),"config.json"))
            def __setattr__(self,k,v):
                if k.startswith("_"):
                    super(Proxy, self).__setattr__(k, v)
                else:
                    self.__o.set(k,v)
            def __getattr__(self,k):
                if k.startswith("_"):
                    return super(Proxy, self).__getattr__(k)
                else:
                    return self.__o.get(k)
        return Proxy()


    def _renderJs(self):
        if self.size and self.size is not FULLSCREEN:
            size=self.size
        else:
            size=None
        js = """
document.addEventListener("DOMContentLoaded", function(event) {
    %s
    %s
},true)



function setupWS( cbCnx ) {
    var url=window.location.origin.replace("http","ws")+"/ws"
    var ws=new WebSocket( url );

    ws.onmessage = function(evt) {
      var r = guy._jsonParse(evt.data);
      guy.log("** WS RECEPT:",r)
      if(r.uuid) // that's a response from call py !
          document.dispatchEvent( new CustomEvent('guy-'+r.uuid,{ detail: r} ) );
      else if(r.event){ // that's an event from anywhere !
          document.dispatchEvent( new CustomEvent(r.event,{ detail: r.args } ) );
      }
    };

    ws.onclose = function(evt) {
        guy.log("** WS Disconnected");
        cbCnx(null);
    };
    ws.onerror = function(evt) {cbCnx(null);};
    ws.onopen=function(evt) {
        guy.log("** WS Connected")
        cbCnx(ws);
    }

    return ws;
}

var guy={
    _jsonParse: function(x) {
        function reviver(key, value) {
            const dateFormat = /^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d(\.\d+)?Z$/;
            if (typeof value === "string" && dateFormat.test(value))
                return new Date(value);
            else
                return value;
        }
        return JSON.parse(x, reviver )
    },
    _log: %s,
    log:function(_) {
        if(guy._log) {
            var args=Array.prototype.slice.call(arguments)
            args.unshift("--")

            console.log.apply(console.log,args.map(x => x==null?"NULL":x));
        }
    },
    _ws: setupWS( function(ws){guy._ws = ws; document.dispatchEvent( new CustomEvent("init") )} ),
    on: function( evt, callback ) {     // to register an event on a callback
        guy.log("guy.on:","DECLARE",evt,callback.name)
        document.addEventListener(evt,function(e) { callback.apply(callback,e.detail) })
    },

    emitMe: function( _) {        // to emit to itself
        let ll=Array.prototype.slice.call(arguments)
        let evt=ll.shift()
        guy.log("guy.emitMe:", evt,ll)
        document.dispatchEvent( new CustomEvent(evt,{ detail: ll }) );
    },

    emit: function( _ ) {        // to emit a event to all clients
        var args=Array.prototype.slice.call(arguments)
        guy.log("guy.emit:", args)
        return guy._call("emit", args)
    },
    init: function( callback ) {
        function start() {
            guy.log("guy.init:",callback.name)
            document.removeEventListener("init", start)
            callback()
        }
        if(guy._ws.readyState == guy._ws.OPEN)
            start()
        else
            document.addEventListener("init", start)
    },
    _call: function( method, args ) {
        guy.log("guy.call:","CALL",method,args)
        var cmd={
            command:    method,
            args:       args,
            uuid:       method+"-"+Math.random().toString(36).substring(2), // stamp the exchange, so the callback can be called back (thru customevent),
        };

        if(guy._ws) {
            guy._ws.send( JSON.stringify(cmd) );

            return new Promise( function (resolve, reject) {
                document.addEventListener('guy-'+cmd.uuid, function handler(x) {
                    guy.log("guy.call:","RESPONSE",method,"-->",x.detail)
                    this.removeEventListener('guy-'+cmd.uuid, handler);
                    var x=x.detail;
                    if(x && x.result!==undefined) {
                        if(x.script)
                            resolve( eval(x.script) )
                        else
                            resolve(x.result)
                    }
                    else if(x && x.error!==undefined)
                        reject(x.error)
                });
            })
        }
        else
            return new Promise( function (resolve, reject) {
                reject("not connected");
            })
    },
    fetch: function(url,obj) {
        guy.log("guy.fetch:", url, "body:",obj)

        var h={"cache-control": "no-cache"};    // !!!
        if(obj && obj.headers)
            Object.keys(obj.headers).forEach( function(k) {
                h["set-"+k]=obj.headers[k];
            })
        var newObj = Object.assign({}, obj)
        newObj.headers=h;
        newObj.credentials= 'same-origin';
        return fetch( "/_/"+url,newObj )
    },
    cfg: new Proxy({}, {
      get: (obj, prop) => {
        return guy._call("cfg_get",[prop])
      },
      set: (obj, prop, value) => {
        return guy._call("cfg_set",[prop,value]);
      },
    }),
    exit: function() {guy._call("exit",[])},

    _instanciateWindow: async function(o) {
        guy.log("Window "+o.name+":","Instanciate, routes=",o.routes);

        self={
            parent: self,
            _promise: new Promise( function (resolve, reject) {
                guy.on(o.event, function(r) {
                    guy.log("Window "+o.name+":","Exited, return = ",r)
                    self._div.parentNode.removeChild(self._div);
                    self=self.parent;
                    resolve( guy._jsonParse(r) )
                })
            }),
            _div: (function(html){
                var x=document.createElement("div");
                x.innerHTML = html
                document.body.appendChild(x);
                return x;
            })(o.html),
            exit: function() {guy.emitMe(o.event, null)},
            run: function() {
                guy.log("Window "+o.name+":","Running")
                return self._promise;
            },
        }

        for(var key of o.routes) {
            (function _(key,id) {
                self[key]=function(_) {return guy._call(id+"."+key, Array.prototype.slice.call(arguments) )}
            })(key,o.id);
        }

        if(o.scripts) eval(o.scripts)
        return self;
    },

};

var self={};


""" % (
        size and "window.resizeTo(%s,%s);" % (size[0], size[1]) or "",
        'if(!document.title) document.title="%s";' % self._name,
        "true" if LOG else "false"
    )

        for k in self._routes.keys():
            if k in ["cfg_get","cfg_set"]: continue
            js += (
                """\nself.%s=function(_) {return guy._call("%s", Array.prototype.slice.call(arguments) )};"""
                % (k, k)
            )
        return js

    async def emit(self, event, *args):
        await wsBroadcast(event=event, args=args)

    def _getRoutage(self,method):
        function=None
        if "." in method:
            id,method = method.split(".")
            for i in self._children.values():
                if i._id == id:
                    log("METHOD CHILD",i._name,method)
                    function=i._routes[method]
        else:
            log("METHOD SELF",method)
            function=self._routes[method]
        return function

    def __call__(self,wsock,method,*args):  #TODO: remove unused wsock

        async def emitMe(event, *args):
            log(">>> emitMe",event,args)
            try:
                await sockwrite(wsock,event=event,args=args)
            except Exception as e:
                print("Socket write : can't")

        function = self._getRoutage(method)

        x=inspect.signature(function )
        if "emitMe" in x.parameters:
            ret= function(*args,**dict(emitMe=emitMe))
        else:
            ret= function(*args)

        if isinstance(ret,Guy):
            ################################################################
            self._children[ ret._name ]=ret
            o=ret

            routes=[k for k in o._routes.keys() if not k.startswith("_")]

            eventExit="event-"+o._id+".exit"
            def exit():
                log("USE %s: EXIT" % o._name,o._json)
                asyncio.create_task(emitMe(eventExit,o._json))

            html=o._render(GETPATH(),includeGuyJs=False)
            scripts=";".join(re.findall('(?si)<script>(.*?)</script>', html))

            o.callbackExit=exit
            if hasattr(o,"init"): o("init")
            obj=dict(
                id=o._id,
                name=o._name,
                html=html,
                routes=routes,
                event=eventExit,
                scripts=scripts,

                script="guy._instanciateWindow(x.result)"
            )
            return obj
            ################################################################

        return ret

    def _render(self,path,includeGuyJs=True,page=None):
        #~ chpages=[i for i in self.children if i.__class__.__name__==page]
        #~ if chpages:
            #~ return chpages[0]._render(path=path,includeGuyJs=includeGuyJs,page=None)
        #~ else:
        html=self.__doc__

        def rep(x):
            d=self.__dict__
            d.update(self.__class__.__dict__)
            for rep in re.findall("<<[^><]+>>", x):
                var = rep[2:-2]
                if var in d:
                    o=d[var]
                    if type(o)==str:
                        x=x.replace(rep, o)
                    else:
                        x=x.replace(rep, jDumps( o ))
            return x


        if html:
            if includeGuyJs: html="""<script src="guy.js"></script>"""+ html
            return rep(html)
        else:
            f=os.path.join(path,"static","%s.html" % self._name)
            if os.path.isfile(f):
                with open(f,"r") as fid:
                    return rep(fid.read())
            else:
                return "ERROR: can't find '%s'" % f

    @property
    def _json(self):
        """ return a json representation of the inner attributs of this"""
        obj={k:v for k,v in self.__dict__.items() if not (k.startswith("_") or callable(v))}
        for i in ["callbackExit","__doc__","_children","size"]:
            if i in obj: del obj[i]
        return jDumps(obj)


def runAndroid(ga):
    import kivy
    from kivy.app import App
    from kivy.utils import platform
    from kivy.uix.widget import Widget
    from kivy.clock import Clock
    from kivy.logger import Logger

    def run_on_ui_thread(arg):
        pass

    webView       = None
    webViewClient = None
    #~ webChromeClient = None
    activity      = None
    if platform == 'android':
        from jnius import autoclass
        from android.runnable import run_on_ui_thread
        webView       = autoclass('android.webkit.WebView')
        webViewClient = autoclass('android.webkit.WebViewClient')
        #~ webChromeClient = autoclass('android.webkit.WebChromeClient')
        activity      = autoclass('org.kivy.android.PythonActivity').mActivity



    class Wv(Widget):
        def __init__(self, guyWindow ):
            self.f2 = self.create_webview # important
            super(Wv, self).__init__()
            self.visible = False

            def exit():
                activity.finish()
                App.get_running_app().stop()
                os._exit(0)

            guyWindow.callbackExit = exit

            self.ws=WebServer( guyWindow )
            self.ws.start()

            Clock.schedule_once(self.create_webview, 0)

        @run_on_ui_thread
        def create_webview(self, *args):
            webview = webView(activity)
            webview.getSettings().setJavaScriptEnabled(True)
            webview.getSettings().setDomStorageEnabled(True)
            webview.setWebViewClient(webViewClient())
            #~ webview.setWebChromeClient(webChromeClient())
            activity.setContentView(webview)
            webview.loadUrl(self.ws.startPage)

    class ServiceApp(App):
        def build(self):
            return Wv( ga )

    ServiceApp().run()



if __name__ == "__main__":

    #~ from testTordu import Tordu as GuyApp
    from testPrompt import Win as GuyApp
    GuyApp().run()
    #~ GuyApp().server(8000)

