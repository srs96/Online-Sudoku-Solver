# Method inspired from Solving Every Sudoku Puzzle by Peter Norvig

import random

#This section creates the puzzle structure

digits = '123456789'
alphabets = 'ABCDEFGHI'
squares = []
for i in alphabets:  # We create a list of all the squares. squares = ['A1', 'A2' ..... 'I9']
    for j in digits:
        squares.append(i+j)

unitlist = [] #This is a 2-D list. Each item consists of the 3 unit lists (row, column and sub-grid units)
for i in alphabets:
    row_unit = []
    for j in digits:  #Here we create the row units
        row_unit.append(i+j)
    unitlist.append(row_unit)

for i in digits:
    column_units = []
    for j in alphabets: #Here we create the column units
        column_units.append(j+i)
    unitlist.append(column_units)

alpha_section = ['ABC', 'DEF', 'GHI']
digit_section = ['123', '456', '789']


for i in alpha_section:
    for j in digit_section:
        subgrid_units = []   #Here we create the sub-grid units
        for i_i in i:
            for j_j in j:
                subgrid_units.append(i_i+j_j)
        unitlist.append(subgrid_units)

unit = dict((s, [u for u in unitlist if s in u]) for s in squares) #Each square is assigned its units.
peers = dict((s, list(set(sq for un in unit[s] for sq in un if sq != s))) for s in squares) #Each square is assigned its peers



def propagate(grid): #This function propagates the initially filled squares
    input_values = [x for x in grid]
    initial_state = dict(zip(squares, input_values))
    possible_values = dict((s, digits) for s in squares) #Initially each square has all digits ('123456789') as its possible value.
    for sq, initial_digit in initial_state.items():
        if initial_digit in digits: #Checking if a square is initally filled.
            possible_values = assign(possible_values, sq, initial_digit) #If a square is initally filled, that value is assigned to it.
            if not possible_values:
                return False #If assignment records a violation, we return a failed state.
    return possible_values


def assign(possible_values, sq, digit): #This fuction assigns a value to a square and calls the eliminate_peers and assign_unit function.
    remaining = possible_values[sq].replace(digit, '')  #We get the remaining values by removing the assigned value from the string's possible values.
    possible_values[sq] = digit

    for p in peers[sq]: #Here we eliminate the assigned value from all its peers
        possible_values = eliminate_peers(possible_values, p, digit)
        if not possible_values: #If assignment records a violation, we return a failed state.
            return False

    for r in remaining:  #We check the number possible places of each remaining value in the square's unit.
        possible_values = assign_unit(possible_values, sq, r)
        if not possible_values:  #If assignment records a violation, we return a failed state.
            return False
    return possible_values

def eliminate_peers(possible_values, sq, digit):
    if digit not in possible_values[sq]: #The value to be eliminated has already been eliminated.
        return possible_values
    possible_values[sq] = possible_values[sq].replace(digit, '') #Eliminate the value from the square's possible values.
    if len(possible_values[sq]) < 1: #If a square is left with no possible values, a violation has occured.
        return False
    if len(possible_values[sq]) == 1: #If a square is left with one possible value, we eliminate that value from all its peers.
        for p in peers[sq]:
            possible_values = eliminate_peers(possible_values, p, possible_values[sq])
            if not possible_values:  #If assignment records a violation, we return a failed state.
                return False
    return possible_values

def assign_unit(possible_values, sq, r):
    for u in unit[sq]: #Looping over the 3 unit lists of a square.
        available_places = [] #Creating a new list of available places for the value.
        for sq_in_unit in u: #Looping over each square of the unit.
            if r in possible_values[sq_in_unit]: #Checking if the value is in the square's possible value list.
                available_places.append(sq_in_unit) #If the value is in a square's possible value list, we add that square to the avaiable places for this value.
        if len(available_places) < 1: #If a value has no available places, a violation has occured.
            return False
        elif len(available_places) == 1: #If a value has one avaiable place, we assign it to that square.
            possible_values = assign(possible_values, available_places[0], r)
            if not possible_values: #If assignment records a violation, we return a failed state.
                return False
    return possible_values

def search(possible_values): #This is the depthfirst backtracking search.
    if not possible_values: #Returns failed state if a violation is detected.
        return False
    solved_flag = 1 #A flag to check if the grid is solved.
    for s in squares:
        if len(possible_values[s]) != 1: #If any square has more than 1 possible values, the puzzle is still unsolved.
            solved_flag = 0 #Flag set to 0 indicates unsolved state.
            break
    if solved_flag == 1: #If flag remains as 1, it indicates that all squares have only 1 possible value, which means the puzzle is solved.
        return possible_values #Return square values as puzzle is solved.

    #uses fewest value ordering.
    lowest = 10 #Variable to find the square with fewest possible values. It is initally set to 10 as the maximum number of possible values are 9.
    lowest_sqaure = 'zzz' #Setting the square with lowest value to a dummy value.
    for s in squares: #This loop finds the square with fewest possible values. Squares with 1 possible value are not considered as they are already solved.
        if len(possible_values[s]) < lowest and len(possible_values[s]) > 1:
            lowest = len(possible_values[s])
            lowest_sqaure = s
    shuffled = possible_values[lowest_sqaure][:]
    new_vals = ''.join(random.sample(shuffled,len(shuffled))) #Here we add randomness to alleviate the parasitic branch issue.
    for d in new_vals: #Attempting to assign each possible value to the selected square.
        attempt = search(assign(possible_values.copy(), lowest_sqaure, d)) #Recursively tries to solve the puzzle with assigned value. As each search branch is independent, we assign a copy of possible values to avoid overwriting issues.
        if attempt: #If an attempt is succesful, we return the values.
            return attempt
    return False


def solve(grid):
    return list(search(propagate(grid)).values())
