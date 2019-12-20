#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:58:12 2019

@author: harshitruwali
"""

import speech_recognition as sr
import os
import sys
import re
import webbrowser
import vlc
import youtube_dl
import wikipedia
import smtplib
from time import strftime
#import random
import requests
import json as simplejson
from bs4 import BeautifulSoup as soup
import urllib
#import urllib2
import urllib.request as urllib2
from urllib.request import urlopen
from pyowm import OWM
import subprocess
import email
import imaplib
import pandas as pd
from googlesearch import *
import pyttsx3
import wolframalpha
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer



'''
engine = pyttsx3.init()
sound = engine.getProperty('voices')
engine.setProperty('voice', sound[32].id)
engine.say("hello I am the first test case")
engine.runAndWait()
'''

def botResponse(audio):
    "speaks audio passed as argument"
    print(audio)
    engine = pyttsx3.init()
    sound = engine.getProperty('voices')
    engine.setProperty('voice', sound[33].id) #10 17 18 28 32 33 36 37 40
    #engine.say("hello I am the first test case")
   
    for line in str(audio).splitlines():
        #os.system("say " + audio)
        engine.say(audio)
    engine.runAndWait()
        
        
def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("How can I help you now?")
        #r.pause_treshold = 1
        #r.adjust_for_ambient_noise(source, duration = 1) # duration was earlier 1
        #audio = r.listen(source)
        audio = r.listen(source, phrase_time_limit = 5)  
    try:
        command = r.recognize_google(audio).lower()
        print("you said: "+ command + "\n")
        
    except sr.UnknownValueError:
        botResponse("Sorry, Cant understand, Please say again")
        command = myCommand()
    return command
    '''
    q = sr.Recognizer()
    t = 0
    with sr.Microphone() as source:
        print("How can I help you now?")
        while t==0:
            audio = q.listen(source)
            try:
                command = q.recognize_google(audio)
                print('you said :{}'.format(text))
                #print("you said: "+command+"\n")
                t=1
            except:
               botResponse("Sorry, Cant understand, Please say again")
               t==0
               command = myCommand();
    return command
    '''

def assistant(command):
    "if statements for executing commands"
    
    if 'hello' in command:
            day_time = int(strftime('%H'))
            if day_time < 12:
                botResponse('Hello, Good morning, Sir')
            elif 12 <= day_time < 18:
                botResponse('Hello, Good afternoon, Sir')
            else:
                botResponse('Hello, Good evening, Sir')

    #asking when you were created?         
    elif 'created' in command:
        botResponse('I was created on 15 December 2019 in the room of VIT  Bhopal University')

    #opening a webpage
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url  = 'https://www.'+domain+'.com'
            webbrowser.open(url)
            botResponse("Opening " + domain)
        else:
            pass

    #how are you and basic conversations
    elif 'how are you' in command:
        botResponse('I am great. Hoping the same for you.')   

    elif 'How do you function' in command:
        botResponse('I am working by the program written by Harshit Ruwali')

        
    #telling you the current time 
    elif 'time' in command:
        import datetime
        now = datetime.datetime.now()
        botResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))
         
    
    #reading an email
    elif 'read email' in command:
        def read_email_from_gmail():
            try:
                mail = imaplib.IMAP4_SSL(SMTP_SERVER)
                mail.login(FROM_EMAIL,FROM_PWD)
                mail.select('inbox')
        
                type, data = mail.search(None, 'ALL')
                mail_ids = data[0]
        
                id_list = mail_ids.split()   
                first_email_id = int(id_list[0])
                latest_email_id = int(id_list[-1])
        
        
                for i in range(latest_email_id,first_email_id, -1):
                    typ, data = mail.fetch(ruwaliharshit@gmail.com, '(RFC822)' )
        
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_string(response_part[1])
                            email_subject = msg['subject']
                            email_from = msg['from']
                            print ('From : ' + email_from + '\n')
                            print ('Subject : ' + email_subject + '\n')
                        else:
                            pass
            except:
                pass

    # to send an email to your contacts having emailId
    elif 'send email' in command:
        botResponse('Whom to send')
        recipient = myCommand()
        #importing the contacts with emailId
        data = pd.read_csv('/Users/harshitruwali/Desktop/Contacts_email.csv')
        for recipient in data:
            if True:
                botResponse("What to mail the recipient?")
                content = myCommand()
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('your_email_address', 'your_password')
                mail.sendmail('sender_email', 'receiver_email', content)
                mail.close()
                botResponse('Email has been sent successfuly.')
                
            else:
                botResponse("The recipient is not in your contacts")

    #opening the desired application in the Mac
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname+".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            botResponse('I have launched the desired application')
        else:
            botResponse('The applicaton does not exixst')
        
    # to tell you the temprature of a perticular city
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            '''
            city = reg_ex.group(1)
            owm = OWM(API_key='221642e84fc28ddb1c3172447bbf1a39')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            k = w.get_status()
            x = w.get_temperature(unit='celsius')
            botResponse('Current weather in %s is %s. The maximum temperature is %0.2f and the minimum temperature is %0.2f degree celcius' % (city, k, x['temp_max'], x['temp_min']))

            city=reg_ex.group(1)
            url="https://api.openweathermap.org/data/2.5/forecast?q=Delhi&appid=221642e84fc28ddb1c3172447bbf1a39&units=metric"
            res=requests.get(url)
            output=res.json()
            '''
            city = reg_ex.group(1)
            
            url ='http://api.openweathermap.org/data/2.5/forecast/daily?q=%s&cnt=3'%city
            response = requests.get(url)
            response.raise_for_status()

            weather_status=output['weather'][0]['description']
            temprature=output['main']['temp']
            output = response.json()
            #humidity=output['main']['humidity']
            #wind_speed=output['wind']['speed']
            botResponse('Current weather stauts is' + weather_status)
            botResponse('Current temparture is ' + str(temprature))

    #tells you the information availabe in net
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                botResponse(ny.content[:500].encode('utf-8'))
        except Exception as e:
                print(e)
                botResponse(e)
        
    #download and play a video from Youtube
    elif 'play the video' in command:
        path = '/Users/harshitruwali/Movies'
        folder = path
        for the_file in os.listdir(folder):
            os.path.join(folder, the_file)
            try:
                if os.path.isfile(the_file):
                    os.unlink(the_file)
            except Exception as e:
                print(e)
                
            botResponse('What to play, Sir?')
            #myvideo = myCommand()
            q=sr.Recognizer()
            t=0

            with sr.Microphone() as source:
                print('Search for the term:')
                
                while t==0:
                    audio =q.listen(source)
                    try:
                        text = q.recognize_google(audio)
                        print('you said :{}'.format(text))
                        t=1

                    except:
                        print('Not understandable')
                        print('Try again')
                        t==0
            myvideo = text

            if myvideo:
                flag = 0
                url = "https://www.youtube.com/results?search_query=" + myvideo.replace(' ', '+') 
                response = urllib2.urlopen(url)
                html = response.read()
                soup1 = soup(html, "lxml")
                url_list = []
                for vid in soup1.findAll(attrs={'class':'yt-uix-tile-link'}):
                    if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                        flag = 1
                        final_url = 'https://www.youtube.com' + vid['href']
                        url_list.append(final_url)
                        url = url_list[0]
                ydl_opts = {}
                os.chdir(path)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    subprocess.Popen(path)
                if flag == 0:
                    botResponse('I have not found anything in Youtube ')
                else:
                    pass
    #tell you a joke
    elif 'joke' in command:
        res = requests.get(
               'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"})
        if res.status_code == requests.codes.ok:
            botResponse(str(res.json()['joke']))
        else:       
            botResponse('Oops! I ran out of jokes')

    #read the news
    elif 'news for today' in command:
            try:
                news_url="https://news.google.com/news/rss"
                Client=urlopen(news_url)
                xml_page=Client.read()
                Client.close()
                soup_page=soup(xml_page,"xml")
                news_list=soup_page.findAll("item")
                for news in news_list[:15]:
                    botResponse(news.title.text.encode('utf-8'))
            except Exception as e:
                    print(e)

    elif "calculate" in command:    
            # write your wolframalpha app_id here 
            app_id = "9Q8RQA-XK2UTE7ALR" 
            client = wolframalpha.Client(app_id) 
  
            indx = input.lower().split().index('calculate') 
            query = input.split()[indx + 1:] 
            res = client.query(' '.join(query)) 
            answer = next(res.results).text 
            botResponse('The answer is ' + answer) 

    #does a google search
    elif 'search' in command:
        botResponse('What to search?')
        #myCommand()

        w=sr.Recognizer()
        t=0

        with sr.Microphone() as source:
            print('Search for the term:')
            
            while t==0:
                audio = w.listen(source)
                try:
                    text =w.recognize_google(audio)
                    print('you said :{}'.format(text))
                    t=1

                except:
                    print('Not understandable')
                    print('Try again')
                    t==0

        #query = myCommand()
        query = text
        safari_path = r'/Applications/Safari.app %s'
        for url in search(query, tld="co.in", num=1, stop = 1, pause = 2):
            webbrowser.open("https://google.com/search?q=%s" % query)

            
    #to terminate the program
    elif 'bye' in command:
        botResponse('Bye bye Sir. Have a nice day')
        sys.exit()

    else:
        response = chatbot.get_response(command)
        botResponse(response)

        
       
'''         
day_time = int(strftime('%H'))
if day_time < 12:
     botResponse('Hello Good morning, Sir')
elif 12 <= day_time < 18:
    botResponse('Hello Good afternoon, Sir')
else:
    botResponse('Hello Good evening, Sir')
'''
chatbot = ChatBot('Lindy')

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
trainer.export_for_training('./ai.yml')
trainer.export_for_training('./botprofile.yml')
trainer.export_for_training('./computers.yml')
trainer.export_for_training('./conversations.yml')
trainer.export_for_training('./emotion.yml')
trainer.export_for_training('./food.yml')
trainer.export_for_training('./gossip.yml')
trainer.export_for_training('./greetings.yml')
trainer.export_for_training('./health.yml')
trainer.export_for_training('./history.yml')
trainer.export_for_training('./humor.yml')
trainer.export_for_training('./literature.yml')
trainer.export_for_training('./money.yml')
trainer.export_for_training('./movies.yml')
trainer.export_for_training('./politics.yml')
trainer.export_for_training('./psychology.yml')
trainer.export_for_training('./science.yml')
trainer.export_for_training('./sports.yml')
trainer.export_for_training('./trivia.yml')

print('Finished training')


botResponse('Hello, I am the Voice assistant created by Harshit Ruwali. How can I help you?')

while True:
    assistant(myCommand())
