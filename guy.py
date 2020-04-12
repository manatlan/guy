#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# #############################################################################
#    Apache2 2019-2020 - manatlan manatlan[at]gmail(dot)com
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#        http://www.apache.org/licenses/LICENSE-2.0
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    more: https://github.com/manatlan/guy
# #############################################################################

#python3.7 -m pytest --cov-report html --cov=guy .

#TODO:
# logger for each part
# cookiejar

__version__="0.6.0" #autoreload's version !

import os,sys,re,traceback,copy,types
from urllib.parse import urlparse
from threading import Thread
import tornado.web
import tornado.websocket
import tornado.platform.asyncio
import tornado.autoreload
import tornado.httpclient
import websocket
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
import logging
import io

class FULLSCREEN: pass
ISANDROID = "android" in sys.executable
FOLDERSTATIC="static"
class JSException(Exception): pass

handler = logging.StreamHandler()
handler.setFormatter( logging.Formatter('-%(asctime)s %(name)s [%(levelname)s]: %(message)s') )
logger = logging.getLogger("guy")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

handler.setLevel(logging.ERROR)

def isFree(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return not (s.connect_ex((ip,port)) == 0)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#
https={}
def http(regex): # decorator
    if not regex.startswith("/"): raise Exception("http decoraton, path regex should start with '/'")
    def _(method):
        https["^"+regex[1:]+"$"] = method
    return _

async def callhttp(web,path): # web: RequestHandler
    for name,method in https.items():
        g=re.match(name,path)
        if g:
            if asyncio.iscoroutinefunction( method ):
                ret=await method(web,*g.groups())
            else:
                ret=method(web,*g.groups())
            if isinstance(ret,Guy):
                ret.parent = web.instance
                web.write( ret._renderHtml() )
            return True
#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#


class readTextFile(str):
    filename=None
    encoding=None
    def __new__(cls,fn:str):
        for e in ["utf8","cp1252"]:
            try:
                with io.open(fn,"r",encoding=e) as fid:
                    obj=str.__new__(cls,fid.read())
                    obj.filename=fn
                    obj.encoding=e
                    return obj
            except UnicodeDecodeError:
                pass
        raise Exception("Can't read '%s'"%fn)

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
    async def get(self,id):
        o=INST.get( id )
        if o:
            self.write(o._renderJs())
        else:
            raise tornado.web.HTTPError(status_code=404)

INST={}

class FavIconHandler(tornado.web.RequestHandler):
    def initialize(self, instance):
        self.instance=instance
    async def get(self):
        self.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x00@\x08\x06\x00\x00\x00\xaaiq\xde\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe4\x04\x0c\x0e-0\xf2:\xad\x05\x00\x00\x00\x1diTXtComment\x00\x00\x00\x00\x00Created with GIMPd.e\x07\x00\x00\x05\xf5IDATx\xda\xe5\x9b_\x88TU\x1c\xc7?\xbf3\x9b\xd4\x16n\x14\x06EP\x10\xe62[\xee\xae\xe3\x1f\xac\x07\xa1\xc8\x97\xc4\x82\x9e,C\xc6\xd6\xad\x85J\x84PL\xf2:\x9aI\x12\xd5\xa6%m\xd8\x1a\x8a\x04\xbdD\xf8\xa6F\x05A5\xbb\x9b\x8a\xfbG1\xa8\x08\xab\x87(#B\xddeN\x0fwf\x9d;s\xe7\xce\xb9g\xee\x9d?t\x1eg\xce\xfd\x9d\xf3\xf9\x9e\xdf\xfd\x9d\xdf\xf9\x9d\x19\xa1\x86\x96]\xa7Y\xf2\x91x>\x1b\xed\xd7\xf7\x00w\x03w\x02\xb7\x03\xf3\x80[\x80\xb9\xc0M@\xbb(\xe6 \xb4\x01\x02h`\x06\xb8\n\xfc\x0b\xfc\x03\\\x12\xc5\x1f\xc0\xef\xc0E\xe0g\xe0\x87\xdew\xe5W"nb\xfb\xe0h\x9f\xbe\x11X\n,\x03V\x00\xcbQtT\x1dP\x19\x8c* \x95\xfb\\\x00\xbe\x06\xbe@\x91\xed\xdd\'\xe3\x00#\x1b4\x8b?\x90\xe8\x05\x18Ik\x16\x0f\xbb\xddF\xd6\xeb\xf9\xc0\xa3\x08\xcf\x8a\xd0\xe9\xe9\xa8\xccF\x13\x83~&}J\xc6\xfbD\x14\xc3\xc0\xc9\x9eA\xb9\x1a\x89\x00\xd9\xb4f\xc9\xb00\xf2\xb4V\\\xc7c\xc0~\xe0\x0e\xdf\xd5i,|\xa9\xc7\x1c\x02\xf6\xf6\x0c\xcad\xcd\x1e\x90M\xeb\xb5"\x1c\x0e\x9c`s\xc1\x17\xb7\xef\x81\'{\x06e\xea\xd4FM\xcf\xa0T\x17\xa0\xb0\xea\xd9\xb4\xee\x04\xce\x8a\x90hQ\xf8\xe2vD\x84\xbe\xee\xb7\xe5J\xa0\xc9"\xf8\r\xc0dUxi\txD\xb1\x16\xe1\xf2\xe9M\xfa^\x80\xd3\x9bt\xb9\xd9"\xf8\xdd\xc0P\xa9a_x\x89\x06\xcc\n\x1ec\xf8\xe2v\xee\xf4&\xfdH\xf7[\xc2\x99\x97t\xf9:f\xd3z\x00x\xaf\xd4\xb85|"Fx[a\xddy\xaf\xec~S\x8e{>\xca\xa6\xf5\x02`\xea\x7f\x00_\xf8n\xfe\xc27\xe4B\xf1\x10\x07C\xc0\xefC\xb3\x14\xe8\x05v\x03\xd3\xb1\xc0Kl\xf0\xa0\xf8\x16\xe0\xccf\x8dd\xd3z>p\xde\x00\xfeC`CjHr\x9e\x8c\xf0y\rW\xd9\x0edZ`\xe5\x8bm\xf7-\xdc+\x07\x95\x08\xab\x03\xe1]#GSC\xf2L)<\xb8\xeb\x9f\x1a\x92\x9d\x92\xc0izx\xafW\xbdS\x18\xee\xfe@#\x8a\xcb\xa9!yjl@\xfb\x0e\x9cz_\x18\x1b\xd0,: ;\x81\xf3M\r\xef\x15\xa0\xfd\xccf\xfd\x80\x02\xae\x0f\x80\x07\xf8\x14`\xd1\x81\xca\xd1\xaf\xe8\xbb\xe1\x16\x81/\xb4\x95\n\x98\t\x80\x078\x1a\xe2l\xf1e\x0b\xc1\x03t\xab*\xf0\x00WB\x080]\xafh\xef\x0b\x15\x0e\x1e\xe06\x95/H\x04\xad\xc6\xe3\xa3\xfd\xba\xea|\xf21bY\xd8T\x19\xb1\x83/\xcb\x04\xa5$C4\xcbY\xa6\xbd\x02\xf8\x0f\xbe.5T\xddR>\x0e\xa4\x8d\xf3\xf4\xb8\xe0%T\xc26\xad\x0cNv\xed\xa3\xfdz[\xbe\xdc\x15\xe4\x01k\x80T\x0b\xc1\xcfbk\x83c\xed\xabc\x03\xfa\x85RO\x18}N\x17\xe0\x9f\x00\x8e6\n\x1eKx\x00\x19\xed\xd7\x87\x80u\x86u\xbc1`\x1f0\x92/dv\x03\x03\xc0\n[x\x94\xc1\x9c\xab\xc0\xcf~\xa7\xc2\xc1\x03\'\xda\xca\x82`\xf0\xa4\x17U\xdc\xebM\x83^Xxb\x837x,\xee\x82\x06\x16\xb6#\x84\xbf\x16\x03\x9a\xb7\x9a\x13\r\xbc\n\x95\x8359<\x16\xf0\x12<=\xddR\xf0*:x_\x01\x9a\xac\x8eg\ro\xba%z\x04h\xca\x82\x86%\xbc\xd1<\x816\xdc\x0b\xc9\xbf\x1aX\xca\xba\xd9\xa2\x9a\x13\t\xbc\xe9\x91%\xd6vj\xa3\x9e\x11E\xa2\x11\xf0\xc0\t\xd5`\xf8\x86\xad<!L\xd7\xb7\xd5\x11\xbe\xe1\x02\x94]X\x06\x171k\x8bM>;\x92(h;\xbbM\x0f\x16\x0eC:\x17\xde\x90\xceU=M\xb8-W\xd4\x1f\xcf3\t\xcbj\x8e\xf5\xcaK\x91\xed6\xdc\xa2hGa\xf0\xb0"\xcc>\xa3\r|-W\xd4_\x8a\x9ei\x10\xbc\xef+`eT\x19\xba\xab\xaa\x0c\x1a\n\x9eh\xe0\xdd)\xa9\x88\x8c\x9b\x8a \xe5c\x84\xac\xe3\x19%l&\xf0HaM,\xd3V+\x11JV]j\xa8\xe6\xd8\xec.\xa5\xf3P\xb5\x1e\\j\x15\xa1\x1e\xf0A\xb7\xdc*\x8a\xd3\x9bu\xca\xdc`x\x7f\xe7\x8fJ\x84DHOh\x00<\x80\xc9\xcdP\xbc\x9e\xd0@xQyTS\x11\x90\xfa\x01\xd4\x03\xde\x83\x19t(\xa9eg\xb0\xde\xb6\xea\x00_\xb6\xcea\x1f\x8e\x0b\xc8z\x0c\x8b\xf9\xab(\x8cD)\x82qBe"\x9a\xc1\xbc\x15%W\xda\x15E ~\x11\xac\xe1\xc50\x86\x95\xb7\x19\x05\\2RT\xc5+\x82-|\xa5\xeb6\xc3]\xeco\x05\xfcb\xecVq\x89 \xf6\xf0b\x0f\x0fpQ\x01\x93\xa1\xde\xad\xa8E\xb0\xad\xe6\xd4\x0e\x0fpN\x01\xdf\x85\x0e0Q\x8a\xd08x\x80\xac\x00\x8c\xef\xd0Sh\x16\x18U\x7f|\xaa<\x81}\xa2n\xd1\xc1\xd3\x95\x11W\x7f\x11\xf6cy\xbd\x1dG\xfa[\x13\xbca\xc2&\t\x8e\x00\xa8\x89\x9d\x1ar\x1c\x14\x83@$b&B,\xa5VSx\xd3\x1b(\xcd\xa0gM\'2:\x03l\xd7\x9a\xaa\xf5=\xdf>1\xbe\x0e\xa6\xc2\x87\xb8~\xfb&\xe9\xc8\xf2Y3\x13\x19M\xd2\x11\xa7\xe2`1N\xa8\x01\xf0\x00k<\xa6\x92\xce\xec\x08\xf75\x93\x081\xc1\xafO:\xf2\xa3\xaf\xb9\xa4#\xe3\xc0J\xe3@"f\xef\x7fT\x15\xdc\x08\xe0\xf7&\x1d\x19\x9e\xd8U\xe1\xa7\x91\x13\xbb4IG\x8e\x03\x0fZ\x18\xaf92{6\x1b\x89\xe6<R\xd4g[\xd2\x91-\x13\x19M\xf2\x15\xa9rDp\xe3\xc2<\xe0+\xa0\xd3$\x98\xf9\xf6)\xfdL\xe7\x03h\x0c\xc7\xda*v\x1eN:\xf2\xf9\xf8\x0eM\xd7\x0e18#y\x85X\r\x1c\xd69\xe6\xd6C\x84\x88\xe1\xf7\x90\xc3Ifdz\xea\xf5\x1c\x9d[\x94\x89\xb3^kS\xafi\x92\x8e|\x96t\xa4\x03\xe1!\xe0\xe3\x9a_\x87\x80,-"\xf8\x9f\x80\x17\x81\xf6\xa4#/\xa3\xdc\xe3\xbe\x1f\xfcV\x8e]3\xbf\x95c\xeca\x95\xd1;:\xee\xe8^\xdc_\x86w\x01w\x01\xb7\x02s\ns\xd49n@\xd3\x81{\xef(\xb3\x9e \x95\xbd\xc5\x02~\x1a\xf8\x13\xf7\xaf\xf5\x93@\x168\xd9\x95\x91\xdf\xf2s\xa4+S\xd9\xc1\xb7rL\xf6\xb0J\xff\x07\xf42b\xc4\x0f\x9fW\xda\x00\x00\x00\x00IEND\xaeB`\x82')

class MainHandler(tornado.web.RequestHandler):

    def initialize(self, instance):
        self.instance=instance
    async def get(self,page): # page doesn't contains a dot '.'
        #####################################################
        if not await callhttp(self,page):
        #####################################################
            if page=="" or page==self.instance._name:
                logger.debug("MainHandler: Render Main Instance (%s)",self.instance._name)
                self.write( self.instance._renderHtml() )
            else:
                chpage=self.instanciate(page) # auto-instanciate each time !
                chpage.parent = self.instance
                if chpage:
                    logger.debug("MainHandler: Render Children (%s)",page)
                    self.write( chpage._renderHtml() )
                else:
                    raise tornado.web.HTTPError(status_code=404)

    async def post(self,page): # page doesn't contains a dot '.'
        await self._callhttp(page)
    async def put(self,page): # page doesn't contains a dot '.'
        await self._callhttp(page)
    async def delete(self,page): # page doesn't contains a dot '.'
        await self._callhttp(page)
    async def options(self,page): # page doesn't contains a dot '.'
        await self._callhttp(page)
    async def head(self,page): # page doesn't contains a dot '.'
        await self._callhttp(page)
    async def patch(self,page): # page doesn't contains a dot '.'
        await self._callhttp(page)

    def instanciate(self,page):
        declared = {cls.__name__:cls for cls in Guy.__subclasses__()}
        gclass=declared[page]
        logger.debug("MainHandler: Auto instanciate (%s)",page)
        x=inspect.signature(gclass.__init__)
        args=[self.get_argument(i) for i in list(x.parameters)[1:]]
        return gclass(*args)

    async def _callhttp(self,page):
        if not await callhttp(self,page):
          raise tornado.web.HTTPError(status_code=404)



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
        url = str(qargs.get('url'))
        if not urlparse(url.lower()).scheme:
            url="http://%s:%s/%s"% (self.instance._webserver[0],self.instance._webserver[1],url.lstrip("/")) 

        if self.request.query:
            url = url + "?" + self.request.query
        headers = {k[4:]: v for k, v in self.request.headers.items() if k.lower().startswith("set-")}

        http_client = tornado.httpclient.AsyncHTTPClient()
        logger.debug("PROXY FETCH (%s %s %s %s)",method,url,headers,body)
        try:
            response = await http_client.fetch(url, method=method,body=body,headers=headers,validate_cert = False)
            self.set_status(response.code)
            for k, v in response.headers.items():
                if k.lower() in ["content-type", "date", "expires", "cache-control"]:
                    self.set_header(k,v)
            logger.debug("PROXY FETCH, return=%s, size=%s",response.code,len(response.body))
            self.write(response.body)
        except Exception as e:
            logger.debug("PROXY FETCH ERROR (%s), return 0",e)
            self.set_status(0)
            self.write(str(e))


async def sockwrite(wsock, **kwargs ):
    if wsock:
        try:
            await wsock.write_message(jDumps(kwargs))
        except Exception as e:
            logger.error("Socket write : can't:%s",wsock)
            if wsock in WebSocketHandler.clients: del WebSocketHandler.clients[wsock]


async def emit(event,*args):
    logger.debug(">>> Emit ALL: %s (%s)",event,args)
    for i in list( WebSocketHandler.clients.keys() ):
        await sockwrite(i,event=event,args=args)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    clients={}
    returns={}

    def initialize(self, instance):
        self.instance=instance

    def open(self,id):
        o=INST.get( id )
        if o:
          logger.debug("Connect %s",id)
          o._connect( self ) # provok l'appel de l'init
          WebSocketHandler.clients[self]=o
        else:
          logger.debug("CAN't Connect %s",id)

    def on_close(self):
        o=WebSocketHandler.clients[self]
        logger.debug("Disconnect %s",o._id)
        if o._id!=self.instance._id: # avoid to remove the main instance
          del INST[o._id]
        del WebSocketHandler.clients[self]

    async def on_message(self, message):

        instance = WebSocketHandler.clients[self]

        o = jLoads(message)
        logger.debug("WS RECEPT: %s",o)
        method,args,uuid = o["command"],o.get("args"),o["uuid"]

        if method == "emit":
            event, *args = args
            await emit( event, *args )  # emit all
        elif method == "return":
            logger.debug(" as JS Response %s : %s",uuid,args)
            WebSocketHandler.returns[uuid]=args
        else:
            async def execution(function, uuid,mode):
                logger.debug(" as Execute (%s) %s(%s)",mode,method,args)
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
                    logger.error("================================= in %s %s", method, mode)
                    logger.error(traceback.format_exc().strip())
                    logger.error("=================================")
                logger.debug(">>> (%s) %s",mode,r)
                await sockwrite(self,**r)

            fct=instance._getRoutage(method)

            if asyncio.iscoroutinefunction( fct ):

                async def function():
                    return await instance(method,*args)

                #asyncio.create_task( execution( function, uuid, "ASYNC") )  #py37
                asyncio.ensure_future ( execution( function, uuid, "ASYNC") ) #py35

            else:
                async def function():
                    return instance(method,*args)

                await execution( function, uuid, "SYNC" )

    def check_origin(self, origin):
        return True


class WebServer(Thread): # the webserver is ran on a separated thread
    port = 39000
    def __init__(self,instance,host="localhost",port=None,autoreload=False):
        super(WebServer, self).__init__()
        self.app=None
        self.instance=instance
        self.host=host
        self.autoreload=autoreload

        if port is not None:
            self.port = port

        while not isFree("localhost", self.port):
            self.port += 1

        self.instance._webserver=(self.host,self.port)

        try: # https://bugs.python.org/issue37373 FIX: tornado/py3.8 on windows
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except:
            pass

    def run(self):
        statics = os.path.join( self.instance._folder, FOLDERSTATIC)

        asyncio.set_event_loop(asyncio.new_event_loop())
        tornado.platform.asyncio.AsyncIOMainLoop().install()
        if self.autoreload:
            print("**AUTORELOAD**")
            tornado.autoreload.start()
            tornado.autoreload.watch( sys.argv[0] )
            if os.path.isdir(statics):
                for p in os.listdir( statics ) :
                    tornado.autoreload.watch(os.path.abspath(os.path.join(statics, p)))

        self.app=tornado.web.Application([
            (r'/_/(?P<url>.+)',             ProxyHandler,dict(instance=self.instance)),
            (r'/(?P<id>[^/]+)-ws',          WebSocketHandler,dict(instance=self.instance)),
            (r'/(?P<id>[^/]+)-js',          GuyJSHandler,dict(instance=self.instance)),
            (r'/(?P<page>[^\.]*)',          MainHandler,dict(instance=self.instance)),
            (r'/favicon.ico',               FavIconHandler,dict(instance=self.instance)),
            (r'/(.*)',                      tornado.web.StaticFileHandler, dict(path=statics ))
        ])
        self.app.listen(self.port,address=self.host)

        self.loop=asyncio.get_event_loop()

        async def _waitExit():
            while self._exit==False:
                await asyncio.sleep(0.1)

        self._exit=False
        self.loop.run_until_complete(_waitExit())

        # gracefull death
        try:
            tasks = asyncio.all_tasks(self.loop) #py37
        except:
            tasks = asyncio.Task.all_tasks(self.loop) #py35
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
    def __init__(self, appname="driver",size=None,lockPort=None):

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

        if lockPort:
            debugport=lockPort
        else:
            debugport = 9222
            while not isFree("localhost", debugport):
                debugport += 1

        if not exe:
            raise Exception("no chrome browser, no app-mode !")
        else:
            args = [ #https://peter.sh/experiments/chromium-command-line-switches/
                exe,
                "--remote-debugging-port=%s" % debugport,
                "--app=http://localhost:%s" % debugport,
                "--aggressive-cache-discard",
                "--disk-cache-dir=MYCACHE",
                "--user-data-dir=MYCACHE/%s%s" % (appname,debugport),
                "--app-id=%s%s" % (appname,debugport),
                "--app-auto-launched",
                "--no-first-run",
                "--no-default-browser-check",
            ]
            if size:
                if size == FULLSCREEN:
                    args.append("--start-fullscreen")
                else:
                    args.append( "--window-size=%s,%s" % (size[0],size[1]) )

            logger.debug("CHROME APP-MODE: %s"," ".join(args))
            self._p = subprocess.Popen(args, stdout=subprocess.PIPE)

            http_client = tornado.httpclient.HTTPClient()
            self._ws = None
            while self._ws == None:
                try:
                    url = http_client.fetch("http://localhost:%s/json" % debugport).body
                    self._ws = json.loads(url)[0]["webSocketDebuggerUrl"]
                except Exception as e:
                    self._ws = None

    def wait(self):
        self._p.wait()

    def __del__(self): # really important !
        self._p.kill()

    def _com(self, payload: dict):
        """ https://chromedevtools.github.io/devtools-protocol/tot/Browser/#method-close """
        payload["id"] = 1
        try:
            ws = websocket.create_connection(self._ws)
            ws.send(json.dumps(payload))
            r=ws.recv() 
            ws.close()
            return json.loads(r)["result"] or True
        except:
            logger.debug("ChromeApp._com(): Can't communicate with chrome instance")
            return False

    def isRunning(self):
        info=self._com(dict(method="Page.getNavigationHistory"))
        return not info["currentIndex"]<0

    def focus(self):
        return self._com(dict(method="Page.bringToFront"))

    def navigate(self, url):
        return self._com(dict(method="Page.navigate", params={"url": url}))

    def exit(self):
        self._com(dict(method="Browser.close"))
        self._p.kill()



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
                "product_version": "Guy/%s" % __version__,
                "user_agent": "Guy/%s (%s)" % (__version__, platform.system()),
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
            def guyInit(width, height):
                if size == FULLSCREEN:
                    if isWin:
                        b.ToggleFullscreen()  # win only
                    else:
                        b.SetBounds(0, 0, width, height)  # not win

            bindings = cef.JavascriptBindings()
            bindings.SetFunction("guyInit", guyInit)
            b.SetJavascriptBindings(bindings)

            b.ExecuteJavascript("guyInit(window.screen.width,window.screen.height)")
            # ===---

            class GuyClientHandler(object):
                def OnLoadEnd(self, browser, **_):
                    pass  # could serve in the future (?)

            class GuyDisplayHandler(object):
                def OnTitleChange(self, browser, title):
                    try:
                        cef.WindowUtils.SetTitle(browser, title)
                    except AttributeError:
                        logger.warning(
                            "**WARNING** : title changed '%s' not work on linux",title
                        )

            b.SetClientHandler(GuyClientHandler())
            b.SetClientHandler(GuyDisplayHandler())
            logger.debug("CEFPYTHON : %s",url)
            return cef

        self.__instance=cefbrowser()

    def wait(self):
        self.__instance.MessageLoop()

    def exit(self):
        self.__instance.Shutdown()


async def doInit( instance ):
    instance._rebind() # WTF ?: need to call this
    if hasattr(instance,"init"):
        self_init = getattr(instance, "init")
        if asyncio.iscoroutinefunction( self_init ):
            await self_init(  )
        else:
            self_init(  )


class Guy:
    _wsock=None     # when cloned and connected to a client/wsock (only the cloned instance set this)

    size=None
    def __init__(self):
        self.parent=None
        self._log=False
        self._name = self.__class__.__name__
        self._id=self._name+"-"+hex(id(self))[2:]
        self._callbackExit=None      #public callback when "exit"
        if hasattr(sys, "_MEIPASS"):  # when freezed with pyinstaller ;-)
            self._folder=sys._MEIPASS
        else:
            self._folder = os.path.dirname( inspect.getfile( self.__class__ ) ) # *ME*

        self._routes={}
        for n, v in inspect.getmembers(self, inspect.ismethod):
            if not v.__func__.__qualname__.startswith("Guy."):
                if n not in ["init","__init__","render"]:
                    self._routes[n]=v

        # guy's inner routes
        self._routes["cfg_get"]=self.cfg_get
        self._routes["cfg_set"]=self.cfg_set
        self._routes["exit"]=self.exit


    def _rebind(self):
        ## REBIND ################################################################
        ## REBIND ################################################################
        ## REBIND ################################################################ DOn't understand why I NEED to made this ?!
        for n, v in inspect.getmembers(self):
            if not n.startswith("_") and inspect.isfunction(v):
                logger.debug("::: REBIND method %s.%s()" % (self._name,n))
                setattr(self,n,types.MethodType( v, self )) #rebound !
        ## REBIND ################################################################
        ## REBIND ################################################################
        ## REBIND ################################################################

    def _connect(self,wsock):
        self._wsock = wsock # save the current socket for this instance !!!
        asyncio.ensure_future( doInit(self) )


    def run(self,log=False,autoreload=False,lockPort=None):
        """ Run the guy's app in a windowed env (one client)"""
        self._log=log
        if log: handler.setLevel(logging.DEBUG)

        if ISANDROID: #TODO: add executable for kivy/iOs mac/apple
            runAndroid(self)
        else:
            ws=WebServer( self, autoreload=autoreload )
            ws.start()

            app=ChromeApp(self._name,self.size,lockPort=lockPort)
            if app.isRunning(): # only true when lockport, and running instance
                print("ALREADY RUNNING")
                app.focus()
                time.sleep(0.1)
            else:
                app.navigate(ws.startPage)

                def exit():
                    ws.exit()
                    app.exit()

                tornado.autoreload.add_reload_hook(exit)

                self._callbackExit = exit
                try:
                    app.wait() # block
                except KeyboardInterrupt:
                    print("-Process stopped")

            ws.exit()
            ws.join()

        return self

    def runCef(self,log=False,autoreload=False):
        """ Run the guy's app in a windowed cefpython3 (one client)"""
        self._log=log
        if log: handler.setLevel(logging.DEBUG)

        ws=WebServer( self, autoreload=autoreload )
        ws.start()

        app=ChromeAppCef(ws.startPage,self.size)

        tornado.autoreload.add_reload_hook(app.exit)

        self._callbackExit = app.exit
        try:
            app.wait() # block
        except KeyboardInterrupt:
            print("-Process stopped")
        ws.exit()
        ws.join()
        return self


    def serve(self,port=8000,log=False,open=True,autoreload=False):
        """ Run the guy's app for multiple clients (web/server mode) """
        self._log=log
        if log: handler.setLevel(logging.DEBUG)

        ws=WebServer( self ,"0.0.0.0",port=port, autoreload=autoreload )
        ws.start()

        def exit():
            ws.exit()

        self._callbackExit = exit
        print("Running", ws.startPage )

        if open: #auto open browser
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
        return self #TODO: technically multiple cloned instances can have be runned (which one is the state ?)

    def exit(self):
        if self._callbackExit: 
            self._callbackExit()
        else:
            self.parent._callbackExit()

    def cfg_set(self, key, value): setattr(self.cfg,key,value)
    def cfg_get(self, key=None):   return getattr(self.cfg,key)

    @property
    def js(self):
        class Proxy:
            def __getattr__(sself,jsmethod):
                async def _(*args):
                    return await self._callMe(jsmethod,*args)
                return _
        return Proxy()

    @property
    def cfg(self):
        class Proxy:
            def __init__(sself):
                if ISANDROID:
                    exepath=os.path.abspath(os.path.realpath(sys.argv[0]))
                    path=os.path.join( os.path.dirname(exepath), "..", "config.json" )
                else:
                    exepath=os.path.abspath(os.path.realpath(sys.argv[0])) # or os.path.abspath(__main__.__file__)
                    classpath= os.path.abspath( os.path.realpath(inspect.getfile( self.__class__ )) )
                    if not exepath.endswith(".exe") and classpath!=exepath: # as module
                        path=os.path.join( os.path.expanduser("~") , ".%s.json"%os.path.basename(exepath) )
                    else: # as exe
                        path = os.path.join( os.path.dirname(exepath), "config.json" )

                logger.debug("Use config: %s",path)
                sself.__o=JDict( path )
                sself._file=path # new >0.5.3
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


    def _renderJs(self,asChild=False):
        if self.size and self.size is not FULLSCREEN:
            size=self.size
        else:
            size=None
        routes=[k for k,v in self._routes.items() if not v.__func__.__qualname__.startswith("Guy.")]
        logger.debug("ROUTES: %s",routes)
        js = """
document.addEventListener("DOMContentLoaded", function(event) {
    %s
},true)



function setupWS( cbCnx ) {
    var url=window.location.origin.replace("http","ws")+"/%s-ws"
    var ws=new WebSocket( url );

    ws.onmessage = function(evt) {
      var r = guy._jsonParse(evt.data);
      guy.log("** WS RECEPT:",r)
      if(r.uuid) // that's a response from call py !
          document.dispatchEvent( new CustomEvent('guy-'+r.uuid,{ detail: r} ) );
      else if(r.jsmethod) { // call from py : self.js.<methodjs>()

          function sendBackReturn( response ) {
            var cmd={
                command:    "return",
                args:       response,
                uuid:       r.key,
            };
            ws.send( JSON.stringify(cmd) );
            guy.log("call jsmethod from py:",r.jsmethod,r.args,"-->",cmd.args)
          }

          let jsmethod=window[r.jsmethod];
          if(!jsmethod)
            sendBackReturn( {error:"Unknown JS method "+r.jsmethod} )
          else {
            if(jsmethod.constructor.name == 'AsyncFunction') {
                jsmethod.apply(window,r.args).then( function(x) {
                    sendBackReturn( { value: x } );
                }).catch(function(e) {
                    sendBackReturn( { error: `JS Exception calling '${r.jsmethod}(...)' : ${e}` } );
                })
            }
            else {
                try {
                    sendBackReturn( { value: jsmethod.apply(window,r.args) } );
                }
                catch(e) {
                    sendBackReturn( { error: `JS Exception calling '${r.jsmethod}(...)' : ${e}` } );
                }

            }
          }
      }
      else if(r.event){ // that's an event from anywhere !
          document.dispatchEvent( new CustomEvent(r.event,{ detail: r.args } ) );
      }
    };

    ws.onclose = function(evt) {
        guy.log("** WS Disconnected");
        setTimeout( function() {setupWS(cbCnx)}, 500);
    };
    ws.onerror = function(evt) {
        guy.log("** WS Disconnected");
        setTimeout( function() {setupWS(cbCnx)}, 500);
    };
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

            console.log.apply(console.log,args.map( function(x) {return x==null?"NULL":x}));
        }
    },
    _ws: setupWS( function(ws){guy._ws = ws; document.dispatchEvent( new CustomEvent("init") )} ),
    on: function( evt, callback ) {     // to register an event on a callback
        guy.log("guy.on:","DECLARE",evt,callback.name)
        var listener=function(e) { callback.apply(callback,e.detail) };
        document.addEventListener(evt,listener)
        return function() { document.removeEventListener(evt, listener) }
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
      get: function (obj, prop) {
        return guy._call("cfg_get",[prop])
      },
      set: function (obj, prop, value) {
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
                var tag_div=document.createElement("div");
                tag_div.innerHTML = html
                document.body.appendChild(tag_div);
                return tag_div;
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

        var tag_js=document.createElement("script");
        tag_js.setAttribute('type', 'text/javascript');
        tag_js.innerHTML = o.scripts
        self._div.appendChild(tag_js)

        return self;
    },

};


var self= {
  exit:function() {guy.exit()},
  %s
};



""" % (
        'if(!document.title) document.title="%s";' % self._name,
        self._id, # for the socket
        "true" if self._log else "false",
        "\n".join(["""\n%s:function(_) {return guy._call("%s", Array.prototype.slice.call(arguments) )},""" % (k, asChild and self._id+"."+k or k) for k in routes])
    )

        return js

    async def emit(self, event, *args):
        await emit(event, *args)

    async def emitMe(self,event, *args):
        logger.debug(">>> emitMe %s (%s)",event,args)
        await sockwrite(self._wsock,event=event,args=args)

    async def _callMe(self,jsmethod, *args):
        logger.debug(">>> callMe %s (%s)",jsmethod,args)
        key=uuid.uuid4().hex
        # send jsmethod
        await sockwrite(self._wsock,jsmethod=jsmethod,args=args,key=key)
        # wait the return (of the key)
        while 1:
            if key in WebSocketHandler.returns:
                response=WebSocketHandler.returns[key]
                del WebSocketHandler.returns[key]
                if "error" in response:
                    raise JSException(response["error"])
                else:
                    return response.get("value")
            await asyncio.sleep(0.01)


    def _getRoutage(self,method):
        function=None
        if "." in method:
            id,method = method.split(".")
            function=INST.get(id)._routes[method]
        else:
            logger.debug("METHOD SELF %s",method)
            function=self._routes[method]
        return function

    def __call__(self,method,*args):
        function = self._getRoutage(method)

        ret= function(*args)

        if isinstance(ret,Guy):
            ################################################################
            o=ret

            routes=[k for k in o._routes.keys() if not k.startswith("_")]

            eventExit="event-"+o._id+".exit"
            def exit():
                logger.debug("USE %s: EXIT (%s)",o._name,o._json)
                try:
                    asyncio.create_task(self.emitMe(eventExit,o._json)) #  py37
                except:
                    asyncio.ensure_future(self.emitMe(eventExit,o._json)) # py35
                del INST[o._id]



            html=o._renderHtml( includeGuyJs=False )
            scripts=";".join(re.findall('(?si)<script>(.*?)</script>', html))

            o.parent = self
            o._callbackExit=exit
            asyncio.ensure_future( doInit(o) )

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

    def _renderHtml(self,includeGuyJs=True):
        INST[self._id]=self # When render -> save the instance in the pool (INST)

        path=self._folder
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

        def repgjs(x,page):
          return re.sub('''src *= *(?P<quote>["'])[^(?P=quote)]*guy\\.js[^(?P=quote)]*(?P=quote)''','src="/%s-js"'%self._id,x)

        if hasattr(self,"render"):
            html = self.render( path )
            html=repgjs(html,self._name)
            return rep(html)
        else:
            if hasattr(self,"_render"):
                print("**DEPRECATING** use of _render() ... use render() instead !")
                html = self._render( path )
                html=repgjs(html,self._name)
                return rep(html)
            else:
                if html:
                    if includeGuyJs: html=("""<script src="guy.js"></script>""")+ html
                    html=repgjs(html,self._name)
                    return rep(html)
                else:
                    f=os.path.join(path,FOLDERSTATIC,"%s.html" % self._name)
                    if os.path.isfile(f):
                        html=readTextFile(f)
                        html=repgjs(html,self._name)
                        return rep(html)
                    else:
                        return "ERROR: can't find '%s'" % f

    @property
    def _dict(self):
        obj={k:v for k,v in self.__dict__.items() if not (k.startswith("_") or callable(v))}
        for i in ["_callbackExit","__doc__","size","parent"]:
            if i in obj: del obj[i]
        return obj

    @property
    def _json(self):
        """ return a json representation of the inner attributs of this"""
        return jDumps(self._dict)


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

            guyWindow._callbackExit = exit

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
    # from testPrompt import Win as GuyApp
    # GuyApp().run()
    pass
