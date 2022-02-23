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

Understand that a guy's class is an html page. Declared methods will be available on client side, and will be directly usable from js side.


## Rendering the UI

The rendering is done after the instanciation of the class : when the client connects, or do a refresh.

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
If you want to separate the UI from the code (best practice). You can put your html in a file named as the class name, in a `static` folder.

It's the preferable way to go, for larger app.

!!! info
    In this case : you should provide a tag `<script src="guy.js"></script>` in your html.

**TODO** : talk about template engine ! (`<<var>>` replaced by instance/class attributs)


### Rendering override
Sometimes, you need to make more things, and you can do it, by overriding the `render(self, path)` method of your class.

For bigger app : I use [vbuild](https://github.com/manatlan/vbuild) to render vuejs/sfc components.
(see [starter-guy-vuejs](https://glitch.com/~starter-guy-vuejs), and [demo](https://starter-guy-vuejs.glitch.me/#/))

```python
class App(Guy):
  
  def render(self,path): # override default 
      with open( os.path.join(path,"app/APP.html") as fid:
          buf=fid.read()
      r=vbuild.render( os.path.join(path,"app/*.vue") )

      buf=buf.replace("<!-- TPLS -->",r.html)
      buf=buf.replace("/* CSS */",r.style)
      buf=buf.replace("/* JS */", r.script)      
      
      return buf
```
!!! info
    In this case : you should provide a tag `<script src="guy.js"></script>` in your response.


## Guy Class

Like a normal class : you can override its constructor and set some attributs at this place. Note that, the constructor is called before the rendering : so it's the perfect place to setup some things before rendering.


***TODO*** : Talk about returning {script: "..."}

***TODO*** : Talk about sync/async methods.

###`init(self)`
Override this method to do thing, when a client is connected. (init method can be sync or async)

###`render(self,path)`
Override this method to override default rendering (see [Rendering override](#rendering-override))

`path` is the path to the data (where static folder sits)

If this method is not overriden : it will try to get the html from the `__doc__`'s string, if not ... from the static folder (`guy.FOLDERSTATIC`)

###`self.exit( returnValue=None )`
Exit the app.

If you want to get a "returnValue", you can set the returned value, which will be returned in py side:

```python
   myapp=MyGuyApp()
   returnValue = myapp.run()
```

###`cleanup( ...)`
**NEW in 0.7.6**
event to define for cleanup things. (*TODO: need better explain*)

###`afterServerStarted( ... )`
**NEW in 0.7.6**
event to define for starting things. (*TODO: need better explain*)

###`async self.emit( event, arg1, arg2 ... )`
Call this method to emit an `event` to all connected clients.

It's a non-sense in `app` or `cef` mode : because there is only one client. It only got sense in `server` mode. Prefer the following `emitMe` to send an event to the gui.

###`async self.emitMe( event, arg1, arg2 ... )`
Call this method to emit an `event` to the connected client.

###`self.parent`
This attribut contains the main instance (the one which starts all (which done `.run()`)). If it's `None`, you are in the main instance.

###`async self.js`
With this wrapping object, you can call js method (from the connected client) from py side, and get back a returned value :

```python
name = await self.js.prompt("what's your name ?")
```
Notes:

- It can throw a `guy.JSException` if something is wrong on js side!
- On py side; you'll need to await the call, even if you don't need to get back the returned value.
- On js side; your js method can be sync or async. But your method needs to be in `window` scope.

!!! info
    Only available for guy >= 0.4.3


###`self.cfg`
A place to get/set vars, which will be stored on server side, in a `config.json` file, where the main executable is runned.
(if the guy'app is embedded in a pip/package, the config file will be stored in ``~/.<package_name>.json`)

To set a var 'name', in py side :

```python
self.cfg.name = "Elton"
```

To get a var 'name', in py side :

```python
name = self.cfg.name
```

###`size`
With this class attribut you can specify the size of your window.

This is a non-sense, in `server` mode. Because, it's the client/browser which determine the size of its tab.

This is a non-sense, when runned on android. Because the window is the full screen.

```python
class Simple(Guy):
    """<button onclick="self.test()">test</button>"""
    size=(400,400)
```

```python
class Simple(guy.Guy):
    """<button onclick="self.test()">test</button>"""
    size=guy.FULLSCREEN
```

!!! info
    `Size` may be relevant for the main window (the first started). It has no effect after a navigation or for embedded window.


## Static content
**guy** will serve everything that is contained in a `static` folder, as static content.

It's really useful, when you don't embbed your html in the docstring of the class, or if you need
static content like images, css files, etc ...

!!! important
    - Static content should contain dots (".") in filename ! If not; current guy's version consider it must be served as dynamic content ! (it may change in the near future)


This static folder should be in the same path as your main guy class, like this :
    
```
  ├── main.py      <- Contains class Index(guy.Guy)
  └── static
      └── Index.html
```

It's possible to use another for this folder, by setting `guy.FOLDERSTATIC = "ui"` at start.

## Hook http
**Guy** provides an `http` decorator to handle specific http requests. It can be useful for a lot of things.

```python
from guy import http

@http("/item/(\d+)") 
def getItem(web,number):
  web.write( "item %s"%number )
```
`web` is a [Tornado's RequestHandler](https://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler)

**TODO** : talk about returning a guy window (for beautiful url)

!!! important
    The url catched by the hook http, can't contain dots (".") ! If there is a dot; current guy's version consider it must be served as static content ! (it may change in the near future)