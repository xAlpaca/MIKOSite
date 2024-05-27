from django.shortcuts import render
from django.contrib import messages
from accounts.models import User
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.conf import settings
from .models import Problem, ProblemHint
from taggit.models import Tag
from fuzzywuzzy import fuzz



# Create your views here.



def index(request):
    all_problems = reversed(Problem.objects.all())
    
    
    user_belongs_to_moderator_group = request.user.groups.filter(name='Moderator').exists()
    tags = list([tag.name for tag in Tag.objects.all()])
    
    if request.method == 'POST':
        tags_to_filter = request.POST.getlist('tags_to_filter')
        max_difficulty = int(request.POST.get('difficulty_max'))
        min_difficulty = int(request.POST.get('difficulty_min'))
        if max_difficulty < min_difficulty:
            return render(request, 'index1.html', {"all_problems": all_problems,  "user_belongs_to_moderator_group": user_belongs_to_moderator_group, "tags": tags})
        else:
            if len(tags_to_filter) == 0:
                filtered_problems = Problem.objects.filter(difficulty__gte=min_difficulty, difficulty__lte=max_difficulty)
                return render(request, 'index1.html', {"all_problems": filtered_problems,  "user_belongs_to_moderator_group": user_belongs_to_moderator_group, "tags": tags})
            else:
                filtered_problems =[]
                for problem in all_problems:
                    problemtags = set([tg for tg in problem.tags.names()])
                    tags_to_filter = set(tags_to_filter)
                    print(tags_to_filter, problemtags)
                    if tags_to_filter.issubset(problemtags):
                        filtered_problems.append(problem)
                return render(request, 'index1.html', {"all_problems": filtered_problems,  "user_belongs_to_moderator_group": user_belongs_to_moderator_group, "tags": tags})

        
        
    #     filtered_problems = Problem.objects.filter(tags__name__in=request.POST.getlist('tags'))
    return render(request, 'index1.html', {"all_problems": all_problems,  "user_belongs_to_moderator_group": user_belongs_to_moderator_group, "tags": tags})

@login_required(login_url='../../signin')
def addproblem(request):
    tags = list([tag.name for tag in Tag.objects.all()])
    if request.method == 'POST':
        
        latex_code = request.POST.get('latex_code')
        source = request.POST.get('source')
        image = request.FILES.get('image')
        difficulty = int(request.POST.get('difficulty'))
        selected_tags = request.POST.getlist('selected_tags')

        problem = Problem(
            latex_code=latex_code,
            source=source,
            image=image,
            difficulty=difficulty,
            author = request.user
        )
        confirm_key = request.POST.get('confirm_key')
        # print(confirm_key)
        if confirm_key == None:
            for tag in selected_tags:
                if tag not in tags:
                    return render(request, 'addproblem.html', {"custom_message": f"Tag {tag} nie istnieje", "confirm_key" : "False", "tags": tags})
            similar_problems=[]
            for selected_Problem in Problem.objects.all():
                selected_Problem_code = selected_Problem.latex_code
                if fuzz.ratio(selected_Problem_code, latex_code) > 64:
                    similar_problems.append(selected_Problem)
            if len(similar_problems) > 0:
                    return render(request, 'addproblem.html', {"tags": tags, "custom_message": f"Możliwe że to zadanie już jest w bazie zadań, sprawdź czy dalej chcesz dodać to zadanie.", "similar_problems": similar_problems, "confirm_key" : "True", "problem": problem})
       
        if confirm_key == "Usuń":
            return render(request, 'addproblem.html', {"custom_message": f"Usinięto zadanie.", "confirm_key" : "False", "tags": tags})
        
        problem.save()
        problem.tags.add(*selected_tags)
        problem.save()
        
        return render(request, 'addproblem.html', {"custom_message": f"Zadanie zostało dodane, id zadania: {problem.problem_id}, ", "confirm_key" : "False", "tags": tags})
    
    return render(request, 'addproblem.html', {"tags": tags, "confirm_key" : "False"})


def view_problem(request, problem_id):
    problem = get_object_or_404(Problem, problem_id=problem_id)
    hinty = ProblemHint.objects.filter(problem=problem, verified=True)
    
    
    return render(request, 'viewproblem.html', {"problem": problem, "user": request.user, "hinty": hinty})

@login_required(login_url='../signin')
def add_solution(request, problem_id):
    problemf = get_object_or_404(Problem, problem_id=problem_id)
    
    if request.method == 'POST':
        hints = ""
        for key, value in request.POST.items():
            if key.startswith('hint'):
                hints += value + "\n"
        hints = hints.rstrip("\n")
        
        problemhint = ProblemHint(
            problem = problemf,
            author = request.user,
            hints = hints,
            latex_solution = request.POST.get('solution'),
            
        )   
        problemhint.save()
        return redirect(f"/bazahintow/view_problem/{problem_id}/")     
    return render(request, 'addsolution.html', {"problem": problemf} )


@login_required(login_url='../../signin')
def verifysolutions(request):
    messages={}
    
    if request.user.groups.filter(name='Moderator').exists() == False:
        return redirect("/")

    solutions_toverify = ProblemHint.objects.filter(verified=False)
    
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('delete_solution') != None:
            hint_to_delete = ProblemHint.objects.get(hintId=request.POST.get('delete_solution'))
            hint_to_delete.delete()
        elif request.POST.get('verify_solution') != None:
            hint_to_verify = ProblemHint.objects.get(hintId=request.POST.get('verify_solution'))
            hint_to_verify.verified = True
            hint_to_verify.save()
        
    
    return render(request, 'verifysolutions.html', {"solutions_toverify": solutions_toverify})