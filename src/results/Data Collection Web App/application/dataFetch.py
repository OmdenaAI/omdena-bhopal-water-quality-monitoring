import ee 
import asyncio
import geemap 
import datetime 
from datetime import date
import numpy as np
import pandas as pd




    
def Temperature(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)
    landsat = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").\
        filterDate(start_date,end_date)
    landsat_AOI = landsat.filterBounds(geometry)
        
    def addtemp(image):
        temp = image.select('ST_B.*').multiply(0.00341802).add(149.0).subtract(273.15).rename('temperature')
        return image.addBands(temp)
    with_temp = landsat_AOI.map(addtemp)
    def meantemp(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['temperature']),
                                  geometry = landsat_AOI,
                                  scale = image.projection().nominalScale().getInfo(),
                                  maxPixels = 100000,
                                  bestEffort = True);
        return mean.get('temperature').getInfo()
    Images_temp = with_temp.select('temperature').toList(with_temp.size())
    temp_coll = []
    for i in range(Images_temp.length().getInfo()):
        image = ee.Image(Images_temp.get(i-1))
        tempe_temp = meantemp(image)
        temp_coll.append(tempe_temp)
    dates = np.array(with_temp.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df5 = pd.DataFrame(temp_coll, index = day, columns = ['Temperature'])
    df5.index = pd.to_datetime(df5.index, format="%Y/%m/%d")
    df5.sort_index(ascending = True, inplace = True)
    return df5
    
def NDCI(geometry, dc1, dc2):
    
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)
   
    sentinel = ee.ImageCollection("COPERNICUS/S2_SR").\
               filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).\
               filterDate(start_date , end_date)
    
    sentinel_AOI = sentinel.filterBounds(geometry)
    def addNDCI(image):
        ndci = image.normalizedDifference(['B5', 'B4']).rename('NDCI')
        return image.addBands(ndci)

    with_ndci = sentinel_AOI.map(addNDCI)
    def meanNDCI(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['NDCI']),
                                geometry = geometry,
                                scale = image.projection().nominalScale().getInfo(),
                                maxPixels = 100000,
                                bestEffort = True);
        return mean.get('NDCI').getInfo()
    print('starting the loop')
    Images_ndci = with_ndci.select('NDCI').toList(with_ndci.size())
    ndci_coll = []
    for i in range(Images_ndci.length().getInfo()):
        image = ee.Image(Images_ndci.get(i-1))
        temp_ndci = meanNDCI(image)
        ndci_coll.append(temp_ndci)
    print("images fetched")
    dates = np.array(with_ndci.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df = pd.DataFrame(ndci_coll, index = day, columns = ['Chlorophyll'])
    df.index = pd.to_datetime(df.index, format="%Y/%m/%d")
    df.sort_index(ascending = True, inplace = True)
    print(df)
    
    return df

def NDTI(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)
    sentinel = ee.ImageCollection("COPERNICUS/S2_SR").\
                    filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).\
                    filterDate(start_date,end_date)

    sentinel_AOI = sentinel.filterBounds(geometry)
    def addNDTI(image):
        ndti = image.normalizedDifference(['B4', 'B3']).rename('NDTI')
        return image.addBands(ndti)
    with_ndti = sentinel_AOI.map(addNDTI)
    
    def meanNDTI(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['NDTI']),
                                  geometry = geometry,
                                scale = image.projection().nominalScale().getInfo(),
                                maxPixels = 100000,
                                bestEffort = True);
        return mean.get('NDTI').getInfo()
    print('starting loop ...')
    Images_ndti = with_ndti.select('NDTI').toList(with_ndti.size())
    ndti_coll = []
    for i in range(Images_ndti.length().getInfo()):
        image = ee.Image(Images_ndti.get(i-1))
        temp_ndti = meanNDTI(image)
        ndti_coll.append(temp_ndti)
    dates = np.array(with_ndti.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df1 = pd.DataFrame(ndti_coll, index = day, columns = ['Turbidity'])
    df1.index = pd.to_datetime(df1.index, format="%Y/%m/%d")
    df1.sort_index(ascending = True, inplace = True)
    print(df1)
    return df1

def NDSI(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)

    sentinel = ee.ImageCollection("COPERNICUS/S2_SR").\
                    filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).\
                    filterDate(start_date,end_date)

    sentinel_AOI = sentinel.filterBounds(geometry)
    def addNDSI(image):
        ndsi = image.normalizedDifference(['B11', 'B12']).rename('NDSI')
        return image.addBands(ndsi)
    with_ndsi = sentinel_AOI.map(addNDSI)   
    def meanNDSI(image):
        mage = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['NDSI']),
                                  geometry = geometry,
                                  scale = image.projection().nominalScale().getInfo(),
                                  maxPixels = 100000,
                                  bestEffort = True);
        return mean.get('NDSI').getInfo() 
    Images_ndsi = with_ndsi.select('NDSI').toList(with_ndsi.size())
    ndsi_coll = []
    for i in range(Images_ndsi.length().getInfo()):
        image = ee.Image(Images_ndsi.get(i-1))
        temp_ndsi = meanNDSI(image)
        ndsi_coll.append(temp_ndsi)
    dates = np.array(with_ndsi.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df2 = pd.DataFrame(ndsi_coll, index = day, columns = ['Salinty'])
    df2.index = pd.to_datetime(df2.index, format="%Y/%m/%d")
    df2.sort_index(ascending = True, inplace = True)
    print(df2)
    return df2
    
def DO(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)

    sentinel = ee.ImageCollection("COPERNICUS/S2_SR").\
                    filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).\
                    filterDate(start_date,end_date)

    sentinel_AOI = sentinel.filterBounds(geometry)
    def addDO(image):
        do = ee.Image(-0.0167).multiply(image.select('B8')).add(ee.Image(0.0067).multiply(image.select('B9'))).add(ee.Image(0.0083).multiply(image.select('B11'))).add(ee.Image(9.577)).rename('DO')
        return image.addBands(do)
    with_do = sentinel_AOI.map(addDO)
    def meanDO(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['DO']),
                                  geometry = geometry,
                                  scale = image.projection().nominalScale().getInfo(),
                                  maxPixels = 100000,
                                  bestEffort = True);
        return mean.get('DO').getInfo()
    Images_do = with_do.select('DO').toList(with_do.size()) 
    do_coll = []
    for i in range(Images_do.length().getInfo()):
        image = ee.Image(Images_do.get(i-1))
        temp_do = meanDO(image)
        do_coll.append(temp_do)
    dates = np.array(with_do.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df4 = pd.DataFrame(do_coll, index = day, columns = ['Dissolved Oxygen'])
    df4.index = pd.to_datetime(df4.index, format="%Y/%m/%d")
    df4.sort_index(ascending = True, inplace = True)
    print(df4)
    return df4

def pH(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)


    sentinel = ee.ImageCollection("COPERNICUS/S2_SR").\
                    filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)).\
                    filterDate(start_date,end_date)

    sentinel_AOI = sentinel.filterBounds(geometry)
    def addpH(image):
        ph = ee.Image(8.339).subtract(ee.Image(0.827).multiply(image.select('B1').divide(image.select('B8')))).rename('PH')
        return image.addBands(ph)
    with_pH = sentinel_AOI.map(addpH)
    
    def meanpH(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['PH']),
                                  geometry = geometry,
                                  scale = image.projection().nominalScale().getInfo(),
                                  maxPixels = 100000,
                                  bestEffort = True);
        return mean.get('PH').getInfo()
    Images_ph = with_pH.select('PH').toList(with_pH.size())
    ph_coll= []
    for i in range(Images_ph.length().getInfo()):
        image = ee.Image(Images_ph.get(i-1))
        temp_ph = meanpH(image)
        ph_coll.append(temp_ph)
    dates = np.array(with_pH.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df6 = pd.DataFrame(ph_coll, index = day, columns = ['pH'])
    df6.index = pd.to_datetime(df6.index, format="%Y/%m/%d")
    df6.sort_index(ascending = True, inplace = True)
    print(df6)
    return df6

def DissolvedOrganicMatter(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)

    sentinel3 = ee.ImageCollection("COPERNICUS/S3/OLCI").\
              filterDate(start_date, end_date)

    sentinel3_AOI = sentinel3.filterBounds(geometry)
    
    def addDM(image):
        rgb = image.select(['Oa08_radiance', 'Oa06_radiance', 'Oa04_radiance'])\
            .multiply(ee.Image([0.00876539, 0.0123538, 0.0115198]))
        dm = rgb.select('Oa08_radiance').divide(rgb.select('Oa04_radiance')).rename('dom')
        return image.addBands(dm)
    with_dm = sentinel3_AOI.map(addDM)
    def meanDM(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['dom']),
                                  geometry = geometry,
                                  scale = image.projection().nominalScale().getInfo(),
                                  maxPixels = 100000,
                                  bestEffort = True);
        return mean.get('dom').getInfo()
    Images_dm = with_dm.select('dom').toList(with_dm.size())
    dm_coll= []
    for i in range(Images_dm.length().getInfo()):
        image = ee.Image(Images_dm.get(i-1))
        temp_dm = meanDM(image)
        dm_coll.append(temp_dm)
        
    dates = np.array(with_dm.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    
    df6 = pd.DataFrame(dm_coll, index = day, columns = ['Dissolved Organic Matter'])
    df6.index = pd.to_datetime(df6.index, format="%Y/%m/%d")
    df6.sort_index(ascending = True, inplace = True)
    du = df6.dropna()
    return du
    
def SuspendedMatter(geometry, dc1, dc2):
    date_components = dc1.split('-')
    year, month, day = [int(item) for item in date_components]

    d = date(year, month, day)
    start_date = str(d)
    
   
    date_components = dc2.split('-')
    year, month, day = [int(item) for item in date_components]

    e = date(year, month, day)
    end_date = str(e)

    sentinel3 = ee.ImageCollection("COPERNICUS/S3/OLCI").\
              filterDate(start_date, end_date)

    sentinel3_AOI = sentinel3.filterBounds(geometry)
    def addSM(image):
        rgb = image.select(['Oa08_radiance', 'Oa06_radiance', 'Oa04_radiance'])\
            .multiply(ee.Image([0.00876539, 0.0123538, 0.0115198]))
        suspended_matter = rgb.select('Oa08_radiance').divide(rgb.select('Oa06_radiance')).rename('suspended_matter')
        return image.addBands(suspended_matter)
    with_sm = sentinel3_AOI.map(addSM)
    def meanSM(image):
        image = ee.Image(image)
        mean = image.reduceRegion(reducer = ee.Reducer.mean().setOutputs(['suspended_matter']),
                                  geometry = geometry,
                                  scale = image.projection().nominalScale().getInfo(),
                                  maxPixels = 100000,
                                  bestEffort = True);
        return mean.get('suspended_matter').getInfo()
    Images_sm = with_sm.select('suspended_matter').toList(with_sm.size())
    sm_coll= []
    for i in range(Images_sm.length().getInfo()):
        image = ee.Image(Images_sm.get(i-1))
        temp_sm = meanSM(image)
        sm_coll.append(temp_sm)
    dates = np.array(with_sm.aggregate_array("system:time_start").getInfo())
    day = [datetime.datetime.fromtimestamp(i/1000).strftime('%Y-%m-%d') for i in (dates)]
    df6 = pd.DataFrame(sm_coll, index = day, columns = ['Suspended Matter'])
    df6.index = pd.to_datetime(df6.index, format="%Y/%m/%d")
    df6.sort_index(ascending = True, inplace = True)
    sr = df6.dropna()
    return sr