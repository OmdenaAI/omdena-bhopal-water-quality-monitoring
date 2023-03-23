import ee 
import geemap 
import json

f = open('coordinates.json')
data = json.load(f)


    
def geometry(): 
    lake = int(input('Choose the lake for which you want to extract the parameters : \n [1] Upper Lake \n [2] Lower Lake \n [3] Kaliyasot Dam \n [4] Kerwa Dam \n [5] Shahpura Lake \n [6] Saranpangi Lake \n [7] Motia Talab \n [8] Hathaikeda Dam/Lake \n [9] Nawab Munshi Hussain Khan Talab \n [10] Nawab Siddique Hasan Khan Talab \n [11] Jawahar Baal Udyan Lake \n [12] Lendia Talab \n [13] Manit Lake '))
    
    if lake == 1:
        geometry = data['features'][0]['geometry']['coordinates']  
    elif lake == 2:
        geometry = data['features'][1]['geometry']['coordinates']
    elif lake == 3: 
        geometry = data['features'][2]['geometry']['coordinates']
    elif lake == 4:
        geometry = data['features'][3]['geometry']['coordinates']
    elif lake == 5: 
        geometry = data['features'][4]['geometry']['coordinates']
    elif lake == 6: 
        geometry = data['features'][5]['geometry']['coordinates']
    elif lake == 7:
        geometry = data['features'][6]['geometry']['coordinates']
    elif lake ==8:
        geometry = data['features'][7]['geometry']['coordinates']
    elif lake ==9:
        geometry = data['features'][8]['geometry']['coordinates']
    elif lake == 10:
        geometry = data['features'][9]['geometry']['coordinates']
    elif lake ==11:
        geometry = data['features'][10]['geometry']['coordinates']
    elif lake ==12:
        geometry = data['features'][11]['geometry']['coordinates']
    elif lake ==13:
        geometry = data['features'][12]['geometry']['coordinates']
    else:
        print('Invalid Lake')
    return geometry

  

  

 