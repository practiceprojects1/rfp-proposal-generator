# Quick Start Guide

Get the Federal RFP Proposal Generator up and running in 5 minutes.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Anthropic API key (for Claude)

## Installation

1. **Navigate to the project directory:**
```bash
cd rfp-proposal-generator
```

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

5. **Verify the setup:**
```bash
python test_structure.py
```

## Running the Agent

Start the agent:
```bash
python main.py
```

## Example Interactions

Once the agent is running, try these commands:

### Search for RFPs
```
Search for AI software development RFPs from the last 30 days
```

### Analyze an RFP
```
Analyze the RFP with solicitation number HQ0034-25-R-0001
```

### Generate a Proposal
```
Generate a proposal for the most relevant RFP
```

### Check Processed RFPs
```
Check which RFPs have already been processed
```

### Full Workflow
```
Find relevant AI RFPs, analyze them, and generate proposals for the top 3
```

## Project Structure

```
rfp-proposal-generator/
├── main.py              # Main agent entry point
├── tools/               # Custom tools
│   ├── rfp_search.py    # Search SAM.gov, Grants.gov
│   ├── rfp_analysis.py  # Analyze RFP relevance
│   └── proposal_generator.py  # Generate proposals
├── skills/              # Domain knowledge
│   └── federal-contracting/  # Federal contracting expertise
├── proposals/           # Generated proposals (saved here)
├── memories/            # Persistent memory storage
└── requirements.txt     # Dependencies
```

## Troubleshooting

### ModuleNotFoundError
If you get import errors, make sure you've installed dependencies:
```bash
pip install -r requirements.txt
```

### API Key Errors
Ensure your `.env` file contains valid API keys:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### File Permission Errors
If the agent can't write to the proposals directory, check permissions:
```bash
chmod +w proposals/
```

## Next Steps

1. Customize the tools to connect to real SAM.gov API
2. Add your company information to the proposal template
3. Configure database persistence for production use
4. Add additional skills for specific domains

## Support

For issues or questions:
- Check the main README.md for detailed documentation
- Review the skills in `skills/` for domain-specific guidance
- Examine tool implementations in `tools/` for customization options