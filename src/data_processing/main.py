import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data_processing.incremental.get_incremental_results import carga_incremental_results
from src.data_processing.carga_bruta.get_all_data_calender import carga_calendario
from src.data_processing.carga_bruta.get_all_urls_results import coletar_urls_estatisticas
from src.data_processing.incremental.get_incremental_statistics import coletar_estatisticas_partidas_incremental
from src.data_processing.upsert.upsert_results import upsert_results
from src.data_processing.upsert.upsert_statistics import upsert_statistics
from src.data_processing.upsert.upsert_calender import upsert_calender
from src.data_processing.upsert.consolidartabelas import ConsolidarTabelas

path_calender = "data/last_update"


def main():
    inicio = time.time()

    print("Iniciando carga das rodadas finalizadas, dados serão inseridos na camada staging")
    carga_incremental_results()

    print("Aguardando 10 segundos antes de iniciar a carga do endpoint calendario")
    time.sleep(10)
    carga_calendario()

    print(f'Aguardando 10 segundos antes de coletar as urls das estatisticas')
    time.sleep(10)
    coletar_urls_estatisticas()

    print(f'Aguardando 10 segundos antes de atualizar as estatisticas das rodadas finalizadas, dados serão inseridos na camada staging')
    time.sleep(10)
    coletar_estatisticas_partidas_incremental()

    print(f'Aguardando 10 segundos antes de realizar o upsert na camada silver, tabela results_consolidado')
    time.sleep(10)
    upsert_results()

    print(f'Aguardando 10 segundos antes de realizar o upsert na camada silver, tabela statistics_consolidado')
    time.sleep(10)
    upsert_statistics()

    print(f'Aguardando 10 segundos antes de realizar o upsert na camada silver, tabela calender_consolidado')
    time.sleep(10)
    upsert_calender()

    print(f'Aguardando 10 segundos para consolidar as tabelas')
    time.sleep(10)
    ConsolidarTabelas()

    fim = time.time()
    duracao = fim - inicio

    minutos = int(duracao // 60)
    segundos = int(duracao % 60)
    print(f"Processo finalizado em {minutos}m {segundos}s.")


if __name__ == "__main__":
    main()