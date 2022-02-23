# The simplest guy app could look like this

```python
#!/usr/bin/python3 -u
from guy import Guy

class Simple(Guy):
    """<button onclick="self.test()">test</button>"""

    def test(self):
        print("hello world")

if __name__ == "__main__":
    app=Simple()
    app.run()
```

Will run an **app mode**. And can be runned on any OS (android, windows, *nix, mac/iOS, ...)


!!! info
    If you want to act as a cef instance, replace `app.run()` by `app.runCef()`

    If you want to act as a http server, replace `app.run()` by `app.serve()`
