# (C) Julius Maylett 2021-2022, Forus Oy
# Ohjelma hakee XML-muodossa kiinteistörajoja annettujen rajojen sisältä. 
# Lue README tarkkaan

import os
import json
import requests
from geojson import FeatureCollection

# Määritä työtiedosto, joka on samassa hakemistossa tämän ajotiedoston kanssa.
fileName = "testi.geojson"

def CQLString(geometry):
    CQLStatement = "CQL_FILTER=INTERSECTS(geometry,POLYGON(("
    for point in geometry:
        lon = point[0]
        lat = point[1]
        CQLStatement = CQLStatement + str(lon) + "%20" + str(lat) + ","
    CQLStatement = CQLStatement[:-1]
    CQLStatement = CQLStatement + ")))"
    return CQLStatement

def CPXML(geometry):
    # Tehdään intersectiohaku annetun geometrian avulla käyttäen CQLSTATEMENTIA
    cql_String = CQLString(geometry)
    CPURL = "https://inspire-wfs.maanmittauslaitos.fi/inspire-wfs/cp/wfs?srsName=EPSG:3067&SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&"\
    "TYPENAMES=cp:CadastralParcel&TYPENAME=cp:CadastralParcel&STARTINDEX=0&COUNT=200000&SRSNAME=EPSG:3067&" + cql_String
    r = requests.get(CPURL) # Haku on erittäin hidas, kärsivällisyyttä
    return r.text

with open(fileName) as f:
    data = json.load(f)

feature_collection = FeatureCollection(data)

i = 0

print("Started")

# Huolehditaan, että output-kansio on olemassa
if not os.path.isdir('./output'):
    os.mkdir('output') 

print(len(feature_collection['features']) + " areas to handle...")

for feature in feature_collection['features']:

    print("Collecting CP data from NLS...")
    # Haetaan geometria, ja määritellään tiedoston nimeksi fid-tunniste
    xml = CPXML(feature['geometry']['coordinates'][0])
    fid = feature['properties']['fid']

    with open('output/{}.xml'.format(fid), 'w') as f:
        f.write(xml)

    i += 1
    print("Completed:" , i , "/" , len(feature_collection['features']))


print("Finished")