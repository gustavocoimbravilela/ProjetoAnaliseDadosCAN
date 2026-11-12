# Projeto Analise de Dados CAN
Projeto de análise de dados de um log bruto de CAN de um caminhão.
Link para obtenção dos dado: https://www.engr.colostate.edu/~jdaily/J1939/candata.html

Engine: PACCAR PX-7 (Cummins CM2350 ECU)

Brakes: Bendix EC-60

Transmission: Allison RDS-2000

Summary: This truck made a cross-country trip from Colorado to Michigan and back. During this trip, a CAN Logger 3 captured all the CAN traffic during the 4 days of driving. The CAN Logger 3 made many files, some were small (1KB) and others were quite large (400MB). These files were concatenated put in cronological order. The expanded file size is just under 2GB, so some smaller snippets of the trip are also available below.

Number of Messages: 37,754,838

File name(s):
2014_KW_T270_Starting_CSU090B6.zip (1,277 KB)


# Formato do log de dados

O arquivo é dividido em linhas com 3 colunas.

Exemplo: (1594704040.266404) can1 18F00E00#3C1FFFFFD59FFFFF

A primeira coluna apresenta o Unix time, sendo caracterizado pelo número de segundos que se passaram desde o dia 01/01/1970. Vamos utilizá-lo como referência de tempo das nossas análises, calculando a diferença entre pontos, saberemos quanto tempo se passou desde o início das gravações.

Na segunda coluna consta o canal da CAN em que foram transmitidos os dados. Ex: can1

Já na terceira coluna, podemos dividir os dados em dois blocos, primeiros temos o CAN ID, em hexadecimal, caracterizado por 29 bits e 8 algarismos que representam os 8 bytes do campo, sendo que um conjunto de dois números hexadecimais representam 1 byte. Podemos dividir esse campo em 3 grandes grupos, o grupo de prioridades, o Parameter Group Number (PGN) e o Source Address (SA).

Como os bytes de prioridade e o SA podem variar de aplicação para aplicação. O que deve ser captado pelo 
DBC é o SA, que é o mesmo para qualquer aplicação sob a J1939.

O DBC estava representando o PGN ET1 da seguinte forma:

BO_ 2566844158 ET1: 8 Vector__XXX
SG_ EngCoolantTemp : 0|8@1+ (0.03125,-273) [-273|-265.03125] "deg C"
SG_ EngFuelTemp1      : 8|8@1+   (1,-40)        [-40|210]  "deg C"
SG_ EngIntercoolerTemp: 48|8@1+  (1,-40)        [-40|210]  "deg C"
SG_ EngOilTemp1       : 16|16@1+ (0.03125,-273) [-273|1734.96875] "deg C"
SG_ EngCoolantTemp    : 0|8@1+   (0.03125,-273) [-273|-265.03125] "deg C"

Porém, ao analisar os tamanhos das informações carregadas na mensagem e as escalas de temperaturas, pode-se perceber que a mensagem SG_ EngCoolantTemp possui 8 bits e está com o fator e o offset de uma mensagem de 16 bits (0.03125,-273), resultando e uma escala absurda para leituras de um sensor de temperatura do líquido de arrefecimento [-273|-265.03125], dessa forma, ao utilizar os parâmetros das outras temperaturas que também possuem 8 bits, os valores passam a ser muito mais plausíveis [-40|210].

Ao decodificar a mensagem 18FEEE00#80FFFFFFFFFFFFFF utilizando-se os valores definidos inicialmente para o DBC, o valor de temperatura de coolant calculado foi de -269°C, o que se mostra um valor incompatível com uma leitura de um sensor de temperatura de coolant. Utilizando-se os valores corretos de fator e offset, o valor calculado passou para 88°C, uma temperatura muito mais coerente para a situação analisada (um caminhão com o motor que já funcionava a um tempo).