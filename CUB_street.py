# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import os
import string
import numpy as np



"""
Fonction
"""
        
def clean_caract(x):
     try:
        t = string.maketrans('','')
        nodigits = t.translate(t, string.digits)
        #return float(str(x).translate(t, nodigits)) version Alex
        return x[:1] + str(x[1:]).translate(t, nodigits)
     except:
        return np.NaN


cwd = os.getcwd()
cwd_data = os.path.join(cwd, 'data')


"""

Chargement des fichiers

"""

# Name street CUB
file_name_street = 'Cub_street.csv'
data_path_street = os.path.join(cwd_data, file_name_street)

print "Loading the csv file of Cub's street ..."
source_street = 'http://data.lacub.fr/files.php?gid=23&format=6'
if not os.path.exists(data_path_street):
    response = urllib2.urlopen(source_street)
    with open(data_path_street, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 


# Ilot INSEE
# Dico des donneés : http://data.lacub.fr/dicopub/#IN_ILOT_S
file_name_INSEE = 'ilot_INSEE.csv'
data_path_INSEE = os.path.join(cwd_data, file_name_INSEE)

print "Loading the csv file of Ilot INSEE ..."
source_INSEE = 'http://data.lacub.fr/files.php?gid=25&format=6'
if not os.path.exists(data_path_INSEE):
    response = urllib2.urlopen(source_INSEE)
    with open(data_path_INSEE, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 

#Commune de la CUB
#Dico : http://data.lacub.fr/dicopub#FV_COMMU_S
file_name_commune = 'commune_CUB.csv'
data_path_commune = os.path.join(cwd_data, file_name_commune)

print "Loading the csv file of CUB's city ..."
source_commune = 'http://data.lacub.fr/files.php?gid=17&format=6'
if not os.path.exists(data_path_commune):
    response = urllib2.urlopen(source_commune)
    with open(data_path_commune, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 


#Commune de la CUB
#Dico : http://data.lacub.fr/dicopub#FV_COMMU_S
file_name_quartier_bdx = 'quartier_bdx.csv'
data_path_quartier_bdx = os.path.join(cwd_data, file_name_quartier_bdx)

print "Loading the csv file of Bordeaux's neighborhood ..."
source_quartier_bdx = 'http://opendatabdx.cloudapp.net/DataBrowser/DownloadCsv?container=databordeaux&entitySet=refvoiesquartiers&filter=NOFILTER'
if not os.path.exists(data_path_quartier_bdx):
    response = urllib2.urlopen(source_quartier_bdx)
    with open(data_path_quartier_bdx, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 


"""

Création de DF

"""

print "Working on Street file..."    
street_load = pd.read_csv(data_path_street, encoding='latin-1')
drop_cols = ['GID', 'DOMANIAL', 'IDENT', 'MOTD', 'NUMEROFR', 'NUMEROEU', 'CDATE', 'MDATE']
1
# Working on colums (droping and renaming)
street = street_load.drop(drop_cols, axis=1)
cols_street = ['type', 'street_simple', 'code_riv', 'street_full', 'code_commune']
street.columns = cols_street
# Nettoyage des code_riv (Caractere présent)
street['code_riv'] = street['code_riv'].apply(clean_caract)

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
                                        'cr': 'Chemin Rural',
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

#Dropint null value in code_commune (53 values)
street = street.dropna(subset=['code_commune'])
# Creating ID for Street (to join with Quartier)
street['code_commune'] = street['code_commune'].astype(int) # ?? Demander explication à Alex pourquoi cast Int puis STR pour enlever ".0"
street['code_riv_commune'] = street['code_riv'] + street['code_commune'].astype(str) + street['type_full'].apply(lambda x: x[:2].decode('latin-1').lower())

# Cleaning some data
street['street_full'] = street['street_full'].str.replace("Caud", "")

print "Working on CUB's City file..."    

cols_commune = ['COM_code_commune', 'COM_code_ilot', 'COM_nom_commune_maj','COM_abscisse', 'COM_ordonne','COM_orientation', 'COM_nom_commune', 'COM_date_creation', 'COM_date_modifiction']
commune = pd.read_csv(data_path_commune, encoding='latin-1')
commune.columns = cols_commune
commune['COM_code_commune'] = commune['COM_code_commune'].astype(int)


print "Merging street & commune file..."
street_commune = pd.merge(street, commune, left_on='code_commune', right_on='COM_code_commune')


print "Working on Ilot INSEE file..."    
ilot = pd.read_csv(data_path_INSEE)
cols_ilot = ['ILOT_id', 'ILOT_code_ilot', 'ILOT_numero', 'ILOT_abscisse', 'ILOT_ordonnées', 'ILOT_orientation', 'ILOT_pop_municipale', 'ILOT_pop_compté_a_part', 'ILOT_pop_totale', 'ILOT_pop_sans_double_compte','ILOT_nbr_residence_prin', 'ILOT_nbr_residence_secon','ILOT_NB_LOG_O', 'ILOT_nbr_logement_vancant', 'ILOT_nbr_logement_total', 'ILOT_date_creation', 'ILOT_date_modif']
ilot.columns = cols_ilot
ilot['ILOT_code_ilot_normalise'] = ilot['ILOT_code_ilot'].map(lambda x: x[:3]).astype(int)
ilot_grouped = ilot.groupby(['ILOT_code_ilot_normalise'])['ILOT_pop_municipale','ILOT_pop_compté_a_part',
                                                        'ILOT_pop_totale', 'ILOT_pop_sans_double_compte', 
                                                        'ILOT_nbr_residence_prin', 'ILOT_nbr_residence_secon', 
                                                        'ILOT_NB_LOG_O', 'ILOT_nbr_logement_vancant',
                                                        'ILOT_nbr_logement_total'].sum().reset_index()
                                                        
print "Merging commune's street and features of INSEE's ilot..."
# on ne peux pas joindre un ilot sur une rue
# on sum donc les features au niveau de la ville
cub_street_enrich = pd.merge(street_commune, ilot_grouped,
                    left_on='COM_code_ilot', right_on='ILOT_code_ilot_normalise',
                    how='left')

print "Working on CUB's City file..." 

quartier_bdx = pd.read_csv(data_path_quartier_bdx, sep=';')
quartier_bdx = quartier_bdx.drop(['DEBUT', 'FIN', 'CODEPOSTAL'], axis=1)
quartier_bdx = quartier_bdx.drop_duplicates()

grouped_quartier = quartier_bdx.groupby(['CODERIVOLI', 'NOMQUARTIER','LIBELLEVOIE', 'TYPEVOIE']).count().reset_index()
grouped_quartier = pd.DataFrame(grouped_quartier[['CODERIVOLI','NOMQUARTIER', 'LIBELLEVOIE', 'TYPEVOIE']])
cols_grouped_quartier = ['QUAR_code_rivoli', 'QUAR_nom_quartier','QUAR_nom_voie', 'QUAR_type']
grouped_quartier.columns = cols_grouped_quartier
grouped_quartier['QUAR_type'] = grouped_quartier['QUAR_type'].str.lower()
grouped_quartier['QUAR_type'] = grouped_quartier['QUAR_type'].str.replace('É','e')


grouped_quartier['QUAR_code_rivoli'] = grouped_quartier['QUAR_code_rivoli'].apply(clean_caract)
grouped_quartier['QUAR_code_rivoli_commune'] = grouped_quartier['QUAR_code_rivoli'] + '18' + grouped_quartier['QUAR_type'].apply(lambda x: x[:2]) # Bordeaux Code Commune
grouped_quartier = grouped_quartier.drop_duplicates('QUAR_code_rivoli_commune')

cub_data = pd.merge(cub_street_enrich, grouped_quartier, left_on='code_riv_commune', right_on='QUAR_code_rivoli_commune', how='left')
cub_data.index.names = ['index']


print "Creating csv from cub_data..."
cub_data.to_csv('data/result/Cub_data.csv', encoding='latin-1')