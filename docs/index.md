# Guy

**Guy** is a way to make a simple GUI for your python script, using html/js/css technologies (a lit bit like [electron](https://electronjs.org/)).
It borrows the idea from [python-eel](https://nitratine.net/blog/post/python-gui-using-chrome/), but provide a lot more things.

The main idea, is to reuse the installed chrome app on the host. So your script (or your freezed app) stays at the minimal footprint. But your user needs to have Chrome (or chromium) on its computer, to run your script/app.

If you want to release a standalone/freezed app, with all included (your script + a chrome container). You can include special mode with [cefpython3](https://github.com/cztomczak/cefpython). But the footprint will be around 60mo (like an electron app). But you can ;-)

There are 3 modes to release your app :

 * **app**: your user will need to have a chrome instance. The GUI will be handled by a chrome instance, runned in "app mode". (on android/ios, the GUI will be handled by webViewClient/kivy)
 * **cef**: (stands for cefpython3): All is embedded, it's the embedded cef instance which will handle your GUI.
 * **server**: it will act as an http server, and any browsers can handle your GUI. So, there can be multiple clients !

Like you understand, your GUI should be built with HTML/JS/CSS. Under the hood, **guy** provides a simple mechanisms (with websockets) to interact with the python technologies. Your GUI can be native HTML/JS or any modern js frameworks : vuejs, angular, etc ...

The **app mode** can be runned on an Android device, using kivy/buildozer toolchain (for building an apk). Understand that the same app can be runned on any android devices or on any computer (win, mac, *nix ...), without any modifications.


