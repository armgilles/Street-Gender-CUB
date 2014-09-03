# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import os

cwd = os.getcwd()
cwd_data = os.path.join(cwd, 'data')

file_name = 'Cub_street.csv'
data_path = os.path.join(cwd_data, file_name)

print "Loading the csv file of Cub's street ..."
source = 'http://data.lacub.fr/files.php?gid=23&format=6'
if not os.path.exists(data_path):
    response = urllib2.urlopen(source)
    with open(data_path, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 

print "Working on Street file..."    
street = pd.read_csv(data_path)
drop_cols = ['GID', 'DOMANIAL', 'CODERIV', 'MOTD', 'IDENT', 'NUMEROFR', 'NUMEROEU', 'RHFV_COMMU', 'CDATE', 'MDATE']

# Working on colums (droping and renaming)
street = street.drop(drop_cols, axis=1)
cols = ['type', 'street_simple', 'street_full']
street.columns = cols

street['type'] = street['type'].str.lower()
street['type_full'] = street['type'].map({'ave' : 'Avenue',
                                        'rue': 'Rue',
                                        'bd' : 'Boulevard',
                                        'aut': 'Autoroute',
                                        'imp': 'Impasse',
                                        'chem': 'Chemin',
                                        'pce': 'Place',
                                        'lot': 'Lotissement',
                                        'all': 'Allée',
                                        'roc': 'Rocade',
                                        'res': 'Résidence',
                                        'rte': 'Route Départementale',
                                        'cim': 'Cimetière',
                                        'voie': 'Voie',
                                        'acc': 'Accès',
                                        'quai': 'Quai',
                                        'cote': 'Côte',
                                        'ech': 'Echangeur',
                                        'cr': 'Chemin Rur',
                                        'vc': 'Voie Communautaire',
                                        'ham': 'Hammeau',
                                        'pont': 'Pont',
                                        'prk': 'Parking',
                                        'pass': 'Passage',
                                        'cite': 'Cité',
                                        'sq': 'Sqaure',
                                        'pimp': 'Petite Impasse',
                                        'crs': 'Cours',
                                        'psup': 'Passage Supérieur',
                                        'rdpt': 'Rond-point',
                                        'ft': 'Forêt',
                                        'hlm': 'H.L.M',
                                        'bret': 'Bretelle',
                                        'parc': 'Parc',
                                        'cam': 'Camin',
                                        'pste': 'Piste Cyclable',
                                        'prom': 'Promenade',
                                        'terr': 'Terrasse',
                                        'parv': 'Parvis',
                                        'mail': 'Mail',
                                        'esp': 'Esplanade',
                                        'pco': 'Passe Communale',
                                        'sent': 'Sentier',
                                        'pch': 'Petit Chemin',
                                        'prue': 'Petite Rue',
                                        'clos': 'Clos',
                                        'car': 'Carrefour',
                                        'pinf': 'Passage Inférieur',
                                        'cd': 'Route Départementale'})


