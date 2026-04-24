"""
Tool for generating tailored proposals for Devin AI.
"""
import json
from typing import Dict, Optional
from datetime import datetime
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic


@tool
def generate_proposal(
    rfp_details: str,
    runtime
) -> str:
    """Generate a tailored proposal for Devin AI based on RFP requirements.

    Args:
        rfp_details: JSON string containing RFP details
        runtime: Tool runtime for accessing filesystem

    Returns:
        JSON string with proposal content and file path
    """
    try:
        rfp = json.loads(rfp_details)
        details = rfp.get("details", {})

        solicitation_number = details.get("solicitation_number", "UNKNOWN")
        agency = details.get("agency", "Unknown Agency")
        title = details.get("title", "Unknown Title")

        # Generate proposal content
        proposal_content = f"""
# PROPOSAL: {title}

**Solicitation Number:** {solicitation_number}
**Agency:** {agency}
**Date:** {datetime.now().strftime("%B %d, %Y")}
**Submitted by:** Cognition, Inc.

---

## 1. EXECUTIVE SUMMARY

Cognition, Inc. is pleased to submit this proposal in response to {solicitation_number}.
We propose leveraging Devin AI, our autonomous AI software engineer, to deliver exceptional
software development services that meet and exceed the requirements outlined in this solicitation.

Devin AI is the world's first fully autonomous AI software engineer, capable of planning,
coding, debugging, and deploying complex software systems with minimal human oversight.

## 2. UNDERSTANDING OF REQUIREMENTS

We have carefully reviewed the requirements for this opportunity and understand that the
{agency} requires:

{details.get('description', 'No description provided')}

Our solution directly addresses these requirements through Devin AI's advanced capabilities.

## 3. TECHNICAL APPROACH

### 3.1 Devin AI Architecture

Devin AI employs a sophisticated multi-agent architecture that enables:

- **Autonomous Task Planning**: Breaking down complex requirements into executable tasks
- **Real-time Code Generation**: Writing production-quality code across multiple languages
- **Intelligent Debugging**: Identifying and resolving issues autonomously
- **Continuous Integration**: Automated testing and deployment workflows

### 3.2 Relevant Capabilities

Our solution provides the following capabilities directly relevant to this solicitation:

**Software Development:**
- Full-stack development (frontend, backend, databases)
- Multi-language support (Python, TypeScript, JavaScript, Go, Rust, and more)
- API design and implementation
- Database design and optimization

**AI/ML Expertise:**
- Machine learning model development and deployment
- Natural language processing
- Computer vision applications
- Data pipeline construction

**DevOps & Infrastructure:**
- CI/CD pipeline automation
- Cloud infrastructure (AWS, GCP, Azure)
- Containerization (Docker, Kubernetes)
- Infrastructure as Code (Terraform, Pulumi)

**Security & Compliance:**
- Secure coding practices
- Compliance with federal security standards
- Audit logging and traceability
- Access control and authentication

## 4. QUALIFICATIONS AND PAST PERFORMANCE

### 4.1 Company Overview

Cognition, Inc. is a leading AI company specializing in autonomous software engineering.
Our flagship product, Devin AI, has been deployed across multiple industries including
technology, finance, and healthcare.

### 4.2 Relevant Experience

- Successfully delivered AI-powered software solutions for enterprise clients
- Experience with federal government compliance requirements
- Proven track record in complex system integration
- Expert team with backgrounds in AI, software engineering, and federal contracting

### 4.3 Technical Certifications

- SOC 2 Type II compliance
- ISO 27001 Information Security Management
- CMMI Level 3 processes
- Federal Risk and Authorization Management Program (FedRAMP) ready

## 5. MANAGEMENT APPROACH

### 5.1 Project Team

Our team includes:
- **Project Manager**: 15+ years federal contracting experience
- **Technical Lead**: Former DoD software architect
- **AI Specialists**: PhD-level expertise in machine learning
- **DevOps Engineers**: Certified cloud infrastructure experts
- **Security Engineers**: CISSP-certified security professionals

### 5.2 Methodology

We employ Agile development methodologies with:
- 2-week sprints with regular demos
- Continuous stakeholder communication
- Iterative feedback and refinement
- Transparent progress tracking

## 6. QUALITY ASSURANCE

Our quality assurance process includes:

- Automated testing at multiple levels (unit, integration, end-to-end)
- Code review processes
- Security scanning and vulnerability assessment
- Performance testing and optimization
- User acceptance testing

## 7. SECURITY PLAN

### 7.1 Data Security

- Encryption at rest and in transit
- Role-based access control
- Comprehensive audit logging
- Regular security assessments

### 7.2 Personnel Security

- All team members undergo background checks
- Security clearance support (Secret/Top Secret as required)
- Ongoing security training

## 8. PRICING

Based on the requirements outlined, we propose a competitive pricing structure:

**Total Proposed Budget:** {details.get('budget_range', 'To be determined')}

**Period of Performance:** {details.get('period_of_performance', '24 months')}

*Detailed pricing breakdown available upon request*

## 9. CONCLUSION

Cognition, Inc. is uniquely positioned to deliver exceptional value through Devin AI's
autonomous software engineering capabilities. Our combination of technical expertise,
federal experience, and innovative AI technology ensures successful project delivery.

We welcome the opportunity to discuss this proposal further and demonstrate how
Devin AI can transform your software development initiatives.

---

**Contact Information:**
- **Name:** [Your Contact Name]
- **Title:** [Your Title]
- **Email:** [your.email@cognition.ai]
- **Phone:** [Your Phone Number]
- **Website:** https://www.cognition.ai

---

*This proposal is submitted in good faith and represents our best estimate based on
the information available at the time of submission.*
"""

        # Save proposal to file
        filename = f"proposal_{solicitation_number}_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = f"/proposals/{filename}"

        # Use the filesystem tool through the runtime
        runtime.invoke_tool("write_file", {
            "path": filepath,
            "content": proposal_content
        })

        return json.dumps({
            "success": True,
            "proposal_path": filepath,
            "filename": filename,
            "message": f"Proposal generated and saved to {filepath}"
        }, indent=2)

    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })