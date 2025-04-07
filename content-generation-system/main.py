import os
import argparse
from dotenv import load_dotenv
from crewai import Crew

from src.agents import AgentsFactory
from src.tools import WebSearchTool, MarkdownParserTool
from src.tasks import create_tasks
from src.utils import ensure_directory_exists, generate_output_filename

def main():
    """Funzione principale che orchestratra il processo di generazione contenuti."""
    # Carica variabili d'ambiente
    load_dotenv()
    
    # Parser argomenti da riga di comando
    parser = argparse.ArgumentParser(description="Generate optimized content on any topic")
    parser.add_argument("--topic", required=True, help="Topic for content generation")
    parser.add_argument("--reference", required=True, help="Path to reference markdown file")
    parser.add_argument("--output", default="output", help="Directory for output")
    
    args = parser.parse_args()
    
    # Verifica esistenza file di riferimento
    if not os.path.exists(args.reference):
        print(f"Error: Reference file '{args.reference}' not found.")
        return
    
    # Crea directory output se non esiste
    output_dir = ensure_directory_exists(args.output)
    
    # Inizializza tool
    web_search_tool = WebSearchTool(api_key=os.getenv("SERPER_API_KEY")).get_tool()
    markdown_tool = MarkdownParserTool(file_path=args.reference).get_tool()
    
    # Crea agenti
    agents_factory = AgentsFactory(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    agents = agents_factory.create_agents(web_search_tool, markdown_tool)
    
    # Crea tasks
    tasks = create_tasks(agents, args.topic)
    
    # Crea e avvia crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True
    )
    
    print(f"Starting content generation for topic: '{args.topic}'")
    print(f"Using reference file: {args.reference}")
    
    # Esegui crew e ottieni risultato
    result = crew.kickoff()
    
    # Salva l'output
    output_file = generate_output_filename(args.topic, output_dir)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Content generation completed! Output saved to: {output_file}")

if __name__ == "__main__":
    main() 