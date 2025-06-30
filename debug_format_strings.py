#!/usr/bin/env python3
"""
Debug script to test format strings and identify the source of the ValueError
"""

def test_format_strings():
    """Test various format string calls to identify the failing one."""
    
    # Mock data
    topic = "Test topic"
    messages = "Test messages"
    report_organization = "Test organization"
    number_of_queries = 2
    context = "Test context"
    feedback = "Test feedback"
    
    # Import the actual functions and strings
    try:
        from open_deep_research.utils import get_today_str
        today = get_today_str()
        print(f"✓ get_today_str() works: {today}")
    except Exception as e:
        print(f"✗ get_today_str() failed: {e}")
        today = "Test date"
    
    # Test graph prompts
    try:
        from open_deep_research.prompts import report_planner_query_writer_instructions
        result = report_planner_query_writer_instructions.format(
            topic=topic,
            report_organization=report_organization,
            number_of_queries=number_of_queries,
            today=today
        )
        print("✓ Graph report_planner_query_writer_instructions format works")
    except Exception as e:
        print(f"✗ Graph report_planner_query_writer_instructions format failed: {e}")
    
    try:
        from open_deep_research.prompts import report_planner_instructions
        result = report_planner_instructions.format(
            topic=topic, 
            report_organization=report_organization, 
            context=context, 
            feedback=feedback
        )
        print("✓ Graph report_planner_instructions format works")
    except Exception as e:
        print(f"✗ Graph report_planner_instructions format failed: {e}")
    
    # Test workflow prompts
    try:
        from open_deep_research.workflow.prompts import report_planner_query_writer_instructions as workflow_query_instructions
        result = workflow_query_instructions.format(
            messages=messages,
            report_organization=report_organization,
            number_of_queries=number_of_queries,
            today=today
        )
        print("✓ Workflow report_planner_query_writer_instructions format works")
    except Exception as e:
        print(f"✗ Workflow report_planner_query_writer_instructions format failed: {e}")
    
    try:
        from open_deep_research.workflow.prompts import report_planner_instructions as workflow_planner_instructions
        result = workflow_planner_instructions.format(
            messages=messages, 
            report_organization=report_organization, 
            context=context, 
            feedback=feedback
        )
        print("✓ Workflow report_planner_instructions format works")
    except Exception as e:
        print(f"✗ Workflow report_planner_instructions format failed: {e}")

if __name__ == "__main__":
    test_format_strings()
