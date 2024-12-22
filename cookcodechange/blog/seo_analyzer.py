import re
from typing import Dict, List
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

class SEOAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))

    def analyze_content(self, title: str, content: str, keywords: List[str] = None) -> Dict:
        """
        Analizza il contenuto e fornisce suggerimenti SEO
        """
        if not title or not content:
            return {
                'success': True,
                'score': 0,
                'suggestions': ['Aggiungi titolo e contenuto per l\'analisi SEO'],
                'keywords': []
            }

        analysis = {
            'success': True,
            'score': 0,
            'suggestions': [],
            'keywords': [],
            'readability': {}
        }

        # Analisi del titolo
        title_score = self._analyze_title(title)
        analysis['score'] += title_score['score']
        analysis['suggestions'].extend(title_score['suggestions'])

        # Analisi del contenuto
        content_score = self._analyze_content_length(content)
        analysis['score'] += content_score['score']
        analysis['suggestions'].extend(content_score['suggestions'])

        # Analisi della leggibilità
        readability = self._analyze_readability(content)
        analysis['readability'] = readability
        analysis['suggestions'].extend(readability['suggestions'])

        # Analisi delle keywords
        if keywords:
            keyword_score = self._analyze_keywords(content, keywords)
            analysis['score'] += keyword_score['score']
            analysis['suggestions'].extend(keyword_score['suggestions'])
        else:
            # Estrai keywords automaticamente
            analysis['keywords'] = self._extract_keywords(content)

        # Normalizza il punteggio finale
        analysis['score'] = min(100, max(0, analysis['score']))

        return analysis

    def _analyze_title(self, title: str) -> Dict:
        """Analizza il titolo per lunghezza e presenza di keywords"""
        result = {'score': 0, 'suggestions': []}
        
        if len(title) < 10:
            result['suggestions'].append('Il titolo è troppo corto. Dovrebbe essere almeno 10 caratteri.')
        elif len(title) > 60:
            result['suggestions'].append('Il titolo è troppo lungo. Dovrebbe essere massimo 60 caratteri.')
        else:
            result['score'] += 20

        if title[0].isupper():
            result['score'] += 5
        else:
            result['suggestions'].append('Il titolo dovrebbe iniziare con una lettera maiuscola.')

        return result

    def _analyze_content_length(self, content: str) -> Dict:
        """Analizza la lunghezza del contenuto"""
        result = {'score': 0, 'suggestions': []}
        words = len(content.split())
        
        if words < 300:
            result['suggestions'].append('Il contenuto è troppo corto. Si consigliano almeno 300 parole.')
        elif words > 2500:
            result['suggestions'].append('Il contenuto è molto lungo. Considera di dividerlo in più articoli.')
        else:
            result['score'] += 20
            if words >= 600:
                result['score'] += 10

        return result

    def _analyze_readability(self, content: str) -> Dict:
        """Analizza la leggibilità del testo"""
        result = {
            'score': 0,
            'suggestions': [],
            'stats': {}
        }

        try:
            sentences = sent_tokenize(content)
            words = word_tokenize(content)
            avg_sentence_length = len(words) / max(len(sentences), 1)

            result['stats']['avg_sentence_length'] = avg_sentence_length
            
            if avg_sentence_length > 25:
                result['suggestions'].append('Le frasi sono troppo lunghe. Prova a mantenerle sotto i 25 parole.')
            else:
                result['score'] += 15

            paragraphs = content.split('\n\n')
            if len(paragraphs) < 3:
                result['suggestions'].append('Aggiungi più paragrafi per migliorare la leggibilità.')
            
        except Exception as e:
            result['suggestions'].append('Non è stato possibile analizzare la leggibilità del testo.')
            print(f"Errore durante l'analisi della leggibilità: {str(e)}")

        return result

    def _analyze_keywords(self, content: str, keywords: List[str]) -> Dict:
        """Analizza la densità e il posizionamento delle keywords"""
        result = {'score': 0, 'suggestions': []}
        
        content_lower = content.lower()
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            density = count / len(content_lower.split()) * 100
            
            if density < 0.5:
                result['suggestions'].append(f'La keyword "{keyword}" appare troppo poco nel testo.')
            elif density > 2.5:
                result['suggestions'].append(f'La keyword "{keyword}" appare troppo spesso nel testo.')
            else:
                result['score'] += 10

        return result

    def _extract_keywords(self, content: str) -> List[str]:
        """Estrae automaticamente le keywords più rilevanti dal contenuto"""
        try:
            words = word_tokenize(content.lower())
            
            # Rimuovi stopwords e parole corte
            words = [word for word in words if word.isalnum() and 
                    word not in self.stop_words and 
                    len(word) > 3]
            
            # Conta le occorrenze
            word_freq = Counter(words)
            
            # Prendi le 5 parole più frequenti
            return [word for word, _ in word_freq.most_common(5)]
        except Exception as e:
            print(f"Errore durante l'estrazione delle keywords: {str(e)}")
            return []

    def generate_meta_description(self, content: str) -> str:
        """
        Genera una meta description basata sul contenuto
        """
        try:
            sentences = sent_tokenize(content)
            if not sentences:
                return ""
            
            # Prendi la prima frase e accorciala se necessario
            description = sentences[0]
            if len(description) > 155:
                description = description[:152] + "..."
            
            return description
        except Exception as e:
            print(f"Errore durante la generazione della meta description: {str(e)}")
            return content[:155] + "..." if content else ""
