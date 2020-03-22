# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:11:46 2020

@author: Ambre
"""
from utils import *

import pickle

a = "hi"

f = open("classement.txt", "wb")
pickle.dump(a, f)
f.close()

b = pickle.load(open("classement.txt", "rb"))
print(b)