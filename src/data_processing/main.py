import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data_processing.carga_bruta.get_all_data_results import carga_incremental
from src.data_processing.carga_bruta.get_all_data_calender import carga_calendario


def main():
    inicio = time.time()

    print("Iniciando carga incremental")
    carga_incremental()

    print("Aguardando 20 segundos antes de iniciar o endpoint calendario")
    time.sleep(20)

    print("Iniciando carga do endpoint calendario")
    carga_calendario()

    fim = time.time()
    duracao = fim - inicio

    minutos = int(duracao // 60)
    segundos = int(duracao % 60)
    print(f"Processo finalizado em {minutos}m {segundos}s.")


if __name__ == "__main__":
    main()