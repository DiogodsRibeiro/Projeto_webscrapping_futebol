# Webscraping de partidas de futebol

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Selenium](https://img.shields.io/badge/Selenium-4.0+-green.svg)
![Pandas](https://img.shields.io/badge/Pandas-Latest-red.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

[Instalação](#-instalação) • [Como Usar](#-como-usar) • [Estrutura](#-estrutura) • [Exemplos](#-exemplos)

</div>

---

## Sobre o Projeto

Este 'e um projeto de web scraping que coleta dados de futebol, incluindo:

- 📅 **Calendário**: Próximas partidas de múltiplos campeonatos
- 📊 **Resultados**: Placares e informações de jogos encerrados
- 📈 **Estatísticas**: Dados detalhados como posse de bola, chutes, cartões, etc.

### Principais Características

- ✅ **Coleta Incremental**: Atualiza apenas dados novos, economizando tempo
- ✅ **Multi-campeonatos**: Suporta 28+ ligas nacionais e internacionais
- ✅ **Pipeline Automatizado**: Execução completa com um único comando
- ✅ **Arquitetura Medalhão**: Organização em camadas (Raw → Staging → Silver → Gold)
- ✅ **Tratamento de Erros**: Sistema robusto com retry automático
- ✅ **Logs Detalhados**: Acompanhamento completo do processo

## Campeonatos que eu considerei para o projeto.

<summary>No momento esses sao os campeonatos que eu trouxe</summary>

### América do Sul
- 🇧🇷 Brasileirão Série A
- 🇧🇷 Brasileirão Série B
- 🇧🇷 Copa do Brasil
- 🇦🇷 Primera División Argentina
- 🏆 Copa Libertadores
- 🏆 Copa Sul-Americana

### Europa
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Championship
- 🇪🇸 La Liga
- 🇮🇹 Serie A
- 🇩🇪 Bundesliga
- 🇫🇷 Ligue 1
- 🇵🇹 Liga Portugal
- 🇳🇱 Eredivisie
- 🏆 UEFA Champions League
- 🏆 UEFA Europa League

### Outros
- 🇸🇦 Liga Saudita
- 🇨🇳 Super Liga Chinesa
- 🇹🇷 Süper Lig

</details>

## 🚀 Instalação

### Pré-requisitos

- Python 3.11+
- Google Chrome
- ChromeDriver

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/DiogodsRibeiro/Projeto_webscrapping_futebol.git
cd Projeto_webscrapping_futebol

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Baixe o ChromeDriver
# https://chromedriver.chromium.org/
# Coloque no PATH do sistema
```

## 💻 Como Usar

### Execução Completa (Recomendado)

```bash
python main.py
```

Isso executará todo o pipeline:
1. Coleta resultados recentes
2. Atualiza calendário
3. Busca estatísticas detalhadas
4. Consolida todos os dados
5. Gera arquivo final CSV

### Execução Individual

```python
# Coletar apenas calendário
from get_calendar import coletar_calendario
coletar_calendario()

# Coletar apenas resultados (últimos 4 dias)
from get_results import coletar_resultados
coletar_resultados(incremental=True, dias_atras=4)

# Coletar apenas estatísticas
from get_statistics import coletar_urls_estatisticas, coletar_estatisticas
urls = coletar_urls_estatisticas(dias_atras=2)
coletar_estatisticas(urls)
```

## 📁 Estrutura do Projeto

```
projeto/
│
├── data/                    # Dados coletados
│   ├── raw/                # Dados brutos
│   │   ├── calendar/       # Calendários por campeonato
│   │   ├── results/        # Resultados por campeonato
│   │   └── statistics/     # Estatísticas detalhadas
│   │
│   ├── staging/            # Dados temporários
│   │   └── results/        # Resultados incrementais
│   │
│   ├── silver/             # Dados consolidados
│   │   ├── calendar_consolidado.json
│   │   ├── results_consolidado.json
│   │   └── statistics_consolidado.json
│   │
│   └── gold/              # Dados finais
│       └── match_consolidado.csv
│
├── logs/                  # Arquivos de log
├── get_calendar.py        # Coleta calendário
├── get_results.py         # Coleta resultados
├── get_statistics.py      # Coleta estatísticas
├── upsert.py             # Atualiza dados consolidados
├── consolidar_tabelas.py  # Gera tabela final
├── utils.py              # Funções auxiliares
└── main.py               # Script principal
```

## 📊 Estrutura dos Dados

### Arquivo Final: `match_consolidado.csv`

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| `id` | Identificador único | "Flamengo_vs_Palmeiras_15012024" |
| `StatusPartida` | Status do jogo | "Partida Encerrada" |
| `Campeonato` | Nome do campeonato | "Brasileirão A" |
| `Data` | Data da partida | "15/01/2024" |
| `Times_Partidas` | Times formatados | "Flamengo x Palmeiras" |
| `placar_casa` | Gols time casa | 2 |
| `placar_visitante` | Gols time visitante | 1 |
| `Posse de bola__home_team` | Posse time casa | "58%" |
| `Chutes__home_team` | Total de chutes | 15 |

## 🔧 Configuração Avançada

### Adicionar Novo Campeonato

Edite o arquivo `data/json/all_url.json`:

```json
{
    "urls": [
        "https://www.flashscore.com.br/futebol/pais/liga/{endpoint}/",
        // ... outras URLs
    ]
}
```

### Ajustar Período de Coleta

No arquivo `main.py`, ajuste os parâmetros:

```python
# Coleta resultados dos últimos X dias
coletar_resultados(incremental=True, dias_atras=7)

# Coleta estatísticas dos últimos X dias
coletar_urls_estatisticas(dias_atras=3)
```

## 📈 Exemplos de Uso

### Análise com Pandas

```python
import pandas as pd

# Carrega dados
df = pd.read_csv('data/gold/match_consolidado.csv')

# Top 5 times com mais vitórias em casa
vitorias_casa = df[df['placar_casa'] > df['placar_visitante']]
top_mandantes = vitorias_casa['time_casa'].value_counts().head()

# Média de gols por campeonato
df['total_gols'] = df['placar_casa'] + df['placar_visitante']
media_gols = df.groupby('Campeonato')['total_gols'].mean()
```

### Visualização

```python
import matplotlib.pyplot as plt

# Gols por rodada no Brasileirão
brasileiro = df[df['Campeonato'] == 'Brasileirão A']
gols_rodada = brasileiro.groupby('Rodada')['total_gols'].sum()

plt.figure(figsize=(12, 6))
gols_rodada.plot(kind='bar')
plt.title('Gols por Rodada - Brasileirão')
plt.xlabel('Rodada')
plt.ylabel('Total de Gols')
plt.show()
```

## 🐛 Solução de Problemas

### Erro: "Chrome driver not found"
```bash
# Instale o webdriver-manager
pip install webdriver-manager
```

### Timeout ao carregar página
Aumente o timeout em `utils.py`:
```python
def esperar_elemento(driver, class_name, timeout=30):  # Aumentado para 30s
```

### Dados não atualizando
1. Verifique os logs em `logs/`
2. Delete os arquivos em `data/staging/`
3. Execute novamente

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request


## 👨‍💻 Autor

**Diogo Ribeiro**

- GitHub: [@DiogodsRibeiro](https://github.com/DiogodsRibeiro)
- Email: diogodsribeiro@gmail.com

---

<div align="center">

Feito com ❤️ e ☕ por Diogo Ribeiro

</div>
