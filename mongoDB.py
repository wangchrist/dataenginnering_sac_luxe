import json
from pymongo import MongoClient

# Making Connection
myclient = MongoClient("localhost", 27017) 
 
# on crée la database sac_luxe
db= myclient["sac_luxe"]
  
# on crée la collection sac_vc

collection_vc= db["sac_vc"]

#on charge et on ouvre le fichier json
with open('data_vc.json') as file:
    file_data1 = json.load(file)
    collection_vc.insert_many(file_data1) 

# on crée la collection sac_mt
collection_mt= db["sac_mt"]


with open('data_mt.json') as file:
    file_data2 = json.load(file)
    collection_mt.insert_many(file_data2) 

##unification des données sac à anses et sac à main signifie la même chaud sur 
# les deux sites, du coup on remplace Sacs à anses par Porté main et pour porté épaule on remplace par Sacs portés épaule

filter_mt= {"categorie": "Sacs à anses"}

update_mt= {"$set": {"categorie": "Porté main"}}
collection_mt.update_many(filter_mt, update_mt)

filter_vc={"categorie": "Porté épaule"}
update_vc={"$set": {"categorie": "Sacs portés épaule"}}
collection_vc.update_many(filter_vc, update_vc)

#### Pour monter le moteur de recherche on utilise full text search de mongodb , l'utilisateur peut chercher en fonction de
# tous les indexes qu'on a défini avec des poids (importance) différents.
collection_vc.create_index([("categorie", 'text'), ("marque", 'text'), ("modele", "text"),
('matiere', "text"),('couleur', "text"),('prix', "text")],weights={"categorie": 3, "marque": 2, "modele": 3, "matiere": 1, "couleur": 3, "prix": 2})

collection_mt.create_index([("categorie", 'text'), ("marque", 'text'), ("modele", "text"),
('matiere', "text"),('couleur', "text"),('prix', "text")],weights={"categorie": 3, "marque": 2, "modele": 3, "matiere": 1, "couleur": 3, "prix": 2})
