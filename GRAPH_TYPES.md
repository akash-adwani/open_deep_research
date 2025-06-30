# Graph Types and Input Formats

This repository contains three different graph implementations with different input formats:

## 1. Graph Implementation (`graph.py`)
- **Graph Name**: `open_deep_research`
- **File**: `./src/open_deep_research/graph.py:graph`
- **Expected Input**: 
  ```python
  {"topic": "Your research topic here"}
  ```
- **Use Case**: Single-threaded workflow with structured planning phase

## 2. Multi-Agent Implementation (`multi_agent.py`)
- **Graph Name**: `open_deep_research_multi_agent` 
- **File**: `./src/open_deep_research/multi_agent.py:graph`
- **Expected Input**:
  ```python
  {"messages": [{"role": "user", "content": "Your research request here"}]}
  ```
- **Use Case**: Multi-agent parallel processing with supervisor coordination

## 3. Workflow Implementation (`workflow.py`)
- **Graph Name**: `odr_workflow_v2`
- **File**: `./src/open_deep_research/workflow/workflow.py:workflow`
- **Expected Input**:
  ```python
  {"messages": [{"role": "user", "content": "Your research request here"}]}
  ```
- **Use Case**: Advanced workflow with human-in-the-loop feedback

## Common Mistakes

### ❌ Wrong Input Format
```python
# WRONG: Using messages input for graph implementation
result = await graph.ainvoke(
    {"messages": [{"role": "user", "content": "Research topic"}]},
    config={"configurable": config.__dict__}
)
```

### ✅ Correct Input Format
```python
# CORRECT: Using topic input for graph implementation
result = await graph.ainvoke(
    {"topic": "Research topic"},
    config={"configurable": config.__dict__}
)
```

## How to Choose the Right Implementation

1. **Use `graph.py`** if you want:
   - Simple, direct topic-to-report generation
   - Single-threaded processing
   - Straightforward configuration

2. **Use `multi_agent.py`** if you want:
   - Faster parallel processing
   - Chat-like interaction
   - Multiple agents working simultaneously

3. **Use `workflow.py`** if you want:
   - Human feedback in the loop
   - More control over the research process
   - Iterative refinement

## Azure OpenAI Configuration

All three implementations support Azure OpenAI with the same configuration:

```python
config = WorkflowConfiguration(
    planner_provider="azure_openai",
    planner_model="your-deployment-name",
    writer_provider="azure_openai", 
    writer_model="your-deployment-name",
    azure_openai_endpoint="https://your-resource.openai.azure.com/",
    azure_openai_api_key="your-api-key",
    azure_openai_api_version="2024-02-15-preview"
)
```
