from django.db import models



class Category(models.Model):
    category = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    img = models.ImageField(upload_to = "categories/")

    def __str__(self):
        return self.category
    

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question[:50]  # qisqaroq ko‘rsatish uchun
