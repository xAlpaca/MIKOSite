from django.shortcuts import render
from django.contrib import messages
from accounts.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from mainSite.models import Post

from pylatex import Document, NoEscape

from django.conf import settings
from .models import Problem

# Create your views here.


def index(request):
    all_problems = reversed(Problem.objects.all())
    
    return render(request, 'index1.html', {"all_problems": all_problems})

def addproblem(request):
    if request.method == 'POST':
        latex_code = request.POST.get('latex_code')
        source = request.POST.get('source')
        image = request.FILES.get('image')
        difficulty = int(request.POST.get('difficulty'))
        genre = request.POST.get('genre')
        
        problem = Problem(
            latex_code=latex_code,
            source=source,
            image=image,
            difficulty=difficulty,
            genre=genre,
            author = request.user
        )
        # Save the problem object
        problem.save()

        return render(request, 'addproblem.html', {"custom_message": f"Zadanie zostało dodane, id zadania: {problem.problem_id}"})
    
    return render(request, 'addproblem.html')


def view_problem(request, problem_id):
    problem = get_object_or_404(Problem, problem_id=problem_id)
    print(problem)
    return render(request, 'viewproblem.html', {"problem": problem})