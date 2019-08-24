# How to build an exe for Windows

It can be very useful to distribute and exe on Microsoft Windows platforms.

You will need [pyinstaller](https://www.pyinstaller.org/) !

```
pyinstaller.exe YourGuyApp.py --noupx --onefile --noconsole --exclude-module cefpython3 --add-data="static;static"
```

Notes:

    - `noupx` : because, with upx it gives me errors ;-)
    - `onefile` : to embed all needed runtime files.
    - `noconsole` : like you want ...
    - `exclude-module cefpython3` : it depends on your need (with or without cef) to avoid to embed cefpython (+60mo) in the EXE. So you will need to have chrome on the host machine to be able to run the exe.
    - `add-data="static;static"` : to embed yours static file for rendering (css, images ...)