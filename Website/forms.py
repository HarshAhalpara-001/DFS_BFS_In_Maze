from django import forms

class MazeInfo(forms.Form):
    rows = forms.IntegerField(label='Rows')
    cols = forms.IntegerField(label='Columns')
    blocks = forms.FloatField(label='Blocks')

class Implementation(forms.Form):
    ALGORITHM_CHOICES = [
        ('DFS', 'Depth-First Search'),
        ('BFS', 'Breadth-First Search'),
    ]
    Algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES, label='Algorithm')
    starting_X= forms.BooleanField(label='Starting_X'),
    starting_Y= forms.BooleanField(label='Starting_Y'),
    Ending_X= forms.BooleanField(label='Ending_X'),
    Ending_Y= forms.BooleanField(label='Ending_Y'),

class StepNavigationForm(forms.Form):
    step_number = forms.IntegerField(label='Step Number', min_value=0,)
