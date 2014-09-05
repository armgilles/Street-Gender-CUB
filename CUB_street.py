# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import os
import nltk
from nltk.corpus import stopwords

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
street_load = pd.read_csv(data_path_street)
drop_cols = ['GID', 'DOMANIAL', 'IDENT', 'MOTD', 'NUMEROFR', 'NUMEROEU', 'CDATE', 'MDATE']

# Working on colums (droping and renaming)
street = street_load.drop(drop_cols, axis=1)
cols_street = ['type', 'street_simple', 'code_riv', 'street_full', 'code_commune']
street.columns = cols_street

#Dropint null value in code_commune (53 values)
street = street.dropna(subset=['code_commune'])
#street['code_ilot'] = street['code_ilot'].astype(int)


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

print "Working on CUB's City file..."    
# commune.GID = street.code_commune

# Certaines rue n'ont pas de code commune
#len(street[street.code_commune.isnull()]) = 53
cols_commune = ['COM_code_commune', 'COM_code_ilot', 'COM_nom_commune_maj','COM_abscisse', 'COM_ordonne','COM_orientation', 'COM_nom_commune', 'COM_date_creation', 'COM_date_modifiction']
commune = pd.read_csv(data_path_commune)
commune.columns = cols_commune
commune['COM_code_commune'] = commune['COM_code_commune'].astype(int)


print "Merging street & commune file..."
street_commune = pd.merge(street, commune, left_on='code_commune', right_on='COM_code_commune')


print "Working on Ilot INSEE file..."    
ilot = pd.read_csv(data_path_INSEE)
cols_ilot = ['ILOT_id', 'ILOT_code_ilot', 'ILOT_numero', 'ILOT_abscisse', 'ILOT_ordonnées', 'ILOT_orientation', 'ILOT_pop_municipale', 'ILOT_pop_compté_a_part', 'ILOT_pop_totale', 'ILOT_pop_sans_double_compte','ILOT_nbr_residence_prin', 'ILOT_nbr_residence_secon','ILOT_NB_LOG_O', 'ILOT_nbr_logement_vancant', 'ILOT_nbr_logement_total', 'ILOT_date_creation', 'ILOT_date_modif']
ilot.columns = cols_ilot
#ilot['ILOT_code_ilot'] = ilot['ILOT_code_ilot'].astype(int)
ilot['ILOT_code_ilot_normalise'] = ilot['ILOT_code_ilot'].map(lambda x: x[:3]).astype(int)
ilot_grouped = ilot.groupby(['ILOT_code_ilot_normalise'])['ILOT_pop_municipale','ILOT_pop_compté_a_part',
                                                        'ILOT_pop_totale', 'ILOT_pop_sans_double_compte', 
                                                        'ILOT_nbr_residence_prin', 'ILOT_nbr_residence_secon', 
                                                        'ILOT_NB_LOG_O', 'ILOT_nbr_logement_vancant',
                                                        'ILOT_nbr_logement_total'].sum()
                                                        
print "Merging commune's street and features of INSEE's ilot..."
cub_street_enrich = pd.merge(street_commune, ilot_grouped,
                    left_on='COM_code_ilot', right_on='ILOT_code_ilot_normalise',
                    how='left')

#quartier_bdx = pd.read_csv(data_path_quartier_bdx, sep=';')




