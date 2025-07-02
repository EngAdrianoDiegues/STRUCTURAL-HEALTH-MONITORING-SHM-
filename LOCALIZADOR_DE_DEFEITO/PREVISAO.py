import numpy as np
import matplotlib.pyplot as plt
import os
import csv
import re
from colorama import init, Fore

init(autoreset=True)

# -----------------------------
# Funções para gerar dados MCD
# -----------------------------

def ler_arquivo_com_lista(caminho_arquivo):
    """Lê um arquivo de texto e retorna os dados numéricos como lista de floats."""
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    return [float(linha.strip()) for linha in linhas[1:] if linha.strip()]

def calcular_curvatura_modal(UY, h):
    """Calcula a curvatura modal usando diferenças finitas centradas."""
    curvatura = np.zeros_like(UY)
    for i in range(1, len(UY) - 1):
        curvatura[i] = (UY[i + 1] - 2 * UY[i] + UY[i - 1]) / (h ** 2)
    curvatura[0] = curvatura[1]
    curvatura[-1] = curvatura[-2]
    return curvatura

def calcular_MCD(curvatura_1, curvatura_2):
    """Calcula a MCD (diferença de curvaturas absolutas)."""
    return np.abs(np.abs(curvatura_1) - np.abs(curvatura_2))

def gerar_dados_mcd(pasta_arquivos, pasta_resultados):
    """Gera os arquivos de MCD, gráficos e CSV com base nos arquivos de entrada."""
    os.makedirs(pasta_resultados, exist_ok=True)

    s = np.linspace(0, 100, 101)
    h = 1.0  # passo (100/100)

    todas_colunas_mcd = []
    cabecalho = []

    padrao = r"VETOR_MODAL_(\d+)_(\d+\.\d+)_(\d+\.\d+)_(\d+\.\d+)\.txt"

    for nome_arquivo in os.listdir(pasta_arquivos):
        if nome_arquivo.startswith("VETOR_MODAL") and nome_arquivo.endswith(".txt"):
            match = re.match(padrao, nome_arquivo)
            if match:
                modo, loc, prof, esp = match.groups()
                caminho_arquivo_defeito = os.path.join(pasta_arquivos, nome_arquivo)
                nome_base = f"VETOR_MODAL_{modo}_0_0_0.txt"
                caminho_arquivo_sem_defeito = os.path.join(pasta_arquivos, nome_base)

                if not os.path.exists(caminho_arquivo_sem_defeito):
                    print(Fore.YELLOW + f"Arquivo sem defeito não encontrado para modo {modo}. Pulando {nome_arquivo}.")
                    continue

                try:
                    UY_sem_defeito = np.array(ler_arquivo_com_lista(caminho_arquivo_sem_defeito))
                    UY_defeito = np.array(ler_arquivo_com_lista(caminho_arquivo_defeito))

                    if len(UY_sem_defeito) != len(UY_defeito):
                        print(Fore.RED + f"Tamanhos diferentes entre arquivos: {nome_arquivo}. Ignorado.")
                        continue

                    curvatura_sem_defeito = calcular_curvatura_modal(UY_sem_defeito, h)
                    curvatura_defeito = calcular_curvatura_modal(UY_defeito, h)
                    mcd = calcular_MCD(curvatura_sem_defeito, curvatura_defeito)

                    todas_colunas_mcd.append(mcd)
                    cabecalho.append(f'MCD_{modo}_{loc}_{prof}_{esp}')

                    # Gráfico da MCD
                    plt.figure(figsize=(8, 4))
                    plt.plot(s, mcd)
                    plt.xlabel('Posição (%)')
                    plt.ylabel('MCD')
                    plt.title(f'MCD - Modo {modo} - Loc {loc} - Prof {prof} - Esp {esp}')
                    plt.grid(True)
                    plt.tight_layout()
                    plt.savefig(os.path.join(pasta_resultados, f"MCD_{modo}_{loc}_{prof}_{esp}.png"))
                    plt.close()

                except Exception as e:
                    print(Fore.RED + f"Erro ao processar {nome_arquivo}: {e}")

    # Salva banco de dados CSV
    caminho_csv_unico = os.path.join(pasta_resultados, "MCD_BANCO_DE_DADOS.csv")
    with open(caminho_csv_unico, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)
        for i in range(len(s)):
            linha = [col[i] for col in todas_colunas_mcd]
            writer.writerow(linha)

    print(Fore.GREEN + f"Arquivo CSV com MCDs salvo em: {caminho_csv_unico}")
    return caminho_csv_unico

# Defina as pastas
pasta_entrada = r"C:\Users\GVA\Desktop\VETORES_MODAIS"
pasta_saida = r"C:\Users\GVA\Desktop\MCD_RESULTADOS"

# Chamada da função

gerar_dados_mcd(pasta_entrada, pasta_saida)
