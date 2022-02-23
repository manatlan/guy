# How to build an APK for Android


You will need to install [kivy](https://kivy.org/) and [buildozer](https://pypi.org/project/buildozer/) !

This How-to assume that you use a linux platform ;-)


## Install the tools

```
sudo apt install python3-kivy zipalign
python3 -m pip install --upgrade buildozer
```
Note :

 - you should install the kivy version which belongs to your platform
 - For buildozer : you can pip it !

## Create your first Guy's apk

Create an empty folder, and from a console inside the folder

Get `guy.py` module (needed, to be embedded in apk)

    wget https://raw.githubusercontent.com/manatlan/guy/master/guy.py
    
Get an icon/splashscreen for the apk

    wget https://raw.githubusercontent.com/manatlan/guy/master/android/data/logo.png

Create the file `buildozer.spec` ([specs](https://buildozer.readthedocs.io/en/latest/specifications.html)), with this content:

    [app]
    title = Guy Demo
    package.name = com.guy
    package.domain = demo
    source.dir = .
    source.include_exts =
    version = 0.1
    requirements = python3,kivy,tornado
    presplash.filename = %(source.dir)s/logo.png
    icon.filename = %(source.dir)s/logo.png
    orientation = portrait
    osx.python_version = 3
    osx.kivy_version = 1.9.1
    fullscreen = 0
    android.permissions = INTERNET
    android.api = 28
    android.ndk = 17c
    android.arch = arm64-v8a

    [buildozer]
    log_level = 2
    warn_on_root = 1

(You can setup your [android.permissions](https://developer.android.com/reference/android/Manifest.permission.html) according your needs (separated by comma "`,`"))

Create the file `main.py` (your file app should be named `main.py`, it's a buildozer's request):

```python
from guy import Guy

class Hello(Guy):
    __doc__="""<button onclick="self.test().then( function(x) {document.body.innerHTML+=x})">test</button>"""

    def test(self):
        return "hello world"

if __name__ == "__main__":
    app=Hello()
    app.run()
```

Run the app in your environment ... to be sure it works as is

    python3 main.py

Connect your smartphone with an usb cable to your computer (and allow `file transfer` mode in your android), and run:

    buildozer android debug deploy run

First run is very long (more than 20min on my computer), second run is a lot faster (10sec) ...

Your android will prompt you to authorize the installation : check yes ...

Your app should start on the phone ;-)



!!! info
    But, recent android, doesn't allow to use http traffic (error `ERR_CLEARTEXT_NOT_PERMITTED`). So you will need to authorize "Clear Text Traffic" for your APK. It's not a problem, or a security risk (the app will only listening http on localhost), see next section.



## Authorize "Clear Text Traffic" in your APK
You will need to authorize your app to access the embedded python http server, which serve on localhost "http" only. To do that, you must enable "Clear Text Traffic" in your "AndroidManifest.xml". Using buildozer, you can change the template which will be used to generate the original.

Open your file `.buildozer/android/platform/build/dists/<<package.name>>/templates/AndroidManifest.tmpl.xml`
(.buildozer/android/platform/build/dists/com.guy/templates/AndroidManifest.tmpl.xml)

Add `android:usesCleartextTraffic="true"` in tag `<application>` in `AndroidManifest.tmpl.xml`

Search the tag `<application>` which look like this :

```xml
    <application android:label="@string/app_name"
                 android:icon="@drawable/icon"
                 android:allowBackup="{{ args.allow_backup }}"
                 android:theme="@android:style/Theme.NoTitleBar{% if not args.window %}.Fullscreen{% endif %}"
                 android:hardwareAccelerated="true" >
```
And change it to :
```xml hl_lines="3"
    <application android:label="@string/app_name"
                 android:icon="@drawable/icon"
                 android:usesCleartextTraffic="true"
                 android:allowBackup="{{ args.allow_backup }}"
                 android:theme="@android:style/Theme.NoTitleBar{% if not args.window %}.Fullscreen{% endif %}"
                 android:hardwareAccelerated="true" >
```

!!! tip
    If you modify `buildozer.spec`, it can alter the manifest. So you will need to reproduce this step !

Alternatively, you can use this sed command to do it, in one line

    sed -i 's/<application android:label/<application android:usesCleartextTraffic="true" android:label/g' .buildozer/android/platform/build/dists/com.guy/templates/AndroidManifest.tmpl.xml

## Deploy in android's playstore

You will need to sign your apk, before uploading it. You will need [OpenJDK tools](https://openjdk.java.net/tools/index.html) !

To release your apk:

    buildozer android release

It will produce an apk file ... but the command ends with an error "FileNotFoundError: [Errno 2] No such file or directory ...""

In fact, the APK release is here : ".buildozer/android/platform/build/dists/com.guy/build/outputs/apk/release/com.guy-release-unsigned.apk"

Just copy it, in the `bin` folder:

    cp .buildozer/android/platform/build/dists/com.guy/build/outputs/apk/release/com.guy-release-unsigned.apk bin/

To sign your APK, you will need to create your self-signed key !

    keytool -genkey -v -keystore my-app.keystore -alias cb-play -keyalg RSA -keysize 2048 -validity 10000

When you get your keystore (file `my-app.keystore `), you can sign the apk, by doing :

    jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore ./my-app.keystore ./bin/com.guy-release-unsigned.apk  cb-play

When it's done, just [zipalign](https://developer.android.com/studio/command-line/zipalign) the apk, like that :

    zipalign -v 4 ./bin/com.guy-release-unsigned.apk ./bin/myapp.apk

Now, your apk `myapp.apk` can be distributed, or uploaded to [playstore](https://play.google.com/apps/publish).

!!! info
    Here is the [myapp.apk (~13Mo)](https://cdn.glitch.com/00392733-d07a-42ad-a17a-c0df9475b388%2Fmyapp.apk?v=1574618969557), that I have released when following this howto. Succesfully installed and tested on android9 & android10 ! And here is [this apk on the playstore](https://play.google.com/store/apps/details?id=demo.com.guy) !


    

## Known Limitations

- The **android's BACK KEY** does nothing ;-( (NEED TO IMPROVE THAT). You should provide a way to let the user quit your app (by calling `self.exit()`)
- If you plan to use [vbuild](https://github.com/manatlan/vbuild) (to compile vue sfc components in html), to generate html. You can't use [PyComponents](https://github.com/manatlan/vbuild/blob/master/doc/PyComponent.md). And you will need vbuild >= 0.8.1. (the module [pscript](https://github.com/flexxui/pscript/issues/38#issuecomment-521960204) can't be embedded in an apk)
- BTW, Some python modules can't be embedded in an APK : use pure python modules !
- When you use html in docstring in a guy class. You will need to prefix your docstring like this `__doc__="""html"""`. Because buildozer remove real docstrings from py files.
- Don't try to embed a GuyApp which are runned by `app.runCef()` or `app.serve()` ... only `app.run()` will work ;-)


## Sources 

 * [https://linuxfr.org/news/minipy-un-serveur-python-dans-son-android](https://linuxfr.org/news/minipy-un-serveur-python-dans-son-android)