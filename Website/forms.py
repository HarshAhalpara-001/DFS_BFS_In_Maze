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

    starting_X = forms.IntegerField(label='Starting X', min_value=0)
    starting_Y = forms.IntegerField(label='Starting Y', min_value=0)
    Ending_X = forms.IntegerField(label='Ending X', min_value=0)
    Ending_Y = forms.IntegerField(label='Ending Y', min_value=0)


class StepNavigationForm(forms.Form):
    step_number = forms.IntegerField(label='Step Number', min_value=0,)
