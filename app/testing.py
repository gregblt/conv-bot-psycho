#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 11:48:56 2018

@author: gregory
"""



from recastai import Request

request = Request('fe8f59c463abfca58a5bddf1ccacb0b7')

res = request.analyse_text("What can we talk about?")

res = request.analyse_text("Who can read our conversation?")

res = request.analyse_text("Good, nothing special")