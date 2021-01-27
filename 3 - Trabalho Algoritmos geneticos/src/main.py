from Interface import *
from statistics import * 

def main(): 
    #Interface grafica
    screenAG = turtle.Screen()
    screenAG.bgcolor("black")
    screenAG.title("Trabalho de Implementação I")
    screenAG.setup(300, 300)

    eltism_flag = True #Não realizar o elitismo nos pais com melhores scores

    #Interface Gráfica
    wall = Wall(); final = Final(); child = Child(SQUARE_SIZE)
    wall_exist, aim_p = CreateMatrix(matrix, wall, child, final, SQUARE_SIZE)

    #Cria a Matrix_Labirinto (Numerica para Função Fitness)
    np_matrix = np.ones([len(matrix),len(matrix[0])])
    np_matrix, aim = locateWalls(np_matrix, wall_exist, aim_p)

    #População inicial
    population = Population(POPULATION_SIZE, PERCOURSE_LIMIT)
    population.createGene(POPULATION_SIZE)

    fit = population.calcFitness(np_matrix, aim, MOV_QUANTIFY)

    solution_flag = False; count_geration = 0

    while ((count_geration < GENERATION_LIMIT) and (not(solution_flag))):
        count_geration = count_geration + 1 #Contador de gerações
        population = population.newGeration(population, eltism_flag, np_matrix, aim, CROSSOVER, CUTS, GENES, SELECT_TOURNAMENT, MUTATION, MOV_QUANTIFY) #Nova Geração 
        fit = population.calcFitness(np_matrix, aim, MOV_QUANTIFY)
        child.move(int(population.getChrPos(0)), screenAG, MOV_QUANTIFY)
        child.move_to_init(aim_p[0])

        if (fit[0] == 0):
            solution_flag = True

    print('/ ***************************************** /')
    print(f'/ Geração numero: {count_geration}')
    print(f'/ Melhor solução: {bin(int(population.getChrPos(0)))} ')
    print(f'/ Media: {mean(fit)}')
    print(f'/ Resultado de Fitness: {fit[0]}')
    print('/ ***************************************** /')

if __name__ == '__main__':
    main()