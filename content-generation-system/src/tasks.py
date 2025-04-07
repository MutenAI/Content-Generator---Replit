from crewai import Task

def create_tasks(agents, topic):
    """Crea la sequenza di task per gli agenti."""
    
    # Task 1: Web Research
    research_task = Task(
        description=f"Research thoroughly on the topic: '{topic}'. Find current, accurate information and summarize the key points in a structured format. Your task is to provide a comprehensive research summary in markdown format. Include key points, facts, and insights on the topic. Use your web search tool to gather current and accurate information. Output format: markdown",
        expected_output="A comprehensive research summary in markdown format with key points, facts, and insights on the topic.",
        agent=agents["web_searcher"],
        async_execution=False
    )
    
    # Task 2: Content Creation
    writing_task = Task(
        description=f"Create engaging and informative content about '{topic}' based on the research summary. Based on the research provided by the Web Research Specialist, create an engaging and informative article in markdown format. Structure the content with clear headings, subheadings, and a logical flow. Make it accessible and interesting for the target audience.",
        expected_output="A well-structured article/blog post in markdown format.",
        agent=agents["copywriter"],
        async_execution=False,
        dependencies=[research_task]
    )
    
    # Task 3: Content Optimization
    editing_task = Task(
        description=f"Optimize the content about '{topic}' to align with the brand voice and style from the reference document. Make sure it follows the format and structure of the reference document while maintaining factual accuracy. Use the markdown_reference tool to access the reference document's tone, style, and structure. Adapt the article to match this style while preserving the factual content. Ensure the content follows the brand's preferred terminology, voice, and formatting. Check for consistency in style throughout the document.",
        expected_output="The final polished content in markdown format, aligned with the brand voice.",
        agent=agents["editor"],
        async_execution=False,
        dependencies=[writing_task]
    )
    
    return [research_task, writing_task, editing_task] 