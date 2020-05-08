#!/usr/bin/python3 -u
from guy import Guy
import random

##################################################### my simplest sudoku resolver ;-)
free  = lambda n:     set("123456789.") ^ set(n)
carre = lambda g,x,y: g[y*9+x:y*9+x+3] + g[y*9+x+9:y*9+x+12] + g[y*9+x+18:y*9+x+21]
inter = lambda g,x,y: free(g[x::9]) & free(g[y*9:y*9+9]) & free(carre(g,(x//3)*3,(y//3)*3))
tri   = lambda k:     len(k[0])

def resolv(x):
    idxs = sorted([(inter(x,i%9,i//9),i) for i,c in enumerate(x) if c=='.'],key=tri)
    if not idxs: return x
    for c in idxs[0][0]:
        ng=resolv(x[:idxs[0][1]] + c + x[idxs[0][1]+1:])
        if ng: return ng
#####################################################


class Sudoku(Guy):
    """
    <style>
    body {margin:0px;text-align:center;background:buttonface}

    div#grid {
       margin:8px;
       border:2px solid black;
       display:inline-block;
    }
    div#grid > input:read-only {
        color:#AAA;
    }
    div#grid > input {
        text-align: center;
        font-size: 30px;
        width:40px;
        height:40px;
        display:block;
        border: 1px solid #ccc;
        float: left;
    }

    div#grid > input:nth-child(9n+4) {
        border-left:2px solid black;
    }
    div#grid > input:nth-child(9n+7) {
        border-left:2px solid black;
    }

    div#grid > input:nth-child(19),div#grid > input:nth-child(20),div#grid > input:nth-child(21),div#grid > input:nth-child(22),div#grid > input:nth-child(23),div#grid > input:nth-child(24),div#grid > input:nth-child(25),div#grid > input:nth-child(26),div#grid > input:nth-child(27) {
        border-bottom:2px solid black;
    }
    div#grid > input:nth-child(46),div#grid > input:nth-child(47),div#grid > input:nth-child(48),div#grid > input:nth-child(49),div#grid > input:nth-child(50),div#grid > input:nth-child(51),div#grid > input:nth-child(52),div#grid > input:nth-child(53),div#grid > input:nth-child(54) {
        border-bottom:2px solid black;
    }

    div#grid > input:nth-child(9n+1) {
        clear:both;
    }

    </style>
    <div id="grid"></div>
    <br/>

    <button onclick="doClear()">Clear</button>
    <button onclick="doRandom()">Random</button>
    <button onclick="doResolv()">Resolv</button>

    <script>
    function grid(g) {
        if(g) {
            let d = document.querySelector("#grid")
            d.innerHTML=""
            for(var i=1;i<=9*9;i++) {
                let c=g[i-1];
                let h=document.createElement("input")
                h.id=`c${i}` ;
                h.maxlength="1";
                h.value=c=="."?"":c
                if(c==".")
                    h.onclick=function() {this.select()}
                else
                    h.readOnly= true
                d.appendChild( h )
            }
        }
    }

    async function doClear() {
        grid(".................................................................................")
    }

    async function doRandom() {
        grid( await self.random() )
    }

    async function doResolv() {
        var g="";
        for(var i=1;i<=9*9;i++) {
            let c=document.querySelector(`#c${i}`).value.trim()
            if(c=="") c="."
            g+=("123456789".indexOf(c)>=0?c[0]:".");
        }
        grid( await self.resolv(g) )
    }

    </script>
    """
    size=(400,410)

    async def init(self):
        g = self.random()
        await self.js.grid(g)

    def resolv(self,g):
        gr=resolv(g)
        print("RESOLV: %s" % g)
        print("----->: %s" % gr)
        return gr

    def random(self):
        ll=list("123456789")
        random.shuffle(ll)
        ll=list(ll[0]+"."*80)
        random.shuffle(ll)

        ll=list(resolv("".join(ll)))
        for i in range(100):
            ll[ random.randint(0,80) ]="."
        g="".join(ll)
        print("RANDOM: %s" % g)
        return g


if __name__=="__main__":
    app=Sudoku()
    app.run()
