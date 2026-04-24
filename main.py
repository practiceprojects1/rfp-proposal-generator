"""
Main agent script for Federal RFP Proposal Generator.
Uses Deep Agents framework for autonomous RFP search and proposal generation.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend, CompositeBackend, StateBackend
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

# Import custom tools
from tools.rfp_search import search_sam_gov, search_grants_gov, get_rfp_details
from tools.rfp_analysis import analyze_rfp_relevance, check_processed_rfps, mark_rfp_processed
from tools.proposal_generator import generate_proposal


def create_agent():
    """Create and configure the Deep Agent for RFP proposal generation."""

    # Configure composite backend for hybrid storage
    # Use FilesystemBackend for proposals (persistent on disk)
    # Use StateBackend for temporary files
    def create_backend(runtime):
        return CompositeBackend(
            default=StateBackend(runtime),
            routes={
                "/proposals/": FilesystemBackend(
                    root_dir=os.path.join(os.path.dirname(__file__), "proposals"),
                    virtual_mode=True
                )
            }
        )

    # Create checkpointer for conversation persistence
    checkpointer = MemorySaver()

    # Create store for long-term memory (tracking processed RFPs)
    store = InMemoryStore()

    # System prompt for the agent
    system_prompt = """You are an expert federal contracting specialist and proposal writer for Cognition, Inc.

Your mission is to:
1. Search for federal RFPs that are relevant to Devin AI's capabilities
2. Analyze RFPs to determine fit and relevance
3. Generate tailored proposals highlighting Devin AI's strengths
4. Track which RFPs have been processed to avoid duplicates

Devin AI Key Capabilities:
- Autonomous software engineering and code generation
- Multi-step task planning and execution
- Real-time debugging and error resolution
- Support for multiple programming languages
- AI/ML development expertise
- DevOps and CI/CD automation
- Security and compliance features

When working:
1. Use search_sam_gov or search_grants_gov to find opportunities
2. Use get_rfp_details to fetch full RFP information
3. Use check_processed_rfps to avoid duplicate work
4. Use analyze_rfp_relevance to determine if an RFP is a good fit
5. Use generate_proposal to create tailored proposals
6. Use mark_rfp_processed to track completed work
7. Use write_todos to plan multi-step tasks
8. Use filesystem tools to save and manage proposals

Always be thorough and professional in your analysis and proposal generation.
"""

    # Create the deep agent
    agent = create_deep_agent(
        name="rfp-proposal-agent",
        model="anthropic:claude-sonnet-4-5",
        tools=[
            search_sam_gov,
            search_grants_gov,
            get_rfp_details,
            analyze_rfp_relevance,
            check_processed_rfps,
            mark_rfp_processed,
            generate_proposal
        ],
        system_prompt=system_prompt,
        backend=create_backend,
        checkpointer=checkpointer,
        store=store,
        skills=["./skills/"]  # Optional: load skills from directory
    )

    return agent


def main():
    """Main entry point for the RFP proposal generator agent."""
    print("=" * 80)
    print("Federal RFP Proposal Generator for Devin AI")
    print("=" * 80)
    print()

    # Create the agent
    print("Initializing agent...")
    agent = create_agent()
    print("Agent ready!")
    print()

    # Configuration for persistent conversation
    config = {"configurable": {"thread_id": "rfp-session-1"}}

    # Example interaction
    print("You can now interact with the agent.")
    print("Example commands:")
    print("  - 'Search for AI software development RFPs from the last 30 days'")
    print("  - 'Analyze the RFP with solicitation number HQ0034-25-R-0001'")
    print("  - 'Generate a proposal for the most relevant RFP'")
    print()

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break

            if not user_input:
                continue

            print("\nAgent: ", end="", flush=True)

            # Stream the response
            for chunk in agent.stream(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config
            ):
                if "messages" in chunk:
                    for message in chunk["messages"]:
                        if hasattr(message, 'content'):
                            print(message.content, end="", flush=True)

            print()  # New line after response

        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'exit' to quit or continue with a new command.")
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()