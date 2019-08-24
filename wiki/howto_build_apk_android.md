# How to build an APK for Android

You will need to install [kivy](https://kivy.org/) and [buildozer](https://pypi.org/project/buildozer/) !

This How-to assume that you use a linux platform ;-)

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
