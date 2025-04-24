import json
import os

arquivo_consolidado = 'data/silver/statistics_results_consolidado.json'
arquivo_incremental = 'data/staging/statistics/incremental_games_statistics.json'

if os.path.exists(arquivo_consolidado):
    with open(arquivo_consolidado, 'r', encoding='utf-8') as f:
        dados_consolidados = json.load(f)
else:
    dados_consolidados = []

with open(arquivo_incremental, 'r', encoding='utf-8') as f:
    dados_incrementais = json.load(f)

ids_consolidados = {item['id'] for item in dados_consolidados}

dados_filtrados = [item for item in dados_incrementais if item['id'] not in ids_consolidados]

dados_consolidados.extend(dados_filtrados)

with open(arquivo_consolidado, 'w', encoding='utf-8') as f:
    json.dump(dados_consolidados, f, ensure_ascii=False, indent=4)

print(f"✅ Arquivo consolidado atualizado com {len(dados_filtrados)} novos jogos.")