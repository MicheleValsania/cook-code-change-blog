from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Nome univoco del tag

    def __str__(self):
        return self.name

class Post(models.Model):

    CATEGORY_CHOICES = [
        ('Cook', 'Cook'),
        ('Code', 'Code'),
        ('Change', 'Change'),
    ]
    title = models.CharField(max_length=200)  # Titolo del post
    content = models.TextField()  # Contenuto del post
    created_at = models.DateTimeField(auto_now_add=True)  # Data di creazione
    updated_at = models.DateTimeField(auto_now=True)  # Data di aggiornamento
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)  # Relazione con i tag
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Cook')
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    
    # Campi SEO
    meta_description = models.CharField(max_length=155, blank=True, help_text="Meta description per SEO (max 155 caratteri)")
    keywords = models.CharField(max_length=200, blank=True, help_text="Keywords separate da virgole")
    seo_title = models.CharField(max_length=60, blank=True, help_text="Titolo ottimizzato per SEO (max 60 caratteri)")
    seo_score = models.IntegerField(default=0, help_text="Punteggio SEO da 0 a 100")
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo per nuovi post
            # Ottimizza SEO prima del salvataggio
            from .seo_analyzer import SEOAnalyzer
            seo = SEOAnalyzer()
            
            # Genera meta description se non specificata
            if not self.meta_description:
                self.meta_description = seo.generate_meta_description(self.content)
            
            # Analizza il contenuto per il punteggio SEO
            analysis = seo.analyze_content(self.title, self.content)
            
            # Imposta il punteggio SEO
            self.seo_score = analysis['score']
            
            # Imposta le keywords se non specificate
            if not self.keywords:
                self.keywords = ', '.join(analysis['keywords'])
        
        super().save(*args, **kwargs)
