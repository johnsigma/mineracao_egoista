import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def cria_repeticoes_por_dia(mineracoesDias):
    repeticoesPorDia = []

    for dia in mineracoesDias:
        repeticoesPorDia.append(np.bincount(dia))

    return repeticoesPorDia


def cria_dataframe(repeticoesPorDia, k_maiores=5):
    df = pd.DataFrame(repeticoesPorDia).fillna(0).astype(int)
    df.columns = [f'Minerador {i}' for i in range(df.shape[1])]
    df.index.name = 'Dia'

    soma_mineradores = df.sum(axis=0)

    maiores_mineradores = soma_mineradores.nlargest(k_maiores).index

    # Agrupar os demais mineradores em "outros"
    df['Outros'] = df.loc[:, ~df.columns.isin(maiores_mineradores)].sum(axis=1)
    df = df[maiores_mineradores.tolist() + ['Outros']]

    return df


def plota_grafico(df):

    # Plotar o gráfico
    df.plot(kind='bar', stacked=True, figsize=(15, 8))
    plt.xlabel('Dia')
    plt.ylabel('Blocos Minerados')
    plt.title('Poder Computacional dos Mineradores por Dia')
    plt.legend(title='Minerador', bbox_to_anchor=(1, 1), loc='upper left')
    plt.show()


def busca_minerador_mais_poderoso(df):
    soma_mineradores = df.loc[:, df.columns != 'Outros'].sum(axis=0)
    maior_minerador = soma_mineradores.idxmax().split()[-1]
    return maior_minerador


def busca_k_maiores_mineradores(df, k_maiores=5):
    soma_mineradores = df.loc[:, df.columns != 'Outros'].sum(axis=0)
    k_maiores_mineradores = soma_mineradores.nlargest(k_maiores)
    return k_maiores_mineradores


def imprime_mineradores(df, k_maiores=5):

    maior_minerador = busca_minerador_mais_poderoso(df)
    k_maiores_mineradores = busca_k_maiores_mineradores(df, k_maiores)

    print(f'O minerador com maior poder computacional é o {maior_minerador}.')
    print(f'Os {k_maiores} mineradores com maior poder computacional são:')
    for i, (minerador, poder) in enumerate(k_maiores_mineradores.items(), 1):
        print(f'{i}. {minerador} com {poder} blocos minerados.')


def conta_mineracoes_sequencia(mineracoesDias, maior_minerador):
    mineracoes_sequencia = 0
    mineracao_aux = -1

    for dia in mineracoesDias:

        for j in range(len(dia)):

            if mineracao_aux != -1:
                if mineracao_aux == dia[j] and mineracao_aux == maior_minerador:
                    mineracoes_sequencia += 1
                mineracao_aux = -1

            mineracaoAtual = str(dia[j])

            mineracaoProxima = str(dia[j+1]) if j+1 < len(dia) else None

            if mineracaoProxima == None:
                mineracao_aux = mineracaoAtual
                break

            if mineracaoAtual == maior_minerador and mineracaoProxima == mineracaoAtual:
                mineracoes_sequencia += 1

    return mineracoes_sequencia


def verifica_permutacao(array1, array2):
    # Verificar se os arrays têm o mesmo tamanho
    if len(array1) != len(array2):
        return False

    # Verificar se os arrays têm os mesmos elementos
    elementos_unicos_array1, contagens_array1 = np.unique(
        array1, return_counts=True)
    elementos_unicos_array2, contagens_array2 = np.unique(
        array2, return_counts=True)

    if not np.array_equal(elementos_unicos_array1, elementos_unicos_array2):
        return False

    # Verificar se as contagens de cada elemento são iguais
    if not np.array_equal(contagens_array1, contagens_array2):
        return False

    return True


def criar_novo_array_permutado(data):

    novo_array = []

    for dia in data:
        novo_dia = np.random.permutation(dia)
        novo_array.append(novo_dia)

    return novo_array


def teste_k_permutacoes(data, maior_minerador, k=1000):
    mineracoes_sequencia = []
    for _ in range(k):
        novo_array = criar_novo_array_permutado(data)
        mineracoes = conta_mineracoes_sequencia(
            novo_array, maior_minerador)
        mineracoes_sequencia.append(mineracoes)

    return mineracoes_sequencia


def calcula_p_value(mineracoes_sequenciais_do_maior_minerador, mineracoes_sequencia):
    p_value = -1

    for i in range(len(mineracoes_sequenciais_do_maior_minerador)):
        numero_sequencias = mineracoes_sequenciais_do_maior_minerador[i]

        if str(numero_sequencias) == str(mineracoes_sequencia):

            p_value = (i+1)/len(mineracoes_sequenciais_do_maior_minerador)
            break

    return p_value
