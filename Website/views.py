from django.shortcuts import render,HttpResponse
import random
# Create your views here.
def hello(request):
    return HttpResponse('Hello this is harsh')
from django.shortcuts import render
from .forms import MazeInfo  # Import the form

def dice_throw(m, n):
    sequence = [0, 0, 0, 0, 1]  # 3/5 will be empty and 2/5 will be filled in maze randomly
    mat = []
    for i in range(m):
        li = []
        for j in range(n):
            li.append(random.choice(sequence))
        mat.append(li)
    return mat

# def Change_Matrix()

def contact_view(request):
    # Check if the request is POST (meaning the form has been submitted)
    if request.method == 'POST':
        form = MazeInfo(request.POST)  # Create a form instance with POST data
        if form.is_valid():  # Validate the form
            # Access form data using `cleaned_data`
            Matrix= dice_throw(form.cleaned_data.get('rows'),form.cleaned_data.get('cols'))
            data={
            'rows' : form.cleaned_data.get('rows'),
            'cols' : form.cleaned_data.get('cols'),
            'Algo' : form.cleaned_data.get('Algo'),
            'Matrix' : Matrix
            }
            print(Matrix)
            return render(request, 'Website/MazeCreation.html', {'data':data,'form':form})
    else:
        form = MazeInfo()  # Empty form instance for GET requests

    return render(request, 'Website/MazeCreation.html', {'form':form})
