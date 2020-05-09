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
    body.bad input {
        color:red;
    }
    body.bad button#r {
        pointer-events:none;
        color:#FFF;
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

    div#grid > input:nth-child(9n+4), div#grid > input:nth-child(9n+7) {
        border-left:2px solid black;
    }

    div#grid > input:nth-child(19),div#grid > input:nth-child(20),div#grid > input:nth-child(21),div#grid > input:nth-child(22),div#grid > input:nth-child(23),div#grid > input:nth-child(24),div#grid > input:nth-child(25),div#grid > input:nth-child(26),div#grid > input:nth-child(27),div#grid > input:nth-child(46),div#grid > input:nth-child(47),div#grid > input:nth-child(48),div#grid > input:nth-child(49),div#grid > input:nth-child(50),div#grid > input:nth-child(51),div#grid > input:nth-child(52),div#grid > input:nth-child(53),div#grid > input:nth-child(54) {
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
    <button id="r" onclick="doResolv()">Resolv</button>

    <script>
    function setGrid(g) {
        document.body.className="";
        let d = document.querySelector("#grid")
        d.innerHTML=""
        for(var i=1;i<=9*9;i++) {
            let c=g[i-1];
            let h=document.createElement("input")
            h.id=`c${i}` ;
            if(c==".") {
                h.onclick=function() {this.select()}
                h.onchange=function() {doValid()}
            }
            else {
                h.value=c
                h.readOnly= true
            }
            d.appendChild( h )
        }
        undo = null;
    }

    function getGrid() {
        var g="";
        for(var i=1;i<=9*9;i++) {
            let c=document.querySelector(`#c${i}`).value.trim()
            g+=(c && "123456789".indexOf(c)>=0?c[0]:".");
        }
        return g
    }

    function doClear() {
        setGrid(".................................................................................")
    }

    async function doValid() {
        let err=await self.checkValid( getGrid() )
        document.body.className=err?"bad":"";
    }

    async function doRandom() {
        setGrid( await self.random() )
    }

    var undo=null;
    async function doResolv() {
        if(undo==null) {
            let current = getGrid()
            let r=await self.resolv( current )
            if(r) {
                setGrid( r )
                undo = current;
            }
        }
        else
            setGrid(undo);
    }

    </script>
    """
    size=(400,410)

    async def init(self):
        await self.js.setGrid( self.random() )

    def resolv(self,g):
        gr=resolv(g)
        print("RESOLV: %s" % g)
        print("----->: %s" % gr)
        return gr

    def random(self):
        ll=80*["."] + [ str(random.randint(1,9)) ]
        random.shuffle(ll)

        ll=list(resolv("".join(ll)))
        for i in range(100):
            ll[ random.randint(0,80) ]="."
        return "".join(ll)
    
    def checkValid(self,g):
        check9=lambda g: all([g.count(c)==1 for c in g.replace(".","")])
        for i in range(0,9):
            if not check9( g[i::9] ): return "Vertical trouble column %s"%i
            if not check9( g[i*9:i*9+9] ): return "Horiz trouble row %s"%i
            if not check9( carre(g,(i*3)%9,(i//3)*3) ): return "Trouble in %s square"%i

if __name__=="__main__":
    app=Sudoku()
    app.run()