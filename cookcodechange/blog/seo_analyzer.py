import re
from typing import Dict, List
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

class SEOAnalyzer:
    def __init__(self):
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
        if not title and not content:
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
        if content:
            content_score = self._analyze_content_length(content)
            analysis['score'] += content_score['score']
            analysis['suggestions'].extend(content_score['suggestions'])

            # Analisi della leggibilità
            readability = self._analyze_readability(content)
            analysis['readability'] = readability
            analysis['suggestions'].extend(readability['suggestions'])
            analysis['score'] += readability.get('score', 0)

            # Analisi delle keywords
            if keywords:
                keyword_score = self._analyze_keywords(content, keywords)
                analysis['score'] += keyword_score['score']
                analysis['suggestions'].extend(keyword_score['suggestions'])
            else:
                # Estrai keywords automaticamente
                analysis['keywords'] = self._extract_keywords(content)
        else:
            analysis['suggestions'].append("Aggiungi del contenuto per ricevere un'analisi completa")

        # Normalizza il punteggio finale
        analysis['score'] = min(100, max(0, analysis['score']))

        return analysis

    def _analyze_title(self, title: str) -> Dict:
        """Analizza il titolo per lunghezza e presenza di keywords"""
        result = {'score': 0, 'suggestions': []}
        
        if not title:
            result['suggestions'].append('Aggiungi un titolo al post')
            return result

        # Analisi lunghezza
        if len(title) < 20:
            result['suggestions'].append('Il titolo è troppo corto (meno di 20 caratteri). Un titolo più lungo aiuta il SEO.')
        elif len(title) > 60:
            result['suggestions'].append('Il titolo è troppo lungo (più di 60 caratteri). Potrebbe essere troncato nei risultati di ricerca.')
        else:
            result['score'] += 20

        # Analisi prima lettera maiuscola
        if not title[0].isupper():
            result['suggestions'].append('Il titolo dovrebbe iniziare con una lettera maiuscola')
        else:
            result['score'] += 5

        # Analisi parole chiave nel titolo
        words = title.lower().split()
        if len(words) < 3:
            result['suggestions'].append('Usa più parole chiave nel titolo (almeno 3 parole)')
        else:
            result['score'] += 10

        # Analisi caratteri speciali
        if any(char in title for char in ['!', '@', '#', '$', '%', '^', '&', '*']):
            result['suggestions'].append('Evita caratteri speciali nel titolo')

        return result

    def _analyze_content_length(self, content: str) -> Dict:
        """Analizza la lunghezza del contenuto"""
        result = {'score': 0, 'suggestions': []}
        words = len(content.split())
        
        if words < 100:
            result['suggestions'].append('Il contenuto è molto corto (meno di 100 parole). Aggiungi più contenuto per migliorare il SEO.')
        elif words < 300:
            result['suggestions'].append('Il contenuto è corto (meno di 300 parole). Si consigliano almeno 300 parole per un buon SEO.')
            result['score'] += 10
        elif words > 2500:
            result['suggestions'].append('Il contenuto è molto lungo (più di 2500 parole). Considera di dividerlo in più articoli.')
            result['score'] += 15
        else:
            result['score'] += 25
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
                result['suggestions'].append('Le frasi sono troppo lunghe (media di {:.1f} parole). Prova a mantenerle sotto le 25 parole.'.format(avg_sentence_length))
            elif avg_sentence_length < 10:
                result['suggestions'].append('Le frasi sono molto corte (media di {:.1f} parole). Varia la lunghezza delle frasi.'.format(avg_sentence_length))
            else:
                result['score'] += 15

            paragraphs = [p for p in content.split('\n\n') if p.strip()]
            if len(paragraphs) < 3:
                result['suggestions'].append('Aggiungi più paragrafi per migliorare la leggibilità (minimo 3 paragrafi)')
            else:
                result['score'] += 10

            # Analisi varietà del vocabolario
            unique_words = len(set(w.lower() for w in words if w.isalnum()))
            if unique_words < len(words) * 0.4:
                result['suggestions'].append('Usa un vocabolario più vario per rendere il contenuto più interessante')
            else:
                result['score'] += 10
            
        except Exception as e:
            result['suggestions'].append('Non è stato possibile analizzare la leggibilità del testo')
            print(f"Errore durante l'analisi della leggibilità: {str(e)}")

        return result

    def _analyze_keywords(self, content: str, keywords: List[str]) -> Dict:
        """Analizza la densità e il posizionamento delle keywords"""
        result = {'score': 0, 'suggestions': []}
        
        content_lower = content.lower()
        total_words = len(content_lower.split())
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = content_lower.count(keyword_lower)
            density = (count / total_words) * 100
            
            if density < 0.5:
                result['suggestions'].append(f'La keyword "{keyword}" appare troppo poco nel testo (densità {density:.1f}%). Prova ad usarla di più.')
            elif density > 2.5:
                result['suggestions'].append(f'La keyword "{keyword}" appare troppo spesso nel testo (densità {density:.1f}%). Riduci la frequenza.')
            else:
                result['score'] += 10

            # Controlla se la keyword appare all'inizio
            first_paragraph = content_lower.split('\n\n')[0] if '\n\n' in content_lower else content_lower
            if keyword_lower not in first_paragraph:
                result['suggestions'].append(f'Prova ad utilizzare la keyword "{keyword}" nel primo paragrafo')

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
