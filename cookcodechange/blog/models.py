from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Nome univoco del tag
    
    def __str__(self) -> str:
        return str(self.name)

class Post(models.Model):

    CATEGORY_CHOICES = [
        ('VENTRE', 'Ventre'),
        ('TETE', 'Tête'),
        ('COEUR', 'Coeur'),
    ]
    title = models.CharField(max_length=200)  # Titolo del post
    content = CKEditor5Field('Content', config_name='default')  # Contenuto del post
    created_at = models.DateTimeField(default=timezone.now)  # Data di creazione
    updated_at = models.DateTimeField(auto_now=True)  # Data di aggiornamento
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)  # Relazione con i tag
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='VENTRE')
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    objects = models.Manager()
    # Campi SEO
    seo_title = models.CharField(max_length=60, blank=True, help_text="Titolo ottimizzato per i motori di ricerca (max 60 caratteri)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Descrizione che apparirà nei risultati di ricerca (max 160 caratteri)")
    keywords = models.CharField(max_length=200, blank=True, help_text="Parole chiave separate da virgole")
    seo_score = models.IntegerField(default=0, help_text="Punteggio SEO da 0 a 100")
    
    def __str__(self) -> str:
        return str(self.title)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        print("Starting save method...")
        if not self.pk:  # Nuovo post
            print(f"New post detected - Title: {self.title}")
            
            if not self.meta_description:
                self.meta_description = self.content[:157] + "..." if len(self.content) > 160 else self.content
                print(f"Generated meta description: {self.meta_description}")
                
            if not self.keywords:
                words = [w.strip('.,!?()[]{}') for w in self.content.lower().split()]
                words = [w for w in words if len(w) > 3 and w.isalnum()]
                word_freq = {}
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
                self.keywords = ', '.join(sorted(word_freq, key=word_freq.get, reverse=True)[:5])
                print(f"Generated keywords: {self.keywords}")
            
            score = self._calculate_seo_score()
            print(f"Calculated SEO score: {score}")
            self.seo_score = score
        
        super().save(*args, **kwargs)

    def _calculate_seo_score(self):
        print("Calculating SEO score...")
        score = 70
        print(f"Initial score: {score}")
        
        if 20 <= len(self.title) <= 60:
            score += 10
            print(f"Title length bonus: +10")
            
        if self.keywords and any(keyword in self.title.lower() for keyword in self.keywords.split(',')):
            score += 5
            print(f"Keyword in title bonus: +5")
            
        word_count = len(self.content.split())
        if word_count > 300:
            score += 10
            print(f"Content length bonus: +10")
        
        if self.meta_description and 50 <= len(self.meta_description) <= 160:
            score += 5
            print(f"Meta description bonus: +5")
        
        print(f"Final score: {score}")
        return min(100, score)
    

class Resource(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField(blank=True)
    objects = models.Manager() 
    def __str__(self) -> str:
        return self.title


class StaticPage(models.Model):
    PAGE_CHOICES = [
        ('CODEUR', 'Le Codeur'),
        ('EXPLORATEUR', 'L\'Explorateur'),
    ]
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    content = CKEditor5Field('Content', config_name='default')
    page_type = models.CharField(max_length=20, choices=PAGE_CHOICES, unique=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_page_type_display()}"

    class Meta:
        verbose_name = "Page statique"
        verbose_name_plural = "Pages statiques"