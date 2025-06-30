#!/usr/bin/env python3
"""
Azure OpenAI Connection Debug Script

This script helps debug Azure OpenAI connection issues by testing:
1. Environment variables
2. Direct Azure OpenAI connection
3. Our wrapper function
"""

import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment_variables():
    """Check if Azure OpenAI environment variables are set."""
    print("=== CHECKING ENVIRONMENT VARIABLES ===")
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    print(f"AZURE_OPENAI_ENDPOINT: {endpoint[:50] + '...' if endpoint and len(endpoint) > 50 else endpoint}")
    print(f"AZURE_OPENAI_API_KEY: {'***' + api_key[-4:] if api_key and len(api_key) > 4 else 'NOT SET'}")
    print(f"AZURE_OPENAI_API_VERSION: {api_version}")
    
    if not endpoint:
        print("❌ AZURE_OPENAI_ENDPOINT is not set!")
        return False
    if not api_key:
        print("❌ AZURE_OPENAI_API_KEY is not set!")
        return False
    if not api_version:
        print("⚠️  AZURE_OPENAI_API_VERSION is not set, using default")
    
    print("✅ Environment variables look good")
    return True

async def test_direct_azure_openai():
    """Test direct connection to Azure OpenAI."""
    print("\n=== TESTING DIRECT AZURE OPENAI CONNECTION ===")
    
    try:
        from langchain_openai import AzureChatOpenAI
        
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        deployment_name = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
        
        print(f"Testing connection to: {endpoint}")
        print(f"Using deployment: {deployment_name}")
        print(f"API Version: {api_version}")
        
        # Create Azure OpenAI client
        client = AzureChatOpenAI(
            azure_deployment=deployment_name,
            azure_endpoint=endpoint,
            api_key=api_key,
            openai_api_version=api_version,
            timeout=30,  # 30 second timeout
            max_retries=1
        )
        
        # Test with a simple message
        messages = [{"role": "user", "content": "Say hello"}]
        print("Sending test message...")
        
        response = await client.ainvoke(messages)
        print(f"✅ Success! Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Direct Azure OpenAI test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Check for common error types
        if "401" in str(e) or "Unauthorized" in str(e):
            print("🔍 This looks like an authentication error - check your API key")
        elif "404" in str(e) or "NotFound" in str(e):
            print("🔍 This looks like a deployment not found error - check your deployment name")
        elif "timeout" in str(e).lower() or "connection" in str(e).lower():
            print("🔍 This looks like a network/timeout error - check your endpoint URL and network")
        elif "quota" in str(e).lower() or "rate" in str(e).lower():
            print("🔍 This looks like a rate limit or quota error - check your Azure OpenAI quotas")
        
        return False

async def test_our_wrapper():
    """Test our custom wrapper function."""
    print("\n=== TESTING OUR WRAPPER FUNCTION ===")
    
    try:
        from open_deep_research.utils import get_chat_model
        
        azure_config = {
            "azure_openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "azure_openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_openai_api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        }
        
        print("Testing our get_chat_model wrapper...")
        
        model = get_chat_model(
            model="shelle-wus-acceptance-gpt-4o-provisionedmanaged",
            model_provider="azure_openai",
            azure_config=azure_config
        )
        
        messages = [{"role": "user", "content": "Say hello"}]
        response = await model.ainvoke(messages)
        print(f"✅ Wrapper test successful! Response: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Wrapper test failed: {e}")
        return False

async def test_configuration():
    """Test the configuration loading."""
    print("\n=== TESTING CONFIGURATION ===")
    
    try:
        from open_deep_research.configuration import WorkflowConfiguration
        
        config = WorkflowConfiguration(
            planner_provider="azure_openai",
            planner_model="shelle-wus-acceptance-gpt-4o-provisionedmanaged",
            writer_provider="azure_openai",
            writer_model="shelle-wus-acceptance-gpt-4o-provisionedmanaged",
            azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview"),
        )
        
        print(f"✅ Configuration created successfully")
        print(f"   Planner: {config.planner_provider}:{config.planner_model}")
        print(f"   Writer: {config.writer_provider}:{config.writer_model}")
        print(f"   Endpoint: {config.azure_openai_endpoint[:50] + '...' if config.azure_openai_endpoint else 'None'}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def main():
    """Run all tests."""
    print("🔍 Azure OpenAI Connection Diagnostics")
    print("=" * 50)
    
    # Step 1: Check environment variables
    if not check_environment_variables():
        print("\n❌ Environment variables are not properly set. Please set them first.")
        return
    
    # Step 2: Test direct Azure OpenAI connection
    if not await test_direct_azure_openai():
        print("\n❌ Direct Azure OpenAI connection failed. Fix this before proceeding.")
        return
    
    # Step 3: Test our wrapper
    if not await test_our_wrapper():
        print("\n❌ Our wrapper function failed. This might be a code issue.")
        return
    
    # Step 4: Test configuration
    if not await test_configuration():
        print("\n❌ Configuration test failed.")
        return
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your Azure OpenAI setup should work with the main script now.")

if __name__ == "__main__":
    asyncio.run(main())
