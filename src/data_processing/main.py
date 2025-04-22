import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data_processing.carga_bruta.get_all_data_results import carga_bruta
from src.data_processing.carga_bruta.get_all_data_calender import carga_calendario
from src.data_processing.last_update.calender import get_last_update_calender

path_calender = "data/last_update"


def main():
    inicio = time.time()

    print("Iniciando carga incremental")
    carga_bruta()

    print("Aguardando 20 segundos antes de iniciar o endpoint calendario")
    time.sleep(20)

    print("Iniciando carga do endpoint calendario")
    carga_calendario()

    print(f'Atualizando a data da ultima atualizaçáo de cada campeonato na pasta {path_calender}')
    get_last_update_calender()


    fim = time.time()
    duracao = fim - inicio

    minutos = int(duracao // 60)
    segundos = int(duracao % 60)
    print(f"Processo finalizado em {minutos}m {segundos}s.")


if __name__ == "__main__":
    main()