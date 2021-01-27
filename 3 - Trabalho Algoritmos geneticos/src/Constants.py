OUTSIDE = 100 
WALL = 50
REPEAT = 15
CORRECT_ROUTE = 1

SQUARE_SIZE = 27

GENES = 24
POPULATION_SIZE = 350
MUTATION = 0.025 #gerar a variação no bit (caso seja necessario) a cada MUTATIONS dos filhos
PERCOURSE_LIMIT = 1048575	 #2^20 bits
MOV_QUANTIFY = 12 #Valor maximo de movimento antes de realizar mutaçao (se necessario)
CROSSOVER = 0.5 #Porcentagem de windividuos que irao realizar o CROSSOVER
CUTS = 2 #Numero de bits para realizar o corte (em CROSSOVER)
SELECT_TOURNAMENT = 2 #Seleciona o melhor de dois para gerar a proxima geração
GENERATION_LIMIT = 50
