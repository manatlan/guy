#!/usr/bin/python3 -u
import guy,os,html

class Tag:
    tag="div" # default one
    def __init__(self,*contents,**attrs):
        self.tag=self.__class__.tag
        self.contents=contents
        self.attrs=attrs
        self.attrs["class"]=self.__class__.__name__
    def add(self,o):
        self.contents.append(o)
    def __repr__(self):
        attrs=['%s="%s"'%(k,html.escape(v)) for k,v in self.attrs.items()]
        return """<%(tag)s %(attrs)s>%(content)s</%(tag)s>""" % dict(
            tag=self.tag,
            attrs=" ".join(attrs),
            content=" ".join([str(i) for i in self.contents]),
        )
    def render(self):
        return """<script src="guy.js"></script>
<style>
div.HBox {display: flex;flex-flow: row nowrap;}
div.VBox {display: flex;flex-flow: column nowrap;}
div.HBox > *,div.VBox > * {flex: 1 1 auto;}
</style> <body>%s</body>""" % self


class Div(Tag):  pass
class HBox(Tag): pass
class VBox(Tag): pass
class Text(Tag):
    tag="span"
class Button(Tag):
    tag="button"


class JustGuy(guy.Guy):
    def render(self,path=None): #here is the magic
        return self.content.render()


class JustPy(JustGuy):
    size=(400,200)

    content=VBox(
        HBox(
            Text("t1"),
            Button('b1',onclick="self.clickme('1')"),
        ),
        HBox(
            Text("t2"),
            Button('b2',onclick='self.clickme("2")'),
        ),
    )

    def clickme(self,n):
        print("click",n)


if __name__=="__main__":
    app=JustPy()
    app.run()
