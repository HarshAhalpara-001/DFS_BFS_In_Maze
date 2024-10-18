from django.shortcuts import render, HttpResponse, redirect
import random
from .forms import MazeInfo, Implementation, StepNavigationForm
from django.http import JsonResponse
import json
from collections import deque


# Global variable to store the stack

# Simple hello world view
def hello(request):
    return HttpResponse('Hello, this is Harsh')

# Function to create a random matrix
def dice_throw(m, n):
    sequence = [0, 0, 0, 0, 1]  # 3/5 empty, 2/5 filled
    return [[random.choice(sequence) for _ in range(n)] for _ in range(m)]

# View for contact form and maze creation
def contact_view(request):
    form1 = MazeInfo(request.POST or None)
    if request.method == 'POST' and form1.is_valid():
        rows = form1.cleaned_data.get('rows')
        cols = form1.cleaned_data.get('cols')
        request.session['matrix'] = dice_throw(rows, cols)
        return render(request, 'Website/MazeCreation.html', {
            'data': {
                'rows': rows,
                'cols': cols,
                'Matrix': request.session['matrix']
            },
            'form1': form1,
            'form2': Implementation()
        })
    
    return render(request, 'Website/MazeCreation.html', {'form1': form1, 'form2': Implementation()})

# Depth First Search function to find path in the maze
def DFS(matrix):
    step = []
    
    def call(matrix, visited, x, y, ending, stack):
        if visited[x][y]:
            return False
        
        visited[x][y] = True
        stack.append((x, y))  # Store the coordinates in the stack
        step.append([row[:] for row in visited])  # Store a copy of visited state
        
        if (x, y) == tuple(ending):
            return True
        
        # Directions for movement: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check if next position is within bounds and not visited
            if (0 <= nx < len(matrix) and 
                0 <= ny < len(matrix[0]) and 
                matrix[nx][ny] == 0 and 
                not visited[nx][ny]):
                
                if call(matrix, visited, nx, ny, ending, stack):
                    return True
        
        # Backtrack: unmark the cell as visited and remove from stack
        visited[x][y] = False
        stack.pop()
        return False

    starting = [0, 0]
    ending = [len(matrix) - 1, len(matrix[0]) - 1]
    
    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    stack = []
    found_path = call(matrix, visited, starting[0], starting[1], ending, stack)
    
    print("Calculated steps:", step)
    return found_path, stack, step

def BFS(matrix):
    steps = []
    
    def call(matrix, starting, ending):
        queue = deque([starting])  # Initialize the queue with the starting position
        visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
        visited[starting[0]][starting[1]] = True  # Mark starting position as visited
        path = []  # To store the path taken
        
        # Directions for movement: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            x, y = queue.popleft()  # Get the current position from the front of the queue
            path.append((x, y))  # Store the current position in the path
            steps.append([row[:] for row in visited])  # Store a copy of visited state
            
            if (x, y) == tuple(ending):
                return True, path  # Path found
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Check if next position is within bounds and not visited
                if (0 <= nx < len(matrix) and 
                    0 <= ny < len(matrix[0]) and 
                    matrix[nx][ny] == 0 and 
                    not visited[nx][ny]):
                    
                    visited[nx][ny] = True  # Mark as visited
                    queue.append((nx, ny))  # Add the new position to the queue
        
        return False, path  # No path found

    starting = [0, 0]
    ending = [len(matrix) - 1, len(matrix[0]) - 1]
    
    found_path, path = call(matrix, starting, ending)
    
    print("Calculated steps:", steps)
    return found_path, path, steps



# Implementation view to process the DFS and navigation
# from django.http import JsonResponse
# from django.shortcuts import render
# import json

def implementation_view(request):
    matrix = request.session.get('matrix')
    if not matrix:
        return JsonResponse({'error': 'Matrix has not been initialized.'}, status=400)

    if request.method == 'POST':
        form2 = Implementation(request.POST)

        if form2.is_valid():
            Algo=form2.cleaned_data.get('Algorithm')
            if Algo=='DFS':
                found_path, stack, step = DFS(matrix)
            if Algo=='BFS':
                found_path, stack, step = BFS(matrix)
            request.session['stack'] = stack
            request.session['step'] = step
            
            data = {
                'intermediate_steps': stack,
                'steps': step,
                'matrix': matrix,
                'path_found': True
            }
            return render(request, 'Website/AlgoRunning.html', {'data': json.dumps(data)})

    else:
        form2 = Implementation()
        form3 = StepNavigationForm()

    return render(request, 'Website/MazeCreation.html', {'form1': MazeInfo(), 'form2': form2, 'form3': form3})
