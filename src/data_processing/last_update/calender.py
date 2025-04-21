import pandas as pd
import os
from glob import glob

path = 'data/raw/results/'

arquivos = glob(os.path.join(path, '*.json'))

lista_resultados = []

for arquivo in arquivos:
    try:
        df = pd.read_json(arquivo)

        df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
        df['chave'] = (
            df['origem'].astype(str) + "_" +
            df['Campeonato'].astype(str) + "_" +
            df['Temporada'].astype(str)
        ).str.replace('.', '', regex=False).str.replace(' ', '', regex=False)

        resultado = df.groupby('chave').agg(data_maxima=('Data', 'max')).reset_index()

        lista_resultados.append(resultado)

    except Exception as e:
        print(f'Erro ao processar {arquivo}: {e}')



df_final = pd.concat(lista_resultados, ignore_index=True)

print(df_final)
