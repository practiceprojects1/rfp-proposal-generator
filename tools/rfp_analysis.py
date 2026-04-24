"""
Tools for analyzing RFPs and matching with Devin AI capabilities.
"""
import json
from typing import Dict, List, Optional
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic


DEVIN_AI_CAPABILITIES = {
    "technical_capabilities": [
        "Autonomous code generation and modification",
        "Multi-step task planning and execution",
        "Real-time debugging and error resolution",
        "Integration with version control systems (Git)",
        "Cross-language support (Python, TypeScript, JavaScript, Go, Rust, etc.)",
        "Automated testing and test generation",
        "Code review and optimization",
        "CI/CD pipeline automation",
        "Documentation generation",
        "API integration and development"
    ],
    "domain_expertise": [
        "Software engineering best practices",
        "DevOps and cloud infrastructure",
        "Machine Learning and AI development",
        "Security and compliance",
        "Federal government compliance requirements",
        "Agile and Scrum methodologies"
    ],
    "security_features": [
        "Secure credential management",
        "Access control and permissions",
        "Audit logging and traceability",
        "Compliance with federal security standards",
        "SOC 2 Type II ready"
    ],
    "integration_capabilities": [
        "REST API integration",
        "GraphQL support",
        "Database integration (SQL, NoSQL)",
        "Cloud provider integration (AWS, GCP, Azure)",
        "Third-party service integrations"
    ]
}


@tool
def analyze_rfp_relevance(rfp_details: str) -> str:
    """Analyze an RFP to determine relevance to Devin AI capabilities.

    Args:
        rfp_details: JSON string containing RFP details

    Returns:
        JSON string with relevance score, matched capabilities, and gaps
    """
    try:
        rfp = json.loads(rfp_details)
        description = rfp.get("details", {}).get("description", "")
        requirements = rfp.get("details", {}).get("requirements", [])

        # Simple keyword matching for relevance
        relevant_keywords = [
            "software development", "AI", "artificial intelligence", "machine learning",
            "automation", "code", "programming", "development", "engineering",
            "DevOps", "CI/CD", "testing", "debugging", "integration"
        ]

        description_lower = description.lower()
        matched_keywords = [kw for kw in relevant_keywords if kw.lower() in description_lower]

        # Calculate relevance score
        relevance_score = min(100, len(matched_keywords) * 15)

        # Match Devin AI capabilities
        matched_capabilities = []
        for capability in DEVIN_AI_CAPABILITIES["technical_capabilities"]:
            if any(keyword in capability.lower() for keyword in matched_keywords):
                matched_capabilities.append(capability)

        analysis = {
            "relevance_score": relevance_score,
            "is_relevant": relevance_score >= 30,
            "matched_keywords": matched_keywords,
            "matched_capabilities": matched_capabilities[:5],  # Top 5 matches
            "rfp_summary": {
                "title": rfp.get("details", {}).get("title", ""),
                "agency": rfp.get("details", {}).get("agency", ""),
                "budget": rfp.get("details", {}).get("budget_range", "Unknown")
            }
        }

        return json.dumps({
            "success": True,
            "analysis": analysis
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@tool
def check_processed_rfps(
    solicitation_number: str,
    runtime
) -> str:
    """Check if an RFP has already been processed.

    Args:
        solicitation_number: The RFP solicitation number
        runtime: Tool runtime for accessing store

    Returns:
        JSON string indicating whether the RFP has been processed
    """
    try:
        store = runtime.store
        namespace = ("processed_rfps",)

        result = store.get(namespace, solicitation_number)

        if result:
            return json.dumps({
                "success": True,
                "is_processed": True,
                "processed_date": result.value.get("processed_date"),
                "proposal_path": result.value.get("proposal_path")
            })
        else:
            return json.dumps({
                "success": True,
                "is_processed": False
            })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })


@tool
def mark_rfp_processed(
    solicitation_number: str,
    proposal_path: str,
    runtime
) -> str:
    """Mark an RFP as processed to avoid duplicate work.

    Args:
        solicitation_number: The RFP solicitation number
        proposal_path: Path to the generated proposal
        runtime: Tool runtime for accessing store

    Returns:
        JSON string confirming the RFP has been marked as processed
    """
    try:
        store = runtime.store
        namespace = ("processed_rfps",)

        from datetime import datetime
        store.put(namespace, solicitation_number, {
            "processed_date": datetime.now().isoformat(),
            "proposal_path": proposal_path
        })

        return json.dumps({
            "success": True,
            "message": f"RFP {solicitation_number} marked as processed"
        })

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })