#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
class GlobalIp:

    def __init__(self, sio=None):
        self.map={}

    def set_ip(self, key, value):

        self.map[key] = value
    def get_ip(self):
        return self.map
    def print_ip(self):
        for key in self.map:
            print (key, "value:", self.map[key])
    def find_ip(self,path):
        for key in list(self.map.keys()):
            if self.map[key]['Path'] == path:
                return 1

    def delete_ip(self,path):
        for key in list(self.map.keys()):
            if self.map[key]['Path'] == path:
                self.map.pop(key)


