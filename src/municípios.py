import pandas as pd

def lista_municípios():
    df = pd.read_csv('src\municípios.csv', sep=';')
    municípios = df['id_municipio']

    return municípios