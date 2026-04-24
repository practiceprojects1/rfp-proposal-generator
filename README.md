# Federal RFP Proposal Generator for Devin AI

An AI-powered system that searches for federal government Requests for Proposals (RFPs) and automatically generates tailored proposals for Cognition's Devin AI.

## Features

- **RFP Discovery**: Searches federal contracting websites (SAM.gov, Grants.gov, etc.) for relevant RFPs
- **Intelligent Analysis**: Analyzes RFP requirements and matches them with Devin AI capabilities
- **Proposal Generation**: Creates customized proposals highlighting Devin AI's strengths
- **Memory & Tracking**: Remembers processed RFPs to avoid duplicates
- **File Management**: Saves proposals and tracks progress
- **REST API**: FastAPI-based web service for easy integration
- **AWS Bedrock Support**: Deploy to AWS with managed foundation model inference

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

## Running as API Server

Start the FastAPI server:

```bash
# Using direct Anthropic API
python api.py

# Using AWS Bedrock
USE_BEDROCK=true python api.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `POST /chat` - Chat with the agent
- `POST /chat/stream` - Streaming chat
- `POST /rfp/search` - Search for RFPs
- `POST /rfp/analyze` - Analyze an RFP
- `POST /proposal/generate` - Generate a proposal

See `AWS_DEPLOYMENT.md` for detailed API documentation.

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

## AWS Deployment

Deploy to AWS ECS Fargate with AWS Bedrock:

```bash
cd rfp-proposal-generator
./aws/deploy.sh
```

See `AWS_DEPLOYMENT.md` for detailed deployment instructions, including:
- ECS Fargate setup
- Application Load Balancer configuration
- AWS Bedrock integration
- Security and IAM permissions
- Monitoring and logging

## Security

This project includes comprehensive security features:

- **CI/CD Pipeline**: Automated security scanning (SAST, dependency scanning, secrets detection)
- **Pre-commit Hooks**: Local security checks before commits
- **Security Policy**: Documented in `SECURITY.md`
- **Container Security**: Non-root user, minimal dependencies
- **Secrets Management**: AWS Secrets Manager integration

See `SECURITY.md` for detailed security information.