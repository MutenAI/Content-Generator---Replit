import os
import requests
import json
from langchain.tools import Tool

class WebSearchTool:
    """Tool per la ricerca web via Serper.dev."""
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    def search(self, query):
        """Esegue una ricerca web e restituisce un riassunto strutturato."""
        try:
            print(f"\nEseguendo ricerca web per: '{query}'")
            print(f"Utilizzo chiave API Serper: {self.api_key[:5]}...{self.api_key[-5:]}")
            
            headers = {
                'X-API-KEY': self.api_key,
                'Content-Type': 'application/json'
            }
            
            payload = {
                'q': query,
                'num': 5  # Numero di risultati
            }
            
            print("Inviando richiesta a Serper.dev...")
            response = requests.post(
                'https://google.serper.dev/search',
                headers=headers,
                json=payload
            )
            
            print(f"Codice di risposta: {response.status_code}")
            
            if response.status_code != 200:
                return f"Errore nella ricerca web: status code {response.status_code}. Risposta: {response.text}"
            
            results = response.json()
            print(f"Ricevuti risultati da Serper.dev. Struttura della risposta: {list(results.keys())}")
            
            # Formatta i risultati in un riassunto strutturato
            summary = f"## Research Summary: {query}\n\n"
            
            if 'organic' in results and results['organic']:
                summary += "### Key Information:\n\n"
                
                for item in results['organic'][:5]:
                    title = item.get('title', 'No Title')
                    snippet = item.get('snippet', 'No description')
                    link = item.get('link', '#')
                    
                    summary += f"**{title}**\n"
                    summary += f"{snippet}\n"
                    summary += f"Source: {link}\n\n"
            else:
                summary += "### Warning: No organic search results found.\n\n"
            
            if 'knowledgeGraph' in results:
                kg = results['knowledgeGraph']
                if 'description' in kg:
                    summary += f"### Overview:\n{kg['description']}\n\n"
            
            summary += "### Summary of Findings:\n"
            
            if 'organic' in results and results['organic']:
                # Estrai punti chiave dai primi risultati
                summary += "Based on the search results, here are the key insights on this topic:\n\n"
                
                # Aggiunta di informazioni reali invece di placeholder
                insights = []
                for i, item in enumerate(results['organic'][:3]):
                    insight = f"{i+1}. {item.get('title', 'Key insight')}: {item.get('snippet', 'Important information from the search')}"
                    insights.append(insight)
                
                summary += "\n".join(insights)
            else:
                summary += "Non sono stati trovati risultati significativi per questa ricerca.\n"
                summary += "1. [Ricerca non ha prodotto risultati rilevanti]\n"
                summary += "2. [Potrebbe essere necessario riformulare la query]\n"
                summary += "3. [Prova una ricerca più specifica]\n"
            
            print("Ricerca completata con successo.")
            return summary
        
        except Exception as e:
            error_message = f"Error performing web search: {str(e)}"
            print(f"ERRORE nella ricerca web: {error_message}")
            import traceback
            print(f"Dettagli dell'errore:\n{traceback.format_exc()}")
            return error_message
    
    def get_tool(self):
        """Restituisce un oggetto Tool per l'integrazione con CrewAI."""
        return Tool(
            name="web_search",
            func=self.search,
            description="Search the web for comprehensive information on a topic. Returns a structured summary of findings."
        )


class MarkdownParserTool:
    """Tool per analizzare un file markdown di riferimento."""
    
    def __init__(self, file_path):
        self.file_path = file_path
        
    def get_content(self, section=None):
        """Legge il contenuto del file markdown, opzionalmente filtrando per sezione."""
        try:
            print(f"\nLeggendo file markdown: {self.file_path}")
            print(f"Sezione richiesta: {section if section else 'intero documento'}")
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"Letto file markdown di {len(content)} caratteri")
            
            if not section:
                return content
            
            # Parsing semplice per trovare sezioni nel markdown
            import re
            
            # Cerca sezioni di livello 2 (##)
            pattern = rf"## {re.escape(section)}(.*?)(?=\n## |\Z)"
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                result = f"## {section}{match.group(1)}"
                print(f"Trovata sezione '{section}' di livello 2 nel documento")
                return result
            else:
                # Cerca sezioni di livello 3 (###)
                pattern = rf"### {re.escape(section)}(.*?)(?=\n### |\n## |\Z)"
                match = re.search(pattern, content, re.DOTALL)
                
                if match:
                    result = f"### {section}{match.group(1)}"
                    print(f"Trovata sezione '{section}' di livello 3 nel documento")
                    return result
                else:
                    print(f"Sezione '{section}' non trovata nel documento")
                    return f"Section '{section}' not found in the reference document."
        
        except Exception as e:
            error_message = f"Error reading markdown file: {str(e)}"
            print(f"ERRORE nella lettura del file markdown: {error_message}")
            import traceback
            print(f"Dettagli dell'errore:\n{traceback.format_exc()}")
            return error_message
    
    def get_tool(self):
        """Restituisce un oggetto Tool per l'integrazione con CrewAI."""
        return Tool(
            name="markdown_reference",
            func=self.get_content,
            description="Get content from the reference markdown file. Optionally specify a section name to get only that part."
        ) 