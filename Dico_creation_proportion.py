# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import os


cwd = os.getcwd()
cwd_data = os.path.join(cwd, 'data')

#Loading the first dico of gender name


file_name2 = 'Gender_proportion.csv'
data_path = os.path.join(cwd_data, file_name2)

print "Loading file of gender - name - number..."
# Source : https://www.data.gouv.fr/fr/dataset/liste-des-prenoms-declares
# Ville : Nantes, Bordeaux, Paris, Sarlat-la-Canéda, Rennes, Toulouse, Digne-les-Bains et Strasbourg.
source = 'https://www.data.gouv.fr/storage/f/2013-11-29T12%3A43%3A16.623Z/prenoms-enfants-france.csv'
if not os.path.exists(data_path):
    response = urllib2.urlopen(source)
    with open(data_path, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 

    
print "Working on it..."    
prenom_annee = pd.read_csv(data_path, sep=';', skiprows=1, names=['prenoms', 'sexe', 'annee', 'nombre', 'ville'])
# Plusieurs ville n'ont pas de renseignement sur le sexe.
prenom_annee = prenom_annee.dropna()
# On supprime les naissances sous 'X'
prenom_annee = prenom_annee[prenom_annee.sexe != 'X']
prenom_annee['prenoms'] = prenom_annee['prenoms'].str.lower()

# On sum sur le group prenoms / sexe
group_prenoms_sexe = pd.DataFrame({'nombre_prenoms_sexe' : prenom_annee.groupby(['prenoms', 'sexe'])['nombre'].sum()}).reset_index()
# On sum sur uniquement prenoms
group_prenoms = pd.DataFrame({'nombre_prenoms' : prenom_annee.groupby(['prenoms'])['nombre'].sum()}).reset_index()

grouped = pd.merge(group_prenoms_sexe, group_prenoms, left_on='prenoms', right_on='prenoms', how='outer')
grouped['proportion'] = grouped['nombre_prenoms_sexe'] / grouped['nombre_prenoms']
# Sorting on prenom ASC / proportion DESC to prepare to drop doublon
grouped = grouped.sort(['prenoms', 'proportion'], ascending=[1,0])
grouped = grouped.drop_duplicates('prenoms')
print "Creating csv..."
grouped.to_csv('data/Dico_gender_proportion.csv')

