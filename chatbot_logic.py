from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import json

# Carregar Dados
perguntas = pd.read_csv("perguntas.csv")
frases = perguntas["frase"].astype(str).tolist()
categorias = perguntas["categoria"].astype(str).tolist()

# Treinamento
vetorizador = CountVectorizer()
x = vetorizador.fit_transform(frases)
modelo = MultinomialNB()
modelo.fit(x, categorias)

# Carregar Respostas
with open("respostas.json", "r", encoding="utf-8") as arquivo:
    respostas_db = json.load(arquivo)

def obter_resposta(pergunta_usuario):
    pergunta_vetorizada = vetorizador.transform([pergunta_usuario.lower()])
    probabilidades = modelo.predict_proba(pergunta_vetorizada)[0]
    maior_probabilidade = max(probabilidades)
    categoria_prevista = modelo.predict(pergunta_vetorizada)[0]

    if maior_probabilidade < 0.10:
        return "Desculpe, não entendi sua solicitação. Pode reformular?", 0
    else:
        return respostas_db[categoria_prevista], maior_probabilidade