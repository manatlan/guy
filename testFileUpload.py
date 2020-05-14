#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import guy


class FileUpload(guy.Guy):
    """
    <style>
    div#drop {
        border:2px dotted green;
        padding:10px;
    }
    </style>
    <body oncontextmenu="return false">
        <hr>
        <input type="file" onchange="upload(this.files[0])"/>
        <hr>
        <div id="drop" ondrop="drop(event)" ondragover="allow(event)">drop files here</div>
        <hr>

    </body>
    <script>

    function allow(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
    }

    function drop(e) {
        if(e.dataTransfer.files) upload(e.dataTransfer.files[0])
        e.preventDefault();
    }
    
    function upload(file) {
        let reader = new FileReader();
        //reader.readAsText(file, "UTF-8");
        reader.readAsBinaryString(file);
        reader.onload = async function (evt) {
            await self.upload( file.name, evt.target.result )
        }
    }

    function add(txt) {
        document.body.innerHTML+=`<li>${txt}</li>`;        
    }
    
    </script>
    """
    size=(300,300)

    
    async def upload(self, name,content):
        await self.js.add(name+" (%s)"%len(content))

if __name__=="__main__":
    FileUpload().run()
