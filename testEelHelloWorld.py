#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy

"""
The python eel "hello world" in a guy's app
(https://github.com/samuelhwilliams/Eel/tree/master/examples/01%20-%20hello_world)
"""

class Hello(guy.Guy):
    """
    <script>
    guy.init( async function() { // ensure that everything is started/connected (socket cnx)

        // declare a local method to print txt, js side
        function say_hello_js(x) { 
            document.body.innerHTML+= `Hello from ${x}<br>`;
        }

        // assign an event to call the local method
        guy.on("say_hello_js", say_hello_js)

        // say local hello from js world
        say_hello_js( "Javascript World!" )

        // say python/distant hello from js world
        await self.say_hello_py("Javascript World!")
    })
    </script>
    """
    size=(300, 200) # set the size of the client window

    async def init(self): # everything is started, we start the process
        # say local hello from pyworld
        self.say_hello_py("Python World!")
        # say js/distant hello from pyworld
        await self.emitMe("say_hello_js","Python World!")

    def say_hello_py(self,x): # declare the python method, to be seen/useful on js side.
        print('Hello from %s' % x)

if __name__ == "__main__":
    Hello().run()