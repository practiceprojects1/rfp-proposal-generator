"""
Simple test script to verify the tools work correctly.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rfp_search import search_sam_gov, get_rfp_details
from tools.rfp_analysis import analyze_rfp_relevance


def test_search():
    """Test RFP search functionality."""
    print("Testing RFP search...")
    result = search_sam_gov.invoke({
        "keywords": "AI software development",
        "days_back": 30,
        "limit": 5
    })
    print(f"Search result: {result}")
    print("✓ Search test passed\n")
    return result


def test_get_details():
    """Test getting RFP details."""
    print("Testing RFP details fetch...")
    result = get_rfp_details.invoke({
        "rfp_url": "https://sam.gov/opp/example-1"
    })
    print(f"Details result: {result}")
    print("✓ Details test passed\n")
    return result


def test_analysis():
    """Test RFP analysis."""
    print("Testing RFP analysis...")
    # Use mock details
    mock_details = {
        "details": {
            "title": "AI Software Development",
            "agency": "Department of Defense",
            "description": "The DoD requires AI software development services for autonomous systems.",
            "requirements": ["AI experience", "Security clearance"],
            "budget_range": "$5M - $10M"
        }
    }

    import json
    result = analyze_rfp_relevance.invoke({
        "rfp_details": json.dumps(mock_details)
    })
    print(f"Analysis result: {result}")
    print("✓ Analysis test passed\n")
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("Testing RFP Proposal Generator Tools")
    print("=" * 60)
    print()

    try:
        search_result = test_search()
        details_result = test_get_details()
        analysis_result = test_analysis()

        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with your API keys")
        print("3. Run the agent: python main.py")

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)