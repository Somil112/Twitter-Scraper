# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 16:08:01 2019

@author: Somil
"""

from twitterscraper import TwitterScraper
                
    
ts = TwitterScraper('iamsrk')

details = ts.get_details()  

posts = ts.get_posts(15)


