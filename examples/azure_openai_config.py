"""
Example configuration for using Azure OpenAI with Open Deep Research

This example shows how to configure the system to use Azure OpenAI models
instead of the default Anthropic Claude models.
"""

import os
from open_deep_research.configuration import WorkflowConfiguration, MultiAgentConfiguration

# Azure OpenAI Workflow Configuration Example
azure_workflow_config = WorkflowConfiguration(
    # Use Azure OpenAI for planning
    planner_provider="azure_openai",
    planner_model="gpt-4o",  # Replace with your actual deployment name
    
    # Use Azure OpenAI for writing
    writer_provider="azure_openai", 
    writer_model="gpt-4o",  # Replace with your actual deployment name
    
    # Azure OpenAI connection details
    azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
    
    # Other configuration options
    number_of_queries=3,
    max_search_depth=2,
    search_api="tavily"
)

# Azure OpenAI Multi-Agent Configuration Example
azure_multiagent_config = MultiAgentConfiguration(
    # Use Azure OpenAI for both supervisor and researcher
    supervisor_model="azure_openai:gpt-4o",  # Format: provider:deployment_name
    researcher_model="azure_openai:gpt-4o",  # Format: provider:deployment_name
    
    # Azure OpenAI connection details
    azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
    
    # Other configuration options
    number_of_queries=2,
    search_api="tavily"
)

# Mixed Provider Configuration Example (Azure + Anthropic)
mixed_config = WorkflowConfiguration(
    # Use Azure OpenAI for planning
    planner_provider="azure_openai",
    planner_model="gpt-4o",
    
    # Use Anthropic for writing
    writer_provider="anthropic",
    writer_model="claude-3-5-sonnet-latest",
    
    # Only Azure config needed since we're using Azure for planner
    azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
)

# Example usage in a script
if __name__ == "__main__":
    # You can use any of these configurations with the graph
    import asyncio
    from open_deep_research.graph import graph
    
    async def run_example():
        result = await graph.ainvoke(
            {"messages": [{"role": "user", "content": "Write a report about AI safety"}]},
            config={"configurable": azure_workflow_config.__dict__}
        )
        print("Generated report:", result["final_report"])
    
    # Uncomment to run
    # asyncio.run(run_example())
