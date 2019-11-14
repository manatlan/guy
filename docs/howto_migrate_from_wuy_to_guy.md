# How to migrate from wuy

- Replace all `wuy` keyword in your py and html/js files, by `guy`
- Replace `wuy.Window`/`wuy.Server` by `guy.Guy`
- `.get() & .set()` configs are replaced by `self.cfg` (py side) and `guy.cfg` (js side)
- At launch, get the instance, and apply one of theses methods:
    - instance.run() : for classical "app mode"
    - instance.runCef() : for app mode in cefpython3
    - instance.serve() : for classical "server mode"

From wuy:

```python
AppWindow()
```

to guy:

```python
app=AppWindow() 
app.run()
```

NOTE:

 - if socket close : client will reconnect !