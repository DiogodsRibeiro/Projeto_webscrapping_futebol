import pandas as pd
from datetime import datetime, timedelta

# Carregar dataset
df = pd.read_csv(r'C:\Users\diogo\projects\projeto_pessoal\websrcapping_futebol\data\gold\match_consolidado.csv')

# Converter DataHora para datetime
df['DataHora'] = pd.to_datetime(df['DataHora'], format='%d/%m/%Y %H:%M:%S')

# Definir data limite (últimos 45 dias)
hoje = pd.Timestamp.now().normalize()
limite_data = hoje - pd.Timedelta(days=45)

# Filtrar jogos encerrados nos últimos 45 dias
df_recente = df[(df['StatusPartida'] == 'Partida Encerrada') & (df['DataHora'] >= limite_data)]

# Filtrar próximas partidas
proximas_partidas = df[df['RodadaMarcada'] == 'ProximaRodada'].sort_values('DataHora')

# Lista para guardar previsões
previsoes = []

# Gerar previsão para cada confronto da próxima rodada
for _, partida in proximas_partidas.iterrows():
    time_casa = partida['time_casa']
    time_visitante = partida['time_visitante']

    df_casa = df_recente[df_recente['time_casa'] == time_casa]
    df_visitante = df_recente[df_recente['time_visitante'] == time_visitante]

    previsao = {
        'Confronto': f'{time_casa} x {time_visitante}',
        'DataHora': partida['DataHora'],
        'Gols Mandante': df_casa['placar_casa'].mean(),
        'Gols Sofridos Mandante': df_casa['placar_visitante'].mean(),
        'Gols Visitante': df_visitante['placar_visitante'].mean(),
        'Gols Sofridos Visitante': df_visitante['placar_casa'].mean(),
        'Escanteios Mandante': df_casa['Escanteios__home_team'].mean(),
        'Escanteios Visitante': df_visitante['Escanteios__away_team'].mean(),
        'Chutes no Gol Mandante': df_casa['Finalizações no alvo__home_team'].mean(),
        'Chutes no Gol Visitante': df_visitante['Finalizações no alvo__away_team'].mean(),
        'Cartões Amarelos Mandante': df_casa['Cartões amarelos__home_team'].mean(),
        'Cartões Amarelos Visitante': df_visitante['Cartões amarelos__away_team'].mean(),
    }

    previsoes.append(previsao)

# Criar DataFrame final
df_previsoes = pd.DataFrame(previsoes)

# Exibir previsões resumidas
print("\n🔮 Previsões baseadas nos últimos 45 dias:\n")
print(df_previsoes[['Confronto', 'DataHora', 'Gols Mandante', 'Gols Visitante']].round(2))

# Salvar se quiser
df_previsoes.to_csv(r'C:\Users\diogo\projects\projeto_pessoal\websrcapping_futebol\data\gold\previsoes_proxima_rodada.csv', index=False)
