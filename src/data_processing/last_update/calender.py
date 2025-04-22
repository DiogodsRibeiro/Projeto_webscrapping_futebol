import pandas as pd
import os
from glob import glob

INPUT = 'data/raw/calender'
OUTPUT_DIR = 'data/last_update'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'last_data_calender.json')

arquivos = glob(os.path.join(INPUT, '*.json'))

if not os.path.exists(INPUT):
    raise FileNotFoundError(f'A pasta {INPUT} não existe.')

# Verifica se a pasta de saída existe
if not os.path.exists(OUTPUT_DIR):
    raise FileNotFoundError(f'A pasta {OUTPUT_DIR} não existe.')

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

if __name__ == '__main__':
    get_last_update_calender()

    try:
        df_final = pd.concat(lista_resultados, ignore_index=True)
        df_final.to_json(OUTPUT_FILE, orient='records', indent=2, force_ascii=False)
        print(f'Arquivo salvo em: {OUTPUT_FILE}')
    except ValueError as ve:
        print(f'Nenhum arquivo válido encontrado na pasta {INPUT}: {ve}')
        
 