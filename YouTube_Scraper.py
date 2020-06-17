#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:46:43 2020

@author: Eric W

"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep
from random import randint
import time
import unidecode


#Building our functions
def Get_VideoLength(Vids_len):
    #finding the length of each video, in str
    len_of_vids = []
    for z in Vids_len:
        length = z.text
        len_of_vids.append(length)
    #finding and cleaning the views list; getting rid of special chars

    return len_of_vids


def Get_VideoNames(Vids):                                                          
    #Here we are locating the tile of each Video 
    rem_words = ['lyric)','lucky','lion','video','edition','by','yoto','films','d.s.','(',')','✅►eres','d.s.)✅','lyric','henyer','lara','ft','edit','-','shot','edit.','"','santo','placard','video','lyric','oficial','iacho','(video','oficial)']
    title_list = []
    for v in Vids:
        title = v.findChild('a')['title']
        #cleaning the name
        title_split = title.split()
        result_words = [word for word in title_split if word.lower() not in rem_words]
        result = ' '.join(result_words)
        result = result.replace('"','')
        result = unidecode.unidecode(result)
        title_list.append(result)
    return title_list

def Get_VideoViews(Views):
    #Finding the views of the videos
    views_list = []
    for x in Views: 
        views = x.findChild().text.split()[0]
        views = views.replace(',','') #removing a comma 
        views = int(views)
        views_list.append(views)
    return views_list
channel_data = []
chan_id = ['UC4YOFVk_s7iSqyTWyGK_cMg','UCQruJDvxfM3b4-qNVIuarSQ','UC-xSFGtsLN0kiZGoPYEhzMg','UCcJAeaMvWQp8Czpz31S7ptQ']

'''
Main Scraping function
'''

def Scrape(chan_id):
    #Scraping the channels and storing the data in a list of dictionaries 
    for channel in chan_id: 
        URL = f'https://www.youtube.com/channel/{channel}/videos'
        source = requests.get(URL)
        sleep(randint(2,10))
        soup = BeautifulSoup(source.text,"lxml")
        #looking into the div's 
        sleep(randint(2,10))
        div_s = soup.find_all("div")
        #getting the number of subscribers
        Subs = div_s[1].find("span",class_='yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip')['title']
        #finding all the videos 
        Vids = soup.find_all('h3', class_='yt-lockup-title')
        #getting the length of the videos 
        Vids_len = div_s[1].find_all('span',class_='video-time')
        #finding the views + Upload Time of the videos 
        Views = div_s[1].find_all('ul', {'class': 'yt-lockup-meta-info'})
        #Title of the Page: 
        pg_title = div_s[1].find_all('img',class_='channel-header-profile-image')[0]['title']
        #Cleaning the data and adding it to list
        sleep(randint(2,10))
        print('')
        print(f'Getting data for {pg_title}...')
        print('')
        data_dict = {
                'Channel':pg_title,
                'Subs':Subs,
                'Videos':Get_VideoNames(Vids),
                'Length':Get_VideoLength(Vids_len),
                'Views':Get_VideoViews(Views),
                }
        channel_data.append(data_dict)
        sleep(randint(2,10))
    return channel_data

Scrape(chan_id)


def SaveAsCSV(channel_data):
    #converting to DataFrame then to CSV
    #saving each dataframe in the /Data Folder and adding the timestamp to it 
    
    #converting our list of dictionaries into separate DF's
    df_Lucky = pd.DataFrame({ key:pd.Series(value) for key, value in channel_data[0].items() })
    df_SP = pd.DataFrame({ key:pd.Series(value) for key, value in channel_data[1].items() })
    df_Iacho = pd.DataFrame({ key:pd.Series(value) for key, value in channel_data[2].items() })
    df_ULF = pd.DataFrame({ key:pd.Series(value) for key, value in channel_data[3].items() })
     
    #timestamp! Today's date
    date_time = time.strftime("%d%m%Y")
    
    path = r'YOUR PATH HERE'
    
    df_Lucky.to_csv(path+'Lucky_'+date_time+'.csv')
    df_SP.to_csv(path+'Santo_Placard_'+date_time+'.csv')
    df_Iacho.to_csv(path+'Iacho_'+date_time+'.csv')
    df_ULF.to_csv(path+'ULF_'+date_time+'.csv')
    

SaveAsCSV(channel_data)







