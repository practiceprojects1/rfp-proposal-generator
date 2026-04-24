# Federal RFP Proposal Generator for Devin AI

An AI-powered system that searches for federal government Requests for Proposals (RFPs) and automatically generates tailored proposals for Cognition's Devin AI.

## Features

- **RFP Discovery**: Searches federal contracting websites (SAM.gov, Grants.gov, etc.) for relevant RFPs
- **Intelligent Analysis**: Analyzes RFP requirements and matches them with Devin AI capabilities
- **Proposal Generation**: Creates customized proposals highlighting Devin AI's strengths
- **Memory & Tracking**: Remembers processed RFPs to avoid duplicates
- **File Management**: Saves proposals and tracks progress

## Architecture

Built with **Deep Agents** framework for:
- Multi-step task planning with TodoListMiddleware
- File management with FilesystemMiddleware
- Persistent memory across sessions with StoreBackend
- Long-term tracking of processed RFPs

## Setup

1. Install dependencies:
```bash
cd rfp-proposal-generator
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Run the agent:
```bash
python main.py
```

## Usage

Interact with the agent to:
- Search for new RFPs
- Analyze specific RFPs
- Generate proposals
- Review saved proposals

## Project Structure

```
rfp-proposal-generator/
├── main.py              # Main agent entry point
├── tools/               # Custom tools for RFP search and analysis
├── skills/              # Domain-specific skills
├── proposals/           # Generated proposals
├── memories/            # Persistent memory storage
└── requirements.txt     # Python dependencies
```

## Tools

- `search_rfps`: Search federal RFP websites
- `analyze_rfp`: Analyze RFP documents
- `generate_proposal`: Generate tailored proposals
- `check_processed_rfps`: Check if an RFP has been processed