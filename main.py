import numpy as np
import funcoes

# Carregar o arquivo npy
data = np.load('block_integer_array.npy')


# Divide o arquivo em 12 subarrays, um para cada mês
data2 = np.array_split(data, 12)

# O mês do meu aniversário é junho, como o array começa em 0, o mês de junho é o 5
mineracoesMes = data2[5]

# Divide o array de junho em 30 subarrays, um para cada dia
mineracoesDias = np.array_split(mineracoesMes, 30)

# cria um array de array que quantos blocos cada minerador minerou em cada dia
repeticoesPorDia = funcoes.cria_repeticoes_por_dia(mineracoesDias)
df = funcoes.cria_dataframe(repeticoesPorDia, 5)

# plota o gráfico, feche a janela do gráfico para continuar a execução
funcoes.plota_grafico(df)

# imprime os 5 mineradores que mais mineraram em junho
funcoes.imprime_mineradores(df, 5)

# busca o minerador que mais minerou em junho
maior_minerador = funcoes.busca_minerador_mais_poderoso(df)

# conta quantas mineracoes em sequencia o minerador mais poderoso fez
mineracoes_sequencia = funcoes.conta_mineracoes_sequencia(
    mineracoesDias, maior_minerador)

print(f'O minerador {maior_minerador} fez {
      mineracoes_sequencia} minerações em sequência.')

# faz 1000 permutações para calcular o p-value
mineracoes_sequenciais_do_maior_minerador = funcoes.teste_k_permutacoes(
    mineracoesDias, maior_minerador, 1000)

# ordena o array para calcular o p-value
mineracoes_sequenciais_do_maior_minerador.sort()

# calcula o p-value
p_value = funcoes.calcula_p_value(
    mineracoes_sequenciais_do_maior_minerador, mineracoes_sequencia)

print(f'O p-value é {p_value}')
