from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addproblem/", views.addproblem, name="addproblem"),
    path("view_problem/<int:problem_id>/", views.view_problem, name="view_problem"),
    
]