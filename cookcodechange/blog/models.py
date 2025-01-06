from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Nome univoco del tag
    
    def __str__(self) -> str:
        return str(self.name)

class Post(models.Model):

    CATEGORY_CHOICES = [
        ('Cook', 'Cook'),
        ('Code', 'Code'),
        ('Change', 'Change'),
    ]
    title = models.CharField(max_length=200)  # Titolo del post
    content = models.TextField()  # Contenuto del post
    created_at = models.DateTimeField(default=timezone.now)  # Data di creazione
    updated_at = models.DateTimeField(auto_now=True)  # Data di aggiornamento
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)  # Relazione con i tag
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Cook')
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    
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
        if not self.pk:  
            if not self.meta_description:
                self.meta_description = self.content[:157] + "..." if len(self.content) > 160 else self.content
                
            if not self.keywords:
                # Qui inseriamo il nuovo codice
                words = [w.strip('.,!?()[]{}') for w in self.content.lower().split()]
                words = [w for w in words if len(w) > 3 and w.isalnum()]
                word_freq = {}
                for word in words:
                    word_freq[word] = word_freq.get(word, 0) + 1
                self.keywords = ', '.join(sorted(word_freq, key=word_freq.get, reverse=True)[:5])
            
            self.seo_score = self._calculate_seo_score()
        
        super().save(*args, **kwargs)

    def _calculate_seo_score(self):
        score = 70
        
        # Title checks
        if 20 <= len(self.title) <= 60:
            score += 10
        if any(keyword in self.title.lower() for keyword in self.keywords.split(',')):
            score += 5
            
        # Content checks    
        word_count = len(self.content.split())
        if word_count > 300:
            score += 10
        
        # Meta description
        if self.meta_description and 50 <= len(self.meta_description) <= 160:
            score += 5
            
        return min(100, score)