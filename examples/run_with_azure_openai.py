#!/usr/bin/env python3
"""
Simple example script showing how to use Azure OpenAI with Open Deep Research

Before running this script, make sure you have:
1. Set up your Azure OpenAI environment variables
2. Installed all dependencies: pip install -e .

Usage:
    python examples/run_with_azure_openai.py "Your research topic here"
"""

import asyncio
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Import after loading env vars
from open_deep_research.graph import graph
from open_deep_research.configuration import WorkflowConfiguration

async def main():
    if len(sys.argv) < 2:
        topic = "The impact of artificial intelligence on renewable energy optimization"
        print(f"No topic provided, using default: {topic}")
    else:
        topic = sys.argv[1]
    
    print(f"Researching topic: {topic}")
    print("Using Azure OpenAI configuration...")
    
    # Configure to use Azure OpenAI
    config = WorkflowConfiguration(
        # Use Azure OpenAI for both planner and writer
        planner_provider="azure_openai",
        planner_model="gpt-4o",  # Replace with your deployment name
        writer_provider="azure_openai",
        writer_model="gpt-4o",   # Replace with your deployment name
        
        # Azure OpenAI settings (will use environment variables if not specified)
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
        
        # Research settings
        number_of_queries=2,
        max_search_depth=2,
        search_api="tavily",
        include_source_str=True
    )
    
    # Verify Azure OpenAI configuration
    if not config.azure_openai_endpoint or not config.azure_openai_api_key:
        print("ERROR: Azure OpenAI configuration missing!")
        print("Please set the following environment variables:")
        print("- AZURE_OPENAI_ENDPOINT")
        print("- AZURE_OPENAI_API_KEY")
        print("- AZURE_OPENAI_API_VERSION (optional)")
        return
    
    print(f"Azure OpenAI Endpoint: {config.azure_openai_endpoint}")
    print(f"Using API Version: {config.azure_openai_api_version}")
    
    try:
        # Run the research workflow
        result = await graph.ainvoke(
            {"messages": [{"role": "user", "content": f"Write a comprehensive research report about: {topic}"}]},
            config={"configurable": config.__dict__}
        )
        
        print("\n" + "="*80)
        print("RESEARCH REPORT COMPLETED")
        print("="*80)
        print(result["final_report"])
        
        if result.get("source_str"):
            print("\n" + "="*80)
            print("SOURCES USED")
            print("="*80)
            print(result["source_str"])
            
    except Exception as e:
        print(f"ERROR: Failed to generate report: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your Azure OpenAI deployment names")
        print("2. Verify your API key has proper permissions")
        print("3. Ensure your endpoint URL is correct")
        print("4. Check if your Azure region supports the requested model")

if __name__ == "__main__":
    asyncio.run(main())
