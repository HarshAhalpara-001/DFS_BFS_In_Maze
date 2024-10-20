from django.shortcuts import render, HttpResponse, redirect
import random
from .forms import MazeInfo, Implementation, StepNavigationForm
from django.http import JsonResponse
import json
from collections import deque

# Simple hello world view
def hello(request):
    return HttpResponse('Hello, this is Harsh')

# Function to create a random matrix with specified number of blocks
def dice_throw(m, n, blocks):
    sequence = []
    num_empty = int((1-blocks) * 10)  # Number of empty spaces (0s)
    num_blocks = int((blocks) * 10)
    sequence.extend([0] * num_empty)
    sequence.extend([1] * num_blocks)
    return [[random.choice(sequence) for _ in range(n)] for _ in range(m)]

# View for the contact form and maze creation
def contact_view(request):
    form1 = MazeInfo(request.POST or None)
    form2 = Implementation(request.POST or None)

    if request.method == 'POST' and form1.is_valid():
        rows = form1.cleaned_data.get('rows')
        cols = form1.cleaned_data.get('cols')
        blocks = form1.cleaned_data.get('blocks')

        matrix = dice_throw(rows, cols, blocks)
        request.session['matrix'] = matrix

        return render(request, 'Website/MazeCreation.html', {
            'data': {
                'rows': rows,
                'cols': cols,
                'Matrix': matrix
            },
            'form1': form1,
            'form2': form2
        })

    return render(request, 'Website/MazeCreation.html', {
        'form1': form1,
        'form2': form2
    })

# Depth First Search function to find path in the maze
def DFS(matrix, starting, ending):
    step = []
    
    def call(matrix, visited, x, y, ending, stack):
        if visited[x][y]:
            return False
        
        visited[x][y] = True
        stack.append((x, y))
        step.append([row[:] for row in visited])
        
        if (x, y) == tuple(ending):
            return True
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(matrix) and 
                0 <= ny < len(matrix[0]) and 
                matrix[nx][ny] == 0 and 
                not visited[nx][ny]):
                if call(matrix, visited, nx, ny, ending, stack):
                    return True
        
        visited[x][y] = False
        stack.pop()
        return False

    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    stack = []
    found_path = call(matrix, visited, starting[0], starting[1], ending, stack)
    
    return found_path, stack, step

# Breadth First Search function to find path in the maze
def BFS(matrix, starting, ending):
    steps = []
    
    def call(matrix, starting, ending):
        queue = deque([starting])
        visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
        visited[starting[0]][starting[1]] = True
        path = []
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            x, y = queue.popleft()
            path.append((x, y))
            steps.append([row[:] for row in visited])
            
            if (x, y) == tuple(ending):
                return True, path
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < len(matrix) and 
                    0 <= ny < len(matrix[0]) and 
                    matrix[nx][ny] == 0 and 
                    not visited[nx][ny]):
                    visited[nx][ny] = True
                    queue.append((nx, ny))
        
        return False, path

    found_path, path = call(matrix, starting, ending)
    
    return found_path, path, steps

# Implementation view to process the DFS and navigation
def implementation_view(request):
    matrix = request.session.get('matrix')
    if not matrix:
        return JsonResponse({'error': 'Matrix has not been initialized.'}, status=400)

    stack = []  # Ensure stack is initialized
    step = []   # Ensure step is initialized

    if request.method == 'POST':
        form2 = Implementation(request.POST)

        if form2.is_valid():
            algo = form2.cleaned_data.get('Algorithm')
            starting_x = form2.cleaned_data.get('starting_X')
            starting_y = form2.cleaned_data.get('starting_Y')
            ending_x = form2.cleaned_data.get('Ending_X')
            ending_y = form2.cleaned_data.get('Ending_Y')

            starting = [starting_x, starting_y]
            ending = [ending_x, ending_y]

            if algo == 'DFS':
                found_path, stack, step = DFS(matrix, starting, ending)
            elif algo == 'BFS':
                found_path, stack, step = BFS(matrix, starting, ending)
            else:
                return JsonResponse({'error': 'Invalid algorithm selected.'}, status=400)

            request.session['stack'] = stack
            request.session['step'] = step
            
            data = {
                'intermediate_steps': stack,
                'steps': step,
                'matrix': matrix,
                'path_found': found_path
            }
            return render(request, 'Website/AlgoRunning.html', {'data': json.dumps(data)})

    else:
        form2 = Implementation()
        form3 = StepNavigationForm()

    return render(request, 'Website/MazeCreation.html', {'form1': MazeInfo(), 'form2': form2, 'form3': form3})
