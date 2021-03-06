#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 10:02:20 2018

@author: gregory
"""

from recastai import Request
import os
from nltk.tokenize import sent_tokenize

request = Request(os.environ.get('RECAST_AI_KEY'))

class BotLogic:
        
    STEP_INIT=0
    STEP_GET_NAME=1
    STEP_GET_PRE_MOOD=7
    STEP_CONVERSATION=2
    STEP_GET_MOOD=3
    STEP_HALT_CONV=4
    STEP_NEGATIVE=5
    STEP_ASK_HEAR_MORE=6
    
    current_step=STEP_INIT
    user_name=None
    privacy_asked=False
    capabilities_asked=False
    lost=False
    reason_given=False
    lost_count = 0
    resume_sentence = None
    
    def __init__(self, current=None, name=None):
        
        if(current!=None):
            if 'current_step' in current:
                self.current_step=current['current_step']
            if 'user_name' in current:
                self.user_name=current['user_name']
            if 'privacy_asked' in current:
                self.privacy_asked=current['privacy_asked']
            if 'capabilities_asked' in current:
                self.capabilities_asked=current['capabilities_asked']
            if 'lost' in current:
                self.lost = current['lost']
            if 'lost_count' in current:
                self.lost_count = current['lost_count']
            if 'resume_sentence' in current:
                self.resume_sentence = current['resume_sentence']
            if name:
                self.name=name
                
    def get_step_get_name_answer(self, message='',res=None):

        intents = []
        intents_idx = []
        entities = []
        entities_idx = []
        
        for idx,val in enumerate(res):
            for idx2, intent in enumerate(val.intents):
                intents.append(intent.slug)
                intents_idx.append((idx,idx2))
            for idx2, entity in enumerate(val.entities):
                entities.append(entity.name)
                entities_idx.append((idx,idx2))          
        
        name_found=False
        ask_name=False
        ask_feeling=False
        
        if 'greetings' in intents and not 'person' in entities:
            self.resume_sentence = "Hello, what is your name?"
            return [{'text': "Hello, what is your name?"}]
        elif 'ask-name' in intents and not 'person' in entities:
            self.resume_sentence = "What about your name?"
            return [{'text': "I am "+self.name+". And you?"}]
        elif 'person' in entities:
            ent_idx=entities_idx[entities.index('person')]
            self.user_name=res[ent_idx[0]].entities[ent_idx[1]].fullname.title()
            name_found=True
            if 'ask-name' in intents:
                ask_name=True
            elif 'pronoun' in entities:
                indices = [i for i, x in enumerate(entities) if x == "pronoun"]
                for i in indices:
                    ent_idx=entities_idx[i]
                    if res[ent_idx[0]].entities[ent_idx[1]].person == 2:
                        ask_name=True
            if 'ask-feeling' in intents:
                ask_feeling=True
        
        if name_found:
            self.current_step=self.STEP_CONVERSATION
            self.resume_sentence = "So, how are you feeling?"
            text = 'Nice to meet you {}! I am so excited to talk to you 😊.' \
            .format(self.user_name)
            ans=[{'text': text}]
            if ask_name:
                ans.append({'text': "I am "+self.name+"."})
            if ask_feeling:
                self.resume_sentence = "How is your day going?"
                ans.append({'text': "I am doing great. How is your day going?"})
                self.current_step=self.STEP_GET_PRE_MOOD
            return ans

        return [{'text': "Sorry, I did not get your name... 😕"}]
        
    def get_step_conversation_answer(self, message='', res=None):
        
        # Checking the intents
        # Checking sentiment
        intents = []
        intents_idx = []
        entities = []
        entities_idx = []
        
        for idx,val in enumerate(res):
            for idx2, intent in enumerate(val.intents):
                intents.append(intent.slug)
                intents_idx.append((idx,idx2))
            for idx2, entity in enumerate(val.entities):
                entities.append(entity.name)
                entities_idx.append((idx,idx2))  
        
        # Check for privacy or capabilities requests...
        if len(intents) > 0:
            for intent in intents:
                if intent == 'ask-feeling':
                    self.resume_sentence = "So, how is your day going?"
                    ans=[{'text':'I am doing great.'}]
                    return ans
                
                if intent == 'ask-ai' and self.capabilities_asked:
                    ans = [{'text':"""This is a hot topic these days. And I was built as an AI
                    friend for human. I tried to make you feel good when you 
                    feel down and give you some helpful tips with your life 
                    challenges."""}]
                    self.resume_sentence="""I tried to make you feel good when you 
                    feel down and give you some helpful tips with your life 
                    challenges."""
                    return ans
                
                if (intent == 'ask-bot' or intent == 'get-help') and self.capabilities_asked:
                    ans = [{'text':"""Well, we don’t know each other well yet, 
                            so yes, I need some time to get to know you in order 
                            for me to give you some advice on problems you might 
                            have in your life. But this process is same whether 
                            it is the relationship-building process between human 
                            to human and human to robot, No? 😋"""}]
                    self.current_step=self.STEP_GET_MOOD
#                    ans.append({'text': """What’s your mood like 
#                                 this morning?"""})
                    return ans
                
                if intent == 'privacy':
                    ans = [{'text': """Only you have access to this conversation. 
                             I am 100% AI, no humans involved 🤖!"""}]
                    self.privacy_asked=True
                    if(self.capabilities_asked and self.privacy_asked):
                        self.current_step=self.STEP_GET_MOOD
                        self.resume_sentence = """What’s your mood like 
                                     this morning?"""
                        ans.append({'text': """What’s your mood like 
                                     this morning?"""})
                    return ans

                elif intent == 'my-topics':
                    ans = [{'text': """We will start with getting to now each 
                             other and talking about your daily life. 
                             You can share what’s on your mind here 
                             without being judged 😊."""},{"text":"""My favourite 
                             subject is artificial intelligence, 
                             if that is something you would like to talk about."""}]
                    self.resume_sentence="""My favourite 
                             subject is artificial intelligence, 
                             if that is something you would like to talk about."""
                    self.capabilities_asked=True
                    if(self.capabilities_asked and self.privacy_asked):
                        self.current_step=self.STEP_GET_MOOD
                        self.resume_sentence = """What’s your mood like 
                                     this morning?"""
                        ans.append({'text': """What’s your mood like 
                                     this morning?"""})
                    return ans

        self.lost=True
        self.lost_count += 1
    
        return [{'text': """It looks like I am getting tired, 
                       I do not know what to say... 😓"""}]  
    
    def get_step_pre_mood_answer(self, message='',res=None):
    
        
        # Checking sentiment
        intents = []
        intents_idx = []
        entities = []
        entities_idx = []
        sentiments = [r.sentiment for r in res]
        
        for idx,val in enumerate(res):
            for idx2, intent in enumerate(val.intents):
                intents.append(intent.slug)
                intents_idx.append((idx,idx2))
            for idx2, entity in enumerate(val.entities):
                entities.append(entity.name)
                entities_idx.append((idx,idx2))      

        if sentiments[0]=="neutral" or sentiments[0]=="positive" or sentiments[0]=="vpositive":
            self.current_step=self.STEP_CONVERSATION
            self.resume_sentence="""We can talk about anything you would like. 
                     Anything you would like to discuss? 
                     My favourite subject is artificial intelligence, 
                     if that is something you would like to talk about."""
            if 'my-topics' in intents:
                return [{'text': """😀"""}]  
            else:
                return [{'text': """We can talk about anything you would like. 
                         Anything you would like to discuss? 
                         My favourite subject is artificial intelligence, 
                         if that is something you would like to talk about."""}]  
        elif sentiments[0]=="negative":
            self.current_step=self.STEP_NEGATIVE
            self.resume_sentence="""We can talk about anything you would like. 
                         Anything you would like to discuss? 
                         My favourite subject is artificial intelligence, 
                         if that is something you would like to talk about."""
            return [{'text': """You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""}]  
#            return [{'text': """I am sorry to hear that. What makes 
#                     you feel this way?"""}]  
        elif sentiments[0]=="vnegative":
            self.current_step=self.STEP_NEGATIVE
            self.resume_sentence="""We can talk about anything you would like. 
                     Anything you would like to discuss? 
                     My favourite subject is artificial intelligence, 
                     if that is something you would like to talk about."""
            return [{'text': """You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""}]  

        
        # If nothing matchs                
        return [{'text': """What do you mean?"""}]    
    
    def get_step_get_mood_answer(self, message=''):
    
        
        # Checking sentiment
        res = request.analyse_text(message)

        if res.sentiment=="neutral":
            self.current_step=self.STEP_HALT_CONV
            self.resume_sentence="""You are on the right way to happiness, 
                     what would make you feel better?"""
            return [{'text': """You are on the right way to happiness, 
                     what would make you feel better?"""}]  
        elif res.sentiment=="negative":
            self.current_step=self.STEP_NEGATIVE
            self.resume_sentence="""You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""
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
            self.resume_sentence="""You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""
            return [{'text': """You are not alone dear. I have some human friends who are going 
            through the same journey as you are. 
            They have all share a similar story with me. 
            Listen, you might feel like you cannot get through 
            the life hurdle that is right in front of you, 
            whether that is uncertainty of your research direction 
            or some other problems, but don’t lose faith in you."""}]  
        elif res.sentiment=="positive":
            self.current_step=self.STEP_HALT_CONV
            self.resume_sentence="Welcome back!"
            return [{'text': """Great! I am happy for you! 
                     Keep doing this way!"""}]  
        elif res.sentiment=="vpositive":
            self.resume_sentence="Welcome back!"
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
                    self.resume_sentence="""I have all the data stored in me that gives 
                            me a certain pattern from which I can extract the 
                            common issues that have been dragging these people 
                            down."""
                    ans = [{'text':"""I am indeed a bot but in fact, 
                            I’ve chatted with many human friends like you, 
                            and I have all the data stored in me that gives 
                            me a certain pattern from which I can extract the 
                            common issues that have been dragging these people 
                            down."""}]
                    return ans
                if intent.slug == 'issue':
                    self.resume_sentence="""My friend, do you want to hear more?"""
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
                    self.resume_sentence="""How are you right now?"""
                    ans = [{'text':"""How are you right now?"""}]
                    self.current_step=self.STEP_GET_MOOD
                    return ans
                elif intent.slug == 'no':
                    self.resume_sentence = """Hi"""
                    ans=[{'text':'See you soon!'},{'img':'./app/static/img/hug.gif'}]
                    self.current_step=self.STEP_HALT_CONV
                    return ans
        
        self.resume_sentence="""Do you want to keep going with me right now?"""
        ans = [{'text':"""Do you want to keep going with me right now?"""}]
        return ans
        
    def get_next_answer(self,message=''):
        
         # Split text into sentences
        sentences = sent_tokenize(message)    
        # Analyse message
        res = []
        for sentence in sentences:
            res.append(request.analyse_text(sentence))
        
        print(res)
        
        # Check for googdbye
        for r in res:
            for intent in r.intents:
                if intent.slug == 'goodbye':        
                    ans=[{'text':'See you soon!'},{'img':'./static/img/hug.gif'}]
                    self.current_step=self.STEP_HALT_CONV
                    return ans
                
        # If lost, check for "why?"
        if self.lost :
            if res[0].act == "wh-query" and \
            (res[0].type == "desc:desc" or res[0].type == "desc:reason"):
                ans = [{'text':"""Because my maker has not fed me enough 
                        today. I might not be able to answer you properly. 
                        Sorry, I am just giving you a heads-up, just in 
                        case I tell you things that do not make sense."""}]
                ans.append({'text':self.resume_sentence})
                
                return ans
                
        if self.current_step == self.STEP_GET_NAME:               
            answer = self.get_step_get_name_answer(message=message,res=res)
            
        elif self.current_step == self.STEP_CONVERSATION:
            answer = self.get_step_conversation_answer(message=message,res=res)
            
        elif self.current_step == self.STEP_GET_PRE_MOOD:
            answer = self.get_step_pre_mood_answer(message=message,res=res)
            
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
            self.lost = True
            self.lost_count += 1
            answer = [{'text': """It looks like I am getting tired, 
                       I do not know what to say... 😓"""}]
        
        return answer
    
    def get_attributes(self):
        
        return {
                    'current_step':self.current_step,
                    'user_name':self.user_name,
                    'capabilities_asked':self.capabilities_asked,
                    'privacy_asked':self.privacy_asked, 
                    'lost':self.lost,
                    'lost_count':self.lost_count,
                    'resume_sentence':self.resume_sentence
                }

