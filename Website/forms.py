from django import forms

class MazeInfo(forms.Form):
    rows = forms.IntegerField()
    cols = forms.IntegerField()
    Algo = forms.CharField()
