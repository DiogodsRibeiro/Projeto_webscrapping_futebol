import pandas as pd
import os
from glob import glob

INPUT = 'data/raw/results/'
OUTPUT_DIR = 'data/last_update'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'calender.json')

arquivos = glob(os.path.join(INPUT, '*.json'))

lista_resultados = []

def get_last_update_calender():

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

            resultado['data_maxima'] = resultado['data_maxima'].dt.strftime('%d/%m/%Y')


            lista_resultados.append(resultado)

        except Exception as e:
            print(f'Erro ao processar {arquivo}: {e}')


try:
    df_final = pd.concat(lista_resultados, ignore_index=True)
    df_final.to_json(OUTPUT_FILE, orient='records', indent=2, force_ascii=False)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f'Arquivo salvo em: {OUTPUT_FILE}')
except ValueError as ve:
    print(f'Arquivos nao existem na pasta {INPUT}: {ve}')

get_last_update_calender()



