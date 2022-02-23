# How to migrate from wuy

(**wuy** is the ancestor of **guy**)

- Replace all `wuy` keyword in your py files, by `guy`
- Replace all `wuy` in html/js files, by `guy` (for core methods) or `self` (for those which you have declared in your class) ... see ([client side](client.md))
- Replace `wuy.Window`/`wuy.Server` by `guy.Guy`
- `.get() & .set()` configs are replaced by `self.cfg` (py side) and `guy.cfg` (js side)
- Rename your `web` folder to `static` folder, if needed.
- At launch, get the instance, and apply one of theses methods:
    - instance.run() : for classical "app mode"
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

!!! info
    Here is my biggest [wuy's app migration to guy](https://github.com/manatlan/jbrout3/commit/17ca6f5054f04de88af2ffdf27468f4c48ee9725)

!!! info
    if socket close : client will reconnect ! (it will not close the app, like **wuy** did)