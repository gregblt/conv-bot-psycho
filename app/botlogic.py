#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 10:02:20 2018

@author: gregory
"""

from recastai import Request, Connect

request = Request('fe8f59c463abfca58a5bddf1ccacb0b7')
res = request.analyse_text('abdul')

WIT_ACCESS_TOKEN="PSSUTXYCMNTIA6KWKIXT36PUXUFN2SJA"

class BotLogic:
        
    STEP_INIT=0
    STEP_GET_NAME=1
    STEP_CONVERSATION=2
    
    current_step=STEP_INIT
    user_name=None
    
    def __init__(self, current=None):
        
        if(current!=None):
            if 'current_step' in current:
                self.current_step=current['current_step']
            if 'user_name' in current:
                self.user_name=current['user_name']
            
        self.client = Wit(WIT_ACCESS_TOKEN)
        
    def get_next_answer(self,message=''):
        
        if self.current_step == self.STEP_GET_NAME:               
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
                answer = [{'text': text}]
            else:
                answer = [{'text': "Sorry, I did not get your name... 😕"}]
        
        return answer

