#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
import guy

# call a http service during an async rpc method call

class Fetch(guy.Guy):    # name the class as the web/<class_name>.html
    size=guy.FULLSCREEN
    __doc__="""
<style>
body,html,center {width:100%;height:100%;margin:0px;padding:0px;cursor:pointer;background:black}
img {
    max-height: 100%;
    width: auto;
}
div {position:fixed;top:10px;right:20px;z-index:2;color:red;font-size:100px;font-family:sans-serif}
</style>
<script>
var list=[];

guy.init( function() {

    guy.fetch("https://www.reddit.com/r/pics/.rss") // not possible with classic window.fetch()
        .then( x=>{return x.text()} )
        .then( x=>{
            list=x.match(/https:..i\.redd\.it\/[^\.]+\..../g)
            change()
        })

})

function change(n) {
    document.querySelector("#i").src=list[0];
    list.push( list.shift() )
}
</script>
<center>
<img id="i" src="" onclick="change()"/>
</center>
<div onclick="guy.exit()">X</div>
    """


if __name__=="__main__":
    Fetch().run()




