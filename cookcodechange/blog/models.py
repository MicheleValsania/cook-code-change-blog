from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Nome univoco del tag

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)  # Titolo del post
    content = models.TextField()  # Contenuto del post
    created_at = models.DateTimeField(auto_now_add=True)  # Data di creazione
    updated_at = models.DateTimeField(auto_now=True)  # Data di aggiornamento
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)  # Relazione con i tag

    def __str__(self):
        return self.title
