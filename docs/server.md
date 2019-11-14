# Server Side : python guy

Basically, you subclass the guy class like this:

```python
#!/usr/bin/python3 -u
from guy import Guy

class Simple(Guy):
    size=(400,400)
    __doc__="""<button onclick="self.test()">test</button>"""

    def test(self):
        print("hello world")

```
And all declared methods will be available on [client side](client.md).

Here there will be a `self.test()` method in client side.


## Rendering 


### Rendering with docstring
It's the simplest thing : just declare your gui/html in the docstring of your class.

```python
class Simple(Guy):
    __doc__="""<button onclick="self.test()">test</button>"""
```

It's a fast way to release a simple component. But it's not adapted for larger app ;-)

!!! info
    here is the `__doc__` declaration. Which is needed if you want to release a component like that on android (because buildozer seems to remove them, if not prefixed)


**TODO** : talk about template engine ! (`<<var>>` replaced by instance/class attributs)


### Rendering with an html file
If you want to separate the UI from the code. You can put your html in a file named as the class name, in a `static` folder.

It's the preferable way to go, for larger app.

!!! info
    In this case : you should provide a tag `<script src="guy.js"></script>` in your html.

**TODO** : talk about template engine ! (`<<var>>` replaced by instance/class attributs)


### Rendering override
Sometimes, you need to make more things, and you can do it, by overriding the `_render(self, path)` method of your class.

For bigger app : I use [vbuild](https://github.com/manatlan/vbuild) to render vuejs/sfc components.
(see [starter-guy-vuejs](https://glitch.com/~starter-guy-vuejs), and [demo](https://starter-guy-vuejs.glitch.me/#/))

```python
class App(Guy):
  
  def _render(self,path): # override default 
      with open( "app/APP.html") as fid:
          buf=fid.read()
      r=vbuild.render( "app/*.vue")

      buf=buf.replace("<!-- TPLS -->",r.html)
      buf=buf.replace("/* CSS */",r.style)
      buf=buf.replace("/* JS */", r.script)      
      
      return buf
```
!!! info
    In this case : you should provide a tag `<script src="guy.js"></script>` in your response.


## Guy Class

###`init(self)`
Override this method to do thing, when a client is connected.

###`async self.emit( event, arg1, arg2 ... )`
Call this method to emit an `event` to all connected clients.

It's a non-sense in `app` or `cef` mode : because there is only one client. It only got sense in `server` mode.

###`async self.emitMe( event, arg1, arg2 ... )`
Call this method to emit an `event` to the connected client.

###`self.cfg`
A place to get/set vars, which will be stored on server side, in a `config.json` file.

###`size`
With this class attribut you can specify the size of your window.

This is a non-sense, in `server` mode. Because, it's the client which determine the size of its tab.

```python
class Simple(Guy):
    size=(400,400)
    """<button onclick="self.test()">test</button>"""
```

```python
class Simple(guy.Guy):
    size=guy.FULLSCREEN
    """<button onclick="self.test()">test</button>"""
```

## Static content
**guy** will serve everything that is contained in a `static` folder, as static content.

## Hook http
**Guy** provides an `http` decorator to handle specific http requests. It can be useful for a lot of things.

```python
from guy import http

@http("/item/(\d+)") 
def getItem(web,number):
  web.write( "item %s"%number )
```
`web` is a [Tornado's TequestHandler](https://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler)
