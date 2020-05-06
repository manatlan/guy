#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from guy import Guy

class Glob:
  i=0
  def test(self):
    Glob.i+=1
    return Glob.i

#==========================================
class Marco(Guy,Glob):
#==========================================
  """ Hello Marco

      <script>
      async function aff( am ) {document.body.innerHTML+=await am();}
      </script>

      <button onclick="aff( self.t1 )">t1</button>
      <button onclick="aff( self.test )">Test</button>


      <a href="/Polo">go to polo</a>
      <a href="/nowhere">go to nowhere</a>
      <a href="/logo.png">go to logo.png</a>

      <button onclick="self.open()">open</button>
  """

  def init(self):
    print("Start Marco")

  def open(self):
    return Polo()

  def t1(self):
    return "t1"


#==========================================
class Polo(Guy,Glob):
#==========================================
  """ Hello Polo

      <script>
      async function aff( am ) {document.body.innerHTML+=await am();}
      </script>

      <button onclick="aff( self.t2 )">t2</button>
      <button onclick="aff( self.test )">Test</button>

      <a href="/">go to marco</a>
  """

  def init(self):
    print("Start Polo")

  def t2(self):
    return "t2"


if __name__ == "__main__":
    app=Marco()
    app.run(log=True)
    #~ app.run()

