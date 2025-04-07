from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class AgentsFactory:
    """Factory per creare i tre agenti specializzati."""
    
    def __init__(self, openai_api_key, anthropic_api_key):
        self.openai_api_key = openai_api_key
        self.anthropic_api_key = anthropic_api_key
        
    def create_agents(self, web_search_tool, markdown_tool):
        """Crea i tre agenti con i loro rispettivi tool."""
        
        # 1. Web Searcher (OpenAI)
        web_searcher = Agent(
            role="Web Research Specialist",
            goal="Produce comprehensive, accurate, and up-to-date summaries on requested topics",
            backstory="You are an expert researcher who finds the most relevant and current information on any topic.",
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(
                temperature=0,
                model_name="gpt-4o",
                api_key=self.openai_api_key
            ),
            tools=[web_search_tool]
        )
        
        # 2. Copywriter (Anthropic)
        copywriter = Agent(
            role="Content Copywriter",
            goal="Create engaging, informative content based on research summaries",
            backstory="You are a skilled writer who transforms research into compelling articles.",
            verbose=True,
            allow_delegation=False,
            llm=ChatAnthropic(
                temperature=0.7,
                model_name="claude-3-opus-20240229",
                api_key=self.anthropic_api_key
            )
        )
        
        # 3. Editor
        editor = Agent(
            role="Content Editor and Brand Aligner",
            goal="Optimize content to match brand voice and style from reference documents",
            backstory="You are an expert editor who ensures content aligns perfectly with brand guidelines.",
            verbose=True,
            allow_delegation=False,
            llm=ChatOpenAI(
                temperature=0.2,
                model_name="gpt-4o",
                api_key=self.openai_api_key
            ),
            tools=[markdown_tool]
        )
        
        return {
            "web_searcher": web_searcher,
            "copywriter": copywriter,
            "editor": editor
        } 