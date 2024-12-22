from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from .models import Post, Tag
from .seo_analyzer import SEOAnalyzer

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'seo_score')
    list_filter = ('tags', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)
    readonly_fields = ('seo_score',)
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'image', 'tags')
        }),
        ('SEO', {
            'fields': ('seo_title', 'meta_description', 'keywords', 'seo_score'),
            'classes': ('collapse',),
            'description': 'Questi campi vengono generati automaticamente ma possono essere modificati manualmente.'
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('analyze-seo/', self.analyze_seo_view, name='analyze-seo'),
        ]
        return custom_urls + urls

    def analyze_seo_view(self, request):
        if request.method == 'POST':
            import json
            data = json.loads(request.body)
            title = data.get('title', '')
            content = data.get('content', '')

            seo = SEOAnalyzer()
            analysis = seo.analyze_content(title, content)

            if analysis['success']:
                return JsonResponse({
                    'success': True,
                    'score': analysis.get('seo_score', 70),
                    'suggestions': analysis.get('analysis', '').split('\n')
                })
            
            return JsonResponse({
                'success': False,
                'error': 'Errore durante l\'analisi SEO'
            })

    def save_model(self, request, obj, form, change):
        if not change:  # Solo per nuovi post
            seo = SEOAnalyzer()
            
            # Genera meta description se non specificata
            if not obj.meta_description:
                obj.meta_description = seo.generate_meta_description(obj.content)
            
            # Analizza il contenuto per il punteggio SEO
            analysis = seo.analyze_content(obj.title, obj.content)
            
            # Imposta il punteggio SEO
            obj.seo_score = analysis.get('score', 0)
            
            # Imposta le keywords se non specificate
            if not obj.keywords:
                obj.keywords = ', '.join(analysis.get('keywords', []))
        
        super().save_model(request, obj, form, change)
