# CS50AI - Introduction to Artificial Intelligence with Python

This course consisted of 7 topics and 12 projects.

## Topic 1: Search
This topic revolves around AI problem-solving, examining how AI can effectively tackle various challenges and identify optimal solutions. The computational significance of **heuristics** in facilitating complex problem-solving is emphasized. The lecture covers multiple search approaches:
- **Depth-First Search (DFS):** This method exhaustively explores one path before backtracking to explore others.
- **Breadth-First Search (BFS):** This approach takes one action on each path at a time, ensuring that all nodes at the present depth level are explored before moving on to nodes at the next depth level.
- **Greedy Best-First Search:** This strategy utilizes heuristics to estimate the best immediate action, prioritizing paths that appear to lead to the goal more quickly.
- **A Search*:** This algorithm combines both heuristic estimates and path costs to evaluate the most promising actions, balancing efficiency and optimality.

Additionally, the lecture addresses **adversarial search**, relevant for scenarios where an agent competes against an opponent with conflicting objectives. The **Minimax** algorithm is introduced as a method for determining optimal solutions in adversarial search problems by minimizing the potential loss for a worst-case scenario.

### Projects:
- **[Degrees](degrees):** Based on the game “Six Degrees of Kevin Bacon”, the AI uses a BFS approach to find the shortest connection between any two Hollywood stars.
- **[TicTacToe](tictactoe):** This is an example of an adversarial search problem. The AI uses a minimax approach to optimally play tic-tac-toe.


## Topic 2: Knowledge
This topic focuses on how AI represents and reasons with knowledge. The lecture explains how AI uses **propositional logic** to represent information through logical sentences. It also highlights AI's ability to generate new knowledge by drawing **inferences** from existing knowledge, allowing the system to make logical conclusions based on known facts.

### Projects:
- **[Knights](knights):** The goal of this project is to determine the identity of some unknown characters. Characters can either be identified as “knights,” who always tell the truth, or “knaves,” who always lie. The AI must use a knowledge base of known facts, represented as propositional logic sentences, to make inferences and deduce the identity of each character based on their statements and relationships.
- **[Minesweeper](minesweeper):** Create an AI capable of solving Minesweeper puzzles. The AI accomplishes this by maintaining a **knowledge base** of known safe squares and potential mine locations. Using logical inference, the AI updates its knowledge base as it uncovers new information, identifying safe moves and potential mines based on the information revealed on the board.


## Topic 3: Knowledge
This topic focuses on how AI makes decisions in environments with incomplete or uncertain information. The lecture explains how AI uses probabilistic models, such as **Bayesian networks**, to represent relationships between variables and update beliefs as new evidence becomes available. It also highlights AI’s ability to infer hidden states and predict outcomes by applying inference algorithms, allowing the system to make informed decisions even when faced with uncertainty. Additionally, this lecture covers some other basic probability theory concepts such as random variables, Bayes’ rule, and joint probability.

### Projects:
- **[PageRank](pagerank):** This project involves implementing an algorithm to rank web pages by their importance, using a simplified version of Google's PageRank. The ranking is determined through a probabilistic random surfer model, which evaluates pages based on the number of links they receive and the importance of the linking pages.
- **[Heredity](heredity):** This project focuses on building a model to predict the likelihood of an individual having a genetic trait. The goal is to use probabilistic reasoning to infer the likelihood of individuals possessing a gene based on family data, even when some information is missing.


## Topic 4: Optimization
This topic builds on Topic 1: Search, expanding the focus to more complex problem-solving techniques. **Local search** and **hill climbing** algorithms are discussed as strategies for finding near-optimal solutions, especially when finding the exact optimal solution is not feasible. Heuristics are introduced to guide these searches. The lecture also presents a new class of problems: **constraint satisfaction problems** (CSPs), where the goal is to assign values to variables while satisfying specified conditions. CSPs are solved by ensuring node consistency (unary constraints) and arc consistency (binary constraints). The **Backtracking Search** algorithm is introduced as a recursive method for solving CSPs by incrementally assigning values to variables, backtracking when a constraint is violated, and trying alternative assignments.

### Project:
- **[Crossword](crossword):** This project involved implementing a backtracking search algorithm to solve a CSP in the form of a crossword puzzle.


## Topic 5: Learning
This chapter provided an interesting introduction to **machine learning**, with a particular focus on supervised learning. Key topics like **classification** and **regression** were explored, demonstrating how machines can learn from labeled data to make predictions or informed decisions. One of the challenges discussed was **overfitting**, where models perform well on training data but fail to generalize to new data. Regularization was introduced as a potential solution to mitigate overfitting and improve model performance. Additionally, the chapter touched on **reinforcement learning**, with a focus on the **Q-Learning** algorithm, which allows agents to learn optimal strategies through interactions with their environment. **Unsupervised learning** was also briefly introduced, showcasing techniques for finding patterns in unlabeled data. The practical aspect of the lecture included demonstrations of how machine learning applications can be implemented using popular libraries like **scikit-learn**, providing a hands-on understanding of how to implement these concepts.

### Projects:
- **[Shopping](shopping):** This project involved implementing a **k-nearest neighbors** (k-NN) model using scikit-learn to predict user purchasing behavior in an online shopping environment. The model was trained on a dataset containing information about online shopping users, including whether or not they made a purchase. Using this data, the model is now able to predict how likely future users are to make a purchase based on their provided information.
- **[Nim](nim):** This project involved creating a reinforcement learning model capable of playing the game Nim. Using a Q-Learning approach and many training games, the AI was able to master the game.


Topic 6: Neural Networks (traffic)

Topic 7: Language (parser, attention)
