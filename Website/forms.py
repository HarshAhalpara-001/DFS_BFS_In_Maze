from django import forms

class MazeInfo(forms.Form):
    rows = forms.IntegerField(label='Rows')
    cols = forms.IntegerField(label='Columns')

class Implementation(forms.Form):
    ALGORITHM_CHOICES = [
        ('DFS', 'Depth-First Search'),
        ('BFS', 'Breadth-First Search'),
    ]
    Algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES, label='Algorithm')
class StepNavigationForm(forms.Form):
    step_number = forms.IntegerField(label='Step Number', min_value=0, required=True)
