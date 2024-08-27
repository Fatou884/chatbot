import streamlit as st
import nltk
import string
from collections import Counter
from math import sqrt
from nltk.corpus import stopwords

# Télécharger les stopwords
nltk.download('stopwords')


def preprocess(text):
    # Convertir le texte en minuscules
    text = text.lower()

    # Supprimer la ponctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokeniser le texte
    words = text.split()

    # Supprimer les mots vides
    stop_words = set(stopwords.words('french'))
    filtered_words = [word for word in words if word not in stop_words]

    return filtered_words


def cosine_similarity(vec1, vec2):
    # Compter les occurrences des mots
    vec1_count = Counter(vec1)
    vec2_count = Counter(vec2)

    # Identifier les mots communs
    common_words = set(vec1_count) & set(vec2_count)

    # Calculer le produit scalaire
    dot_product = sum([vec1_count[word] * vec2_count[word] for word in common_words])

    # Calculer les magnitudes
    magnitude1 = sqrt(sum([val ** 2 for val in vec1_count.values()]))
    magnitude2 = sqrt(sum([val ** 2 for val in vec2_count.values()]))

    # Éviter la division par zéro
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0

    # Calculer la similarité cosinus
    return dot_product / (magnitude1 * magnitude2)


def get_most_relevant_sentence(query, sentences):
    # Prétraiter la requête utilisateur
    query_tokens = preprocess(query)

    # Initialiser les valeurs de la meilleure similarité
    best_similarity = 0
    best_sentence = ""

    # Parcourir chaque phrase et calculer la similarité avec la requête
    for sentence in sentences:
        sentence_tokens = preprocess(sentence)
        similarity = cosine_similarity(query_tokens, sentence_tokens)

        if similarity > best_similarity:
            best_similarity = similarity
            best_sentence = sentence

    return best_sentence


def chatbot(user_input, text_data):
    # Découper le texte en phrases
    sentences = text_data.split('.')

    # Trouver la phrase la plus pertinente
    response = get_most_relevant_sentence(user_input, sentences)

    return response

def main():
    st.title("Chatbot - Récit: Ce que vous visez")

    # Lire le contenu du fichier texte en utilisant l'encodage 'ISO-8859-1'
    try:
        with open("Récit.txt", "r", encoding='utf-8') as file:
            text_data = file.read()
    except UnicodeDecodeError:
        with open("Récit.txt", "r", encoding='ISO-8859-1') as file:
            text_data = file.read()

    # Inviter l'utilisateur à poser une question
    user_input = st.text_input("Posez une question sur le texte:")

    # Si une question est posée, appeler le chatbot pour obtenir une réponse
    if user_input:
        response = chatbot(user_input, text_data)
        st.write("Chatbot:", response)

if __name__ == "__main__":
    main()
