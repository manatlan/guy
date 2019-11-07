#!/usr/bin/python
# -*- coding: utf-8 -*-
from guy import Guy
import tornado
import os

class Win(Guy):
    size=(200,200)

    __doc__="""
    Hello <b self="name"></b>

    <button onclick="self.name='yo'">yolo</button>
    <button onclick="self.name='zu'">zut</button>
    <button onclick="self.change('ko')">server=ko</button>
    <button onclick="self.change('ki')">server=ki</button>


    """
    def init(self):
        self.name="world"

    def change(self,v):
        self.name = v


if __name__ == "__main__":
    x=Win()
    x.run()
