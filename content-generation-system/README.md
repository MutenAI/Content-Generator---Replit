# Content Generation System with CrewAI - POC

**PROPRIETÀ DI FYLLE SRL**  
**SVILUPPATO PER SIEBERT FINANCIAL CORP**

Questo Proof of Concept (POC) è stato sviluppato per validare il concetto di Multi Agent System nella generazione automatica di contenuti finanziari. Utilizza CrewAI con tre agenti specializzati per generare contenuti allineati allo stile di un brand.

## Architettura del Sistema

```
content-generation-system/
├── .env                       # API keys (OpenAI, Anthropic, Serper)
├── main.py                    # Script principale
├── requirements.txt           # Dipendenze
├── reference/                 # Directory per file markdown di riferimento
├── output/                    # Directory per contenuti generati
└── src/
    ├── __init__.py
    ├── agents.py              # Definizione dei tre agenti
    ├── tools.py               # Web search e markdown parser
    ├── tasks.py               # Definizione sequenza task
    └── utils.py               # Funzioni di utilità
```

## Prerequisiti

- Python 3.8+
- Account OpenAI con API key
- Account Anthropic con API key 
- Account Serper.dev con API key

## Installazione

1. Clona questo repository
2. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

3. Configura il file `.env` con le tue API key:

```
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
SERPER_API_KEY=your-serper-api-key
```

## Utilizzo

Per generare contenuti su un argomento specifico:

```bash
python main.py --topic "Strategie di investimento per millennials" --reference "reference/siebert-system-brief-optimized.md"
```

Parametri:
- `--topic`: L'argomento su cui generare il contenuto
- `--reference`: Il percorso del file markdown di riferimento per lo stile del contenuto
- `--output`: Directory dove salvare l'output (default: "output")

## Flusso di Lavoro

1. Il Web Searcher (OpenAI) esegue la ricerca e produce un summary strutturato
2. Il Copywriter (Anthropic) crea un articolo basato sul summary
3. L'Editor ottimizza l'articolo per allinearlo allo stile e tono del file di riferimento
4. Il risultato finale viene salvato come file markdown nella directory di output

## Personalizzazione

### Aggiungere Nuovi File di Riferimento

Puoi aggiungere qualsiasi file markdown nella directory `reference/` e specificarlo come parametro `--reference` quando esegui lo script.

### Modificare gli Agenti

Gli agenti possono essere personalizzati modificando il file `src/agents.py`. Puoi:
- Cambiare i modelli LLM utilizzati
- Modificare i role, goal e backstory
- Aggiungere ulteriori strumenti

## Note

- Il sistema è progettato per funzionare con API key valide
- Le ricerche web utilizzano l'API di Serper.dev che ha un limite di utilizzo gratuito
- I contenuti generati sono salvati con un timestamp per evitare sovrascritture 