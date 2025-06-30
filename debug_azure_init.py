#!/usr/bin/env python3
"""
Debug script to test Azure OpenAI initialization
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def test_direct_azure_openai():
    """Test direct AzureChatOpenAI initialization"""
    print("=== Testing Direct AzureChatOpenAI Initialization ===")
    
    try:
        from langchain_openai import AzureChatOpenAI
        
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        deployment_name = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
        
        print(f"Endpoint: {endpoint}")
        print(f"API Key: {'***' if api_key else None}")
        print(f"API Version: {api_version}")
        print(f"Deployment: {deployment_name}")
        
        # Test different parameter combinations
        print("\n--- Testing with openai_api_version ---")
        try:
            client1 = AzureChatOpenAI(
                azure_deployment=deployment_name,
                azure_endpoint=endpoint,
                api_key=api_key,
                openai_api_version=api_version,
            )
            print("✅ Success with openai_api_version")
        except Exception as e:
            print(f"❌ Failed with openai_api_version: {e}")
        
        print("\n--- Testing with api_version ---")
        try:
            client2 = AzureChatOpenAI(
                azure_deployment=deployment_name,
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version,
            )
            print("✅ Success with api_version")
        except Exception as e:
            print(f"❌ Failed with api_version: {e}")
            
        print("\n--- Testing with environment variable fallback ---")
        try:
            # Set the environment variable
            os.environ["OPENAI_API_VERSION"] = api_version
            client3 = AzureChatOpenAI(
                azure_deployment=deployment_name,
                azure_endpoint=endpoint,
                api_key=api_key,
            )
            print("✅ Success with OPENAI_API_VERSION env var")
        except Exception as e:
            print(f"❌ Failed with OPENAI_API_VERSION env var: {e}")
            
    except Exception as e:
        print(f"❌ Import or setup failed: {e}")

def test_utils_function():
    """Test the utils function"""
    print("\n=== Testing Utils Function ===")
    
    try:
        from open_deep_research.utils import init_azure_chat_model
        
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        deployment_name = "shelle-wus-acceptance-gpt-4o-provisionedmanaged"
        
        print("Calling init_azure_chat_model...")
        client = init_azure_chat_model(
            model=deployment_name,
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        print("✅ Utils function succeeded")
        
    except Exception as e:
        print(f"❌ Utils function failed: {e}")
        import traceback
        traceback.print_exc()

def test_get_chat_model():
    """Test the get_chat_model function"""
    print("\n=== Testing get_chat_model Function ===")
    
    try:
        from open_deep_research.utils import get_chat_model
        
        azure_config = {
            "azure_openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "azure_openai_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_openai_api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        }
        
        print("Calling get_chat_model...")
        client = get_chat_model(
            model="shelle-wus-acceptance-gpt-4o-provisionedmanaged",
            model_provider="azure_openai",
            azure_config=azure_config
        )
        print("✅ get_chat_model succeeded")
        
    except Exception as e:
        print(f"❌ get_chat_model failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Azure OpenAI Debug Script")
    print("=" * 50)
    
    test_direct_azure_openai()
    test_utils_function()
    test_get_chat_model()
