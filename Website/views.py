from django.shortcuts import render
from collections import deque
import random
import json
from .forms import MazeInfo, Implementation, StepNavigationForm

def dice_throw(m, n, blocks):
    """Creates a random matrix with specified number of blocks."""
    num_empty = int((1 - blocks) * 10)
    num_blocks = int(blocks * 10)
    sequence = [0] * num_empty + [1] * num_blocks
    return [[random.choice(sequence) for _ in range(n)] for _ in range(m)]

class MazeSessionData:
    """Class to manage session data for the maze."""
    def __init__(self, request):
        self.request = request

    @property
    def matrix(self):
        return self.request.session.get('matrix')

    @matrix.setter
    def matrix(self, value):
        self.request.session['matrix'] = value

    @property
    def stack(self):
        return self.request.session.get('stack', [])

    @stack.setter
    def stack(self, value):
        self.request.session['stack'] = value

    @property
    def step(self):
        return self.request.session.get('step', [])

    @step.setter
    def step(self, value):
        self.request.session['step'] = value

def contact_view(request):
    """View for the maze creation form."""
    form1 = MazeInfo(request.POST or None)
    form2 = Implementation(request.POST or None)

    if request.method == 'POST' and form1.is_valid():
        rows, cols, blocks = form1.cleaned_data.values()
        matrix = dice_throw(rows, cols, blocks)

        maze_session = MazeSessionData(request)
        maze_session.matrix = matrix

        return render(request, 'Website/MazeCreation.html', {
            'data': {'rows': rows, 'cols': cols, 'Matrix': matrix},
            'form1': form1,
            'form2': form2
        })

    return render(request, 'Website/MazeCreation.html', {'form1': form1, 'form2': form2})

def DFS(matrix, starting, ending):
    """Depth First Search to find a path in the maze."""
    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    stack, steps = [], []

    def call(x, y):
        if visited[x][y]:
            return False
        visited[x][y] = True
        stack.append((x, y))
        steps.append([row[:] for row in visited])

        if (x, y) == tuple(ending):
            return True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and
                    matrix[nx][ny] == 0 and not visited[nx][ny]):
                if call(nx, ny):
                    return True

        visited[x][y] = False
        stack.pop()
        return False

    found_path = call(starting[0], starting[1])
    return found_path, stack, steps

def BFS(matrix, starting, ending):
    """Breadth First Search to find a path in the maze."""
    visited = [[False] * len(matrix[0]) for _ in range(len(matrix))]
    queue = deque([starting])
    visited[starting[0]][starting[1]] = True
    path, steps = [], []

    while queue:
        x, y = queue.popleft()
        path.append((x, y))
        steps.append([row[:] for row in visited])

        if (x, y) == tuple(ending):
            return True, path, steps

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and
                    matrix[nx][ny] == 0 and not visited[nx][ny]):
                visited[nx][ny] = True
                queue.append((nx, ny))

    return False, path, steps

def implementation_view(request):
    """View to process maze algorithms."""
    maze_session = MazeSessionData(request)

    if not maze_session.matrix:
        return JsonResponse({'error': 'Matrix has not been initialized.'}, status=400)

    if request.method == 'POST':
        form2 = Implementation(request.POST)

        if form2.is_valid():
            algo = form2.cleaned_data['Algorithm']
            starting = [form2.cleaned_data['starting_X'], form2.cleaned_data['starting_Y']]
            ending = [form2.cleaned_data['Ending_X'], form2.cleaned_data['Ending_Y']]
            if maze_session.matrix[starting[0]][starting[1]] == 1 or maze_session.matrix[ending[0]][ending[1]] ==1:
                return render(request, 'Website/MazeCreation.html', {'form1': MazeInfo(), 'form2': form2,})
            if algo == 'DFS':
                found_path, stack, step = DFS(maze_session.matrix, starting, ending)
            elif algo == 'BFS':
                found_path, stack, step = BFS(maze_session.matrix, starting, ending)
            else:
                return JsonResponse({'error': 'Invalid algorithm selected.'}, status=400)

            maze_session.stack = stack
            maze_session.step = step
            
            data = {
                'intermediate_steps': stack,
                'steps': step,
                'matrix': maze_session.matrix,
                'path_found': found_path
            }
            return render(request, 'Website/AlgoRunning.html', {'data': json.dumps(data)})

    form2 = Implementation()
    form3 = StepNavigationForm()

    return render(request, 'Website/MazeCreation.html', {'form1': MazeInfo(), 'form2': form2, 'form3': form3})
