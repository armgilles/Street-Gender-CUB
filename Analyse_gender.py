# -*- coding: utf-8 -*-
import pandas as pd
import os
import numpy as np
from nltk.corpus import stopwords
#from nltk import metrics
import difflib

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
        
        
def get_close_name(s1, cutoff):
    try:
        return difflib.get_close_matches(s1, dico_gender['prenoms'], n=1, cutoff=cutoff)[0]
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


#result['genre_confiance'] = (result['proportion_join_1'] + result['proportion_join_2']) / 2

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
                                # On check si les Titres sont aussi inconnu                            
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


#test = result.nom_street_1.apply(lambda x: x in list_title.titre.values)


"""
def fuzzy_match(s1, s2, max_dist=3):
    return metrics.edit_distance(s1, s2) <= max_dist
"""
"""
result['test_0.8'] = result['nom_street_1'].apply(lambda x: get_close_name(x, 0.8))
result['test_0.9'] = result['nom_street_1'].apply(lambda x: get_close_name(x, 0.95))


analyse_join = pd.DataFrame({'nombre_prenoms_sexe' : result.groupby(['nom_street_1', 'test_0.8', 'test_0.9'])['nom_street_1'].count()}).reset_index()

nom_street_1_group = pd.DataFrame({'nbr' : result.groupby('nom_street_1')['nom_street_1'].count()}).reset_index()
nom_street_2_group = pd.DataFrame({'nbr' : result.groupby('nom_street_2')['nom_street_2'].count()}).reset_index()
nom_street_2_group.columns = ['nom_street_1', 'nbr']

grouped_nom_street = nom_street_1_group.append(nom_street_2_group)
grouped_nom_street = pd.DataFrame({'nbr': grouped_nom_street.groupby('nom_street_1')['nbr'].sum()}).reset_index()
grouped_nom_street['bool_prenom'] = grouped_nom_street.nom_street_1.apply(lambda x: x in mydata.name.values)



TO DO 

mask1 = pd.DataFrame(result.nom_street_1[result.street_genre == 'Inconnu'])
grouped_mask1 = pd.DataFrame(columns=['nbr'],data= mask1.nom_street_1.value_counts())
grouped_mask1 = grouped_mask1.reset_index()
grouped_mask1.columns=['nom', 'nbr']

mask2 = pd.DataFrame(result.nom_street_2[result.street_genre == 'Inconnu'])
grouped_mask2 = pd.DataFrame(columns=['nbr'],data= mask2.nom_street_2.value_counts())
grouped_mask2 = grouped_mask2.reset_index()
grouped_mask2.columns=['nom', 'nbr']

grouped_street = grouped_mask1.append(grouped_mask2)

"""


# Analyse of word .
# In case you want to improve the model.
# You can see with it street's word who match with first name or not
# the goal is to create a manual list of titre ('President etc..) and Personnalité (Voltaire etc..)
"""
print "Create a list of word and check if they can be a name..."

nom_street_1_group = pd.DataFrame({'nbr' : result.groupby('nom_street_1')['nom_street_1'].count()}).reset_index()
nom_street_2_group = pd.DataFrame({'nbr' : result.groupby('nom_street_2')['nom_street_2'].count()}).reset_index()
nom_street_2_group.columns = ['nom_street_1', 'nbr'] # To prepare the append()

list_nom_prenom = nom_street_1_group.append(nom_street_2_group)
list_nom_prenom = pd.DataFrame({'nbr': list_nom_prenom.groupby('nom_street_1')['nbr'].sum()}).reset_index()
list_nom_prenom['bool_prenom'] = list_nom_prenom.nom_street_1.apply(lambda x: x in dico_name.name.values)
list_nom_prenom = list_nom_prenom[list_nom_prenom.bool_prenom == True]
list_nom_prenom.columns = ['nom', 'nbr', 'bool_prenom']

print "Working with the list of name..."
result['nom_street_1_prenom'] = result['nom_street_1'].apply(lambda x:  np.where(x in list_nom_prenom.nom.values, 1, 0))
result['nom_street_2_prenom'] = result['nom_street_2'].apply(lambda x:  np.where(x in list_nom_prenom.nom.values, 1, 0))

"""

"""
ANALYSE
analyse_genre = result[['street_full', 'type_full', 'COM_nom_commune', 	'ILOT_pop_municipale',	'ILOT_pop_compté_a_part',	'ILOT_pop_totale',	'ILOT_pop_sans_double_compte',	'ILOT_nbr_residence_prin',	'ILOT_nbr_residence_secon',	'ILOT_NB_LOG_O','ILOT_nbr_logement_vancant',	'ILOT_nbr_logement_total','QUAR_nom_quartier','street_genre','genre_confiance']]
analyse_genre.columns = ['street_full', 'type_full', 'COM_nom_commune', 'ville_pop_municipale',	'ville_pop_compté_a_part',	'ville_pop_totale',	'ville_pop_sans_double_compte',	'ville_nbr_residence_prin',	'ville_nbr_residence_secon',	'ville_NB_LOG_O','ville_nbr_logement_vancant',	'ville_nbr_logement_total','nom_quartier', 'street_genre','genre_confiance']

result_s_inco = result[result.street_genre != 'Inconnu']
genre_par_ville = pd.DataFrame({'genre_par_ville' : result_s_inco.groupby(['COM_nom_commune', 'street_genre'])['1'].sum()}).reset_index()
nbr_rue_ville = pd.DataFrame({'rue_par_ville': result_s_inco.groupby('COM_nom_commune')['1'].sum()}).reset_index()
genre_ville = pd.merge(genre_par_ville, nbr_rue_ville, left_on='COM_nom_commune', right_on='COM_nom_commune', how='left')


analyse_genre.to_csv('analyse_genre.csv')




result_s_inco_quartier = result[(result.street_genre != 'Inconnu') & (result.QUAR_nom_quartier.isnull())]
genre_par_quartier = pd.DataFrame({'genre_par_quartier' : result_s_inco_quartier.groupby(['QUAR_nom_quartier', 'street_genre'])['QUAR_nom_quartier'].count()}).reset_index()

nbr_rue_ville = pd.DataFrame({'rue_par_ville': result_s_inco.groupby('COM_nom_commune')['1'].sum()}).reset_index()
genre_ville = pd.merge(genre_par_ville, nbr_rue_ville, left_on='COM_nom_commune', right_on='COM_nom_commune', how='left')



"""
