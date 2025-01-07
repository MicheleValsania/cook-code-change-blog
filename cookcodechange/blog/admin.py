from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from .models import Post, Tag
import json

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

    def save_model(self, request, obj, form, change):
        print("AdminModel: Starting save_model...")
        super().save_model(request, obj, form, change)
        print("AdminModel: save_model completed")

    def analyze_seo_view(self, request):
        if request.method == 'POST':
            try:
                print("AdminModel: Starting analyze_seo_view...")
                data = json.loads(request.body)
                title = data.get('title', '')
                content = data.get('content', '')
                
                # Creiamo un oggetto Post temporaneo per usare i suoi metodi
                temp_post = Post(title=title, content=content)
                score = temp_post._calculate_seo_score()
                
                return JsonResponse({
                    'success': True,
                    'score': score,
                    'suggestions': [
                        f'Lunghezza titolo: {len(title)} caratteri',
                        f'Lunghezza contenuto: {len(content.split())} parole'
                    ]
                })
            except Exception as e:
                print(f"AdminModel Error: {str(e)}")
                return JsonResponse({
                    'success': False, 
                    'error': str(e)
                }, status=400)