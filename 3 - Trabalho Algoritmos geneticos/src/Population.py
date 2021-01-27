import numpy as np
import random
from Constants import WALL, SQUARE_SIZE, POPULATION_SIZE, PERCOURSE_LIMIT, MOV_QUANTIFY, OUTSIDE, REPEAT, GENERATION_LIMIT, CROSSOVER, CUTS, GENES, SELECT_TOURNAMENT, MUTATION

class Population():
    def __init__(self, size, perc_limit):

        self.route = np.zeros([size])
        self.size = size 
        self.perc_limit = perc_limit
        self.realSize = 0
    
    def getChrPos(self, pos):
        return self.route[pos]

    def getPopulation(self):
        return self.route

    def getRealSizePop(self):
        return self.realSize

    def setChr(self, pos, routes):
        self.route[pos] = routes
        self.realSize = self.realSize + 1
        return

    def createGene(self, size):
        for i in range(size):
            self.route[i] = random.randint(0, self.perc_limit)
            self.realSize = self.realSize + 1
        return self.route

    def calcFitness(self, matrix_map, objective, mov_quantify):
        fit = []; route_map = []
        Line, Column = matrix_map.shape

        line_init, column_init = objective[0].split(',')
        line_final, column_final = objective[1].split(',')

        line_final = int(line_final)
        column_final = int(column_final)

        for i in range((self.size)):

            score = 0 #score DESTE filho
            route = int(self.route[i]) #caminho atribuido
            route_map.clear()  #penalidade

            line = int(line_init)
            col = int(column_init)
            correct = True  #verificar se esta fora da tela

            for t in range(mov_quantify):
                move = route & 0b000000000000000000000011
                route = route>>2 # deve separar o byte m significativo -> 2bits pra veficar a posicao

                if move == 0:
                    line = line + 1 #esquerda
                elif move == 1:
                    col = col + 1 #cima
                elif move == 2:
                    line = line - 1 #direita
                elif move == 3:
                    col = col - 1 #baixo

                if(line>=0 and line<Line and col>=0 and col<Column):    
                    score = score + matrix_map[line][col]
                    if(matrix_map[line][col] == WALL and correct == True):
                       correct = False
                else:
                    score = score + OUTSIDE
                    correct = False
                
                mp = f'{line}{col}'

                if (route_map.count(mp) == 1): #Procura os valores de rotas/caminho
                    score = score + REPEAT
                else:
                    route_map.append(mp)

            score = score + abs(line_final - line)
            score = score + abs(column_final - col)

            if (line_final == line and column_final == col and correct == True):
                score = 0

            fit.append(score)

        return fit

    def newGeration(self, population, eltism_flag, np_matrix, objective, crossover, cuts, sizeGenes, select_tourn, mutation, mov_quantify):
        new_pop_pos = 0
        new_pop = Population(self.size, self.perc_limit)

        #Obtem o melhor da geração anterior
        if (eltism_flag):
            new_pop.setChr(new_pop_pos, population.getChrPos(0))
            new_pop_pos = new_pop_pos + 1

        while(self.size > new_pop.getRealSizePop() ):
            #Torneio
            fathers = population.tourFunction(np_matrix, objective, select_tourn, mov_quantify)
            childs = Population(2, self.perc_limit)

            #CrossOver
            if (random.random() <= crossover):
                childs = self.crossOver(fathers.getChrPos(0), fathers.getChrPos(1), cuts, sizeGenes)
            else:
                childs.setChr(0, fathers.getChrPos(0))
                childs.setChr(1, fathers.getChrPos(1))
            
            #Seleciona a melhor child para utilziar na prox gen
            fit_childs = childs.calcFitness(np_matrix, objective, mov_quantify)
            childs.popOrder(fit_childs)

            #Mutacao
            if (random.random() <= mutation):
                child_mutate = Population(1, self.perc_limit)
                child_mutate = self.genMutation(childs.getChrPos(0), sizeGenes)
                childs.setChr(0, child_mutate.getChrPos(0))

            new_pop.setChr(new_pop_pos, childs.getChrPos(0))
            new_pop_pos = new_pop_pos + 1

        # Avalia e Ordena a nova População
        fit_new = new_pop.calcFitness(np_matrix, objective, mov_quantify)
        new_pop.popOrder(fit_new)

        return new_pop

    def tourFunction(self, np_matrix, objective, qtd_select, mov_quantify):

        tournament = Population(qtd_select, self.perc_limit)
        fathers = Population(2, self.perc_limit)

        select = []

        qtd = qtd_select
        try_out = 0

        while(qtd>0):
            selected = self.getChrPos(random.randint(0, self.size-1))
            try_out = try_out + 1
            if((select.count(selected) != 1) or (try_out>10000)):
                select.append(selected)
                qtd = qtd -1
                try_out = 0
        
        for i in range(qtd_select):
            tournament.setChr(i, select[i])

        fit_tournament = tournament.calcFitness(np_matrix, objective, mov_quantify)
        fit_tournament.sort(reverse=True)
        fathers.setChr(0, tournament.getChrPos(0))
        fathers.setChr(1, tournament.getChrPos(1))

        return fathers

    def crossOver(self, chr1, chr2, quant_cut, sizeGenes):

        childs = Population(2, self.perc_limit)
        cut_point = []; chr1Cut = []; chr2Cut = []

        #Gera os pontos de corte aleatorios 
        qtd = quant_cut
        try_out = 0
        while(qtd>0):
            point = random.randint(1, int(sizeGenes/quant_cut)+3)
            try_out = try_out + 1
            if ((((sum(cut_point) + point) < (sizeGenes-1)) and (cut_point.count(point) != 1)) or (try_out>5000)):
                cut_point.append(point)
                qtd = qtd - 1
                try_out = 0

        cut_point = sorted(cut_point,)

        masks = createMask(quant_cut, cut_point, sizeGenes)

        for i in range(quant_cut+1):
            cut = int(chr1) & masks[i]
            chr1Cut.append(cut)

        for i in range(quant_cut+1):
            cut = int(chr2) & masks[i]
            chr2Cut.append(cut)

        child1_e = 0
        child1_o = 0
        child2_e = 0
        child2_o = 0

        for i in range(quant_cut+1):
            if (i % 2) == 0:
                child1_e = child1_e + chr1Cut[i]
                child2_e = child2_e + chr2Cut[i]
            else:
                child1_o = child1_o + chr1Cut[i]
                child2_o = child2_o + chr2Cut[i]

        childs.setChr(0, (child1_e + child2_o))
        childs.setChr(1, (child2_e + child1_o))

        return childs

    def genMutation(self, chr, sizeGenes):

        mutant = Population(1, self.perc_limit)
        chrCut = []
        mask = []
        pos = random.randint(1, sizeGenes)
        thisFrame = 0 

        for t in range(pos-1):
            thisFrame = thisFrame << 2
            thisFrame = thisFrame + 3
        mask.append(thisFrame)

        thisFrame = 0 
        thisFrame = thisFrame + 3
        thisFrame = thisFrame << (2*(pos-1))
        mask.append(thisFrame)

        thisFrame = 0 
        rest = (sizeGenes - pos)
        for t in range(rest):
            thisFrame = thisFrame << 2
            thisFrame = thisFrame + 3
        thisFrame = thisFrame << (2*(pos))
        mask.append(thisFrame)

        for i in range(3):
            cut = int(chr) & mask[i]
            chrCut.append(cut) 

        chrCut[1] = chrCut[1] >> (2*(pos-1))
        mutate = 0  
        bit = 0 

        bit = chrCut[1] & 0b01
        if (bit == 0):
            mutate = mutate + 1
        chrCut[1] = chrCut[1] >> 1
        bit = chrCut[1] & 0b01
        if (bit == 0):
            mutate = mutate + 2
        
        mutate = mutate << (2*(pos-1))
        mutate = chrCut[0] + mutate + chrCut[2]

        # print('Cromossomo')
        # print(bin(int(chr)))
        # print()
        # print('Mutante')
        # print(bin(mutate))
        # print()
        mutant.setChr(0, mutate)

        return mutant

    def popOrder(self, fit):
        flag = True; fit_temp = 0; route_temp = 0

        while (flag):
            flag = False
            for i in range(len(self.route) - 1):
                if (fit[i] > fit[i+1]):
                    fit_temp = fit[i]
                    route_temp = self.route[i]

                    fit[i] = fit[i+1]
                    fit[i+1] = fit_temp

                    self.route[i] = self.route[i+1]
                    self.route[i+1] = route_temp

                    flag = True
        return fit

def createMask(quant_cut, cut_point, GENES):
    mask = []; shitf_ant = 0; shitf = 0; pos = 0  
    
    for i in range(quant_cut):
        thisFrame = 0
        shitf = 0
        pos = int(cut_point[i])

        for i in range(pos):
            thisFrame = thisFrame << 2
            thisFrame = thisFrame + 3
            shitf = shitf + 1

        thisFrame = thisFrame << (shitf_ant*2)
        shitf_ant = shitf_ant + shitf

        mask.append(thisFrame)

    pos = abs(GENES - shitf_ant)

    thisFrame = 0
    for t in range(pos):
        thisFrame = thisFrame << 2
        thisFrame = thisFrame + 3

    thisFrame = thisFrame << (shitf_ant*2)
    mask.append(thisFrame)

    #for m in mask: print(bin(int(m)))

    return mask