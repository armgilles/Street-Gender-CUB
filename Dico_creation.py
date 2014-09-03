# -*- coding: utf-8 -*-
import pandas as pd
import urllib2
import os


cwd = os.getcwd()
cwd_data = os.path.join(cwd, 'data')

#Loading the first dico of gender name


print "loading the first file od gender - name..."
data1= pd.read_csv("data/Gender1.csv")
# Delete colums 'Genre' et 'Genre_detail'. We don't need it.
data1 = data1.drop(['Genre', 'Genre_detail'], axis=1)
data1 = data1.drop_duplicates()

## To see doublon on the first file
#doublon = data[data.duplicated('Prenom')]
#doublon = data1.groupby('Prenom').size()
#df = pd.DataFrame(doublon, columns=['size'])
#df = df[df.size>1]
#doublon_nom = data1[data1.Prenom.isin(df.index)]

print "doing some work on the first file..."
# We have to sort the dataset to filter by "Homme" is priority
data1['sort_genre'] = data1.Genre_main.map({'Homme': 1, 'Femme': 2,'Non défini': 3})
data1 = data1.sort(['Prenom', 'sort_genre'], ascending=[1,1])
data1 = data1.drop('sort_genre', axis=1)
data1 = data1.drop_duplicates('Prenom')
data1.columns = ['gender', 'name']
cols = ['name', 'gender']
data1 = data1[cols]



#Loading the seconde dico of gender name
file_name2 = 'Gender2.csv'
data2_path = os.path.join(cwd_data, file_name2)

print "Loading the seconde file of gender - name..."
source = 'https://gist.githubusercontent.com/ptigas/1965524/raw/d41bca0e4c5adc47bad461597b5576c2efac5365/names.csv'
if not os.path.exists(data2_path):
    response = urllib2.urlopen(source)
    with open(data2_path, 'wb') as fh:
        x = response.read()
        fh.write(x)
    print "Downloading OK !"
else:
    print "File is already in the directory..." 
        

header = ['name', 'Nbr', 'gender', 'year']
data2 = pd.read_csv(data2_path , names=header)
data2['name'] = data2['name'].str.lower()
data2['gender'] = data2.gender.map({'male': 'Homme', 'female': 'Femme'})
data2 = pd.DataFrame({'count' : data2.groupby(['name', 'gender']).size()}).reset_index()
# On trie sur le count pour faire le drop duplicates
data2 = data2.sort(['name', 'count'], ascending=[1,0])
data2 = data2.drop_duplicates('name')
data2 = data2.drop('count', axis=1)


# To see doublon on the seconde file
#doublon = data2.groupby('name').size()
#doublon = pd.DataFrame(doublon, columns=['size'])
#doublon = doublon[doublon.size>1]
#doublon = data2[data2.name.isin(doublon.index)]


# We append the first and seconde file on a news Dataset
print "Creating our new dico of gender - name ..."
mydata = data1.append(data2)

mydata['sort_genre'] = mydata.gender.map({'Homme': 1, 'Femme': 2,'Non défini': 3})
mydata = mydata.sort(['name', 'gender'], ascending=[1,1])
mydata = mydata.drop('sort_genre', axis=1)
mydata= mydata.drop_duplicates('name')


mydata.to_csv('data/Dico_gender.csv')


