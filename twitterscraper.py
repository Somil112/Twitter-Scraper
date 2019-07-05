# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 18:26:55 2019

@author: Somil
"""

import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd


class TwitterScraper:
    def __init__(self,handle):
        """
        Initialize class by creating a Beautiful soup instance.
        """
        self.url = "https://www.twitter.com/{}".format(handle)
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text,"html.parser")
        
    def get_details(self):
        """
        Function to get the basic information of the profile.
        Includes:
            Profile Picture Link
            User Name
            No of Tweets
            Following
            Followers
            No of Likes
        Returns a List containing all the information.
        """
        profile_picture = self.soup.find_all("a",{"class":"ProfileAvatar-container"})[0]['href']
        
        user = self.soup.find_all("title")[0].string.split("(")[0].strip()
        
        tweets = self.soup.find_all("span",{"class":"ProfileNav-value"})[0].string.strip()
        
        following = self.soup.find_all("span",{"class":"ProfileNav-value"})[1].string.strip()
        
        followers = self.soup.find_all("span",{"class":"ProfileNav-value"})[2].string.strip()
        
        likes = self.soup.find_all("span",{"class":"ProfileNav-value"})[3].string.strip()
        
        return [profile_picture,user,tweets,following,followers,likes]
    
    def get_posts(self,num = 20):
        """
        Get up to 20 posts from the Twitter handle.
        A function for getting more than 20 posts will be written soon.
        Post information contains any embed links, post contents and the timestamp
        """
        num = min(20,num)
        plinks = []
        posts = []
        count = 1
        for post in self.soup.find_all("p",{"class":"TweetTextSize"}):
            if(count<=num):
                links = []
                for link in post.find_all("a"):
                    if(link['href'].startswith('http')):
                        links.append(link['href'])
                plinks.append(links)
                posts.append(post.find_all(text=True)[0])
                count += 1
            else:
                break
        timestamp = []   
        count = 1
        for times in self.soup.find_all("a",{"class":"tweet-timestamp"}):
            if(count <= num):
                timestamp.append(times['title'])
                count += 1
            else:
                break
        return pd.DataFrame({"Posts": posts,"Links":plinks,"Time Stamp":timestamp})
    
    def export_as_csv(self,df,name):
        """
        Export the dataframe to csv.
        """
        df.to_csv("{}.csv".format(name))