# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 22:34:34 2019

@author: Herru
"""
#%%
import os
import sqlite3
dir_path = os.path.dirname(os.path.realpath(__file__))
#filename = os.path.join(fileDir, 'Folder1.1/same.txt')
print(dir_path)
#%%
conn = sqlite3.connect(r'c:\Users\herru\Desktop\newsweb\db.sqlite3')