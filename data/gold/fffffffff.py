import pandas as pd
from datetime import datetime
from scipy.stats import poisson

# Carregar dataset
df = pd.read_csv(r'C:\Users\diogo\projects\projeto_pessoal\websrcapping_futebol\data\gold\match_consolidado.csv')
df['DataHora'] = pd.to_datetime(df['DataHora'], format='%d/%m/%Y %H:%M:%S')

# Função para calcular as previsões para um intervalo de tempo
def calcular_previsoes(df, periodo_dias):
    hoje = pd.Timestamp.now().normalize()  # Certificando-se de que a data de hoje está normalizada
    limite_data = hoje - pd.Timedelta(days=periodo_dias)

    df_recente = df[(df['StatusPartida'] == 'Partida Encerrada') & (df['DataHora'] >= limite_data)]
    previsoes = []

    for _, partida in proximas_partidas.iterrows():
        time_casa = partida['time_casa']
        time_visitante = partida['time_visitante']

        df_casa = df_recente[df_recente['time_casa'] == time_casa]
        df_visitante = df_recente[df_recente['time_visitante'] == time_visitante]

        media_gols_casa = df_casa['placar_casa'].mean()
        media_gols_sofridos_casa = df_casa['placar_visitante'].mean()
        media_gols_visitante = df_visitante['placar_visitante'].mean()
        media_gols_sofridos_visitante = df_visitante['placar_casa'].mean()

        # Gols esperados com base em médias
        gols_esperados_mandante = (media_gols_casa + media_gols_sofridos_visitante) / 2
        gols_esperados_visitante = (media_gols_visitante + media_gols_sofridos_casa) / 2

        # Distribuição conjunta de Poisson
        max_gols = 7
        probs = []
        for i in range(max_gols + 1):
            for j in range(max_gols + 1):
                prob = poisson.pmf(i, gols_esperados_mandante) * poisson.pmf(j, gols_esperados_visitante)
                probs.append({
                    'gols_casa': i,
                    'gols_fora': j,
                    'prob': prob,
                    'resultado': (
                        'Mandante' if i > j else
                        'Visitante' if j > i else
                        'Empate'
                    ),
                    'btts': i > 0 and j > 0,
                    'total_gols': i + j
                })

        df_probs = pd.DataFrame(probs)

        # Probabilidades principais
        prob_mandante = df_probs[df_probs['resultado'] == 'Mandante']['prob'].sum()
        prob_empate = df_probs[df_probs['resultado'] == 'Empate']['prob'].sum()
        prob_visitante = df_probs[df_probs['resultado'] == 'Visitante']['prob'].sum()
        prob_btts = df_probs[df_probs['btts']]['prob'].sum()

        # Over gols
        prob_mais_1_5 = df_probs[df_probs['total_gols'] > 1]['prob'].sum()
        prob_mais_2_5 = df_probs[df_probs['total_gols'] > 2]['prob'].sum()
        prob_mais_3_5 = df_probs[df_probs['total_gols'] > 3]['prob'].sum()

        previsao = {
            'Confronto': f'{time_casa} x {time_visitante}',
            'Periodo': f'Últimos {periodo_dias} dias',
            'DataHora': partida['DataHora'],
            'Gols Mandante (média)': round(media_gols_casa, 2),
            'Gols Sofridos Mandante (média)': round(media_gols_sofridos_casa, 2),
            'Gols Visitante (média)': round(media_gols_visitante, 2),
            'Gols Sofridos Visitante (média)': round(media_gols_sofridos_visitante, 2),
            'Gols Esperados Mandante': round(gols_esperados_mandante, 2),
            'Gols Esperados Visitante': round(gols_esperados_visitante, 2),
            'Prob Vitória Mandante (%)': round(prob_mandante * 100, 1),
            'Prob Empate (%)': round(prob_empate * 100, 1),
            'Prob Vitória Visitante (%)': round(prob_visitante * 100, 1),
            'Prob Ambos Marcam (BTTS) (%)': round(prob_btts * 100, 1),
            'Prob +1.5 Gols (%)': round(prob_mais_1_5 * 100, 1),
            'Prob +2.5 Gols (%)': round(prob_mais_2_5 * 100, 1),
            'Prob +3.5 Gols (%)': round(prob_mais_3_5 * 100, 1)
        }

        previsoes.append(previsao)
    
    return previsoes

# Carregar próximas partidas
proximas_partidas = df[df['RodadaMarcada'] == 'ProximaRodada'].sort_values('DataHora')

# Criar previsões para os 4 períodos
previsoes_15_dias = calcular_previsoes(df, 15)
previsoes_30_dias = calcular_previsoes(df, 30)
previsoes_45_dias = calcular_previsoes(df, 45)
previsoes_60_dias = calcular_previsoes(df, 60)

# Unir todas as previsões
todas_previsoes = previsoes_15_dias + previsoes_30_dias + previsoes_45_dias + previsoes_60_dias

# Criar DataFrame final
df_previsoes = pd.DataFrame(todas_previsoes)

# Exibir principais colunas
print("\n🔮 Previsões completas da próxima rodada:\n")
print(df_previsoes[['Confronto', 'Periodo', 'DataHora',
                    'Gols Esperados Mandante', 'Gols Esperados Visitante',
                    'Prob Vitória Mandante (%)', 'Prob Empate (%)',
                    'Prob Vitória Visitante (%)', 'Prob Ambos Marcam (BTTS) (%)',
                    'Prob +1.5 Gols (%)', 'Prob +2.5 Gols (%)', 'Prob +3.5 Gols (%)']])

# Salvar
df_previsoes.to_csv(r'C:\Users\diogo\projects\projeto_pessoal\websrcapping_futebol\data\gold\previsoes_proxima_rodada.csv', index=False)
