#!/usr/bin/python3 -u
import guy,os

class Tag:
    tag="div" # default one
    klass=""  # default one
    def __init__(self,*contents,**attrs):
        self.tag=self.__class__.tag
        self.contents=contents
        self.attrs=attrs
        if self.__class__.klass: self.attrs["class"]=self.__class__.klass
    def add(self,o):
        self.contents.append(o)
    def __repr__(self):
        attrs=['%s="%s"'%(k,v) for k,v in self.attrs.items()]
        return """<%(tag)s %(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag,
            attrs=" ".join(attrs),
            content=" ".join([str(i) for i in self.contents]),
        )
    def render(self):
        return """<script src="guy.js"></script>
<style>
div.hbox {display: flex;flex-flow: row nowrap;}
div.vbox {display: flex;flex-flow: column nowrap;}
div.hbox > *,div.vbox > * {flex: 1 1 auto;}
</style> <body>%s</body>""" % self


class Div(Tag):
    pass
class Text(Tag):
    tag="span"
class Button(Tag):
    tag="button"
class HBox(Tag):
    klass="hbox"
class VBox(Tag):
    klass="vbox"


class JustGuy(guy.Guy):
    def render(self,path=None): #here is the magic
        return self.content.render()


class JustPy(JustGuy):
    size=(400,200)

    content=VBox(
        HBox(
            Text("t1"),
            Button('b1',onclick="self.clickme(1)"),
        ),
        HBox(
            Text("t2"),
            Button('b2',onclick="self.clickme(2)"),
        ),
    )

    def clickme(self,n):
        print("click",n)


if __name__=="__main__":
    app=JustPy()
    #~ print(app.render())
    app.run()
