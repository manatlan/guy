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

!!! info
    Since 0.5.1 versions, you can use `autoreload`'s mode to help you during dev process (in production : don't set the `autoreload` to `True`)


## The differents modes
Each method starts the loop (and provide the GUI). And when exiting : it returns the exit's returnValue (see js/exit() or py/exit())
### app mode

Use `app.run()`

Classical mode, on desktop : it uses the installed chrome browser in app mode. (it's the way to run on android too)

Optionnal parameters:

 - one: (bool), permit to run just once instance at the same time (if True, running a second one will re-focus to the already runned one), default: False
 - log: (bool) enable logging (client & server side) (don't have any effect on android), default: False
 - autoreload: (bool) autoreload on changes (don't have any effect on android), default: False
 - args: (list) add any additional startup arguments for the browser. _Example:_ `args=["--autoplay-policy=no-user-gesture-required"]`


`app.run(one=True, args=["--autoplay-policy=no-user-gesture-required"])`

To be able to store things in js/localStorage, you must use the `one` parameter, to make storage persistent. By default, storage is not persistent, and removed after each use!


### cef mode

Use `app.runCef()`

Special mode for desktop : when you want to provide a standalone app, with all included. You will need cefpython3 !
(and you user don't need to have a chrome/chromum installed)

Optionnal parameters:

 - one: (bool), permit to run just once instance at the same time (if True, running a second one will re-focus to the already runned one), default: False
 - log: (bool) enable logging (client & server side), default: False
 - autoreload: (bool) autoreload on changes, default: False

To be able to store things in js/localStorage, you must use the `one` parameter, to make storage persistent. By default, storage is not persistent, and removed after each use!


### server mode

Use `app.serve()`

Server mode, for servers.

Optionnal parameters:

 - log: (bool) enable logging (client & server side), default: False
 - port: (number) listening port, default: 8000.
 - open: (bool) open default browser to the client, default: True
 - autoreload: (bool) autoreload on changes, default: False


## To summarize the choice

Just a table to help you to select the best mode for your needs

 | Mode :                                 | App | Cef  | Server |
 |:---------------------------------------|:---:|:----:|:------:|
 | Your users need chrome to run your app | yes | no   | no     |
 | Works on android/apk                   | yes | no   | no     |
 | Works on any OS                        | yes | yes  | yes    |
 | Your script is freezable, on any OS    | yes | yes  | yes    | 
 | Your script is pip packageable         | yes | yes  | yes    | 
 | Minimum size of the freezed executable | 6mo | 60mo | 6mo    |
 | Many clients at same time              | no  | no   | yes    |
 | Host your app on a server (glitch.com) | no  | no   | yes    |

!!! info
    Pip-packageable is only enabled for guy >= 0.4.0
    