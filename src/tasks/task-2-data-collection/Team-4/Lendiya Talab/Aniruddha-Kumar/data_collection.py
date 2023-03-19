import ipywidgets as widgets
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import geemap
import ee

#ee.Authenticate()
#ee.Initialize()

def get_data(long, lat, start_date, end_date):

  Map = geemap.Map()

  # geometry1 = ee.Geometry.Point([long,lat])

  #start_date = '2021-01-01'
  #end_date = '2021-06-30'

  # Kankaria Lake, Ahmedabad

  # geometry1 = ee.Geometry.Point([72.6026,23.0063])
  geometry = ee.Geometry.Point([long,lat])
  image = ee.ImageCollection("COPERNICUS/S2_SR") \
              .filterBounds(geometry) \
              .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',20)) \
              .first()
  # Create an NDWI image, define visualization parameters and display.
  ndwi = image.normalizedDifference(['B3', 'B8'])
  # Mask the non-watery parts of the image, where NDWI < 0.4.
  ndwiMasked = ndwi.updateMask(ndwi.gte(0.4))
  ndwiMasked1= ndwiMasked.toInt()
  # vectors = ndwiMasked1.reduceToVectors({
  #   'scale': 30.0,
  #   'geometryType': 'polygon',
  #   'eightConnected': False,
  #   'maxPixels':10000000
  # })
  vectors = ndwiMasked1.reduceToVectors(scale = 30.0, geometryType = 'polygon', eightConnected = False, maxPixels = 10000000, bestEffort=True)
  # geometry = ee.Geometry.Polygon([
  #   [72.5986408493042,23.006549566021803],
  #  [72.59902708740235,23.004890477468116],
  #  [72.60070078582764,23.003863412427236],
  #  [72.60040037841797,23.007142092704626],
  #  [72.60215990753174,23.006668071566512],
  #  [72.60173075408936,23.003784407100333],
  #   [72.60366194458008,23.00516699364359],
  #  [72.60374777526856,23.00686558057643],
  #   [72.6026748916626,23.00805062856477],
  #   [72.60082953186036,23.00880115357416],
  #   [72.59945624084473,23.00809012998513],
  #   [72.5986408493042,23.006549566021803],
  #     [72.5986408493042,23.006549566021803],
  #   [72.59902708740235,23.004890477468116],
  #   [72.60070078582764,23.003863412427236],
  #   [72.60040037841797,23.007142092704626],
  #   [72.60215990753174,23.006668071566512],
  #   [72.60173075408936,23.003784407100333],
  #     [72.60366194458008,23.00516699364359],
  #   [72.60374777526856,23.00686558057643],
  #     [72.6026748916626,23.00805062856477],
  #     [72.60082953186036,23.00880115357416],
  #     [72.59945624084473,23.00809012998513],
  #     [72.5986408493042,23.006549566021803]
  # ])

  Map.addLayer(geometry)
  sentinel = ee.ImageCollection("COPERNICUS/S2_SR").filterBounds(vectors) \
                .filterDate(start_date,end_date) \
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20)) \
                .median()

  visualization = {
  'min': 0,
  'max': 3000,
  'bands': ['B4', 'B3', 'B2'],
  }
  Map.addLayer(sentinel, visualization, 'sent2rgb')

  mndwi = sentinel.normalizedDifference(['B3','B11']).rename('mndwi')
  mndwitr = mndwi.gt(0)
  ndsi = sentinel.normalizedDifference(['B11','B12']).rename('ndsi')
  ndsi2 = sentinel.normalizedDifference(['B11','B12']).rename('ndsi2').mask(mndwitr)
  Map.addLayer(ndsi2,{'min':0.1,'max':0.4,'palette':['cyan','orange','red']},'salinity')
  ndti = sentinel.normalizedDifference(['B4','B3']).rename('ndti')
  ndti2 = sentinel.normalizedDifference(['B4','B3']).rename('ndti2').mask(mndwitr)
  Map.addLayer(ndti2,{'min':-1,'max':+1,'palette':['blue','pink','brown']},'turbidity')

  ndci = sentinel.normalizedDifference(['B5','B4']).rename('ndci')
  ndci2 = sentinel.normalizedDifference(['B5','B4']).rename('ndci2').mask(mndwitr)
  Map.addLayer(ndci2,{'min':-1,'max':+1,'palette':['green','pink','brown']},'chlorophyll')


  ph  = ee.Image(8.339).subtract(ee.Image(0.827).multiply(sentinel.select('B1').divide(sentinel.select('B8')))).rename('ph')
  ph2  = ee.Image(8.339).subtract(ee.Image(0.827).multiply(sentinel.select('B1').divide(sentinel.select('B8')))).rename('ph2').mask(mndwitr)
  Map.addLayer(ph2,{'min':0,'max':14,'palette':['red','yellow','cyan']},'ph')

  dissolvedoxygen  = ee.Image(-0.0167).multiply(sentinel.select('B8')).add(ee.Image(0.0067).multiply(sentinel.select('B9'))).add(ee.Image(0.0083).multiply(sentinel.select('B11'))).add(ee.Image(9.577)).rename('dissolvedoxygen')
  dissolvedoxygen2  = ee.Image(-0.0167).multiply(sentinel.select('B8')).add(ee.Image(0.0067).multiply(sentinel.select('B9'))).add(ee.Image(0.0083).multiply(sentinel.select('B11'))).add(ee.Image(9.577)).rename('dissolvedoxygen2').mask(mndwitr)
  Map.addLayer(dissolvedoxygen2,{'min':6.5,'max':8,'palette':['red','green','blue']},'do')



  col = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
  .filterDate(start_date,end_date) \
  .filterBounds(vectors).median()

  temp  = col.select('ST_B.*').multiply(0.00341802).add(149.0).subtract(273.15).rename('temp')


  ## Test Data


  starting = start_date
  ending = end_date

  data = ee.ImageCollection('COPERNICUS/S3/OLCI').filterDate(starting, ending).filterBounds(vectors)

  rgb = data.select(['Oa08_radiance', 'Oa06_radiance', 'Oa04_radiance'])\
                .median().multiply(ee.Image([0.00876539, 0.0123538, 0.0115198])).clip(vectors)
  dm_2021_Jan_August_test = rgb.select('Oa08_radiance').divide(rgb.select('Oa04_radiance')).rename('dom')
  dom2 = rgb.select('Oa08_radiance').divide(rgb.select('Oa04_radiance')).mask(mndwitr)
  Map.addLayer(dom2,{'min':0,'max':0.8,'palette':['green','red','yellow']},'Dissolved organic matter')
  suspended_matter_2021_Jan_August_test= rgb.select('Oa08_radiance').divide(rgb.select('Oa06_radiance')).rename('suspended_matter')
  suspended_matter2 = rgb.select('Oa08_radiance').divide(rgb.select('Oa06_radiance')).mask(mndwitr)
  Map.addLayer(suspended_matter2,{'min':0,'max':0.8,'palette':['green','red','yellow']},'suspended_matter')

  Map.to_streamlit(width = 100, height=900)




  latlon = ee.Image.pixelLonLat().addBands(dm_2021_Jan_August_test)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100,
    tileScale = 16)
  # get data into three different arrays

  data_dom_2021_Jan_August_test = np.array((ee.Array(latlon.get("dom")).getInfo()))

  latlon = ee.Image.pixelLonLat().addBands(suspended_matter_2021_Jan_August_test)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100,
    tileScale = 16)
  # get data into three different arrays
  data_sm_2021_Jan_August_test= np.array((ee.Array(latlon.get("suspended_matter")).getInfo()))

  latlon = ee.Image.pixelLonLat().addBands(temp)


  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100)

  data_lst = np.array((ee.Array(latlon.get("temp")).getInfo()))


  latlon = ee.Image.pixelLonLat().addBands(ndti)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100)
  # get data into three different arrays
  data_ndti = np.array((ee.Array(latlon.get("ndti")).getInfo()))

  latlon = ee.Image.pixelLonLat().addBands(ndsi)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100)
  # get data into three different arrays
  data_ndsi = np.array((ee.Array(latlon.get("ndsi")).getInfo()))

  latlon = ee.Image.pixelLonLat().addBands(ndci)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100)
  # get data into three different arrays
  data_ndci = np.array((ee.Array(latlon.get("ndci")).getInfo()))

  latlon = ee.Image.pixelLonLat().addBands(dissolvedoxygen)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100,
    tileScale = 16)
  # get data into three different arrays
  data_do = np.array((ee.Array(latlon.get("dissolvedoxygen")).getInfo()))

  latlon = ee.Image.pixelLonLat().addBands(ph)
  # apply reducer to list
  latlon = latlon.reduceRegion(
    reducer=ee.Reducer.toList(),
    geometry=vectors,
    scale=100)
  # get data into three different arrays
  data_ph = np.array((ee.Array(latlon.get("ph")).getInfo()))

  df = pd.concat([pd.DataFrame(data_do, columns = ['Dissolved Oxygen']),\
             pd.DataFrame(data_ndsi, columns = ['Salinity']),\
             pd.DataFrame(data_lst, columns = ['Temperature']),\
             pd.DataFrame(data_ph, columns = ['pH']),\
             pd.DataFrame(data_ndti, columns = ['Turbidity']),\
             pd.DataFrame(data_dom_2021_Jan_August_test, columns = ['Dissolved Organic Matter']),\
             pd.DataFrame(data_sm_2021_Jan_August_test, columns = ['Suspended Matter']),\
             pd.DataFrame(data_ndci, columns = ['Chlorophyll'])], axis=1, sort=False)

  return df

def send_df(df2):
  df2 = df2.dropna()
  df2['Dissolved Organic Matter'] = df2['Dissolved Organic Matter']*1000
  df2['Suspended Matter'] = df2['Suspended Matter']*1000
  test = pd.DataFrame(MinMaxScaler().fit_transform(df2.drop(['Salinity'], axis=1)), columns=df2.drop(['Salinity'], axis=1).columns)
  return df2, test