import json

arquivo_consolidado = 'data/silver/results_consolidado.json'
arquivo_incremental = 'data/staging/results/all_results_incremental.json'

try:
    with open(arquivo_consolidado, 'r', encoding='utf-8') as f:
        dados_consolidados = json.load(f)
except FileNotFoundError:
    dados_consolidados = []

with open(arquivo_incremental, 'r', encoding='utf-8') as f:
    dados_incremental = json.load(f)

ids_consolidados = {item['id'] for item in dados_consolidados}

dados_filtrados = [
    item for item in dados_incremental if item['id'] not in ids_consolidados
]

novos_itens = len(dados_filtrados)

dados_consolidados.extend(dados_filtrados)

with open(arquivo_consolidado, 'w', encoding='utf-8') as f:
    json.dump(dados_consolidados, f, ensure_ascii=False, indent=4)

print(f"Dados atualizados em: {arquivo_consolidado}")
print(f"{novos_itens} itens novos foram adicionados.")