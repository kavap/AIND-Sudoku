# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: While performing Depth first search of our solution, at every given level, we can identify presence of Naked twins by looking at row,column 
   and diagonal units and comparing candidate values of cells that belong to the same unit. When we find Naked Twins pair in a given unit (same row, column or diagonal), we look at each unit-mate cell of the Naked Twins and apply the constrain that the candidate values of any of the unitmates can not be any of the candidate values of Naked Twins cells. When a cell belongs to a unit which also contains Naked Twins, the given cell is subjected to the Naked Twins constraint. This reduces the Search space of the Depth First Search.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In case of diagonal Sudoku, the diagonal Sudoku specific constraint on any given cell is : If the cell is along the major or minor 
   diagonal, the cell can not have a number that's duplicate of any of the solved cell along the diagonal that given cell is part of. We can treat this constraint to add a new set of peers for the given cell. From there, the solution aligns with the Elimination strategy that we use to account for all the Peers.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

