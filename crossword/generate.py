import sys

from crossword import *
from collections import deque

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            remove = []
            for word in self.domains[var]:
                if len(word) != var.length:
                    remove.append(word)
            for word in remove:
                self.domains[var].remove(word)
        return    
        raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # If there is overlap, it is possible we need to remove
        if self.crossword.overlaps[x, y]:
            x_overlap, y_overlap = self.crossword.overlaps[x, y]
            remove = []
            # Checking if each word in x's domain has a corresponding solution in y's domain
            for x_word in self.domains[x]:
                need_remove = True
                for y_word in self.domains[y]:
                    # If the same letter is present at the intersection point, no remove needed
                    if x_word[x_overlap] == y_word[y_overlap]:
                        need_remove = False
                if need_remove:
                    remove.append(x_word)
            if remove:
                for word in remove:
                    self.domains[x].remove(word)
                return True
        return False
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Arcs is none, set arcs to all arcs
        if arcs == None:
            arcs = deque() 
            for first in self.domains:
                for second in self.domains:
                    if first != second and self.crossword.overlaps[first,second]:
                        arcs.append((first, second))
        
        else:
            arcs = deque(arcs)
        
        # AC-3 algorithm - arcs are revised and new arcs are added as needed
        while arcs:
            x,y = arcs.popleft()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z, x))
        return True
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) == len(self.crossword.variables):
            return True
        return False
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        word_list = []
        for variable, word in assignment.items():
            # Ensure words are distinct
            if word in word_list:
                return False
            word_list.append(word)
            # Ensure words are correct length
            if variable.length != len(word):
                return False
            # Ensure no conflicts between neighbours
            for int_var, int_word in assignment.items():
                if int_var in self.crossword.neighbors(variable):
                    x_overlap, y_overlap = self.crossword.overlaps[variable, int_var]
                    if word[x_overlap] != int_word[y_overlap]:
                        return False 
        return True
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        val_list = {}
        # Loop through each word in var's domain
        for word in self.domains[var]:
            removed = 0
            # Loop through var's neighbors (if not already in assignment)
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    x_overlap, y_overlap = self.crossword.overlaps[var, neighbor]
                    # Loop through words in neighbor's domain, iterate removed if not valid with var's word
                    for int_word in self.domains[neighbor]:
                        if word[x_overlap] != int_word[y_overlap]:
                            removed += 1
            val_list[word] = removed
        # Sort list
        return sorted(val_list, key=lambda x: val_list[x])
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        chosen_var = None
        min_remaining = float('inf')
        # Check each variable not in assignment
        for variable in self.domains:
            if variable not in assignment:
                # If there is less values in the domain
                if len(self.domains[variable]) < min_remaining:
                    chosen_var = variable
                    min_remaining = len(self.domains[variable])
                # If equal values in domain, chose variable with more neighbors
                elif len(self.domains[variable]) == min_remaining:
                    if len(self.crossword.neighbors(variable)) > len(self.crossword.neighbors(chosen_var)):
                        chosen_var = variable
        return chosen_var
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        # Use backtrack algo from lecture
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]
        return None   
        
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
