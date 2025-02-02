from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils.safestring import mark_safe
from .models import Post, Tag, Resource, StaticPage
import json

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_posts_count')
    search_fields = ('name',)
    list_per_page = 20
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    get_posts_count.short_description = 'Posts'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_url_link', 'description')
    search_fields = ('title', 'description')
    list_per_page = 20
    
    def get_url_link(self, obj):
        return mark_safe(f'<a href="{obj.url}" target="_blank">{obj.url}</a>')
    get_url_link.short_description = 'URL'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_category_display', 'get_tags_count', 'created_at', 'updated_at', 'seo_score', 'get_image_thumbnail')
    list_filter = ('category', 'tags', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)
    readonly_fields = ('seo_score', 'created_at', 'updated_at', 'get_image_preview')
    ordering = ('-created_at',)
    list_per_page = 20

    fieldsets = (
        ('Contenu', {
            'fields': (
                'title',
                'content',
                ('category', 'tags'),
                ('image', 'get_image_preview'),
                ('created_at', 'updated_at'),
            )
        }),
        ('SEO', {
            'fields': ('seo_title', 'meta_description', 'keywords', 'seo_score'),
            'classes': ('collapse',),
            'description': 'Ces champs sont générés automatiquement mais peuvent être modifiés manuellement.'
        }),
    )

    def get_category_display(self, obj):
        return obj.get_category_display()
    get_category_display.short_description = 'Catégorie'
    get_category_display.admin_order_field = 'category'

    def get_tags_count(self, obj):
        return obj.tags.count()
    get_tags_count.short_description = 'Tags'

    def get_image_thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return ''
    get_image_thumbnail.short_description = 'Image'

    def get_image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" style="max-height: 200px; object-fit: contain;" />')
        return ''
    get_image_preview.short_description = 'Image Preview'

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

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('get_page_type_display', 'title', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        (None, {
            'fields': (
                'page_type',
                'title',
                'subtitle',
                'content',
                'updated_at',
            )
        }),
    )

    def has_add_permission(self, request):
        # Controlla se esistono già tutte le pagine statiche
        existing_count = StaticPage.objects.count()
        return existing_count < len(StaticPage.PAGE_CHOICES)

    def has_delete_permission(self, request, obj=None):
        # Impedisce l'eliminazione delle pagine statiche
        return False

    def has_add_permission(self, request):
        # Controlla se esistono già tutte le pagine statiche
        existing_count = StaticPage.objects.count()
        return existing_count < len(StaticPage.PAGE_CHOICES)

    def has_delete_permission(self, request, obj=None):
        # Impedisce l'eliminazione delle pagine statiche
        return False