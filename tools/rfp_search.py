"""
Tools for searching federal RFP websites.
"""
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool


@tool
def search_sam_gov(
    keywords: str,
    days_back: int = 30,
    limit: int = 10
) -> str:
    """Search SAM.gov for federal contracting opportunities.

    Args:
        keywords: Search terms (e.g., "AI software development", "machine learning")
        days_back: Number of days to look back for opportunities (default: 30)
        limit: Maximum number of results to return (default: 10)

    Returns:
        JSON string containing RFP listings with title, agency, due date, and link
    """
    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        # SAM.gov API endpoint (requires API key in production)
        # This is a mock implementation - in production, use actual SAM.gov API
        api_key = os.getenv("SAM_API_KEY")

        # For demonstration, return mock data
        # In production, replace with actual API call:
        # url = f"https://api.sam.gov/opportunities/v2/search"
        # params = {
        #     "api_key": api_key,
        #     "keywords": keywords,
        #     "postedFrom": start_date.strftime("%Y-%m-%d"),
        #     "postedTo": end_date.strftime("%Y-%m-%d"),
        #     "limit": limit
        # }

        mock_results = [
            {
                "title": "Artificial Intelligence Software Development Services",
                "agency": "Department of Defense",
                "solicitation_number": "HQ0034-25-R-0001",
                "posted_date": start_date.strftime("%Y-%m-%d"),
                "response_deadline": (end_date + timedelta(days=30)).strftime("%Y-%m-%d"),
                "description": "The DoD seeks AI software development services for autonomous systems.",
                "link": "https://sam.gov/opp/example-1",
                "naics": "541511"
            },
            {
                "title": "Machine Learning Platform for Federal Agencies",
                "agency": "General Services Administration",
                "solicitation_number": "GS00Q-25-R-0001",
                "posted_date": (start_date + timedelta(days=5)).strftime("%Y-%m-%d"),
                "response_deadline": (end_date + timedelta(days=45)).strftime("%Y-%m-%d"),
                "description": "GSA requires a machine learning platform for data analysis across federal agencies.",
                "link": "https://sam.gov/opp/example-2",
                "naics": "511210"
            }
        ]

        import json
        return json.dumps({
            "success": True,
            "count": len(mock_results),
            "results": mock_results,
            "search_params": {
                "keywords": keywords,
                "days_back": days_back,
                "limit": limit
            }
        }, indent=2)

    except Exception as e:
        import json
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@tool
def search_grants_gov(
    keywords: str,
    eligibility: str = "all",
    limit: int = 10
) -> str:
    """Search Grants.gov for federal grant opportunities.

    Args:
        keywords: Search terms (e.g., "artificial intelligence", "software development")
        eligibility: Eligibility criteria (e.g., "small business", "all")
        limit: Maximum number of results to return (default: 10)

    Returns:
        JSON string containing grant opportunity listings
    """
    try:
        # Mock implementation for demonstration
        mock_results = [
            {
                "title": "AI Research and Development Grant",
                "agency": "National Science Foundation",
                "opportunity_number": "NSF-25-001",
                "posted_date": datetime.now().strftime("%Y-%m-%d"),
                "closing_date": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "description": "NSF seeks proposals for AI research in software engineering.",
                "link": "https://grants.gov/example-1",
                "eligible_applicants": ["Small businesses", "Universities"]
            }
        ]

        import json
        return json.dumps({
            "success": True,
            "count": len(mock_results),
            "results": mock_results,
            "search_params": {
                "keywords": keywords,
                "eligibility": eligibility,
                "limit": limit
            }
        }, indent=2)

    except Exception as e:
        import json
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@tool
def get_rfp_details(rfp_url: str) -> str:
    """Fetch detailed information about a specific RFP.

    Args:
        rfp_url: URL to the RFP listing

    Returns:
        JSON string containing detailed RFP information including full description, requirements, and evaluation criteria
    """
    try:
        # Mock implementation - in production, fetch actual content
        mock_details = {
            "title": "Artificial Intelligence Software Development Services",
            "agency": "Department of Defense",
            "solicitation_number": "HQ0034-25-R-0001",
            "description": """
            The Department of Defense requires comprehensive AI software development services
            to support autonomous systems development. The contractor shall provide:
            - AI/ML model development and training
            - Software engineering best practices
            - DevOps and CI/CD pipeline implementation
            - Security clearance requirements for personnel
            - Agile development methodology
            """,
            "requirements": [
                "Experience with large-scale AI systems",
                "Security clearance (Secret level)",
                "CMMI Level 3 or higher certification",
                "Minimum 5 years in federal contracting",
                "Team size: 10-20 FTEs"
            ],
            "evaluation_criteria": [
                "Technical approach (40%)",
                "Past performance (30%)",
                "Price (20%)",
                "Small business participation (10%)"
            ],
            "budget_range": "$5M - $10M",
            "period_of_performance": "24 months",
            "point_of_contact": {
                "name": "John Smith",
                "email": "john.smith@defense.gov",
                "phone": "555-0100"
            }
        }

        import json
        return json.dumps({
            "success": True,
            "details": mock_details,
            "source_url": rfp_url
        }, indent=2)

    except Exception as e:
        import json
        return json.dumps({
            "success": False,
            "error": str(e)
        })