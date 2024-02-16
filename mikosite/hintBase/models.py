from django.db import models
from accounts.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Problem(models.Model):
    GENRE_CHOICES = [
        ('geometry', 'Geometry'),
        ('combinatorics', 'Combinatorics'),
        ('numbertheory', 'Number Theory'),
        ('algebra', 'Algebra'),
        ('other', 'Other'),
    ]
    
    problem_id = models.AutoField(primary_key=True)
    latex_code = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='problem_images/', blank=True, null=True)
    pdf = models.FileField(upload_to='problem_pdfs/', blank=True, null=True)
    difficulty = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    genre = models.CharField(max_length=15, choices=GENRE_CHOICES)

    def __str__(self):
        if self.author is not None:
            return f'Problem by {self.author.username}, problem id: {self.problem_id}'
        else:
            return f'Problem, problem id: {self.problem_id}, no author'

class ProblemHint(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    hints = models.TextField()  # Serialized list of hints
    latex_solution = models.TextField()
    solution_pdf = models.FileField(upload_to='hint_pdfs/', blank=True, null=True)

    def __str__(self):
        return f'Hint for Problem {self.problem.problem_id} by {self.author.username}'
    
