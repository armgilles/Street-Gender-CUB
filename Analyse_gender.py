# -*- coding: utf-8 -*-
import pandas as pd
import os
import numpy as np
from nltk.corpus import stopwords
#from nltk import metrics
#import difflib

"""
Fonction
"""

stopw = stopwords.words('french')

def clean_stopwords_1(x):

    try:
        x = [w for w in x.split() if w.lower() not in stopw]
        return x[0].lower()
    except:
        return('')

def clean_stopwords_2(x):
    try:
        x = [w for w in x.split() if w.lower() not in stopw]
        return x[1].lower()    
    except:
        return('')
        
"""
Chargement fichiers
"""
cwd = os.getcwd()
cwd_data = os.path.join(cwd, 'data')
cwd_result = os.path.join(cwd, 'data/result')

# Name street CUB
file_name_street = 'Cub_data.csv'
data_path_street = os.path.join(cwd_result, file_name_street)

# Dico_gender
file_name_proportion = 'Dico_gender_proportion.csv'
data_path_dico_prop = os.path.join(cwd_result, file_name_proportion)

# Dico_name
file_name_dico_name = 'Dico_gender.csv'
data_path_dico_name = os.path.join(cwd_result, file_name_dico_name)

#list_titre
file_name_list_title = 'liste_titre.csv'
data_path_list_title = os.path.join(cwd_data, file_name_list_title)

#list_personal
file_name_list_personal = 'liste_personnalite.csv'
data_path_list_personal = os.path.join(cwd_data, file_name_list_personal)


print "Loading the result of Cub Street..."
cub_data = pd.read_csv(data_path_street, index_col='index')

print "Loading the result of dico names proportion..."
dico_gender = pd.read_csv(data_path_dico_prop, index_col='index')

print "Loading the result of dico names..."
dico_name = pd.read_csv(data_path_dico_name)

print "Loading list of title..."
list_title = pd.read_csv(data_path_list_title, sep=';')

print "Loading list of personnality..."
list_personal = pd.read_csv(data_path_list_personal, sep=';')


"""
DF
"""

print "working on Cub street..."

# Clear stopword from name's street
cub_data['nom_street_1'] = cub_data['street_simple'].apply(clean_stopwords_1)
cub_data['nom_street_2'] = cub_data['street_simple'].apply(clean_stopwords_2)

print "Merging Cub street & Dico gender..."

result = pd.merge(cub_data, dico_gender, left_on='nom_street_1', right_on='prenoms', how='left')
result = pd.merge(result, dico_gender, left_on='nom_street_2', right_on='prenoms', how='left', suffixes=('_join_1', '_join_2'))

#Filling empty values
result['sexe_join_1'] = result['sexe_join_1'].fillna('Inconnu')
result['sexe_join_2'] = result['sexe_join_2'].fillna('Inconnu')

result['proportion_join_1'] = result['proportion_join_1'].fillna(1)
result['proportion_join_2'] = result['proportion_join_2'].fillna(1)


# Merging with list of title
print "Merging with list of title..."
result = pd.merge(result, list_title, left_on='nom_street_1', right_on='title_name', how='left')
result = pd.merge(result, list_title, left_on='nom_street_2', right_on='title_name', how='left', suffixes=['_1', '_2'])

result['title_genre_1'] = result['title_genre_1'].fillna('Inconnu')
result['title_genre_2'] = result['title_genre_2'].fillna('Inconnu')

result['title_coef'] = 0
result['title_coef'][(~result['title_name_1'].isnull()) | (~result['title_name_2'].isnull())] = 2
                                                                                                                              
result['street_genre'] = np.where((result['sexe_join_1'] == 'Inconnu') & (result['sexe_join_2'] == 'Inconnu') & (result['title_coef'] == 0),
                            'Inconnu',
                            np.where((result['sexe_join_1'] == 'Inconnu') & (result['sexe_join_2'] == 'Inconnu'),
                                # Checking if Title are unknow                            
                                np.where(result['title_genre_1'] == 'Inconnu', 
                                    result['title_genre_2'], 
                                    result['title_genre_1']),
                                np.where(result['sexe_join_1'] == 'Inconnu',
                                    result['sexe_join_2'],
                                    np.where((result['proportion_join_1'] <= result['proportion_join_2']) & (result['sexe_join_2'] != 'Inconnu'),
                                        result['sexe_join_2'],
                                        result['sexe_join_1']))))


# Merging with list of personnality
print "Merging with list of personnality..."
result = pd.merge(result, list_personal, left_on='nom_street_1', right_on='perso_nom', how='left')
result = pd.merge(result, list_personal, left_on='nom_street_2', right_on='perso_nom', how='left', suffixes=['_1', '_2'])

result['perso_genre_1'] = result['perso_genre_1'].fillna('Inconnu')
result['perso_genre_2'] = result['perso_genre_2'].fillna('Inconnu')

result['street_genre'] = np.where((result['street_genre'] == 'Inconnu') & 
                        ((result['perso_genre_1'] != 'Inconnu') | (result['perso_genre_2'] != 'Inconnu')),
                            np.where(result['perso_genre_1'] != 'Inconnu',
                                result['perso_genre_1'],
                                result['perso_genre_2']),
                            result['street_genre'])


result.to_csv('data/result/result_cub.csv')
