import string, random
# Importation de la librairie Natural Language Tool Kit pour les traitements NLP sur le text 
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
# importation de la fonction load_model pour le chargement du model
from tensorflow.python.keras.saving.save import load_model

# chargement des différents dictionnaires de mots
nltk.download('omw-1.4')
nltk.download("punkt")
nltk.download("wordnet")

# initialisation de lemmatizer pour obtenir la racine des mots
lemmatizer = WordNetLemmatizer()

# Listes des features généré
words = []

# Liste des intentions, actions , commandes dans le réseau télématique
classes = []

doc_X = []
doc_y = []

# Utilisation d'un dictionnaire pour représenter un fichier JSON d'intentions
data = {
    "intents": [
        {
            "tag": "grettings",
            "patterns": ["salut à toi!", "hello", "comment vas tu?", "salutations!", "enchanté", "hey"
                    "hey hey", "he", "heyyy"
                    "bonjour!",
                    "salut, comment ca va",
                    "bonjour, comment ca va",
                    "salut, comment vas-tu",
                    "comment vas-tu",
                    "enchantée.",
                    "salut, content de te connaitre.",
                    "un plaisir de te connaitre.",
                    "passe une bonne journée",
                    "quoi de neuf"],
            "responses" : ["Salut", "Bonjour", "Hello !", "Hi"]
        },
        {
            "tag" : "network_status",
            "patterns" : [ "quel est l état de fonctionnement du réseau", "quoi de neuf dans le réseau","quel est le statut de mon réseau",
            "ce qu'il y a de nouveau dans mon réseau"
            ], 
            "responses" : ["l'état du réseau est le suivant","l'état est le suivant","le statut est le suivant"]
        },
        {
            "tag" : "activity_status",
            "patterns" : [ "je voudrais les activités dans le réseau", "quel est le statut du réseau",
                    "quel est le rapport des alertes","quelles sont les informations du jour", "alertes dans le réeau"
            ], 
            "responses" : ["les activités sont", "Le rapport est le suivant"]
        },
        {
            "tag" : "yesterday_activity_status",
            "patterns" : [ "que s'est il passé hier dans mon réseau","qu'il y avait il dans mon réseau hier",
                "les actualités d'hier", "combien d'analyse ont été effectuées hier","statut d'hier"
            ], 
            "responses" : ["Liste des activités d'hier"]
        },
        {
            "tag" : "general_activity_status",
            "patterns" : [ "les activtés générales du réseau", "rapport général", "activités générales"
            ], 
            "responses" : ["le rapport général est le suivant"]
        },
        {
            "tag" : "machine_network_summary",
            "patterns" : ["rapport du monitoring réseau", "rapport du débit réseau","rapport de la bande passante","rapport prtg",
                "performances du réseau", "fonctionnement du réseau", "métrique de fonctionnement du réseau",
                "métriques réseau" 
            ], 
            "responses" : ["le rapport du monitoring est le suivant"]
        },
        {
            "tag" : "machine_system_summary",
            "patterns" : ["donne moi rapport de fonctionnement système","métrique cpu","métrique processeur","métrique ram",
            "métrique système", "métrique disque", "rapport des machines du système"
            ], 
            "responses" : ["le rapport du système est le suivant"]
        },
        {
            "tag" : "machine_services_summary",
            "patterns" : ["rapport du fonctionnement des services", "donne moi le rapport des services","rapport service", 
                "liste des services", "régime de fonctionnement des services"
            ], 
            "responses" : ["le rapport de fonctionnement des services est le suivant"]
        },
        {
            "tag" : "red_code",
            "patterns" : ["code rouge", "code code rouge", "arrêter tout les services", "éteindre le réseau", 
                        "arrêter les serveurs", "stoper les serveur", "éteindre les serveurs", 
                        "éteindre les services"],
            "responses" : ["Code rouge activé"]
        },
        {
            "tag": "ssh_connections",
            "patterns": ["afficher la liste des connexions SSH", "Afficher les dernière connexions SSH",
                    "connexion SSH"],
            "responses": ["Voici la liste des dernière connexions SSH"]
        },
        {
            "tag": "stop_maia",
            "patterns": ["Au revoir", "A plus", "Bye", "Stop", "cya", "Au revoir"],
            "responses": ["C'était sympa de vous parler", "à plus tard", "A plus!"]
        }
]}

# Nous iterrons sur tous les intentions et nous tokenisons chaque patterns que nous ajoutons à la liste words
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        doc_X.append(pattern)
        doc_y.append(intent["tag"])

    # Ajouter le tag aux classes
    if intent["tag"] not in classes:
        classes.append(intent["tag"])
# Conversion en minuscule de tous les mots du vocalbulaire 
# et lemmatisation 
# On evite les caractères de pontuation
words = [lemmatizer.lemmatize(word.lower())
         for word in words if word not in string.punctuation]

# trie par ordre alphabétique et supression des doubles en convertissant les listes en set
words = sorted(set(words))
classes = sorted(set(classes))

"""
Une fois lancée, cette fonction permet de construire et d'entrainer le modèle.
Le modèle issue est sauvegardé dans une fichier maia_model au format HDF5
"""
def train_model() -> None:
    global model 
    # liste pour les données d'entraînement
    training = []
    out_empty = [0] * len(classes)
    # création du modèle d'ensemble de mots
    for idx, doc in enumerate(doc_X):
        bow = []
        text = lemmatizer.lemmatize(doc.lower())
        for word in words:
            bow.append(1) if word in text else bow.append(0)
        # marque l'index de la classe à laquelle le pattern atguel est associé à
        output_row = list(out_empty)
        output_row[classes.index(doc_y[idx])] = 1
        # ajoute le one hot encoded BoW et les classes associées à la liste training
        training.append([bow, output_row])
    # mélanger les données et les convertir en liste
    random.shuffle(training)
    training = np.array(training, dtype=object)
    # séparer les features et les labels(différentes classes)
    train_X = np.array(list(training[:, 0]))
    train_y = np.array(list(training[:, 1]))

    # définition des paramètres pour la création du modèle 
    input_shape = (len(train_X[0]),)
    output_shape = len(train_y[0])
    epochs = 200

    # Modèle Deep Learning de MAIA
    model = Sequential()
    # Couche d'entrée du réseau de neurones
    model.add(Dense(128, input_shape=input_shape, activation="relu"))
    model.add(Dropout(0.5))
    # Couche cachée L=1
    # ReLU : Rectified Linear Unit , f(x) = max(0,x)
    # C'est une fonction de redressement
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.3))
    # Couche de sortie
    # softmax(exponentielle normalisée) : 
    # permet de générer une sortie probabiliste pour la classification
    model.add(Dense(output_shape, activation="softmax"))
    # Ajout de la fonction d'optimisation Adam(Adaptive Moment Estimation)
    adam = tf.keras.optimizers.Adam(learning_rate=0.01, decay=1e-6)

    # Définition des paramètres pour la retropropagation
    model.compile(loss='categorical_crossentropy',
                optimizer=adam, metrics=["accuracy"])

    # Entrainement du modèle sur 200 itérations 
    model.fit(x=train_X, y=train_y, epochs=200, verbose=1)

    # sauvegarde du modèle
    model.save('maia_model.hdf5')

    # Affichage du bilan de l'entrainement
    print("***************************************")
    print("FIN DE L'ENTRAINEMENT DU MODELE")
    print(f"Nombre de classes : {len(classes)}")
    print(f"Nombre de features : {len(words)}")
    print("***************************************")

# Chargement du modèle le plus à jour
model = load_model('maia_model.hdf5')

# fonction utilisée pour reformater l'entrée de l'utilisateur 
# en utilisant un tokeniseur et le lemmatiseur
def clean_text(text):
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

# Fonction de transformation des tokens en base 2 (0,1) pour l'envoi des listes de données dans le 
# réseau de neurones et l'application des fonctions mathématiques
def bag_of_words(text, vocab):
    tokens = clean_text(text)
    bow = [0] * len(vocab)
    for w in tokens:
        for idx, word in enumerate(vocab):
            if word == w:
                bow[idx] = 1
    return np.array(bow)


def class_prediction(text, vocab, labels):
    bow = bag_of_words(text, vocab)
    result = model.predict(np.array([bow]))[0]
    thresh = 0.2
    y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]
    y_pred.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in y_pred:
        return_list.append(labels[r[0]])
    return return_list


def get_intent(intents_list, dataset_json_intents):
    tag = intents_list[0]
    list_of_intents = dataset_json_intents["intents"]
    for intent in list_of_intents:
        if intent["tag"] == tag:
            break
    return intent

# lancement de l'agent conversationnel pour le test
if __name__ == '__main__' : 
    while True:
        # TODO :  remove this line is production // break 
        # break ; 
        message = input("")
        intents = class_prediction(message.lower(), words, classes)
        result = random.choice(get_intent(intents, data)["responses"])
        print(result)
