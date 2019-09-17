#!/usr/bin/env python3
import guy,os
import vbuild # vbuild>=0.8.1 !!!!!!

class VueApp(guy.Guy):
    size=(400,200)

    def _render(self,path): #here is the magic
        # this method is overrided, so you can render what you want
        # load your template (from static folder)
        with open( os.path.join(path,"static/index.html") ) as fid:
            content=fid.read()

        # load all vue/sfc components
        v=vbuild.render( os.path.join(path,"static/*.vue") )

        # and inject them in your template
        return content.replace("<!-- HERE -->",str(v))

if __name__=="__main__":
    VueApp().run()
