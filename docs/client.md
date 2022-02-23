# Client side : guy.js

Not like the good old [wuy](https://github.com/manatlan/wuy); javascript's apis are in two objetcs :

- **guy** : to handle the core of guy.
- **self** : to handle the declared methods in the guy's class, on [server side](server.md)

## Guy's apis

----
###`guy.init( function() { ... } )`

Will run the `function` when everything is started. It's a good place to start your logic.

BTW, since >=0.4.3 ... it's a better practice to call a js method, from py side, to start your logic ... like this :

```python
class Example(Guy):
    """
    <script>
    function start() {
        // ....
    }
    </script>
    """
    async def init(self):
        await self.js.start()
```

----
###`guy.on( event, function(arg1, arg2, ...) { ... } )`

To listen to an `event` ...

It returns a method to unsubscribe the listenner.

----
###`guy.emit( event, arg1, arg2, ...)`

To emit an `event` to all connected clients. 

It's a non-sense in `app` or `cef` mode : because there is only one client. It only got sense in `server` mode.

----
###`guy.emitMe( event, arg1, arg2, ...)`

To emit an `event` to the current client (only me;-)). 

----
###`guy.fetch( url, options )`

Same as [`window.fetch`](https://developer.mozilla.org/en-US/docs/Web/API/WindowOrWorkerGlobalScope/fetch), but it's the server which will do the request, to avoid CORS issues.

----
###`guy.exit( returnValue=None )`
Exit the app.

If you want to get a "returnValue", you can set here the returned value, in py side:

```python
   myapp=MyGuyApp()
   returnValue = myapp.run()
```

----
###`async guy.cfg`
A place to get/set vars, which will be stored on server side, in a `config.json` file, where the main executable is runned.
(if the guy'app is embedded in a pip/package, the config file will be stored in ``~/.<package_name>.json`)

To set a var 'name', in js side :

```javascript
guy.cfg.name = "Elton";
```

To get a var 'name', in js side :

```javascript
var name = await guy.cfg.name;
```


## Self's apis

It's all the apis which have been defined in the class instance.

If you have a class like that, on py side:
```python
class Simple(Guy):
    """<button onclick="self.test()">test</button>"""

    def test(self):
        print("hello world")

```

You wil have a `self.test()` method in client side !

Theses methods can be sync or async, depending on your need.

###`self.exit( returnValue=None )`
Exit the current instance, if it's the main instance : it quits the app.

If you want to get a "returnValue", you can set the returned value, which will be returned in py side:

```python
   myapp=MyGuyApp()
   returnValue = myapp.run()
```
