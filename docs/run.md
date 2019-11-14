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
## The differents modes
### app mode

Use `app.run()`

Classical mode, on desktop : it uses the installed chrome browser in app mode. (it's the way to run on android too)

### cef mode

Use `app.runCef()`

Special mode for desktop : when you want to provide a standalone app, with all included. You will need cefpython3 !

### server mode

Use `app.serve()`

Server mode, for servers.

Optionnal parameters:

 - port: (number) listening port, default: 8000.
 - open: (bool) open default browser to the client, default: True



## To summarize the choice

Just a table to help you to select the best mode for your needs

 | Mode :                                 | App | Cef  | Server |
 |:---------------------------------------|:---:|:----:|:------:|
 | Your users need chrome to run your app | yes | no   | no     |
 | Works on android/apk                   | yes | no   | no     |
 | Works on any OS                        | yes | yes  | yes    |
 | Your script is freezable, on OS        | yes | yes  | yes    | 
 | Minimum size of the freezed executable | 6mo | 60mo | 6mo    |
 | Many clients at same time              | no  | no   | yes    |
 | Host your app on a server (glitch.com) | no  | no   | yes    |

