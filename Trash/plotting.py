# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import os
import osmapi
from nominatim import Nominatim
import sys
import timeit

start_street_name = timeit.default_timer()


street = Nominatim()

osm = osmapi.OsmApi()

cwd = os.getcwd()
cwd_result = os.path.join(cwd, 'data/result')

# CUB's result
file_result_cub = 'result_cub.csv'
data_path_result_cub = os.path.join(cwd_result, file_result_cub)
osm_count = 0
"""
 OLD
def get_osmid(x):
    global osm_count
    osm_count = osm_count + 1
    try:
        osm_id = street.query(x.encode('latin-1'))[0]['osm_id']
        print str(osm_count) + ' :' + str(osm_id) + ': '  + x
    except:
        osm_id = np.nan
        print str(osm_count) + ' :' + str(osm_id) + ': ' + x
    return (osm_id)
"""    
def get_way(way_name, way_gender):
    try:
        query = street.query(way_name.encode('utf-8'))
        way_osm_id = query[0]['osm_id']
        lat = query[0]['lat']
        lon = query[0]['lon']
    except:
        way_osm_id = np.nan
        lat = np.nan
        lon = np.nan
    return(way_osm_id, lat, lon)
        
"""
To change abscisse & ordonne from CUB's data to lontitide & lattitude
"""
# ANTS
# http://ants.builders/


def L(phi):
    return(0.5 * np.log( (1 + np.sin(phi)) / (1 - np.sin(phi)))
            - e/2 * np.log( (1 + e * np.sin(phi)) / (1 - e * np.sin(phi))))

def toLambert(lon, lat):
    
    lon = lon * pi/180
    lat = lat * pi/180
        
    YS = N0 + C * np.exp(-n * L(phi0))
    
    R = C * np.exp(-n * L(lat))
    
    gamma = n * (lon - lon0)
    X = E0 + R * np.sin(gamma)
    Y = YS - R * np.cos(gamma)
    
    return(X, Y)          

def toLontLat(X, Y): # 1415898.46, 4188713.91

    dX = X + deltaX - E0 # -284101.54000000004
    dY = Y + deltaY - N0 - C * np.exp(-n * L(phi0)) #-6399393.9617670337

    R = np.sqrt(dX * dX + dY * dY) # 6405697.211305787
    
    gamma = np.arctan(-dX / dY) # -0.044365937581327786
    
    lon = gamma / n  + lon0 # -0.010381217055076129
    
    #dichotomy
    p0 = 2 * np.arctan(np.power(C/R, 1/n)) - pi/2 # 0.77927903614466842
    p1 = 2 * np.arctan(np.power(C/R, 1/n) * np.power((1 + e * np.sin(p0)) /
        (1 - e * np.sin(p0)), e/2) ) - pi/2 #0.78262412618386135
    delta = np.abs(p1 - p0) # 0.0033450900391929217
    """
    while(delta > 0.000001):
        p0 = p1
        p1 = 2 * np.arctan(np.power(R/C, 1/n) * np.power((1 + e * np.sin(p0)) /
                (1 - e * np.sin(p0)), e/2 ) -pi/2 )
        delta = np.abs(p1 - p0) # 4.759037608437211e-10
    """
    
    lon = lon*180/pi # -0.5947999234650917
    lat = p1*180/pi # -98.265139064722007
    
    return (lon, lat) #lon, lat
    
#  stellar parameters
a = 6378137             # demi grand axe
f = 1.0 / 298.257222101 # applatissement
b = (1-f)*a
## REVOIR LE FLOAT
e = np.sqrt(np.power(a,2, dtype=float)-np.power(b,2, dtype=float))/a
pi = np.pi
lon0 = 3 * pi/180

# CC is the number of the lamber projection 
# deltaX, deltaY are the shifts from the original center
CC = 45 # pour le SUD OUEST FRANCE
# We don't need deltaX & deltaY for this
deltaX = 0
deltaY = 0
NZ = CC - 41
phi0 = (41.0 + NZ)
phi1 = (phi0 - 0.75)
phi2 = (phi0 + 0.75)

phi0 = phi0 * pi/180
phi1 = phi1 * pi/180
phi2 = phi2 * pi/180

E0 = 1700000
N0 = (NZ * 1000000) + 200000

n = np.log( np.cos(phi2)/np.cos(phi1) * np.sqrt(1 - np.power(e * np.sin(phi1), 2)) /
         np.sqrt(1 - np.power(e * np.sin(phi2), 2)) ) / (L(phi1) - L(phi2))

C = a * np.cos(phi1) * np.exp(n * L(phi1)) / (n * np.sqrt(1 - np.power(e * np.sin(phi1), 2)))


##################

# Loading file

print "Loading the result of Cub Street..."
data = pd.read_csv(data_path_result_cub, index_col=[0], encoding='latin-1')

#data['lonlat'] = data.apply(lambda x: toLontLat(x['COM_abscisse'], x['COM_ordonne']), axis=1)
#data['longitude'] = data['lonlat'].apply(lambda x: x[0])
#data['latitude'] = data['lonlat'].apply(lambda x: x[1])
data['adresse'] = data['street_full'] + ' '+ data['COM_nom_commune']
df = pd.DataFrame(columns=['way_name', 'way_gender', 'way_lat', 'way_lon', 'way_id'])
osm_info = []
data['way_osm_id']= ''
data['lat']= ''
data['lon']= ''
data = data.head(15)
for index, row in data.iterrows():
    osm_info.append(get_way(row['adresse'], row['street_genre']))
    data.loc[index, 'way_osm_id'] = osm_info[index][0]
    data.loc[index, 'lat'] = osm_info[index][1]
    data.loc[index, 'lon'] = osm_info[index][2]
    #small_data['osm_way_id'] = small_data.apply(lambda x: x.)
    print "index : " + str(index)
stop_street_name = timeit.default_timer()
print stop_street_name - start_street_name

#data['osm_id'] = data['adresse'].apply(get_osmid)
start_geo_street = timeit.default_timer()

df = pd.DataFrame(columns=['way_osm_id', 'node_osm_id', 'node_lat', 'node_lon'])

#data = data.dropna(subset=["way_osm_id"])
"""

for index, row in data.iterrows():
    try:
        way = osm.WayGet(int(row.way_osm_id))
        nb_node = 0
        print "way : " + str(index)
        while nb_node < len(way[u'nd']):
            node = osm.NodeGet(way[u'nd'][nb_node])
            df.loc[len(df)+1] = [row.way_osm_id, node[u'id'], node[u'lat'], node[u'lon']]
            print "node : " + str(nb_node)
            nb_node = nb_node + 1
    except:
        pass

print "Merging data..."
#merging data
geo_street = pd.merge(data, df, left_on='way_osm_id', right_on='way_osm_id', how='left')

geo_street = geo_street[['way_osm_id', 'adresse', 'street_genre', 'node_lat', 'node_lon']]

stop_geo_street = timeit.default_timer()

print "temps de recherche nom de rue : " + str(stop_street_name - start_street_name)
print "temps de recherche geo sur les rues : " + str(stop_geo_street - start_geo_street)

print "Create csv..."

geo_street.to_csv('geo_street.csv', encoding='latin-1')

data
"""
"""
osm_id = street.query('rue des faussets bordeaux')[0]['osm_id']
wayrelation = osm.WayRelations(int(osm_id))

for w in wayrelation:
    for n in w['member']:
        node = osm.NodeGet(wayrelation[m]['member'])
        n = 1
            while (n >= len(node)):
                node_info = osm.NodeGet(node[n]['ref'])
                lat = node_info['lat']
                lon = node_info['lon']
                
                
                
                
                
                
                
for w in wayrelation:
     ...:     for m in w['member']:
     ...:         node = osm.NodeGet(w[m]['member'])
     ...:         for n in node:
     ...:             node_info = osm.NodesGet(n['ref'])
     ...:             lat = node_info['lat']
     ...:             lon = node_info['lon']
     ...:             print '\n'
     ...:             print "lat = " + str(lat) + ", lon = " + str(lon)
     


test = dict()
test['nom'] = dict()
test['nom']['lat'] = dict()
test['nom']['lon'] = dict()

m = 0
w = 0
lat = []
lon = []
osm_id = street.query('rue des faussets bordeaux')[0]['osm_id']
test['nom'] = 'rue des faussets bordeaux'
wayrelation = osm.WayRelations(int(osm_id))
while w < len(wayrelation):
    while m < (len(wayrelation[w]['member']) - 1):
        m = m + 1
        node = osm.NodeGet(wayrelation[w]['member'][m]['ref'])
        #test['lat'] = node['lat']
        #test['lon'] = node['lon']
        lat.append(node['lat'])
        lon.append(node['lon'])
    w = w + 1

query = street.query("Avenue de l'Eglise Romane Artigues-Près-Bordeaux")
way_id = []
q = 0
# list osm_id by street
while q < len(query):
    way_id.append(query[q]['osm_id'])
    q = q + 1


way = osm.WaysGet(way_id)
nodesid = []
i = 0
while i < len(way):
    nodesid.append(way[int(way_id[i])][u'nd'])
    i = i + 1
n = 0
lat = []
lon = []
while n < len(nodesid):
    nodes = osm.NodesGet(nodesid[n])
    for nid in nodes:
        nd=nodes[nid]
        lat.append(nd['lat'])
        lon.append(nd['lon'])
    n = n + 1



for way in small_geo_street:
    plt.plot(small_geo_street['node_lat'], small_geo_street['node_lon'], label=small_geo_street['street_genre'])

plt.legend()
plt.show() 


for index, grp in small_geo_street.groupby(['street_genre']):
     for wayid, way in grp.groupby(['way_osm_id']):
        plt.plot(way.node_lat, way.node_lon)

plt.legend()



for index, grp in small_geo_street.groupby(['way_osm_id']):
     for way, way in grp.groupby(['street_genre']):
        plt.plot(way.node_lat, way.node_lon)
plt.legend()


for wayid, way in geo_street_i.groupby(['way_osm_id']):
     plt.plot(way.node_lat, way.node_lon, color='g')

for wayid, way in geo_street_f.groupby(['way_osm_id']):
     plt.plot(way.node_lat, way.node_lon, color='b')
 
for wayid, way in geo_street_m.groupby(['way_osm_id']):
     plt.plot(way.node_lat, way.node_lon, color='r')
plt.legend(g)

"""

    
