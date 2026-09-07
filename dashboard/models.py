from django.db import models

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name
    class Meta: verbose_name_plural = "Expense Categories"

class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_incurred = models.DateField()
    def __str__(self): return f"{self.description} - {self.amount}"
    class Meta: ordering = ['-date_incurred']