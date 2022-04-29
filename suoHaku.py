# (C) Julius Maylett 2021-2022, Forus Oy
# Ohjelma hakee XML-muodossa kiinteistörajoja annettujen rajojen sisältä. 
# Lue README tarkkaan

import os
import json
import requests
from geojson import FeatureCollection

# Määritä työtiedoston nimi, joka on read-hakemistossa projektin juuressa
filename = "uudetAlueetSimplifiedBuffer"

file = "read/"+ filename +".geojson"
NEXT_INDEX, i = 0, 1

def CQLString(geometry):
    CQLStatement = "CQL_FILTER=INTERSECTS(geometry,POLYGON(("
    for point in geometry:
        CQLStatement = CQLStatement + str(int(point[0])) + "%20" + str(int(point[1])) + ","
    CQLStatement = CQLStatement[:-1]
    CQLStatement = CQLStatement + ")))"
    return CQLStatement

def CPXML(geometry):
    # Tehdään intersectiohaku annetun geometrian avulla käyttäen CQLSTATEMENTIA
    cql_String = CQLString(geometry)
    CPURL = "https://inspire-wfs.maanmittauslaitos.fi/inspire-wfs/cp/wfs?"\
    "srsName=EPSG:3067&SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&"\
    "TYPENAMES=cp:CadastralParcel&TYPENAME=cp:CadastralParcel&STARTINDEX=0&"\
    "COUNT=200000&SRSNAME=EPSG:3067&" + cql_String
    #r = requests.get(CPURL) # Haku on erittäin hidas, kärsivällisyyttä
    return "r.text"
    

def writeXML(fid, xml, NEXT_INDEX=None):
    if NEXT_INDEX == None: fileString = 'output/{}.xml'.format(fid)
    else: fileString = 'output/{}_{}.xml'.format(fid, NEXT_INDEX)
    with open(fileString, 'w') as f:
        f.write(xml)
        NEXT_INDEX += 1

## STARTING ##
with open(file) as f: data = json.load(f)
feature_collection = FeatureCollection(data)

print("Started")

if not os.path.isdir('./output'):
    # Huolehditaan, että output-kansio on olemassa
    os.mkdir('output') 

#print(len(feature_collection['features']) + " areas to handle...")

for feature in feature_collection['features']:
   
    if (feature['geometry']['type'] == 'MultiPolygon'): 
        for poly in feature['geometry']['coordinates']: 
            writeXML(feature['properties']['fid'], CPXML(poly[0]), NEXT_INDEX)
            NEXT_INDEX += 1
        NEXT_INDEX = 0
    if (feature['geometry']['type'] == 'Polygon'): writeXML(feature['properties']['fid'], CPXML(feature['geometry']['coordinates'][0]))
    print("Completed:" , i , "/" , len(feature_collection['features']))
    i += 1

print("Finished")