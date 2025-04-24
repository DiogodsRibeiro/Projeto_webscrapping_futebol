import json
import os

# Pasta com os arquivos brutos
pasta_raw = 'data/raw/calender'
arquivo_consolidado = 'data/silver/calender_consolidado.json'

# Lista para armazenar todos os dados
dados_consolidados = []

# Percorrer todos os arquivos da pasta
for nome_arquivo in os.listdir(pasta_raw):
    if nome_arquivo.endswith('.json'):
        caminho_arquivo = os.path.join(pasta_raw, nome_arquivo)
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            try:
                dados = json.load(f)
                if isinstance(dados, list):
                    dados_consolidados.extend(dados)
                else:
                    dados_consolidados.append(dados)
            except json.JSONDecodeError as e:
                print(f"⚠️ Erro ao ler {nome_arquivo}: {e}")

# Salvar o arquivo consolidado
with open(arquivo_consolidado, 'w', encoding='utf-8') as f:
    json.dump(dados_consolidados, f, ensure_ascii=False, indent=4)

print(f"✅ Consolidado salvo com {len(dados_consolidados)} registros em {arquivo_consolidado}")
