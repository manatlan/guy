# Run your app

Admit you've got an app:

```python
from guy import Guy

class YourApp(Guy):
    ...

if __name__ == "__main__":
    app=YourApp()
    app.run()           #<- this is how to run it ;-)
```

## app mode

Use `app.run()`

Classical mode, on desktop : it uses the installed chrome browser in app mode. (it's the way to run on android too)

## cef mode

Use `app.runCef()`

Special mode for desktop : when you want to provide a standalone app, with all included. You will need cefpython3 !

## server mode

Use `app.serve()`

Server mode, for servers.

Optionnal parameters:

 - port: (number) listening port, default: 8000.
 - open: (bool) open default browser to the client, default: True