#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 12 08:36:39 2018

@author: gregory
"""


from flask import Flask, request, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
import json
import os
import uuid
from app.botlogic import BotLogic

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

from app.models import Conversations

def init_conv(template):
    
    cookie=str(uuid.uuid4());
    resp = make_response(render_template(template,
                                         chat=["Hi there  👋 ! What is your name?"]

                                         
                            )    
                        )
    resp.set_cookie('userId-psycho-bot', cookie)
    current = json.dumps({
                    'current_step':BotLogic.STEP_GET_NAME,
                    'user_name':None
            })
    u = Conversations(cookie = cookie, current=current)
    print("user created", u)
    db.session.add(u)
    db.session.commit()
                    
    return resp

 #We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/jacques", methods=['GET', 'POST'])
def receive_message():

    
    if request.method == 'GET':
        return init_conv('chat.html')

    if request.method == 'POST':
        	return "not implemented"
    
@app.route("/api/v1/message",  methods=['POST'])
def post_message():
        
        # Get arguments
        data=json.loads(request.data)
        
        # Get conv status
        conversation=Conversations.query.filter_by(cookie=request.cookies['userId-psycho-bot']).first()

        # Get next answer
        bot=BotLogic(current=json.loads(conversation.current))
        ans=bot.get_next_answer(message=data['text'])
        chat=[]
        img=[]
        for value in ans:
            if 'text' in value:
                chat.append(value['text'])
                print(value['text'])
            if 'img' in value:
                img.append(value['img'])
        resp = make_response(render_template('msg_bot_nice.html',
                                         chat=chat,img=img))
        # Update db
        current = bot.get_attributes()
        conversation.current=json.dumps(current)
        db.session.commit()
        
        # Return response to client
        return resp
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/bernard", methods=['GET', 'POST'])
def receive_message_nice():

    if request.method == 'GET':
        return init_conv('chat_nice.html')
       
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
        