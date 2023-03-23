import os
import ee
import geemap
import ipywidgets as widgets
import pandas as pd
import numpy as np
from datetime import datetime, timedelta 
from parameters import Temprature, NDCI, NDSI, NDTI, DissolvedOrganicMatter, SuspendedMatter, DO, pH
from polygon import geometry
     

service_account = 'akshitsrivastava@omdena-380215.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'omdena-380215-345e4f158b8c.json')
ee.Initialize(credentials)


coords = geometry()

geometry = ee.Geometry.Polygon(coords)
#geometry = ee.Geometry.Polygon([[77.39546956268856,23.265850898429633],[77.39576192347118,23.263643049175467],[77.39595504252026,23.263781040825478],[77.39609988180706,23.263738453582683],[77.39656926838467,23.26489905664098],[77.39658804384777,23.265207070617443],[77.39640297142574,23.265850201505117],[77.39614011494228,23.266249384632868],[77.3959443136842,23.26634548409614],[77.39546956268856,23.265850898429633]])


#While defining the date time for Suspended Matter & Dissolved Organic Matter , It must be taken care of to take small interval of time due to lot of missing data in satellite which increases the time taken to fetch the results 
choice = "Y"
while choice != 'N':
    ans = int(input('To Fetch the data for following parameters Enter \n [1] NDCI \n [2] NDTI \n [3] NDSI \n [4] DO \n [5] pH \n [6] Temprature \n [7] Dissolved Organic Matter \n [8] Suspended Matter: '))
    if ans == 1:
        NDCI(geometry)
    elif ans == 2:
        NDTI(geometry)
    elif ans == 3:
        NDSI(geometry)
    elif ans == 4:
        DO(geometry)
    elif ans == 5:
        pH(geometry)
    elif ans == 6:
        Temprature(geometry)
    elif ans == 7: 
        DissolvedOrganicMatter(geometry)
    elif ans == 8: 
        SuspendedMatter(geometry)
    else:
        print('Invalid response')
    choice = input("do you want to collect more data? ( Y/N) :").upper()
    
    

