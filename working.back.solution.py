assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    def removeChars(givenString,charsToRemove):
        for c in charsToRemove:
            givenString = givenString.replace(c,'')
        return givenString
    
    sudokuBoard = getSudokuBoard()
    rows = sudokuBoard['rows']
    cols = sudokuBoard['cols']
    boxes = sudokuBoard['boxes']
    peers = sudokuBoard['peers']
    units = sudokuBoard['units']
    unitlist = sudokuBoard['unitlist']
        
    prevValues = values
    moreTwinsMayExist = True
    while moreTwinsMayExist:
        for givenUnit in unitlist:
            for box in filter(lambda box: len(values[box]) == 2 ,givenUnit):
                for boxPeer in filter(lambda boxPeer: (boxPeer != box) and (values[boxPeer] == values[box]) ,givenUnit):
                    twin = boxPeer
                    for boxPeer in filter(lambda boxPeer:boxPeer not in (box,twin), givenUnit) :    #Now eliminate Naked twin choices from all Peers except Naked twin
                        values[boxPeer] = removeChars(values[boxPeer],values[box])
        if values == prevValues:
            moreTwinsMayExist = False
        else:
            prevValues = values
    return values
 

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def diagonals(rows,cols):
    d1 = [row+col for row,col in zip(rows,cols)]
    d2 = [row+col for row,col in zip(rows,reversed(cols))]
    diagonals = [d1] + [d2]
    return diagonals #d1.append(d2)    

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    sudokuBoard = getSudokuBoard()
    rows = sudokuBoard['rows']
    cols = sudokuBoard['cols']
    boxes = sudokuBoard['boxes']
    peers = sudokuBoard['peers']
    units = sudokuBoard['units']
    unitlist = sudokuBoard['unitlist']

    assert len(grid) == 81, "Grid should have 81 values"
    
    return dict(zip(boxes,['123456789'if item == '.' else item for item in list(grid)]))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    sudokuBoard = getSudokuBoard()
    rows = sudokuBoard['rows']
    cols = sudokuBoard['cols']
    boxes = sudokuBoard['boxes']
    peers = sudokuBoard['peers']
    units = sudokuBoard['units']
    unitlist = sudokuBoard['unitlist']

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):

    sudokuBoard = getSudokuBoard()
    rows = sudokuBoard['rows']
    cols = sudokuBoard['cols']
    boxes = sudokuBoard['boxes']
    peers = sudokuBoard['peers']
    units = sudokuBoard['units']
    unitlist = sudokuBoard['unitlist']

    solved_boxes = [key for key in values if len(values[key]) == 1 ]
    
    for solved_box in solved_boxes:
        for peer in peers[solved_box]:
            values[peer] = values[peer].replace(values[solved_box],'')
    return values

def only_choice(values):
    def peersHave(box,candidateValue):
        for peer in peers[box]:
            if candidateValue in values[peer]:                
                return True
        return False

    sudokuBoard = getSudokuBoard()
    rows = sudokuBoard['rows']
    cols = sudokuBoard['cols']
    boxes = sudokuBoard['boxes']
    peers = sudokuBoard['peers']
    units = sudokuBoard['units']
    unitlist = sudokuBoard['unitlist']

    # For each cell that is unsolved
    for box in filter(lambda box: len(values[box]) > 1, boxes):        
        # For each candidate value in the cell check if the peers have that value.
        # If the candidate value is unique to the cell amongst peers, it is the only choice for
        # given cell
        for candidateValue in filter(lambda candidateValue: not peersHave(box,candidateValue), values[box]):  
            values[box] = candidateValue  # Set the cell value to the candidate value that's
                                          # not repeated amongst peers
    return values

def reduce_puzzle(values):

    stalled = False
    iterations = 0

    while not stalled:
         
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy       
        values = eliminate(values)
        
        # Only Choice Strategy
        values = only_choice(values)
      
        # Naked Twins Strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        #iterations += 1
        #print(iterations)
        
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    #display(values)
    #print()
    
    # Check if the Puzzle is already solved (Exit condition for Recursion)
    solved_values = len([box for box in values.keys() if len(values[box]) == 1])
    if solved_values == 81:
        return values    
    #print(solved_values)

    # Choose one of the unfilled squares with the fewest possibilities
    fewestOptions = 9
    splitPointCell = ''
    for box,value in values.items():
        if (1 < len(value)) and  (len(value) < fewestOptions) :
            fewestOptions = len(value)
            splitPointCell = box    
        
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[splitPointCell]:
        newSudoku = values.copy()
        newSudoku[splitPointCell] = value
        searchNode = search(newSudoku)
        if searchNode:
            return searchNode

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Create Board layout and components representations. Other functions rely on them
    values = search(grid_values(grid))
    return values

def getSudokuBoard():

    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows,cols)
 
    row_units = [cross(r, cols) for r in rows]
    column_units = [cross(rows, c) for c in cols]
    square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
    diagonal_units = diagonals(rows,cols)

    unitlist = row_units + column_units + square_units + diagonal_units

    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
    
    sudokuBoard = {'rows':rows,
                   'cols':cols,
                   'boxes': boxes,
                   'row_units':row_units,
                   'column_units':column_units,
                   'square_units':square_units,
                   'diagonal_units':diagonal_units,
                   'unitlist':unitlist,
                   'units':units,
                   'peers':peers}

    return sudokuBoard


if __name__ == '__main__':

    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
