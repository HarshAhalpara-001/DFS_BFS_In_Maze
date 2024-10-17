from django.shortcuts import render, HttpResponse, redirect
import random
from .forms import MazeInfo, Implementation, StepNavigationForm
from django.http import JsonResponse

# Global variable to store the stack
global_stack = []

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
    step=[]
    def call(matrix, visited, x, y, ending, stack):
        if visited[x][y]:
            return False
        visited[x][y] = True
        stack.append((x, y))  # Store the coordinates in the stack
        step.append(visited)
        if (x, y) == tuple(ending):
            return True
        
        # Directions for movement: right, down, left, up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and matrix[nx][ny] == 0:
                if call(matrix, visited, nx, ny, ending, stack):
                    return True
        
        return False

    starting = [0, 0]
    ending = [len(matrix) - 1, len(matrix[0]) - 1]
    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    stack = []
    found_path = call(matrix, visited, starting[0], starting[1], ending, stack)
    
    return found_path, stack, step

# Implementation view to process the DFS and navigation
def implementation_view(request):
    global global_stack  # Declare the global stack variable
    matrix = request.session.get('matrix')
    if not matrix:
        return JsonResponse({'error': 'Matrix has not been initialized.'}, status=400)

    if request.method == 'POST':
        form2 = Implementation(request.POST)
        form3 = StepNavigationForm(request.POST)

        # Process the main implementation form
        if form2.is_valid():
            found_path, stack, step = DFS(matrix)
            data = {
                'Matrix': matrix,
                'intermediate_steps': global_stack,
                'step_Matrix': step,
                'path_found': found_path
            }
            return render(request, 'Website/AlgoRunning.html', {'data': data, 'form2': form2, 'form3': form3, 'stack': global_stack})

        # Process the step navigation form
        elif form3.is_valid():
            step_number = form3.cleaned_data.get('step_number')
            if 0 <= step_number < len(global_stack):
                current_step = global_stack[step_number]  # Get the specific step
                data = {
                    'Matrix': matrix,
                    'intermediate_steps': global_stack,
                    'current_step': current_step,
                    'path_found': True
                }
                return render(request, 'Website/AlgoRunning.html', {'data': data, 'form3': form3})

    else:
        form2 = Implementation()
        form3 = StepNavigationForm()

    return render(request, 'Website/MazeCreation.html', {'form1': MazeInfo(), 'form2': form2, 'form3': form3})
