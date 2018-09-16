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

def init_conv(template,bot_name):
    

    resp = make_response(render_template(template,
                                         chat=["Hi there  👋 ! What is your name?"]

                                         
                            )    
                        )
    
    
    current = json.dumps({
                    'current_step':BotLogic.STEP_GET_NAME
            })
    u=None
    if 'userId-psycho-bot' in request.cookies:
        u = Conversations.query.filter_by(cookie=request.cookies['userId-psycho-bot']).first()
        
    if u:
        if(bot_name=='Robert'):
            u.currentRobert = current
        elif(bot_name=='Jacques'):
            u.currentJacques = current
        elif(bot_name=='Bernard'):
            u.currentBernard = current
    else:      
        cookie=str(uuid.uuid4());
        resp.set_cookie('userId-psycho-bot', cookie)
        u = Conversations(cookie = cookie,
                          currentBernard=current,
                          currentJacques=current,
                          currentRobert=current)
        print("user created", u)
        db.session.add(u)
        
    db.session.commit()
                    
    return resp

 #We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/jacques", methods=['GET', 'POST'])
def receive_message():

    
    if request.method == 'GET':
        return init_conv('chat.html','Jacques')

    if request.method == 'POST':
        	return "not implemented"
    
@app.route("/api/v1/message",  methods=['POST'])
def post_message():
        
        # Get arguments
        data=json.loads(request.data)
        
        # Get conv status
        conversation=Conversations.query.filter_by(cookie=request.cookies['userId-psycho-bot']).first()

        # Get which bot
        bot_name=data['bot']
        print(bot_name)
        # Get next answer
        curr={}
        if(bot_name=='Robert'):
            curr=conversation.currentRobert
        elif(bot_name=='Jacques'):
            curr=conversation.currentJacques
        elif(bot_name=='Bernard'):
            curr=conversation.currentBernard
            
        bot=BotLogic(current=json.loads(curr),name=bot_name)
        ans=bot.get_next_answer(message=data['text'])
        chat=[]
        img=[]
        for value in ans:
            if 'text' in value:
                chat.append(value['text'])
                print(value['text'])
            if 'img' in value:
                img.append(value['img'])

        if bot_name == "Bernard":
            resp = make_response(render_template('msg_bot_nice.html',
                                             chat=chat,img=img))
        else:
            resp = make_response(render_template('msg_bot.html',
                                 chat=chat,img=img))
        # Update db
        current = bot.get_attributes()
        print(current)
        if(bot_name=='Robert'):
            conversation.currentRobert=json.dumps(current)
        elif(bot_name=='Jacques'):
            conversation.currentJacques=json.dumps(current)
        elif(bot_name=='Bernard'):
            conversation.currentBernard=json.dumps(current)
        
        db.session.commit()
        
        # Return response to client
        return resp
#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/bernard", methods=['GET', 'POST'])
def receive_message_nice():

    if request.method == 'GET':
        return init_conv('chat_nice.html','Bernard')
       
    if request.method == 'POST':
        	return "not implemented"

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/robert", methods=['GET', 'POST'])
def receive_message_ugly():

    if request.method == 'GET':
        return init_conv('chat_ugly.html','Robert')
       
    if request.method == 'POST':
            return "not implemented"
        