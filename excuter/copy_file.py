#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import shutil 
import os
import time

shutil.rmtree('F:\\Desktop\\download_csv_copy')  
time.sleep(3)
shutil.copytree('F:\\Desktop\\download_csv', 'F:\\Desktop\\download_csv_copy', symlinks=False, ignore=None)
time.sleep(3)
shutil.rmtree('F:\\Desktop\\download_csv')  
time.sleep(3)
os.mkdir('F:\\Desktop\\download_csv')     


# In[ ]:
import sys
sys.exit()


