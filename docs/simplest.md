# The simplest guy app could look like this

```python
#!/usr/bin/env python3
from guy import Guy

class Simple(Guy):
    size=(400,400)
    __doc__="""<button onclick="test()">test</button>"""

    def test(self):
        print("hello world")

if __name__ == "__main__":
    gui=Simple()
    gui.run()
```

Will run an **app mode**. And can be runned on any OS (android, windows, *nix, mac/iOS, ...)


!!! info
    If you want to act as a cef instance, replace `gui.run()` by `gui.runCef()`

!!! info
    If you want to act as a http server, replace `gui.run()` by `gui.serve()`
