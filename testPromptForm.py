# -*- coding: utf-8 -*-
import guy

class Prompt(guy.Guy):
    """
        <style>body {background:#EEE}</style>

        <<title>> ?
        <form onsubmit="self.post( this.txt.value ); return false">
            <input name="txt" value="<<value>>"/>
            <input type="submit" value="ok"/>
        </form>    
    """
    size=(300,200)

    def __init__(self,title,value=""):
        self.title=title
        self.value=value
        super().__init__()

    def post(self,value):
        if value.strip():
            self.exit(value.strip())

if __name__=="__main__":
    app=Prompt("name","yolo")
    print(app.run())
