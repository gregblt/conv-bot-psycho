#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 08:36:39 2018

@author: gregory
"""


from flask import Flask, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import json
import uuid
from app.botlogic import BotLogic

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dgslhenqaydtqj:72133439322c29aa8b3016d9b170be82cd7a0d89f09b2696c7e001ec5b1cf340@ec2-107-21-98-165.compute-1.amazonaws.com:5432/d8p00huj4sr3f1'

db = SQLAlchemy(app)

from app.models import User

db2=[]

# ACCESS_TOKEN = 'EAACawl29g0QBACM0wJqDiZANhKKwZA77d4Ot67gKzcPZB5wmIm3g1Kg3y2XmUaQTvEFZCZAAa63XYNGPZAjZCBBQ9CZB1Fr4Jlm6SXYqZBV1FekToIHxEGIeH7wOpdzEBbUmDe0VZCuZAYKeaokpGtnwPoJ6lzpNFbBhS3YXR9C0TxNlQZDZD'
# VERIFY_TOKEN = 'TESTINGTOKEN'
# bot = Bot(ACCESS_TOKEN)

dbfb=[]

@app.route('/add/')
def webhook():
    name = "ram"
    email = "ram@ram.com"
    u = User(id = 1, nickname = name, email = email)
    print("user created", u)
    db.session.add(u)
    db.session.commit()
    return "user created"

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
        