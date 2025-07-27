import pandas as pd
import json

# Caminhos dos arquivos
path_calendar = r'C:\Users\diogo\Documents\projects\projeto_pessoal\Webscrapping_futebol\data\silver\calender_consolidado.json'
path_results = r'C:\Users\diogo\Documents\projects\projeto_pessoal\Webscrapping_futebol\data\silver\results_consolidado.json'
path_stats = r'C:\Users\diogo\Documents\projects\projeto_pessoal\Webscrapping_futebol\data\silver\statistics_results_consolidado.json'

def ConsolidarTabelas():

    # Carregar JSONs
    df_calendar = pd.read_json(path_calendar)
    df_results = pd.read_json(path_results)

    # Normalizar campo 'id' (remoção de prefixos, se houver)
    df_calendar['id'] = df_calendar['id'].str.replace(r'^(Avanca_na_competicao_|Vencedor_)', '', regex=True)
    df_results['id'] = df_results['id'].str.replace(r'^(Avanca_na_competicao_|Vencedor_)', '', regex=True)

    # Ajustar os nomes das colunas antes do append
    df_calendar.rename(columns={'Time da Casa': 'time_casa', 'Time Visitante': 'time_visitante'}, inplace=True)
    df_results.rename(columns={'Time da Casa': 'time_casa', 'Time Visitante': 'time_visitante', 
                        'Placar da Casa': 'placar_casa', 'Placar do Visitante': 'placar_visitante'}, inplace=True)

    # Adicionar a coluna StatusPartida
    df_calendar['StatusPartida'] = 'Partida não Iniciada'
    df_results['StatusPartida'] = 'Partida Encerrada'

    # Converter a coluna Data para datetime para ordenação
    df_calendar['Data'] = pd.to_datetime(df_calendar['Data'], format='%d/%m/%Y')

    # Adicionar coluna RodadaMarcada com valor ProximaRodada para a primeira data de cada campeonato
    df_calendar['RodadaMarcada'] = ''
    # Encontrar a primeira data de cada campeonato
    primeiras_datas = df_calendar.groupby('Campeonato')['Data'].min()
    # Atribuir 'ProximaRodada' para as partidas que são as primeiras de cada campeonato
    for campeonato, data in primeiras_datas.items():
        mask = (df_calendar['Campeonato'] == campeonato) & (df_calendar['Data'] == data)
        df_calendar.loc[mask, 'RodadaMarcada'] = 'ProximaRodada'

    # Converter a coluna Data de volta para o formato original
    df_calendar['Data'] = df_calendar['Data'].dt.strftime('%d/%m/%Y')

    # Fazer o append (acrescentar as linhas de df_results em df_calendar)
    df_appended = pd.concat([df_calendar, df_results], ignore_index=True)

    # Adicionar as colunas Times_Partidas e DataHora depois de juntar as tabelas
    df_appended['Times_Partidas'] = df_appended['time_casa'] + ' x ' + df_appended['time_visitante']
    df_appended['DataHora'] = pd.to_datetime(df_appended['Data'] + ' ' + df_appended['Hora'], format='%d/%m/%Y %H:%M').dt.strftime('%d/%m/%Y %H:%M:%S')

    # Carregar e normalizar JSON de estatísticas
    with open(path_stats, 'r', encoding='utf-8') as f:
        stats_raw = json.load(f)

    df_stats = pd.json_normalize(stats_raw, sep='__')

    # Corrigir id no df_stats também
    df_stats['id'] = df_stats['id'].astype(str).str.replace(r'(Avanca_na_competicao_|Vencedor_)', '', regex=True)

    # Mesclar o DataFrame resultante (df_appended) com df_stats pela coluna 'id'
    df_merged = df_appended.merge(df_stats, on='id', how='outer')

    # Renomear os nomes dos campeonatos
    rename_campeonatos = {
        "Liga Profissional Saudita": "Liga Saudita",
        "Copa Libertadores": "Libertadores",
        "Brasileirão Série B Superbet": "Brasileirão B",
        "Brasileirão Betano": "Brasileirão A",
        "Copa Betano do Brasil": "Copa do Brasil",
        "Copa Sul-Americana": "Sul-Americana",
        "Liga dos Campeões": "UEFA"
    }
    df_merged['Campeonato'] = df_merged['Campeonato'].replace(rename_campeonatos)

    # Colunas a serem removidas
    cols_to_remove = [
        'Gols esperados (xG)__home_team', 'Gols esperados (xG)__away_team',
        'Posse de bola__home_team', 'Posse de bola__away_team',
        'Passes__home_team', 'Passes__away_team',
        'xG das finalizações no alvo (xGOT)__home_team', 'xG das finalizações no alvo (xGOT)__away_team',
        'Finalizações de fora da área__home_team', 'Finalizações de fora da área__away_team',
        'Cruzamentos__away_team', 'Passes no terço final__away_team',
        'Passes no terço final__home_team', 'Bolas longas__away_team',
        'Bolas longas__home_team', 'Faltas Cobradas__away_team',
        'Toques dentro da área adversária__away_team', 'Rebatidas__away_team',
        'Rebatidas__home_team', 'Passes longos__away_team',
        'Passes longos__home_team', 'Passes em profundidade certos__away_team',
        'Passes em profundidade certos__home_team', 'Erros que resultaram em gol__away_team',
        'Erros que resultaram em gol__home_team', 'Erros que resultaram em finalização__away_team',
        'Erros que resultaram em finalização__home_team', 'Gols de cabeça__away_team',
        'Gols de cabeça__home_team', 'Gols evitados__away_team',
        'Gols evitados__home_team', 'xGOT enfrentado__away_team',
        'xGOT enfrentado__home_team', 'Defesas do goleiro__home_team',
        'Bolas afastadas__home_team', 'Bolas afastadas__away_team',
        'Interceptações__home_team', 'Interceptações__away_team',
        'Erros que levaram a chute__home_team', 'Erros que levaram a chute__away_team',
        'Erros que levaram a gol__home_team', 'Erros que levaram a gol__away_team',
        'Finalizações de dentro da área__home_team', 'Finalizações de dentro da área__away_team',
        'Bolas na trave__home_team', 'Bolas na trave__away_team',
        'Toques dentro da área adversária__home_team', 'Passes em profundidade__home_team',
        'Passes em profundidade__away_team', 'Desarmes__away_team', 'Desarmes__home_team',
        'Finalizações para fora__home_team', 'Finalizações para fora__away_team',
        'Faltas Cobradas__home_team', 'Cruzamentos__home_team',
        'Assistências esperadas (xA)__home_team', 'Assistências esperadas (xA)__away_team',
        'Duelos ganhos__home_team', 'Duelos ganhos__away_team',
        'Laterais Cobrados__away_team', 'Defesas do goleiro__away_team',
        'Laterais Cobrados__home_team', 'Finalizações bloqueadas__away_team',
        'Finalizações bloqueadas__home_team'
    ]

    # Remover as colunas especificadas
    df_merged.drop(columns=cols_to_remove, inplace=True, errors='ignore')

    # Caminho de saída para o arquivo CSV
    output_path = r'C:\Users\diogo\Documents\projects\projeto_pessoal\Webscrapping_futebol\data\gold\match_consolidado.csv'

    # Salvar o DataFrame como CSV
    df_merged.to_csv(output_path, index=False, encoding='utf-8')

    print(f"Arquivo CSV salvo em: {output_path}")