0.7.2+ (IN PROGRESS ....the next one ;-)

 - EVOL: Add guy.WSGUY to be able to set manually the ws server (ex: glitch app with custom domain)) (ex: wss://example.com)
 - EVOL: automatically apply a "wsguy" class on body, when socket-communication (client to server)

0.7.2 (15/05/2020)

 - It's the version which shoulded be the 0.7.1, and fix that bug for real ;-) ... sorry for the noise

0.7.1 (14/05/2020)

 - FIX: reload(f5) was broken, when using self.render()
 - remove INST replaced by Guy._instances
 - create the instance in Guy._instances at __init__


0.7.0 (06/05/2020) : the REAL good one ;-)

 - EVOL (BROKE COMPATIBILITY): new way to return (.run()->x ,.runcef()->x,.serve()->x) with exit(x) : x is returned !
 - FIX: (server mode : isolation context execution was broken for 0.4.3 < version <=0.6.0 ) since commit "bf869e1cad5d630c1a2f38858b2da98ecaae60ce"
        Now, it's a lot better !
 - EVOL: remove (previously deprecated) "embedded window" (instanciateWindow)
 - EVOL: nice quit when cef is broken (cefpython3+py3.8.2 on linux)
 - EVOL: response content is gzipped now (thanks @icarito)
 - pytests 100%ok

0.6 (24/04/20)

 - new logo: and rendered as default favicon.ico
 - one mode available in app & cef mode : let run one instance only with chrome cache (stored belongs the guy's app). Else the app can't count - on cache/chrome ! (removed at end)
 - app-mode: new ChromeApp, better interaction with chrome !!
 - app-mode: when one mode on -> focus on current running (win+*nix)
 - cef-mode: when one mode on -> focus on current running (win only!!!) (broken on *nix)
 - app-mode: resize browser at start (no more js based)
 - app-mode: chrome process outputs to null
 - fix: logging server side
 - the use of embed window (returning guy class) is now (really) deprecated (wants to simplify)
 - app-mode: disable google translate

0.5.7: (14/04/2020)

    fix: dead socket on on_message

0.5.6: (09/04/2020)

    fix: js log was always on. now: it depends if the log is activated or on server side too

0.5.5: (26/03/2020)

 - FIX: on win, when freezed, cant be considered as module

0.5.4: (21/03/2020)

 - FIX: ability to read html files with encoding utf8 or cp1252
 - EVOL: expose config file path (py side) : self.cfg._file
 - EVOL: tornado application is available as "app" attribut on guy instance (for specials customizations), thanks @dferens !

0.5.3: (11/02/2020)
 - FIX: thanks @icarito https://github.com/manatlan/guy/pull/8/commits/9477b548b91ae81bfc327dac7ba1ec80804f4f8d

0.5.2: (09/02/2020)
 - FIX: guy crashed when autoreload with no static folder

0.5.1: (09/02/2020)
 - EVOL : autoreload available

0.5.0: (08/02/2020)
 - BIGGEST CHANGES:
    - "real instances" (no more clonage) .. a lot simpler
    - better system to manage instances (same fo embbeded or redirected)
    - pyside: each window now have a reference (.parent) to the main instance (the one which starts all)
    - a lot of little fixes
    - more pytest coverage (mainly main features)
    - _render() -> render() and replace "guy.js" in all cases
    - resolve query params when redirecting to another instance for match the constructor

0.4.3: (01/02/2020)
 - EVOL: Py side : can call js method directly ( `await self.js.jsmethod(...)` )

0.4.2: (31/01/2020)
 - FIX : trouble to find config folder when symbolic link used
 - EVOL: "init" can now be async too
 - FIX: the right "init" is now called when a instance is created (on ws call)

0.4.1: (31/01/2020)

- FIX: trouble with venv (ability to find static data)

0.4.0: (26/01/2020)

- BIG CHANGES :
    - Guy doesn't change/enforce the CWD !!!
    - Ability to be embbeded in a pip/package (see the how-to with poetry)
    - When pip-packaged : save in `~/.<package_name>.json`
    - The use of guy's config is now displayed in log (when log on)
    - use logging (no more print())

0.3.9: (16/11/2019)

- FIX: tornado/py3.8 on windows

0.3.8: (14/11/2019)

- FIX: better regex to replace guy.js script

changelog 0.3.7: initial public release (14/11/2019)

- "/guy.js" refer to the main instance now (like in the past)
- global method emit(event,*args) (old wsBroadcast())
- chrome's folder doesn't contains the port now ! (so same apps share the same chrome's cfg folder)
- guy.on("evt", ...) -> return an unsubscriber method (like wuy) (thanks PR from alemoreau)
- remove "reactivity commented code"

changelog 0.3.6 "i-wall":

- BIG CHANGE in jshandler ( guy.js -(when rendered)-> "/klassname/guy.js") (no more referer needed!!)
- BUG FIXED: nb crash when sockets change !!!!!!!
- BUG FIXED: when cloning instance : init() takes 1 positional argument but 2 were given
- http handler decorator (full verb support +async or sync), and ability to return Guy Instance (redirect url) !!!
- auto remove broken socket
- better children rendered (new methods)
- serve(...open=True...) to open browser by default

changelog 0.3.5:

- js handler now use urlparse (better)

changelog 0.3.4:

- ws reconnect on lost
- js for instanciateWindow is now attached in dom, no more only eval'uated

changelog 0.3.3:

- compat py35

changelog 0.3.2:

- jshandler: remove queryparams from referer
- _render: include "guy.js?<name>" to avoid history.back trouble for class with html embedded

changelog 0.3.1:

- MULTI PAGE, via children (useful in server mode !!!)
- GLOBAL STATIC FOLDER VAR
- remove js (=>) incompatibility for ie11

changelog 0.3:

- reactive property client side
- clone server instance at each socket
- on android : save the cfg in a persistant storage (can reinstall without loose)
- runner accept a log parameter, default to False
- manage ctrl-c
- better runner detection in android/kivy
- .server(port=8000) : can set a specific port in server mode, else 8000
- refacto ws.on_message
- evil script dict
- no more "guy.use"
- introduce self (current guy instance), js side !
- self != guy !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
- no more guy.EXIT()

changelog 0.2:

- fetch ssl bypass
- guy.EXIT()
