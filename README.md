**GUY** is a py3 module, which let you quickly release a GUI (html/js) for yours python (>=3.5) scripts, targetting **any** platforms ... and **android** too.

A simple **guy's app** code, could be :

```python
from guy import Guy

class Simple(Guy):
    """<button onclick="self.test()">test</button>"""

    async def test(self):
        print("Your name is", await self.js.prompt("What's your name ?") )

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
 - a [pip/package app](https://guy-docs.glitch.me/howto_build_whl_package/) (all modes)
 - an **apk** for android (with buildozer/kivy) (**app mode** only)

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
<img src="https://manatlan.github.io/guy/shot_ubuntu.png" width="300" border="1" style="border:1px solid black"/>             </td>
            <td valign="top">
                On Android10<br>
    <img src="https://manatlan.github.io/guy/shot_android10.jpg" width="300" border="1" style="border:1px solid black"/>
           </td>
        </tr>
    </table>
</p>

[![Join the chat at https://gitter.im/guy-python/community](https://badges.gitter.im/jessedobbelaere/ckeditor-iconfont.svg)](https://gitter.im/guy-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

If you want to build guy app, without any html/js/css knowlegments, you can try [gtag](https://github.com/manatlan/gtag) : it's a guy sub module which let you build GUI/GUY app in [more classical/python3 way](https://github.com/manatlan/gtag/wiki).