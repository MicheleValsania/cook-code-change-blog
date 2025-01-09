# blog/templatetags/blog_filters.py

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter
def first_letter_content(content):
    """Estrae la prima lettera dal contenuto HTML"""
    # Rimuove i tag HTML
    clean_text = strip_tags(content)
    # Prende la prima lettera
    first_letter = clean_text[0] if clean_text else ''
    return mark_safe(first_letter)

@register.filter
def remaining_content(content):
    """Restituisce il contenuto HTML senza la prima lettera"""
    # Rimuove i tag HTML per trovare la prima lettera
    clean_text = strip_tags(content)
    if not clean_text:
        return ''
    
    # Trova la posizione della prima lettera nel testo HTML originale
    first_letter = clean_text[0]
    pattern = re.escape(first_letter)
    
    # Sostituisce solo la prima occorrenza della lettera
    modified_content = re.sub(pattern, '', content, count=1)
    return mark_safe(modified_content)
