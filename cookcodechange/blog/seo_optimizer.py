import openai
from django.conf import settings
from typing import Dict, List

class SEOOptimizer:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def analyze_content(self, title: str, content: str, keywords: List[str] = None) -> Dict:
        """
        Analizza il contenuto del post e fornisce suggerimenti SEO
        """
        prompt = f"""Analizza il seguente contenuto del blog e fornisci suggerimenti SEO:
        Titolo: {title}
        
        Contenuto:
        {content}
        
        Keywords target (se specificate):
        {', '.join(keywords) if keywords else 'Non specificate'}
        
        Fornisci suggerimenti per:
        1. Ottimizzazione del titolo
        2. Meta description
        3. Struttura del contenuto (headings)
        4. Keywords principali da targetizzare
        5. Lunghezza e leggibilità del contenuto
        6. Internal linking suggeriti
        7. Alt text per le immagini
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "Sei un esperto SEO che analizza contenuti blog e fornisce suggerimenti dettagliati per l'ottimizzazione."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.7
            )

            return {
                'success': True,
                'analysis': response.choices[0].message.content,
                'status': 'Analisi completata'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 'Errore durante l\'analisi'
            }

    def generate_meta_description(self, content: str) -> str:
        """
        Genera una meta description ottimizzata per SEO
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "Genera una meta description SEO-friendly di massimo 155 caratteri."
                }, {
                    "role": "user",
                    "content": f"Contenuto: {content[:1000]}..."  # Limitiamo il contenuto per l'analisi
                }],
                temperature=0.7
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Errore nella generazione della meta description: {str(e)}"

    def suggest_keywords(self, content: str) -> List[str]:
        """
        Suggerisce keywords rilevanti per il contenuto
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": "Analizza il contenuto e suggerisci 5-7 keywords rilevanti per SEO."
                }, {
                    "role": "user",
                    "content": content
                }],
                temperature=0.7
            )

            # Assumiamo che la risposta sia una lista di keywords separate da virgole
            keywords = response.choices[0].message.content.split(',')
            return [k.strip() for k in keywords]

        except Exception as e:
            return [f"Errore nell'analisi delle keywords: {str(e)}"]
