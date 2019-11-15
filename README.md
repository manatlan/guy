**GUY** is a py3 module, which let you quickly release a GUI (html/js) for yours python (>=3.5) scripts, targetting **any** platforms ... and **android** too. 

A simple **guy's app** code, could be :

```python
from guy import Guy

class Simple(Guy):
    """<button onclick="self.test()">test</button>"""

    def test(self):
        print("hello world")

if __name__ == "__main__":
    app=Simple()
    app.run()
```

A **guy's app** can be runned in 3 modes :

- can reuse a chrome browser (in app mode), on the host. To keep the minimal footprint. (**app mode**)
- can embbed its CEF (like electron) (thanks cefpython3), to provide all, to the users. (**cef mode**)
- can act as a classical web server. Any browser can be a client (**server mode**)

A **guy's app** can be released as :

 - a simple py3 file, with only guy dependancy (**app mode** & **server mode**)), or with guy+cefpython3 dependancies (**cef mode**))
 - a freezed executable (pyinstaller compliant) (all modes)
 - an **apk** (with buildozer/kivy) (**app mode** only)

Read the [Guy's DOCUMENTATION](https://guy-docs.glitch.me/) !

Available on :

 - [Guy's Github](https://github.com/manatlan/guy)
 - [Guy's Pypi](https://pypi.org/project/guy/)

Here is a [demo](https://starter-guy.glitch.me/#/) ([sources](https://glitch.com/edit/#!/starter-guy)), of a simple guy's app (server mode).

Here is a [demo](https://starter-guy-vuejs.glitch.me/#/) ([sources](https://glitch.com/edit/#!/starter-guy-vuejs)), of a guy's app serving a vuejs/sfc UI.

Here is a simple **guy's app** (**app mode**):
<p align="center">
    <table>
        <tr>
            <td valign="top">
                On Ubuntu<br>
<img src="https://raw.githubusercontent.com/manatlan/guy/master/docs/shot_ubuntu.png" width="300" border="1" style="border:1px solid black"/>             </td>
            <td valign="top">
                On Android 10<br>
    <img src="https://raw.githubusercontent.com/manatlan/guy/master/docs/shot_android10.jpg" width="300" border="1" style="border:1px solid black"/>                
           </td>
        </tr>
    </table>
</p>