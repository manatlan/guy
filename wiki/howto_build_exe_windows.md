# How to build an exe for Windows

It can be very useful to distribute and exe on Microsoft Windows platforms.

You will need [pyinstaller](https://www.pyinstaller.org/) !

## A "light" one, with the need of chrome on the host

Who doesn't have chrome on its computer ?!

If there is a chrome on the host. It's the best option : the exe will reuse the installed chrome in "app mode". The exe will be lighter (6mo min)

It's the best option for `app.run()` or `app.server()` modes in your main py file.

```
pyinstaller.exe YourGuyApp.py --noupx --onefile --noconsole --exclude-module cefpython3 --add-data="static;static"
```

Notes:

    - `noupx` : because, with upx it gives me errors ;-)
    - `onefile` : to embed all needed runtime files.
    - `noconsole` : like you want ...
    - `exclude-module cefpython3` : So you will need to have chrome on the host machine to be able to run the exe.
    - `add-data="static;static"` : to embed yours static file for rendering (css, images ...)

## A full one ; all included

If you target an unknow windows computer, perhaps you should embed a chrome in the exe. It's possible with [cefpython3](https://pypi.org/project/cefpython3/) module.

Install cefpython
```python3 -m pip install cefpython3```

And change your `app.run()` into `app.runCef()` in your main py file.

```
pyinstaller.exe YourGuyApp.py --noupx --onefile --noconsole  --add-data="static;static"
```

Notes:

    - `noupx` : because, with upx it gives me errors ;-)
    - `onefile` : to embed all needed runtime files.
    - `noconsole` : like you want ...
    - `add-data="static;static"` : to embed yours static file for rendering (css, images ...)
