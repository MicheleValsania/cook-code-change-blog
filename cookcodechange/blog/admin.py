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
            'classes': ('collapse',)
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
