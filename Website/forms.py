from django import forms

class MazeInfo(forms.Form):
    rows = forms.IntegerField(label='Rows')
    cols = forms.IntegerField(label='Columns')
    
    ALGORITHM_CHOICES = [
        ('DFS', 'Depth-First Search'),
        ('BFS', 'Breadth-First Search'),
    ]
    
    Algo = forms.ChoiceField(choices=ALGORITHM_CHOICES, label='Algorithm')
