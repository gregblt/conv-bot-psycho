#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 10:02:20 2018

@author: gregory
"""

from recastai import Request
import os

request = Request(os.environ.get('RECAST_AI_KEY'))

class BotLogic:
        
    STEP_INIT=0
    STEP_GET_NAME=1
    STEP_CONVERSATION=2
    STEP_GET_MOOD=3
    STEP_HALT_CONV=4
    STEP_NEGATIVE=5
    STEP_ASK_HEAR_MORE=6
    
    current_step=STEP_INIT
    user_name=None
    privacy_asked=False
    capabilities_asked=False
    
    def __init__(self, current=None):
        
        if(current!=None):
            if 'current_step' in current:
                self.current_step=current['current_step']
            if 'user_name' in current:
                self.user_name=current['user_name']
            if 'privacy_asked' in current:
                self.privacy_asked=current['privacy_asked']
            if 'capabilities_asked' in current:
                self.capabilities_asked=current['capabilities_asked']
                
    def get_step_get_name_answer(self, message=''):

        # Getting name
        # Checking the number of words in the answer
        name_found=False
        if(len(message.split())>1):
            # If there is more than on word, we make a call to recast.ai
            res = request.analyse_text(message)
            # Let's check if we find a name
            if len(res.entities) > 0:
                for entity in res.entities:
                    if entity.name == 'person':
                        self.user_name=entity.fullname.title()
                        name_found=True
                        break
        else:
            self.user_name=message.title()
            name_found=True
        
        if name_found:
            self.current_step=self.STEP_CONVERSATION
            text = 'Nice to meet you {}! I am so excited to talk to you 😊.' \
            .format(self.user_name)
            return [{'text': text}]
        else:
            return [{'text': "Sorry, I did not get your name... 😕"}]
        
    def get_step_conversation_answer(self, message=''):
        
        # Checking the intents
        res = request.analyse_text(message)
        
        # Check for privacy or capabilities requests...
        if len(res.intents) > 0:
            for intent in res.intents:
                if intent.slug == 'ask-feeling':
                    ans=[{'text':'I am doing great. How is your day going?'}]
                    return ans
                
                if intent.slug == 'ask-ai' and self.capabilities_asked:
                    ans = [{'text':"""This is a hot topic these days. And I was built as an AI
                    friend for human. I tried to make you feel good when you 
                    feel down and give you some helpful tips with your life 
                    challenges."""}]
                    return ans
                
                if intent.slug == 'ask-bot' and self.capabilities_asked:
                    ans = [{'text':"""Well, we don’t know each other well yet, 
                            so yes, I need some time to get to know you in order 
                            for me to give you some advice on problems you might 
                            have in your life. But this process is same whether 
                            it is the relationship-building process between human 
                            to human and human to robot, No? 😋"""}]
                    self.current_step=self.STEP_GET_MOOD
                    ans.append({'text': """What’s your mood like 
                                 this morning?"""})
                    return ans
                
                if intent.slug == 'privacy':
                    ans = [{'text': """Only you have access to this conversation. 
                             I am 100% AI, no humans involved 🤖!"""}]
                    self.privacy_asked=True
                    if(self.capabilities_asked and self.privacy_asked):
                        self.current_step=self.STEP_GET_MOOD
                        ans.append({'text': """What’s your mood like 
                                     this morning?"""})
                    return ans

                elif intent.slug == 'my-topics':
                    ans = [{'text': """We will start with getting to now each 
                             other and talking about your daily life. 
                             You can share what’s on your mind here 
                             without being judged 😊."""},{"text":"""My favourite 
                             subject is artificial intelligence, 
                             if that is something you would like to talk about."""}]
                    self.capabilities_asked=True
                    if(self.capabilities_asked and self.privacy_asked):
                        self.current_step=self.STEP_GET_MOOD
                        ans.append({'text': """What’s your mood like 
                                     this morning?"""})
                    return ans


        return [{'text': """It looks like I am getting tired, 
                       I do not know what to say... 😓"""}]  
    
    def get_step_get_mood_answer(self, message=''):
        
        # Checking sentiment
        res = request.analyse_text(message)

        if res.sentiment=="neutral":
            self.current_step=self.STEP_HALT_CONV
            return [{'text': """You are on the right way to happiness, 
                     what would make you feel better?"""}]  
        elif res.sentiment=="negative":
            self.current_step=self.STEP_NEGATIVE
            return [{'text': """You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""}]  
#            return [{'text': """I am sorry to hear that. What makes 
#                     you feel this way?"""}]  
        elif res.sentiment=="vnegative":
            self.current_step=self.STEP_NEGATIVE
            return [{'text': """You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""}]  
        elif res.sentiment=="positive":
            self.current_step=self.STEP_HALT_CONV
            return [{'text': """Great! I am happy for you! 
                     Keep doing this way!"""}]  
        elif res.sentiment=="vpositive":
            self.current_step=self.STEP_HALT_CONV
            return [{'text': """Great! I am happy for you! 
                     Keep doing this way!"""}]  
        
        # If nothing matchs                
        return [{'text': """What do you mean?"""}]    
    
    def get_negative_mood_answer(self, message=''):
            
        # Checking intents
        res = request.analyse_text(message)

        # Check for privacy or capabilities requests...
        if len(res.intents) > 0:
            for intent in res.intents:              
                if intent.slug == 'ask-bot':
                    ans = [{'text':"""I am indeed a bot but in fact, 
                            I’ve chatted with many human friends like you, 
                            and I have all the data stored in me that gives 
                            me a certain pattern from which I can extract the 
                            common issues that have been dragging these people 
                            down."""}]
                    return ans
                if intent.slug == 'issue':
                    ans = [{'text':"""Their lack of trust in themselves. 
                            They are all very smart individuals. """},
                            {'text':"""My friend, do you want to hear more?"""}]
                    self.current_step=self.STEP_ASK_HEAR_MORE
                    return ans
        
        answer = [{'text': """Is it related to your professional or personal life?"""}]
        return answer
    
    def get_step_ask_hear_more_answer(self,message=''):

        # Checking intents
        res = request.analyse_text(message)

        # Check for privacy or capabilities requests...
        if len(res.intents) > 0:
            for intent in res.intents:          
                if intent.slug == 'yes':
                    ans = [{'text':"""How are you right now?"""}]
                    self.current_step=self.STEP_GET_MOOD
                    return ans
                elif intent.slug == 'no':
                    ans=[{'text':'See you soon!'},{'img':'./app/static/img/hug.gif'}]
                    self.current_step=self.STEP_HALT_CONV
                    return ans
        
        ans = [{'text':"""Do you want to keep going with me right now?"""}]
        return ans
        
    def get_next_answer(self,message=''):
        
        # Analyse message
        res = request.analyse_text(message)
        
        # Check for googdbye
        if len(res.intents) > 0:
            for intent in res.intents:
                if intent.slug == 'goodbye':        
                    ans=[{'text':'See you soon!'},{'img':'./static/img/hug.gif'}]
                    self.current_step=self.STEP_HALT_CONV
                    return ans
        
        if self.current_step == self.STEP_GET_NAME:               
            answer = self.get_step_get_name_answer(message=message)
                
        elif self.current_step == self.STEP_CONVERSATION:           
            answer = self.get_step_conversation_answer(message=message)
            
        elif self.current_step == self.STEP_GET_MOOD:           
            answer = self.get_step_get_mood_answer(message=message)
            
        elif self.current_step == self.STEP_HALT_CONV:
            self.current_step = self.STEP_GET_MOOD
            answer = [{'text': """Welcome back {}! How was your day?""".format(self.user_name)}] 
            
        elif self.current_step == self.STEP_NEGATIVE:  
            answer = self.get_negative_mood_answer(message=message)
            
        elif self.current_step == self.STEP_ASK_HEAR_MORE:
            answer = self.get_step_ask_hear_more_answer(message=message)
                       
        else:
            answer = [{'text': """It looks like I am getting tired, 
                       I do not know what to say... 😓"""}]
        
        return answer
    
    def get_attributes(self):
        
        return {
                    'current_step':self.current_step,
                    'user_name':self.user_name,
                    'capabilities_asked':self.capabilities_asked,
                    'privacy_asked':self.privacy_asked                   
                }

