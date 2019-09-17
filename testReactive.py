#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,re
import guy

class Win(guy.Guy):
    size=(200,200)

    orig="hello"

    __doc__="""
    <i self=orig></i> <b self="name"></b>

    <button onclick="self.name='yo'">yolo</button>
    <button onclick="self.name='zu'">zut</button>
    <button onclick="self.change('ko')">server=ko</button>
    <button onclick="self.change('ki')">server=ki</button>
    <button onclick="self.prints()">print server state</button>

    <input self="name"/>
    """
    def init(self):
        self.name="world"

    def change(self,v):
        self.name = v

    def prints(self):
        print(self._dict)


if __name__ == "__main__":
    Win().run(True)
