#!/usr/bin/python3 -u
import guy

@guy.http(r"/item/(\d+)") 
def getItem(web,number):
    return Win(number)

class Win(guy.Guy):
    """
    Hello <<info>>

    <button onclick="self.test()">Test</button>
    """
    def __init__(self,q):
        self.info=q
        super().__init__()
  
    def test(self):
        return dict(script="""
        document.body.innerHTML+="ok";
        """)


class App(guy.Guy):
    """
    <a href="/item/42">Via HTTP hook</a>
    <a href="/Win?q=43">classic redirection</a>
    """    

        
        
if __name__ == "__main__": 
    app=App()
    app.serve()
