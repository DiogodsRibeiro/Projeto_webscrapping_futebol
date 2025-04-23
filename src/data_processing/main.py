import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data_processing.carga_bruta.get_all_data_results import carga_bruta
from src.data_processing.carga_bruta.get_all_data_calender import carga_calendario
from src.data_processing.last_update.calender import get_last_update_calender
from src.data_processing.carga_bruta.get_all_data_statistics import coletar_estatisticas_partidas
from src.data_processing.carga_bruta.get_all_urls import coletar_urls_estatisticas

path_calender = "data/last_update"


def main():
    inicio = time.time()

    print("Iniciando carga das rodadas finalizadas")
    carga_bruta()

    print("Aguardando 10 segundos antes de iniciar a carga do endpoint calendario")
    time.sleep(10)
    carga_calendario()

    print(f'Aguardando 10 segundos antes de atualizar a data da ultima atualizaçáo de cada campeonato na pasta {path_calender}')
    time.sleep(10)
    get_last_update_calender()

    print(f'Aguardando 10 segundos antes de coletar as urls das estatisticas')
    time.sleep(10)
    coletar_urls_estatisticas()

    print(f'Aguardando 10 segundos antes de atualizar as estatisticas das rodadas')
    time.sleep(10)
    coletar_estatisticas_partidas()

    fim = time.time()
    duracao = fim - inicio

    minutos = int(duracao // 60)
    segundos = int(duracao % 60)
    print(f"Processo finalizado em {minutos}m {segundos}s.")


if __name__ == "__main__":
    main()