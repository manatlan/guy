# Client side : guy.js

Not like the good old [wuy](https://github.com/manatlan/wuy); javascript's apis are in two objetcs :

- **guy** : to handle the core of guy.
- **self** : to handle the declared methods in the guy's class, on [server side](server.md)

## Guy's apis

----
###`guy.init( function() { ... } )`

Will run the `function` when everything is started. It's a good place to start your logic.

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

To emit an `event` to the current client (me only;-)). 

----
###`guy.fetch( url, init )`

Same as `window.fetch`, but it's the server which will do the request, to avoid CORS issues.

----
###`guy.exit()`
Exit the app.

----
###`guy.cfg`
A place to get/set vars, which will be stored on server side, in a `config.json` file.


## Self's apis

It's all the apis which have been defined in the class instance.

If you have a class like thant, on py side:
```python
class Simple(Guy):
    """<button onclick="self.test()">test</button>"""

    def test(self):
        print("hello world")

```

You wil have a `self.test()` method in client side !


###`self.exit()`
Exit the current instance, if it's the main instance : it quits the app.

###`self.parent`
A reference to the parent guy window, if embbeded window (WILL DETAIL SOON)
...