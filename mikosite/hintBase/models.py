from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import random
from taggit.managers import TaggableManager
class Problem(models.Model):
    
    problem_id = models.AutoField(primary_key=True)
    latex_code = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='problem_images/', blank=True, null=True)
    difficulty = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    tags = TaggableManager()
    
    
    def __str__(self):
        if self.author is not None:
            return f'Problem by {self.author.username}, problem id: {self.problem_id}'
        else:
            return f'Problem, problem id: {self.problem_id}, no author'

class ProblemHint(models.Model):
    hintId = models.AutoField(primary_key=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    hints = models.TextField()  # Serialized list of hints
    latex_solution = models.TextField()

    def __str__(self):
        return f'Hint for Problem {self.problem.problem_id} by {self.author.username}'
    
