# Multiple instances

Not like the good old [wuy](https://github.com/manatlan/wuy). With **guy** : you can use multiple guy's instance ! It's the main new feature over **wuy**.

You can declare many Guy's class, and use them in a same app : it's easier to make bigger app ; you can leverage your logic/ui in multiple guy's class component.

You can use theses others guy's class, using a simple **Navigate to another window**

!!! info
    Note that the 'main instance' refers to the one which starts the loop. This instance will live til its dead (exit). Others guy's instances are (re)created on demand.
    So, the main instance can be useful to store persistent data during the life of the guy's app. Each instances have always access to the main one, using [self.parent](server.md#selfparent).
    

## Navigate to another window

Consider this guy's app:

```python
from guy import Guy

class Page2(Guy):
  """ 
      <<txt>>
      <a href="/Page1">go to Page1</a>
      <a href="/">go to Page1 too !</a>
  """
  def __init__(self,txt):
    Guy.__init__(self)
    self.txt = txt

class Page1(Guy):
  """ 
      <a href="/Page2?txt=Hello">go to Page2</a>
  """

if __name__ == "__main__":
    app=Page1()
    app.run()
```

When the app is started, the `Page1` will be rendered, and you can navigate to `Page2`, and go back to `Page1`. Each page/class is available under its name.

The main instance, is the default one, and is available at root ('/') too.

BTW, when you are on `Page2`, `Page1` methods are not available anymore, and vis versa (the other instance is "dead", in fact).

See [testRedirect.py](https://github.com/manatlan/guy/blob/master/testRedirect.py)

!!! info
    - All windows share the same socket ! But each instance (on server side) is unique to a client.
    - Since >= 0.5.0, query parameters are used to resolve the constructor signature
