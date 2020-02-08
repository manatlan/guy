0.5.0: (08/02/2020)
 - BIGGEST CHANGES:
    - "real instances" (no more clonage) .. a lot simpler
    - better system to manage instances (same fo embbeded or redirected) 
    - pyside: each window now have a reference (.parent) to the main instance (the one which starts all)
    - a lot of little fixes 
    - more pytest coverage (mainly main features)
    - _render() -> render()
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