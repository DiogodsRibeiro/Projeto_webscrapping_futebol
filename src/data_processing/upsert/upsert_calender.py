import json
import os

# Pastas e arquivos
pasta_raw = 'data/raw/calender'
arquivo_consolidado_Results = 'data/silver/results_consolidado.json'
arquivo_consolidado = 'data/silver/calender_consolidado.json'



def upsert_calender():

    dados_consolidados = []

    ids_existentes = set()

    if os.path.exists(arquivo_consolidado_Results):
        with open(arquivo_consolidado_Results, 'r', encoding='utf-8') as f:
            try:
                dados_results = json.load(f)
                for item in dados_results:
                    if isinstance(item, dict) and 'id' in item:
                        ids_existentes.add(item['id'])
            except json.JSONDecodeError as e:
                print(f"⚠️ Erro ao ler {arquivo_consolidado_Results}: {e}")

    for nome_arquivo in os.listdir(pasta_raw):
        if nome_arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(pasta_raw, nome_arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                try:
                    dados = json.load(f)
                    if isinstance(dados, list):
                        for item in dados:
                            if isinstance(item, dict) and item.get('id') not in ids_existentes:
                                dados_consolidados.append(item)
                    elif isinstance(dados, dict) and dados.get('id') not in ids_existentes:
                        dados_consolidados.append(dados)
                except json.JSONDecodeError as e:
                    print(f"⚠️ Erro ao ler {nome_arquivo}: {e}")

    if dados_consolidados:
        with open(arquivo_consolidado, 'w', encoding='utf-8') as f:
            json.dump(dados_consolidados, f, ensure_ascii=False, indent=4)
        print(f"✅ Consolidado salvo com {len(dados_consolidados)} novos registros em {arquivo_consolidado}")
    else:
        print("ℹ️ Nenhum novo registro para consolidar.")