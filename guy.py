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


__version__="0.7.3+"

import os,sys,re,traceback,copy,types,shutil
from urllib.parse import urlparse
from threading import Thread
import tornado.web
import tornado.websocket
import tornado.platform.asyncio
import tornado.autoreload
import tornado.httpclient
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado import gen
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
CHROMECACHE=".cache"
WSGUY=None # or "wss://example.com" (ws server)
class JSException(Exception): pass

handler = logging.StreamHandler()
handler.setFormatter( logging.Formatter('-%(asctime)s %(name)s [%(levelname)s]: %(message)s') )
handler.setLevel(logging.ERROR)
logger = logging.getLogger("guy")
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


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

def wsquery(wsurl,msg): # Synchrone call, with tornado
    """ In a simple world, could be (with websocket_client pypi):
            ws = websocket.create_connection(wsurl)
            ws.send(msg)
            resp=ws.recv()
            ws.close()
            return resp
    """
    @gen.coroutine
    def fct(ioloop,u,content):
        cnx=yield websocket_connect(u)
        cnx.write_message(msg)
        resp=yield cnx.read_message()
        cnx.close()
        ioloop.stop()
        ioloop.response=resp

    ioloop = IOLoop.instance()
    fct(ioloop,wsurl,msg)
    ioloop.start()
    return ioloop.response

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
        o=Guy._instances.get( id )
        if o:
            self.write(o._renderJs(id))
        else:
            raise tornado.web.HTTPError(status_code=404)


class FavIconHandler(tornado.web.RequestHandler):
    def initialize(self, instance):
        self.instance=instance
    async def get(self):
        self.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00@\x00\x00\x00@\x08\x06\x00\x00\x00\xaaiq\xde\x00\x00\x00\x06bKGD\x00\xd4\x00{\x00\xff\xf0\x90\n\xda\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xe4\x04\x0e\x0f)\x02\xf5J\x9b=\x00\x00\x00\x1diTXtComment\x00\x00\x00\x00\x00Created with GIMPd.e\x07\x00\x00\x06RIDATx\xda\xdd\x9b_\x88Te\x14\xc0\x7f\xe7\x9bu\xcd\x08D\x82\xfe=\xf4\x92\x88\xceV\xfe\x99\x9d\x82z(0{\x8a\x08\xa2\x07\xa9\xb0Q\x14\xb7\xb2\xcdXVLb\xd42)\x82\xb0\x82\xc5\xd5\x1a,\xd9\xe7\x02{)\x08|*[w\xdd\x9d\xd04\t\x0c\xa2\x1e\x82\xd0(1\xd7\x9d\xd3\xc3\xfc\xd9;3\xf7\xde\xef\xbbw\xef\xfc\xd9.\x0c\xbb;\xf7\xfbs\xbe\xdfw\xce\xf9\xce9\xf7\xae\xd0\x82\xeb\xccKz\'p\x0fp7p\x17p\xbb\x96\xb8\x15X\n\xdc\x02\xdc\x0c\xf4\x02=\x80\x00\x8arCK\\\x07\xae\x02\x7f\x03\x7f\x01\x7f\x02\x7f\x00\xbf\x03\xbf\x02\x972\xa3\xf2\xb3w\xae\xf1MJ\xf6\x98\xc4\x965V\xcf\xd3[\x95\xfe#\xe5\xaegvh\x1f%\xb2\xc0\xa3\xc0\xc3\xc0r\xbf>\xaa\x80Z\x06V\xd0\x92\x83\x00%\xae\x00\xdf\x02\'\x81S\xc0\xf7\x99\xa3\xf2O[\x00L\rj/\xb0^K\xe4\x80g<BY/um\xa3N\x10\x1a\x01\x9fG9\x0c|\xd9\xff\x89\\\x048\x9dS\xfa\x0b\x92\x0c\x80\xa9A]\x05\x0c\x03/\x04\xeeh\xe7!T\xfb\xfd\x06\xbc\xcc\x0c_\xf4\x7f&\xa5\xf1\x9c\x92\r\x00!!\x0bf\xcd!ajPW\x02c\xc0Z\'\xb5\xee4\x84f(\xcfg\x0br<\xb2\x06L\xbf\xaa\x8bU9\n<\x17*\xe8\xc2\x800\x0b\xdc\x9b-\xc8\xf9Fm0u\x8b\xde\xa9\xd5\x9f+\x10\xae\x89\t_<\x80\x88\x0fF\xe3\xe0|\\\xdbHtO\xd68\xb6\x08)\xe0\xc7\xf1\x9cn\xcd\x16\x84\xf1\x9c6\x8bZ\x1cRV\xbf/L\xef\xd4\r\xc0\x85H\x82\xfa\t\x99$\x04\x17\x00v\x08\x00\xa3\xe39=\xe0\x85P\xd7m\xfa5\xdd\x00|\xe5\xa7v\x1aW\xad\x932\x87Y\x07\x10>\xe6\xe8\x1d[\xe7\xee\xbd\x98-\xc8H\x1d\x80\xe2\x90.\x07.\xd6:\xfc\xff!\xac\xcc\x16\xe4\x82)\x0ekUeO\xd5\xa9\x8e$\xa8\xb2\x92\x909\xa4\x9a\xbe\x9a\x01\x0e\x00kQ\x1e\x00>\xb4\x99\x83\xc7\\?\xae\x89V\x1c\xd6-\xc0Q\xefn-\x00M\xc8\xd3\xcb\xfe\xccG\xf5\xab\x9d\xd8\xa6\x068\x82\xb2\xd9A\x13VT\xd9|\xd0\xb8[-\xd1\x04\x93\x98&\xe43\xa3\xb2\x9f\x99\xe6{\x99Q)eFe\x0b\xc2X\xd8\xd8" \xc2\x93\xa68\xac\x0fU\x92\x93&\x8f\xda\xa5\x10~Z7"\xfb\'\x07\x94\xcca\x7f\xdb\x9a\x1cP2\xa3\xf2,\x86k\x96\xb1\xef3\xc0\xe3a\xc7J\x17B(\x00\xac\x1b\tv,\x9e{\x9f\xfb\xcd\xe5\x19\xfb&\x03\xac\xb6\x9d\xad]\x06\xe1d\x84\xdcm,h\xae\xca\xd87\x0cp\x9bK\x80\x11\x06!\xb6\x97\x8f\xd7o&\x02\x80\x7f\xc3\x80\x8b)\x7f=\xe3\x1ae\xd5\x8e\x10q\x08\x87]\x16\xe3\xd8\xaf\xa1\xcd\x83\x93\x03\xf6\x04ab\x9b\x02<e\xd1:5\x92r *s\x9fN@h\x18;\x17f\xff\x9e\xd3\x00`\x93\xc5\xf4\xd4\x04\x04\x18\xdd\x0c!39\xa0\x1b-;\xcf\xc46\xddSw\xba\x05@0!QV(\x04:\x0balr@\x9f\x06\x98\xd8\xaeM;?9\xa0;\x80\xb7B\x07+\xcf\xaf\xf2\xc3n\xfd\x1ax,R\xbc]\xf2\xa9\x05h\xf4\x1a\xa0\xfaE\x87.\xfd\xe6\xda\x9c\x04F\x80\xe9J\x81\xb5\x1f\xd8\x01\xacs\xac/\x1e\xeb\xf1\x8b\xb7\xad\x10LYp\x91\x8a\x1cJ\xb5\xb6[\xb7[\xaav\x85R\xd3\x00A\xec\x00<c?R\xf9\x04kk\xf8Xj\x1c\x93\x8e@;\x920s0nV\xd5\xc9\x82\x8a\x99W!")\x08\x9d\xab*\xa9\t\xdb\x9a\xc8\x10Xx\x10\x8cM?#A0\x0b\x0e\x82\x1a\'#\x956Ch_}Q]\xf6\xd7\xbd:k\xec\xc2tA-\xa1\x0e@\x8fkV!\xc6\xb1N_="\xab\xed}\x8e\xa2\xda\xbd\xf2u9t>"\x1e\x91\xc6~\xfe{\x8e\xfa\xab\xce\x00Z\x04av\xcd!YF\x07/\x13\xb5Cls\x08\xa8%L\r*\x0b\n@\xd2\x10:}\x191\x01\x9e7\x01\x87\xe3]\xb4+\x84\xe2P{5\xa2\xa7v\xdec\x8f\xdd}\x9d\x89\xcd\'\xc8\\\x92\xe3\xe7\x13\x1aA\xde\xff\x9eP\x1c\xd2\xab\x18\xae;\xc9\xe0\xf5/\x12\x96u\xf9:GO2\x14\x17\x82\x99?\x04\x1f\xd3Y\x02,q\x99_\x03\xb2\xd1\xc0\x0c\xb6\xfey\xc7\x12\xd3\x14\xf9\xb5\xca\x1c\x82\xea\x8bI\xf9\x05\x89\xe1\x8f\x04LS\xc7\xb8\x10R\x11!t\xc2!\xfa\x04j\xc6w\x17b\n\x17\xbb\xb4\x96\x90\xa6\xc5\xc9[L\x90*\x8ai\x0b\x04\x89t\x9a\x88e\xfc\x18\xc9\x9b\tKz\xda\x00a&\xce\xee[!D\x88Q\x8c-\xf3k1\x04\xb5\x86b\x01\xbb\x1e*\x97q\x87`\\\xaa\xb3-\x85\x10\xd7\xee\xc5\x0e\xc1\xc5\x97\x19\xdfI\xba\x04\x82\xb5\xaf\x84\x07\xf3\x91j\x82\xdd\x06\xc1\xb5\x8f\xcc\x13\x82\t]`\x92\x10L\xeb\x80\xcd\x07\x82\xb1\n*\xf3[L\xe4#*\xae\xb9\x88\xc3\x06\x88?\x80\x1b\xd6\xb0\xd2D\x9f\xb0\x13\x10\xe2\xa4\xf1=\x94\xdf\xcboZ\x9c6&\x18~Op\\\x92\x90\x00\x08\x95\xa4D\x80\xa5\xc5a\xf5\xaa\xfd\x95VC\xf0>\xf9\xea\xa1\xfcf5q \xf8\xb6\x89\x10\xd5\xa1,\x06.\'q\\FN\xe3g\xe7\x96t!\xd4\xae,\xe6 13\xba\xaa:\xb6{\xf1\x8d\x8e\xd6\x00\xe3V\xe7\xd2J\x08\x1d\xbc$\x05\xa6o\x9fL8y\xd8\x16AH4\xe7\x8f\x9b!K\x8a\xe3\xb1\x8e\x996C\x10K\xa2\x13G\xa3*\xefIp(\xa9\'6-\x83\xe0XE\x8a\n\xc1\x00\xa4\xf3r\x1a\xf8.I\x08IV|\xc4\xd4\xafY\x12\x84\xe0m\xba\xd1\xb5\xb3\xd3\xb3\xbb\x84 \x04\xc9\x93\x14\x84Z\xb3t^.\x01\x9b\xbb\t\x82-,o\x82\x10#o\xa959\xf7\xa6\x92\xceK\x01x\xb7\x1b \x04\xbeY\x1a\x06!F\xf26\xa7\x01o\x08\xe7\xf6)\xe9\xbc\xec\x02\xf6\xcc\x0b\x82_\xa5y\xbe\x89\x8d\xb1@\x88\x99\xbc\xd5\xddJ\xe7\x85\xb3{\x95t^\xde\x06\xd6\xc7\x86\x10\xf3M\x0f\xd7\x98\xc3\xba\xd3\xc6\x1dB\xd3\xd7}{\x85\xf3\xef\x94H\xe7\xe5\x1bJ\xf4\x02\x07\x93\x82`-kG\x01g;n\x1d!\x98\xdd\x9ch\xfar\xe5\xaeZ\xc9t&\x9d\x97\xd7)\xbfr\xfa\n\xf0K\xab 8G\x9b!\xe3\x8bD\x87 \x00\xbb9!\x07y"0\xa7;\x9bW\xfa\xf6I\xf5\xf7;*\xe6\x91\x05VQ\xfe\x17\xf9e\xc0\xa2j{ux\xfb\xb3\xb1M\x9d`\n\xa4\xea\xfe\x9a\x05\xae\x89!\x05\xa4\x9a\xc6\xaf\xfc-=,\xd2RSnj\xfc\xdeF\xad<S\xfc\xf4?\xd9\xf1\xf7\xdeE\\\xb8\xa0\x00\x00\x00\x00IEND\xaeB`\x82')

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


async def sockwrite(theSock, **kwargs ):
    if theSock:
        try:
            await theSock.write_message(jDumps(kwargs))
        except Exception as e:
            logger.error("Socket write : can't:%s",theSock)
            if theSock in WebSocketHandler.clients: del WebSocketHandler.clients[theSock]


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
        o=Guy._instances.get( id )
        if o:
            logger.debug("Connect %s",id)

            async def doInit( instance ):
                init=instance._getRoutage("init")
                if init:
                    if asyncio.iscoroutinefunction( init ):
                        await instance(self,"init")
                    else:
                        instance(self,"init")

            asyncio.ensure_future( doInit(o) )

            WebSocketHandler.clients[self]=o

    def on_close(self):
        current=WebSocketHandler.clients[self]
        logger.debug("Disconnect %s",current._id)
        del WebSocketHandler.clients[self]

    async def on_message(self, message):
        current = WebSocketHandler.clients.get(self,None)
        if current is None:
            return

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

            fct=current._getRoutage(method)

            if asyncio.iscoroutinefunction( fct ):

                async def function():
                    return await current(self,method,*args)

                #asyncio.create_task( execution( function, uuid, "ASYNC") )  #py37
                asyncio.ensure_future ( execution( function, uuid, "ASYNC") ) #py35

            else:
                async def function():
                    return current(self,method,*args)

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
        ], compress_response=True)
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
    def __init__(self, url, appname="driver",size=None,lockPort=None,chromeargs=[]):

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

        if not exe:
            raise Exception("no chrome browser, no app-mode !")
        else:
            args = [ #https://peter.sh/experiments/chromium-command-line-switches/
                exe,
                "--app=" + url, # need to be a real http page !
                "--app-id=%s" % (appname),
                "--app-auto-launched",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-notifications",
                "--disable-features=TranslateUI",
                #~ "--no-proxy-server",
            ] + chromeargs
            if size:
                if size == FULLSCREEN:
                    args.append("--start-fullscreen")
                else:
                    args.append( "--window-size=%s,%s" % (size[0],size[1]) )

            if lockPort: #enable reusable cache folder (coz only one instance can be runned)
                self.cacheFolderToRemove=None
                args.append("--remote-debugging-port=%s" % lockPort)
                args.append("--disk-cache-dir=%s" % CHROMECACHE)
                args.append("--user-data-dir=%s/%s" % (CHROMECACHE,appname))
            else:
                self.cacheFolderToRemove=os.path.join(tempfile.gettempdir(),appname+"_"+str(os.getpid()))
                args.append("--user-data-dir=" + self.cacheFolderToRemove)
                args.append("--aggressive-cache-discard")
                args.append("--disable-cache")
                args.append("--disable-application-cache")
                args.append("--disable-offline-load-stale-cache")
                args.append("--disk-cache-size=0")

            logger.debug("CHROME APP-MODE: %s"," ".join(args))
            # self._p = subprocess.Popen(args)
            self._p = subprocess.Popen(args,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            #~ if lockPort:
                #~ http_client = tornado.httpclient.HTTPClient()
                #~ self._ws = None
                #~ while self._ws == None:
                    #~ try:
                        #~ url = http_client.fetch("http://localhost:%s/json" % debugport).body
                        #~ self._ws = json.loads(url)[0]["webSocketDebuggerUrl"]
                    #~ except Exception as e:
                        #~ self._ws = None

    def wait(self):
        self._p.wait()

    def __del__(self): # really important !
        self._p.kill()
        if self.cacheFolderToRemove: shutil.rmtree(self.cacheFolderToRemove, ignore_errors=True)

    #~ def _com(self, payload: dict):
        #~ """ https://chromedevtools.github.io/devtools-protocol/tot/Browser/#method-close """
        #~ payload["id"] = 1
        #~ r=json.loads(wsquery(self._ws,json.dumps(payload)))["result"]
        #~ return r or True

    #~ def focus(self): # not used
        #~ return self._com(dict(method="Page.bringToFront"))

    #~ def navigate(self, url): # not used
        #~ return self._com(dict(method="Page.navigate", params={"url": url}))

    def exit(self):
        #~ self._com(dict(method="Browser.close"))
        self._p.kill()



class CefApp:
    def __init__(self, url, size=None, chromeArgs=None,lockPort=None):  # chromeArgs is not used
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
            if lockPort:
                settings["remote_debugging_port"]=lockPort
                settings["cache_path"]= CHROMECACHE

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




def chromeBringToFront(port):
    if not isFree("localhost", port):
        http_client = tornado.httpclient.HTTPClient()
        url = http_client.fetch("http://localhost:%s/json" % port).body
        wsurl= json.loads(url)[0]["webSocketDebuggerUrl"]
        wsquery(wsurl,json.dumps(dict(id=1,method="Page.bringToFront")))
        return True

class LockPortFile:
    def __init__(self,name):
        self._file = os.path.join(CHROMECACHE,name,"lockport")

    def bringToFront(self):
        if os.path.isfile(self._file): # the file is here, perhaps it's running
            with open(self._file,"r") as fid:
                port=fid.read()

            if not isFree("localhost", int(port)): # if port is taken, perhaps it's running
                http_client = tornado.httpclient.HTTPClient()
                url = http_client.fetch("http://localhost:%s/json" % port).body
                wsurl= json.loads(url)[0]["webSocketDebuggerUrl"]
                print("*** ALREADY RUNNING")
                wsquery(wsurl,json.dumps(dict(id=1,method="Page.bringToFront")))
                return True


    def create(self) -> int:
        if os.path.isfile(self._file):
            os.unlink(self._file)
        # find a freeport
        port=9990
        while not isFree("localhost", port):
            port += 1

        if not os.path.isdir( os.path.dirname(self._file)):
            os.makedirs( os.path.dirname(self._file) )
        with open(self._file,"w") as fid:
            fid.write(str(port))

        return port



class GuyBase:
    def run(self,log=False,autoreload=False,one=False,args=[]):
        """ Run the guy's app in a windowed env (one client)"""
        self._log=log
        if log:
            handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        if ISANDROID: #TODO: add executable for kivy/iOs mac/apple
            runAndroid(self)
        else:
            lockPort=None
            if one:
                lp=LockPortFile(self._name)
                if lp.bringToFront():
                    return
                else:
                    lockPort = lp.create()

            ws=WebServer( self, autoreload=autoreload )
            ws.start()

            app=ChromeApp(ws.startPage,self._name,self.size,lockPort=lockPort,chromeargs=args)

            self.RETOUR=None
            def exit(v=None):
                self.RETOUR=v

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
            return self.RETOUR


    def runCef(self,log=False,autoreload=False,one=False):
        """ Run the guy's app in a windowed cefpython3 (one client)"""
        self._log=log
        if log:
            handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        lockPort=None
        if one:
            lp=LockPortFile(self._name)
            if lp.bringToFront():
                return
            else:
                lockPort = lp.create()

        ws=WebServer( self, autoreload=autoreload )
        ws.start()

        self.RETOUR=None
        try:
            app=CefApp(ws.startPage,self.size,lockPort=lockPort)

            def cefexit(v=None):
                self.RETOUR=v
                app.exit()

            tornado.autoreload.add_reload_hook(app.exit)

            self._callbackExit = cefexit
            try:
                app.wait() # block
            except KeyboardInterrupt:
                print("-Process stopped")
        except Exception as e:
            print("Trouble with CEF:",e)
        ws.exit()
        ws.join()
        return self.RETOUR


    def serve(self,port=8000,log=False,open=True,autoreload=False):
        """ Run the guy's app for multiple clients (web/server mode) """
        self._log=log
        if log:
            handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

        ws=WebServer( self ,"0.0.0.0",port=port, autoreload=autoreload )
        ws.start()

        self.RETOUR=None
        def exit(v=None):
            self.RETOUR=v
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
        return self.RETOUR


    def _renderJs(self,id):
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
    var url=%s+"/%s-ws"
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
    _cptFetch: 0,
    _applyClass: function(i) {
        guy._cptFetch+=i;
        if(guy._cptFetch>0)
            document.body.classList.add("wsguy")
        else
            document.body.classList.remove("wsguy")
    },
    _call: function( method, args ) {
        guy._applyClass(1);
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
                    guy._applyClass(-1);
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
    exit: function(x) {guy._call("exit",[x])},
};


var self= {
  exit:function(x) {guy.exit(x)},
  %s
};



""" % (
        'if(!document.title) document.title="%s";' % self._name,
        'window.location.origin.replace("http","ws")' if WSGUY is None else '"%s"'%WSGUY,
        id, # for the socket
        "true" if self._log else "false",
        "\n".join(["""\n%s:function(_) {return guy._call("%s", Array.prototype.slice.call(arguments) )},""" % (k, k) for k in routes])
    )

        return js

    def _renderHtml(self,includeGuyJs=True):
        cid=self._id

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

        def repgjs(x):
            return re.sub('''src *= *(?P<quote>["'])[^(?P=quote)]*guy\\.js[^(?P=quote)]*(?P=quote)''','src="/%s-js"'%(cid,),x)


        def _caller(self,method:str,args=[]):
            isBound=hasattr(method, '__self__')
            if isBound:
                r=method(*args)
            else:
                r=method(self, *args)
            return r

        if hasattr(self,"render"):
            html = _caller(self, self.render, [path] )
            html=repgjs(html)
            return rep(html)
        else:
            if hasattr(self,"_render"):
                print("**DEPRECATING** use of _render() ... use render() instead !")
                html = _caller(self, self.render, [path] )
                html=repgjs(html)
                return rep(html)
            else:
                if html:
                    if includeGuyJs: html=("""<script src="guy.js"></script>""")+ html
                    html=repgjs(html)
                    return rep(html)
                else:
                    f=os.path.join(path,FOLDERSTATIC,"%s.html" % self._name)
                    if os.path.isfile(f):
                        html=readTextFile(f)
                        html=repgjs(html)
                        return rep(html)
                    else:
                        return "ERROR: can't find '%s'" % f

class Guy(GuyBase):
    _wsock=None     # when cloned and connected to a client/wsock (only the cloned instance set this)
    _instances={}   # class variable handling all rendered instances

    size=None
    def __init__(self):
        self.parent=None
        self._log=False
        self._name = self.__class__.__name__
        self._id=self._name+"_"+hex(id(self))[2:]   # unique (readable) id to this instance
        self._callbackExit=None      #public callback when "exit"
        if hasattr(sys, "_MEIPASS"):  # when freezed with pyinstaller ;-)
            self._folder=sys._MEIPASS
        else:
            self._folder = os.path.dirname( inspect.getfile( self.__class__ ) ) # *ME*

        self._routes={}
        for n, v in inspect.getmembers(self, inspect.ismethod):
            if not v.__func__.__qualname__.startswith("GuyBase."):  # only "Guy." and its subclass
                if not n.startswith("_") and n!="render" :
                    #~ print("------------Route %s: %s" %(self._id,n))
                    self._routes[n]=v

        Guy._instances[self._id]=self # When render -> save the instance in the pool


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

    def exit(self,v=None):
        if self._callbackExit:
            self._callbackExit(v)
        else:
            self.parent._callbackExit(v)

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


    def _getRoutage(self,method): # or None
        return self._routes.get(method)

    #~ def __call__(self,theSock,method,*args):
        #~ ####################################################################
        #~ ## not the best (no concurrent client in servermode)
        #~ ####################################################################

        #~ self._wsock=theSock

        #~ for k, v in self._routes.items():
            #~ setattr(self,k,v) #rebound ! (for init())

        #~ function = self._getRoutage(method)
        #~ print("__CALL__",method,args)
        #~ return function(*args)


    def __call__(self,theSock,method,*args):
        ####################################################################
        ## create a context, contextual to the socket "theSock" -> context
        ####################################################################
        context = copy.copy(self) # important (not deepcopy!), to be able to share mutable

        for n, v in inspect.getmembers(context):
            if n in self._routes.keys():
                if inspect.isfunction(v):
                    v=types.MethodType( v, context )
                    setattr( context, n, v )
                context._routes[n]=v

        context._wsock=theSock
        ####################################################################
        try:
            function = context._getRoutage(method)
            r=function(*args)
        finally:
            del context
        return r




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

            def exit(v):
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
