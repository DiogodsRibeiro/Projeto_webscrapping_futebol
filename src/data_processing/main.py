import sys
import os
from datetime import datetime

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.data_processing.carga_bruta.get_all_data_results import carga_incremental

def main():
    escolha = input("Escolha a operação: 1 para Carga Bruta, 2 para Carga Incremental: ")

    if escolha == '1':
        print("Iniciando carga incremental...")
        carga_incremental() 
    else:
        print("Escolha inválida. Por favor, escolha 1 ou 2.")

if __name__ == "__main__":
    main()
