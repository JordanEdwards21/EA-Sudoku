import random #import libary to help produce random solutions
import numpy #import libary to help matrix format 
from copy import deepcopy #import deepcopy to help make copys

class population:#class population to help us generate population
    def __init__(self, size):
        self.size = size#initial conditions
        self.children = []#reset children

    def seed(self, nc, grid):#class function to populate the population
        self.children = []#reset children
        for x in range(0,nc): #repeat process for the number of children needed in the population
            guide = numpy.zeros(Nd, dtype =list) #create an empty guide
            for y in range(Nd): #for every row
                temp=[1,2,3,4,5,6,7,8,9] #temp value
                for z in range(Nd): #for every 
                    if grid[y][z] != 0: # if this location is a given value
                        temp.remove(grid[y][z]) #remove this value from the temp value
                    guide[y] = temp #store the available values in the row for the guide to use
            g=child()#create an instance of the class child which is a proposed solution
            for i in range(0,Nd):#for every row 
                for j in range(0,Nd): #for every columm
                    if grid[i][j] != 0: #if the value is given 
                        g.values[i][j] = grid[i][j] # store the element value as given value
                    else:
                        if len(guide[i])==1: # empty the last element of the guide
                            g.values[i][j]=guide[i][0] #add the last element into child value
                        else:
                            a = random.randint(0,len(guide[i])-1) #pick a random element in row guide
                            g.values[i][j] = guide[i][a] # add that element into the grid
                            del guide[i][a] #remove placed value from the guide
            g.fitnessfunction() #call fitness function to calculate child fitness
            self.children.append(g) #add completed child to population 

            ###############################################
            # Same code but for sub blocks
            #guide = numpy.zeros((3, 3), dtype=list)
            #for i in range(0,3):
            #    for j in range(0,3):
            #       temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            #       for y in range(0,3):
            #              for z in range(0,3):
            #                  if grid[y+(3*i)][z+(3*j)] != 0:
            #                       temp.remove(grid[y+(3*i)][z+(3*j)])
            #        guide[i][j] = temp
            #g = child()
            #for i in range(0,3):
            #   for j in range(0,3):
            #       for x in range(0,3):
            #           for y in range(0,3):
            #               if grid[x+(3*i)][y+(3*j)] != 0:
            #                   g.values[x+(3*i)][y+(3*j)] = grid[x+(3*i)][y+(3*j)]
            #               else:
            #                   if len(guide[i][j]) ==1:
            #                       g.values[x+(3*i)][y+(3*j)] = guide[i][j][0]
            #                       del guide[i][j][0]
            #                   else:
            #                       a = random.randint(0, len(guide[i][j])-1)              
            #                       g.values[x+(3*i)][y+(3*j)] = guide[i][j][a]
            #                       del guide[i][j][a]
            #g.fitnessfunction()
            #self.children.append(g)

    def sort(self): #function that sorts population
        self.children.sort(reverse=False, key=myFunc) #sorts the popultion based upon a key function which it based upon fitness

    def selectionprogress(self, Nc): #tournament selection progress function
        a = random.randint(0, Nc-1) #select fighter 1 from breeding pool
        b = random.randint(0, Nc-1) #select fighter 2 from breedinh pool
        c1 = self.children[a] #calling the values of fighter 1
        c2 = self.children[b] #calling the values of fighter 2
        f1 = c1.fitness #storing fitness of fighter 1 
        f2 = c2.fitness #storing fitness of fight 2
        # Find the fittest and the weakest.
        if(f1 > f2): #fighter one is stronger
            fittest = c1 
            weakest = c2
        else: #fighter two is stronger or fighters are equal
            fittest = c2
            weakest = c1

        selection_rate = 85 #threshold value
        r = random.randint(0, 100) #randomise fight
        if(r < selection_rate): #stronger fighter won 
            return fittest #return to be used as a parent 
        else:#weaker fighter won 
            return weakest #retun to be used as a parent 


class child: #class child used to emulate proposed solutions 
    def __init__(self):
        self.values = numpy.zeros((Nd, Nd), dtype=int)
        self.fitness = 0 #inital condiions

    def fitnessfinal(self):#final fitness function
        self.fitness = 0
        a=self.checkrows() #same as fitness function
        b=self.checkcolumms()
        c=self.checkboxs()
        print(a)
        print(b) #expect we output eack individual fitness
        print(c)
        self.fitness = int(a+b+c)

    def fitnessfunction(self):
        self.fitness = 0 #reset fitness
        a=self.checkrows() #check rows for conflicts
        b=self.checkcolumms()#check columms for conflicts
        c=self.checkboxs()  #check subgrid for conflicts
        self.fitness = int(a+b+c) #total the conflict for total fitness score 
    
    def checkrows(self):#function to check all rows for conflicts
        rowconflicts = 0 #reset counter
        for row in range(Nd):#for every row
            counter = numpy.zeros(Nd) # reset counter
            for columm in range(Nd): #for every elemnt in a given row
                counter[self.values[row][columm]-1] += 1 #record institance of that number 
            for x in range(len(counter)): #for every number 
                if counter[x] > 1: #if occurance that row is more than one
                    rowconflicts += (counter[x] -1) #record coflicts
        return rowconflicts #return total conflicts

    def checkcolumms(self): #function to check all columms for conflicts
        colummconflicts = 0 #reset counter
        for columm in range(Nd): #for every columm
            counter = numpy.zeros(Nd) #reset counte
            for row in range(Nd): # for every element in that give colum 
                counter[self.values[row][columm]-1] += 1 #record occurance of that number
            for x in range(len(counter)): # for every number 
                if counter[x] > 1: #if occurance that columm is more than one
                    colummconflicts += (counter[x] -1)  #record conflicts
        return colummconflicts #return total conflicts
    
    def checkboxs(self):
        blockconflicts =0 
        for i in range(0,Nd,3): #for each subgrid 
            for j in range(0,Nd,3):
                boxcount=numpy.zeros(Nd) #reset counter
                boxcount[self.values[i][j]-1] += 1
                boxcount[self.values[i+1][j]-1] += 1
                boxcount[self.values[i+2][j]-1] += 1

                boxcount[self.values[i][j+1]-1] += 1
                boxcount[self.values[i+1][j+1]-1] += 1 #record occurance of numbers in every element of that subgrid
                boxcount[self.values[i+2][j+1]-1] += 1

                boxcount[self.values[i][j+2]-1] += 1
                boxcount[self.values[i+1][j+2]-1] += 1
                boxcount[self.values[i+2][j+2]-1] += 1
                
                for x in range(len(boxcount)): #for every number
                    if boxcount[x] > 1: #if occurance in that sub grid  is more than one
                        blockconflicts += (boxcount[x]-1)    #record conflicts 
        
        return blockconflicts#return total conflicts

def crossover(parent1, parent2): #crossover function for two given parents
    a = numpy.zeros((Nd, Nd) , dtype =int)#set up child 1
    b = numpy.zeros((Nd, Nd) , dtype =int)#set up child 2
    choice = random.randint(0,2) # random choice of  crossover function 
     
        # splice method
    if choice == 0: 
        for x in range(Nd): #for every row
            cross = random.randint(0, 9) #choice random row to cut the parents   
            for y in range(Nd): #for every element in columm
                if x < cross: # above cut point 
                    a[x][y] = parent1[x][y] #populate child 1 with parent 1 elements
                    b[x][y] = parent2[x][y] #populate child 2 with parent 2 elements
                else: #above cut point 
                    a[x][y] = parent2[x][y] #populate child 1 with parent 2 elements
                    b[x][y] = (parent1[x][y]) #populate child 2 with parent 1 elements
        
        # rand rows method
    elif choice == 1:
            for x in range(Nd):#for every row    
                #choice random parent 
                cross = random.randint(0, 1)   
                for y in range(Nd): #for every element in row 
                    if cross == 0: #parent 1 is chosen 
                        a[x][y] = parent1[x][y] #populate child 1 with parent 1 elements 
                        b[x][y] = parent2[x][y] #populate child 2 with parent 2 elements
                    else: #parent 2 is chosen
                        a[x][y] = parent2[x][y] #populate child 1 with parent 2 elements
                        b[x][y] = (parent1[x][y]) #populate child 2 with parent 1 elements
        # rows of 3
    elif choice == 2:        
        for x in range(0, Nd,3): #for every 3 rows 
            cross = random.randint(0, 1)   #randomly chose parent 
            for y in range(Nd):# for every element in rows 
                if cross == 0:#parent 1 is dominant
                        a[x][y] = parent1[x][y]
                        b[x][y] = parent2[x][y]
                        a[x+1][y] = parent1[x+1][y]
                        b[x+1][y] = parent2[x+1][y]     #populate child 1 with 3 rows of parent 1 elements
                        a[x+2][y] = parent1[x+2][y]     #populate child 2 with 3 rows of parent 2 elements
                        b[x+2][y] = parent2[x+2][y]

                else: #parent 2 is dominant 
                        a[x][y] = parent2[x][y]
                        b[x][y] = (parent1[x][y])          
                        a[x+1][y] = parent2[x+1][y]      #populate child 1 with 3 rows of parent 2 elements
                        b[x+1][y] = parent1[x+1][y]     #populate child 2 with 3 rows of parent 1 elementss
                        a[x+2][y] = parent2[x+2][y]
                        b[x+2][y] = parent1[x+2][y]
        
    return a , b #return populated offspring

def myFunc(e):#function to help sort fitness
    return e.fitness #key is the fitness value

def mutate(values, given): #function mutates a child with respect to given values 
    mutationrate = 80 #set threshold
    row = random.randint(0, 8)  #select random row
    a = random.randint(0, 8) #select element 1 in row
    b = random.randint(0, 8) #select element 2 in row
    while (values[row][a] == given[row][a]):#if element 1 is given
        a = random.randint(0, 8) #try again until we find a non given value
    while (values[row][b] == given[row][b]):# if element 2 is given
        b = random.randint(0, 8) #try again until we find a non given value
    mutatechance = random.randint(0, 100) # generate the mutatation chance 
    if mutatechance > mutationrate: # if mutation is succesfull
            temp1 = values[row][a]
            temp2 = values[row][b] # swap element 1 and 2
            values[row][a] = temp2
            values[row][b] = temp1
    
    #############################################
    # Mutation in Sub- grids
    # mutationrate = 80
    #for i in range(3):
    #    for j in range(3):
    #        a = random.randint(0, 2)
    #        b = random.randint(0, 2)
    #        c = random.randint(0, 2)
    #        d = random.randint(0, 2)
    #       
    #        while (values[a+(3*i)][b+(3*j)] == given[a+(3*i)][+(3*i)]):
    #            a = random.randint(0, 2)
    #            b = random.randint(0, 2)
    #        while (values[c+(3*i)][d+(3*j)] == given[c+(3*i)][d+(3*i)]):
    #            c = random.randint(0, 2)
    #            d = random.randint(0, 2)
    #        mutatechance = random.randint(0, 100)
    #        if mutatechance > mutationrate:
    #            temp1 = values[a+(3*i)][b+(3*j)]
    #            temp2 = values[c+(3*i)][d+(3*j)]
    #            values[a+(3*i)][b+(3*j)] = temp2
    #            values[c+(3*i)][d+(3*j)] = temp1
    #############################################   
    #Mutation of whole rolls
    # mutationrate = 80
    #mutatechance = random.randint(0,100)
    #if mutatechance > mutationrate:
    #    help=[]
    #    a = random.randint(0,8)
    #    for columm in range(Nd):
    #       temp =[1,2,3,4,5,6,7,8,9]
    #        if(values[a][columm] == given[a][columm]):
    #            temp.remove(values[a][columm])
    #        else:
    #            values[a][columm]=0
    #        help.append(temp)
    #    for reshuffle in range(Nd):
    #        if values[a][reshuffle]==0:
    #            b = random.randint(0,len(temp)-1)
    #            values[a][reshuffle]=help[reshuffle][b]
    #            help[reshuffle].remove(values[a][reshuffle]) 
    #################################################
    return values # return the child 


class sudoku: # main class
    def __init__(self, size):
        self.size = size #initial conditions
    def accepct(self): #function to set up problme
        print("Welcome to  Evolutionary Algorithm for Sudoku") #instructions
        gridnumber = int(input("Which Grid would you like to solve? 1,2 or 3 ")) # get the input of the desired grid that the user wants to solve
        valid = False #set acceptance critea
        while valid == False: #while no grid has been loaded
            if gridnumber==1: #if grid 1 is selected
                valid = True #valid grid has been picked
                f = open("Grid1.ss", "r") #open grid 1
            elif gridnumber==2: #if grid 2 is selected
                valid = True #valid grid has been picked
                f = open("Grid2.ss", "r") #open grid 1
            elif gridnumber == 3: #if grid 3 is selected
                valid = True #valid grid has been picked
                f = open("Grid3.ss", "r") #open grid 3
            else: #if no valid grid was picked 
                print("Please enter a valid number 1, 2 or 3")
                gridnumber = int(input("Which Grid would you like to solve? 1,2 or 3 ")) #prompyt another selection 
        # Import and format grid
        #----------------------------------------#
        g = f.readlines() #read in the selected grid 
        g = [word.replace('.', '0') for word in g] #replace all dots with 0s
        g = [word.replace('\n', '') for word in g]#get rid of any newlines 
        del g[3] # delete unneccessary row
        del g[6] # delete unneccessary row
        g = [word.replace('!', '') for word in g] #get rid of any useless !s
        global grid #global grid variable
        grid = [] #reset grid 
        for x in range(9): #for every row 
            grid.append([int(a) for a in g[x]]) #populate the grid row with all integers in that given row 
        print("Which population would you like to use?")  #instructions
        popnumber = int(input("10 (1), 100 (2), 1,000 (3) or 10,000 (4)")) #prompt the user to select a population size
        global Nc #global number of candiates in population
        Nc=0 #reset 
        valid = False #set acceptance critea
        while valid == False: #while a valid population hasnt been selected loop
            if popnumber==1: # #if pop size 1 is selected
                valid = True #valid pop size has been picked
                Nc = 10 #pop size of 10 has been selected 
            elif popnumber==2: #if pop size 2 is selected
                valid = True #valid pop size has been picked
                Nc = 100 #pop size of 100 has been selected
            elif popnumber == 3: #if pop size 1 is selected
                valid = True #valid pop size has been picked
                Nc = 1000 #pop size of 1000 has been selected
            elif popnumber == 4: #if pop size 1 is selected
                valid = True #valid pop size has been picked
                Nc = 10000 #pop size of 10000 has been selected
            else: #no valid pop size has been selected 
                print("Which population would you like to use?")
                popnumber = int(input("10 (1), 100 (2), 1,000 (3) or 10,000 (4)")) #prompt to try again 
        #----------------------------------------#


    def solve(self): #main function
        stale = 0 #reset stale function
        Ne = int(0.05*Nc) #calculate number of elites need for pop size
        if (Ne % 2 != 0): #if elites are odd
            Ne += 1  # add another elite.
        if (Ne == 0):#if we have no elites
            Ne += 1 #add one
        Ng = 250  # Number of generations.
        truncationrate = 0.7 #cut rate
        parents = truncationrate*Nc # number of parents in breeding pool
        self.population = population(9) # instance of population 
        self.population.seed(Nc, grid) # generate popultion of pop size wrt to given values 
        alltimebest = [] #reset all time best 
        alltimefitness = 100000 #set a high non zero fitness bar 
        alltimegen = 0 #reset all time gen
        solved = False #set acceptance critea 
        for generation in range(Ng):#for every generation 
            best_fitness = 10000 #reset best fitness
            bestgrid = [] #reset best grid
            print("\n")#format
            print("Generation " + str(generation + 1)) #print current gen
            for i in range(0, Nc):# for every child in population 
                if self.population.children[i].fitness < best_fitness: #find the best fitness
                    best_fitness = self.population.children[i].fitness #make a note of that solution
                    bestgrid = self.population.children[i].values
            print(best_fitness) # print the best solution from that gen along with its fitness score
            print(bestgrid)
            if  best_fitness < alltimefitness: #check to see if it beats all time best solution 
                alltimefitness = best_fitness
                alltimebest = bestgrid # if it does update the all time best 
                alltimegen = generation+1
            self.population.sort() #sort the population in terms of fitness
            if(best_fitness == 0): #if solution is found
                print("\n")
                print("Solution found at generation " +  str(generation+1))
                print(bestgrid) #print best solution 
                solved = True # solved 
                break
            next_gen = [] #reset next gen
            for x in range(Ne):
                next_gen.append(self.population.children[x]) #set aside the elite    
            # Crossover
            for x in range(Ne, Nc,2):  #rest of the population begin the breeading process
                a = self.population.selectionprogress(parents) #parent 1 picked from breeding pool using tournament style 
                b = self.population.selectionprogress(parents) #parent 1 picked from breeding pool using tournament style
                next1 = child() #instance of a new child 
                next2 = child() #instance of a new child 
                parent1 = deepcopy(a.values) #make copy of parent 1 state
                parent2 = deepcopy(b.values) #make copy of parent 2 state
                next1.values, next2.values = crossover(parent1, parent2) # call for crossover of parents 1 and 2 to generate child 1 and 2 using the crossover function 
                next1.values = mutate(next1.values, grid) #mutate child 1
                next2.values = mutate(next2.values, grid) #mutate child 2
                next1.fitnessfunction() #redefine fitness
                next2.fitnessfunction() # redefine fitness
                next_gen.append(next1) #add child 1 to next gen 
                next_gen.append(next2) #add child 2 to next gen 
            self.population.children = next_gen # select next generation of population 
            self.population.sort() #sort the next gen into fitness order
            if(self.population.children[0].fitness != self.population.children[1].fitness): #if progress has been made
                stale = 0 #reset stale count 
            else: #if no progress has been made
                stale += 1 # add one to stale count
            # Re-seed the population if 75 generations have passed with the fittest two candidates always having the same fitness.
            if(stale >= 75): #if stale goes past limit 
                print("The population has gone stale. Re-seeding...")
                self.population.children = []
                self.population.seed(Nc, grid) #population is killed and re seeded              
                stale = 0 #reset counter
                print("Re-seed complete")
        if solved == False: #if after all the generations are complete and no solution is found        
            print("This was the best proposed solution")        
            print(alltimebest)
            print(alltimegen)
            print(alltimefitness) # we print the closest solution that we found
            p=child()
            p.values = alltimebest #and some useful information about fitness
            p.fitnessfinal()        

Nd = 9 #size of suduko
s = sudoku(Nd) #creates an instance of class suduko 
s.accepct() #calls the class function to set up the problem 
s.solve() #start solving the problem 
