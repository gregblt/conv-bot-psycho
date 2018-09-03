#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 08:36:39 2018

@author: gregory
"""


from flask import render_template, make_response
import random
from flask import Flask, request
import requests
import json
import uuid
from random import randint
import sys
from app.botlogic import BotLogic

app = Flask(__name__)

db2=[]

# ACCESS_TOKEN = 'EAACawl29g0QBACM0wJqDiZANhKKwZA77d4Ot67gKzcPZB5wmIm3g1Kg3y2XmUaQTvEFZCZAAa63XYNGPZAjZCBBQ9CZB1Fr4Jlm6SXYqZBV1FekToIHxEGIeH7wOpdzEBbUmDe0VZCuZAYKeaokpGtnwPoJ6lzpNFbBhS3YXR9C0TxNlQZDZD'
# VERIFY_TOKEN = 'TESTINGTOKEN'
# bot = Bot(ACCESS_TOKEN)

dbfb=[]

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/jacques", methods=['GET', 'POST'])
def receive_message():

    
    if request.method == 'GET':
        userId=str(uuid.uuid4());
        resp = make_response(render_template('chat.html',
                                             chat=["Hi there  👋🏻 ! What is your name?"]

                                             
                                )    
                            )
        resp.set_cookie('userId-travelbot', userId)
        db2.append({'id':userId,'current':{'currentStep':2,'city':'','searchResults':[],'currentCursor':0,
                   'active':None,'metropolitan':None}})
                        
        return resp
    if request.method == 'POST':
    	return "not implemented"
    
@app.route("/api/v1/message",  methods=['POST'])
def post_message():
        
        # Get arguments
        data=json.loads(request.data)
        
        # Get next answer
        bot=BotLogic(current={'current_step':BotLogic.STEP_GET_NAME})
        ans=bot.get_next_answer(message=data['text'])
        chat=[]
        for value in ans:
            if 'text' in value:
                chat.append(value['text'])
        resp = make_response(render_template('msg_bot_nice.html',
                                         chat=chat))        
        return resp
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/bernard", methods=['GET', 'POST'])
def receive_message_nice():

    
    if request.method == 'GET':
        userId=str(uuid.uuid4());
        resp = make_response(render_template('chat_nice.html',
                                             chat=["Hi there 👋! What is your name?"]

                                             
                                )    
                            )
        resp.set_cookie('userId-travelbot', userId)
        db2.append({'id':userId,'current':{'currentStep':2,'city':'','searchResults':[],'currentCursor':0,
                   'active':None,'metropolitan':None}})
                        
        return resp
    if request.method == 'POST':
    	return "not implemented"

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/robert", methods=['GET', 'POST'])
def receive_message_ugly():

    
    if request.method == 'GET':
        userId=str(uuid.uuid4());
        resp = make_response(render_template('chat_ugly.html',
                                             chat=["Hi there."],quickReplies=[{'title':"Good",'payload':"good"}
                                             ,{'payload':'bad','title':"I have been better"}]

                                             
                                )    
                            )
        resp.set_cookie('userId-travelbot', userId)
        db2.append({'id':userId,'current':{'currentStep':2,'city':'','searchResults':[],'currentCursor':0,
                   'active':None,'metropolitan':None}})
                        
        return resp
    if request.method == 'POST':
        return "not implemented"
        

if __name__ == "__main__":
    app.run()