---
# Maze Solver - DFS & BFS Visualization

Welcome to the Maze Solver project! This application visualizes pathfinding algorithms within a randomly generated maze, specifically Depth First Search (DFS) and Breadth First Search (BFS).

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Algorithms Explained](#algorithms-explained)
- [Screenshots](#screenshots)
- [Live Website](#live-website)
- [Contributing](#contributing)
- [License](#license)

## Features
- Generate a random maze with customizable dimensions and block density.
- Visualize pathfinding using DFS and BFS algorithms.
- Step through the algorithm visually, with options to start and stop the visualization.
- Responsive and dark-themed user interface.
- Display the status of the path found and the current step during visualization.

## Technologies Used
- **Django**: A high-level Python web framework that encourages rapid development.
- **HTML/CSS**: For structuring and styling the web application.
- **JavaScript**: For adding interactivity to the front end.
- **Bootstrap**: For responsive design (if included).
- **Git**: Version control for managing changes.

## Installation
To set up this project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HarshAhalpara-001/DFS_BFS_In_Maze.git
   cd DFS_BFS_In_Maze
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install django
   ```

4. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and go to `http://127.0.0.1:8000/`.

## Usage
1. **Generate a Maze**:
   - Fill in the maze configuration form with the number of rows, columns, and block density.
   - Click the "Generate Maze" button to create the maze.

2. **Select Algorithm**:
   - Choose between **DFS** or **BFS** from the algorithm dropdown.
   - Specify the starting (X, Y) and ending (X, Y) coordinates for the pathfinding.

3. **Visualize the Pathfinding**:
   - Click "Run" to visualize the algorithm step by step.
   - Use the "Previous Step" and "Next Step" buttons to navigate through the steps.
   - Click "Start" to automatically advance through the steps at a set interval.

4. **Stop Visualization**:
   - Click "Stop" to pause the automatic visualization.

## How It Works
The maze is represented as a grid of cells, where each cell can either be a wall (blocked) or an open path. The application uses a random matrix generator to create the maze layout based on user input. 

### Pathfinding Algorithms
- **Depth First Search (DFS)**: This algorithm explores as far as possible along each branch before backtracking. It uses a stack to remember the path taken, allowing it to return to previous cells when necessary.

- **Breadth First Search (BFS)**: This algorithm explores all neighbors at the present depth before moving on to nodes at the next depth level. It uses a queue to keep track of the nodes that need to be explored, ensuring that it explores the shortest path first.

## Algorithms Explained
### Depth First Search (DFS)
- **Process**:
  1. Start at the initial position.
  2. Mark the current node as visited.
  3. Explore each unvisited neighbor recursively.
  4. Backtrack if no unvisited neighbors are left.
  
- **Time Complexity**: O(V + E), where V is the number of vertices and E is the number of edges.

### Breadth First Search (BFS)
- **Process**:
  1. Start at the initial position.
  2. Mark the current node as visited and add it to the queue.
  3. Dequeue a node and explore its unvisited neighbors.
  4. Repeat until the queue is empty.
  
- **Time Complexity**: O(V + E), where V is the number of vertices and E is the number of edges.

## Screenshots
### Maze Generation
![Screenshot 2024-10-20 225056](https://github.com/user-attachments/assets/c888f73e-2dcf-484d-9985-efd39dccc912)

### Pathfinding Visualization
![Screenshot 2024-10-20 225142](https://github.com/user-attachments/assets/7fce81c6-f87e-44b8-80e4-8df6f73a0e70)

## Live Website
You can access the live version of the application at [**Link**](https://pythonbyh.pythonanywhere.com/). Please note that the availability of this site may vary; it can be active or inactive at times.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve this project. To contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a Pull Request.
