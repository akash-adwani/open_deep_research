import os
from enum import Enum
from dataclasses import dataclass, fields, field
from typing import Any, Optional, Dict, Literal

from langchain_core.runnables import RunnableConfig

DEFAULT_REPORT_STRUCTURE = """Use this structure to create a report on the user-provided topic:

1. Introduction (no research needed)
   - Brief overview of the topic area

2. Main Body Sections:
   - Each section should focus on a sub-topic of the user-provided topic
   
3. Conclusion
   - Aim for 1 structural element (either a list or table) that distills the main body sections 
   - Provide a concise summary of the report"""

class SearchAPI(Enum):
    PERPLEXITY = "perplexity"
    TAVILY = "tavily"
    EXA = "exa"
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    LINKUP = "linkup"
    DUCKDUCKGO = "duckduckgo"
    GOOGLESEARCH = "googlesearch"
    NONE = "none"

@dataclass(kw_only=True)
class WorkflowConfiguration:
    """Configuration for the workflow/graph-based implementation (graph.py)."""
    # Common configuration
    report_structure: str = DEFAULT_REPORT_STRUCTURE
    search_api: SearchAPI = SearchAPI.NONE
    search_api_config: Optional[Dict[str, Any]] = None
    process_search_results: Literal["summarize", "split_and_rerank"] | None = None
    summarization_model_provider: str = "azure_openai"
    summarization_model: str = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
    max_structured_output_retries: int = 3
    include_source_str: bool = False
    
    # Workflow-specific configuration
    number_of_queries: int = 2 # Number of search queries to generate per iteration
    max_search_depth: int = 2 # Maximum number of reflection + search iterations
    planner_provider: str = "azure_openai"
    planner_model: str = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
    planner_model_kwargs: Optional[Dict[str, Any]] = None
    writer_provider: str = "azure_openai"
    writer_model: str = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
    writer_model_kwargs: Optional[Dict[str, Any]] = None
    
    # Azure OpenAI configuration
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_api_version: Optional[str] = "2024-08-01-preview"

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "WorkflowConfiguration":
        """Create a WorkflowConfiguration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {}
        
        for f in fields(cls):
            if f.init:
                field_name = f.name
                # Handle Azure OpenAI specific environment variable names
                if field_name == "azure_openai_endpoint":
                    env_value = os.environ.get("AZURE_OPENAI_ENDPOINT")
                elif field_name == "azure_openai_api_key":
                    env_value = os.environ.get("AZURE_OPENAI_API_KEY")
                elif field_name == "azure_openai_api_version":
                    env_value = os.environ.get("AZURE_OPENAI_API_VERSION")
                else:
                    env_value = os.environ.get(field_name.upper())
                
                config_value = configurable.get(field_name)
                values[field_name] = env_value or config_value
        
        return cls(**{k: v for k, v in values.items() if v is not None})

@dataclass(kw_only=True)
class MultiAgentConfiguration:
    """Configuration for the multi-agent implementation (multi_agent.py)."""
    # Common configuration
    search_api: SearchAPI = SearchAPI.NONE #SearchAPI.TAVILY
    search_api_config: Optional[Dict[str, Any]] = None
    process_search_results: Literal["summarize", "split_and_rerank"] | None = None
    summarization_model_provider: str = "azure_openai"
    summarization_model: str = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
    include_source_str: bool = False
    
    # Multi-agent specific configuration
    number_of_queries: int = 2 # Number of search queries to generate per section
    supervisor_model: str = "azure_openai:shelle-wus-acceptance-gpt-4o-provisionedmanaged"
    researcher_model: str = "azure_openai:shelle-wus-acceptance-gpt-4o-provisionedmanaged"
    ask_for_clarification: bool = False # Whether to ask for clarification from the user
    # MCP server configuration
    mcp_server_config: Optional[Dict[str, Any]] = None
    mcp_prompt: Optional[str] = None
    mcp_tools_to_include: Optional[list[str]] = None
    
    # Azure OpenAI configuration
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_api_version: Optional[str] = "2024-08-01-preview"
    

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "MultiAgentConfiguration":
        """Create a MultiAgentConfiguration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {}
        
        for f in fields(cls):
            if f.init:
                field_name = f.name
                # Handle Azure OpenAI specific environment variable names
                if field_name == "azure_openai_endpoint":
                    env_value = os.environ.get("AZURE_OPENAI_ENDPOINT")
                elif field_name == "azure_openai_api_key":
                    env_value = os.environ.get("AZURE_OPENAI_API_KEY")
                elif field_name == "azure_openai_api_version":
                    env_value = os.environ.get("AZURE_OPENAI_API_VERSION")
                else:
                    env_value = os.environ.get(field_name.upper())
                
                config_value = configurable.get(field_name)
                values[field_name] = env_value or config_value
        
        return cls(**{k: v for k, v in values.items() if v is not None})

# Keep the old Configuration class for backward compatibility
Configuration = WorkflowConfiguration
