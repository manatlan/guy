#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from guy import Guy,FULLSCREEN
import asyncio,datetime
CSS="""

main {filter: blur(20px);}

div#back {position:fixed;z-index:1;top:0px;left:0px;right:0px;bottom:0px;
    background-color: rgba(0,0,0, .2);
    text-align:center;
    text-shadow: 0 0 0.5em black, 0 0 0.2em white;
    box-shadow: inset 0 0 0.5em black, 0 0 0.2em white;
    color: white;
}
div#back button,div#back input {box-shadow: 0 0 0.5em black, 0 0 0.2em white;margin:4px}
"""


class Spinner(Guy):
    size=(300,20)
    __doc__="""
<style>
"""+CSS+"""
</style>
<div id='back'>
    <h3>Wait...</h3>
</div>
"""
    def init(self):
        print("I'm spinner")

class MsgBox(Guy):
    size=(300,150)
    __doc__="""
<style>
"""+CSS+"""
</style>
<div id='back'>
    <h3><<title>></h3>
    <button onclick="self.exit()">OK</button>
</div>
"""
    def __init__(self,title="unknown"):
        Guy.__init__(self)
        self.title=title

    def init(self):
        print("I'm MsgBox")



class Confirm(Guy):
    size=(300,20)
    __doc__="""
<style>
"""+CSS+"""
</style>
<div id='back'>
    <h3><<title>></h3>
    <button onclick="self.confirmChoice(true)">OK</button>
    <button onclick="self.confirmChoice(false)">Cancel</button>
</div>
"""
    def __init__(self,title):
        Guy.__init__(self)
        self.title=title
        self.ret=False

    def confirmChoice(self,val):
        self.ret=val
        self.exit()

    def init(self):
        print("I'm Confirm")


class Prompt(Guy):
    size=(300,20)
    __doc__="""
<style>
"""+CSS+"""
div#back form {display:inline}
</style>
<div id='back'>
    <h3><<title>></h3>
    <form onsubmit="self.post( this.txt.value ); return false">
        <input id='n' name="txt" value="<<txt>>" onfocus="var val=this.value; this.value=''; this.value= val;" />
        <button> > </button>
    </form>
    <button onclick="self.exit()">Cancel</button>
</div>
<script>
document.querySelector("#n").focus()
</script>
    """
    def __init__(self,title,txt=""):
        Guy.__init__(self)
        self.title=title
        self.txt=txt
        self.ret=None

    def post(self,txt):
        self.ret=txt
        self.exit()

    def init(self):
        print("I'm Prompt")

class Win(Guy):
    size=(400,500)
    #~ size = FULLSCREEN
    __doc__="""
<style>
body {background:#EEE;
    -webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
    font-size: 1.5em;
}
* {font-size: 1em;}
* {font-family: arial;-webkit-tap-highlight-color: transparent;outline: none;}
.click, button {cursor:pointer;color:blue}
button {border-radius:4px;background:blue;color:white }


</style>
<script>

async function change(title,item,el) {
    var w=await self.winPrompt(title, el.innerText )
    var r=await w.run()
    if(r.ret) {
        el.innerText=r.ret
        guy.cfg[item]=r.ret
    }
}

async function exit() {
    var w=await self.winConfirm()
    var r = await w.run()
    if(r.ret) guy.exit()
}

async function mbox() {
    var w=await self.winMbox()
    var r=await w.run();
}

async function wait() {
    var w=await self.winSpinner()
    setTimeout( w.exit, 1000)
}

document.addEventListener("contextmenu", function (e) {
        e.preventDefault();
    }, false);
</script>
<main>
    <button style="float:right" onclick="exit()">X</button>
    <h1>My GuyAPP ;-)</h1>
    <hr/>
    <div>
        Name: <span class='click' onclick="change('Name ?','name', this)"><<defaultName>></span>
    </div>
    <div>
        Surname: <span class='click' onclick="change('Surname ?','surname', this)"><<defaultSurname>></span>
    </div>

    <button onclick="mbox()">test</button>
    <button onclick="wait()">Wait</button>
</main>
 """
    def __init__(self):
        Guy.__init__(self)
        self.defaultName=self.cfg.name or "empty"
        self.defaultSurname=self.cfg.surname or "empty"

    def init(self):
        print("I'm Win")

    def winPrompt(self,txt,val):
        return Prompt(txt,val)

    def winConfirm(self):
        return Confirm("Quit ?")

    def winMbox(self):
        return MsgBox("Just a message box")

    def winSpinner(self):
        return Spinner()

if __name__ == "__main__":

    #~ x=MsgBox("Juste un test pour voir si ca marche toujours ;-)")
    #~ x.run()


    #~ x=Confirm("Quit?")
    #~ x.run()
    #~ print( x.ret )

    #~ x=Prompt("Name ?","kiki")
    #~ x.run()
    #~ print( x.ret )

    x=Win()
    # x.runCef()
    x.run(autoreload=True)
    # x.serve()


