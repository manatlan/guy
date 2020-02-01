#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy

"""
The python eel "hello world" in a guy's app
(https://github.com/samuelhwilliams/Eel/tree/master/examples/01%20-%20hello_world)

NEED GUY >= 0.4.3
"""

class Hello(guy.Guy):
    """
    <script>
    guy.init( async function() { // ensure that everything is started/connected (socket cnx)
        say_hello_js( "Javascript World!" ) // say local hello from js world
        await self.say_hello_py("Javascript World!") // say python/distant hello from js world (await not needed in this case)
    })

    function say_hello_js(x) {  // declare a local method to print txt, js side
        document.body.innerHTML+= `Hello from ${x}<br>`;
    }
    </script>
    """
    size=(300, 200) # set the size of the client window

    async def init(self): # everything is started, we start the process
        self.say_hello_py("Python World!") # say local hello from pyworld
        await self.js.say_hello_js("Python World!") # say js/distant hello from pyworld

    def say_hello_py(self,x): # declare the python method, to be seen/used on js side.
        print('Hello from %s' % x)

if __name__ == "__main__":
    Hello().run(log=True)