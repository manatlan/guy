# How to build an APK for Android

You will need to install [kivy](https://kivy.org/) and [buildozer](https://pypi.org/project/buildozer/) !

This How-to assume that you use a linux platform ;-)

## Limitations

- If you plan to use [vbuild](https://github.com/manatlan/vbuild) (to compile vue sfc components in html), to generate html. You can't use [PyComponents](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md). And you will need vbuild >= 0.8.1. (the module [pscript](https://github.com/flexxui/pscript/issues/38#issuecomment-521960204) can't be embedded in an apk)
- BTW, Some python modules can't be embedded in an APK. Use pure python modules !
- When you use html in docstring in a guy class. You will need to prefix your docstring like this `__doc__="""html"""`. Because buildozer remove real docstrings from py files.
- You can't run many instance in a GuyApp : only one ;-)
- Don't try to embed GuyApp which are runned by `app.runCef()` or `app.serve()` ... only `app.run()` will work ;-)

## install the tools :

```
sudo apt install python3-kivy
python3 -m pip install --upgrade buildozer
```
Note :

 - you should install the kivy version which belongs to your platform
 - For buildozer : you can pip it !

## Create your first Guy's app

Create an empty folder, and from it, run :

```
buildozer init
```

Note:

 - it will create ...

** TODO **
** TODO **
** TODO **

(mainly from https://linuxfr.org/news/minipy-un-serveur-python-dans-son-android )


## Authorize "Clear Text Traffic" in your APK
You will need to authorize your app to access the embedded python http server, which serve on localhost "http" only. To do that, you must enable "Clear Text Traffic" in your "AndroidManifest.xml". Using buildozer, you can change the template which will be used to generate the original.

Add `android:usesCleartextTraffic="true"` in tag `<application>` in `AndroidManifest.tmpl.xml`

** TODO **
** TODO **
** TODO **

## Test on your smartphone

Connect your smartphone with an usb cable to your computer, and run:

    $ buildozer android debug deploy run

Your app should start on the phone ;-)

## Deploy in play store

You will need to sign your apk, before uploading it.

** TODO **
** TODO **
** TODO **
