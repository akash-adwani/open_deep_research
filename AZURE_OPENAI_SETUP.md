# Using Azure OpenAI with Open Deep Research

This repository has been updated to support Azure OpenAI alongside the existing providers (Anthropic, OpenAI, etc.). Here's how to configure and use Azure OpenAI:

## Configuration

### Environment Variables

Set the following environment variables to use Azure OpenAI:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### Using Azure OpenAI Models

To use Azure OpenAI models, set the model provider to `azure_openai` and specify your deployment name:

#### Workflow Configuration Example

```python
from open_deep_research.configuration import WorkflowConfiguration

config = WorkflowConfiguration(
    planner_provider="azure_openai",
    planner_model="your-gpt-4-deployment-name",
    writer_provider="azure_openai", 
    writer_model="your-gpt-4-deployment-name",
    azure_openai_endpoint="https://your-resource.openai.azure.com/",
    azure_openai_api_key="your-azure-openai-api-key",
    azure_openai_api_version="2024-02-15-preview"
)
```

#### Multi-Agent Configuration Example

```python
from open_deep_research.configuration import MultiAgentConfiguration

config = MultiAgentConfiguration(
    supervisor_model="azure_openai:your-gpt-4-deployment-name",
    researcher_model="azure_openai:your-gpt-4-deployment-name",
    azure_openai_endpoint="https://your-resource.openai.azure.com/",
    azure_openai_api_key="your-azure-openai-api-key",
    azure_openai_api_version="2024-02-15-preview"
)
```

## Model Deployment Names

Make sure you have deployed models in your Azure OpenAI resource. Common deployments might include:
- `gpt-4o` for GPT-4 Omni
- `gpt-4-turbo` for GPT-4 Turbo
- `gpt-35-turbo` for GPT-3.5 Turbo

The `planner_model` and `writer_model` should reference your actual deployment names, not the base model names.

## Fallback Behavior

If Azure OpenAI credentials are not provided or incomplete, the system will automatically fall back to using regular OpenAI with the specified model names.

## Configuration Priority

Configuration values are resolved in this order:
1. Explicitly passed parameters
2. Environment variables (e.g., `AZURE_OPENAI_ENDPOINT`)
3. Default values

## Example Usage

```python
import asyncio
from open_deep_research.graph import graph
from open_deep_research.configuration import WorkflowConfiguration

async def main():
    config = WorkflowConfiguration(
        planner_provider="azure_openai",
        planner_model="gpt-4o",  # Your deployment name
        writer_provider="azure_openai",
        writer_model="gpt-4o",   # Your deployment name
    )
    
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": "Write a report about renewable energy"}]},
        config={"configurable": config.__dict__}
    )
    
    print(result["final_report"])

if __name__ == "__main__":
    asyncio.run(main())
```

## Environment Setup

You can also set up a `.env` file in your project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-azure-openai-api-key
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

Then load it in your application:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Troubleshooting

1. **Authentication Errors**: Ensure your API key is correct and has proper permissions
2. **Deployment Not Found**: Verify your deployment names match exactly what's configured in Azure
3. **Rate Limiting**: Azure OpenAI has different rate limits than OpenAI - adjust accordingly
4. **Regional Availability**: Some models may not be available in all Azure regions

## Mixed Provider Usage

You can also mix providers within the same configuration:

```python
config = WorkflowConfiguration(
    planner_provider="azure_openai",
    planner_model="gpt-4o",
    writer_provider="anthropic", 
    writer_model="claude-3-5-sonnet-latest",
    azure_openai_endpoint="https://your-resource.openai.azure.com/",
    azure_openai_api_key="your-azure-openai-api-key"
)
```
