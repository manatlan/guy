# How to migrate from wuy

**wuy** is the ancestor of **guy**.

- Replace all `wuy` keyword in your py and html/js files, by `guy`
- Replace `wuy.Window`/`wuy.Server` by `guy.Guy`
- `.get() & .set()` configs are replaced by `self.cfg` (py side) and `guy.cfg` (js side)
- At launch, get the instance, and apply one of theses methods:
    - instance.run() : for classical "app mode"
    - instance.runCef() : for app mode in cefpython3
    - instance.serve() : for classical "server mode"
- Rename your `web` folder to `static` folder, if needed.

From wuy:

```python
AppWindow()
```

to guy:

```python
app=AppWindow() 
app.run()
```

!!! info
    if socket close : client will reconnect ! (it will not close the app, like **wuy** did)