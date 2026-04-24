"""
Simple test to verify project structure without requiring dependencies.
"""
import os
import sys


def test_structure():
    """Verify all necessary files and directories exist."""
    print("Verifying project structure...")
    print()

    required_files = [
        "requirements.txt",
        ".env.example",
        "README.md",
        "main.py",
        "tools/__init__.py",
        "tools/rfp_search.py",
        "tools/rfp_analysis.py",
        "tools/proposal_generator.py",
        "skills/federal-contracting/SKILL.md"
    ]

    required_dirs = [
        "tools",
        "skills",
        "proposals",
        "memories"
    ]

    missing_files = []
    missing_dirs = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✓ {file}")

    for dir in required_dirs:
        if not os.path.isdir(dir):
            missing_dirs.append(dir)
        else:
            print(f"✓ {dir}/")

    print()

    if missing_files or missing_dirs:
        print("Missing items:")
        for f in missing_files:
            print(f"  ✗ {f}")
        for d in missing_dirs:
            print(f"  ✗ {d}/")
        return False
    else:
        print("All required files and directories exist! ✓")
        return True


def test_imports():
    """Test that the tools can be imported (without executing them)."""
    print("\nTesting tool imports (syntax check)...")
    print()

    try:
        # Try to compile the files without importing dependencies
        files_to_check = [
            "tools/rfp_search.py",
            "tools/rfp_analysis.py",
            "tools/proposal_generator.py",
            "main.py"
        ]

        for file in files_to_check:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print(f"✓ {file} - syntax OK")

        print("\nAll Python files have valid syntax! ✓")
        return True

    except SyntaxError as e:
        print(f"\n✗ Syntax error in {e.filename}: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("RFP Proposal Generator - Structure Test")
    print("=" * 60)
    print()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    structure_ok = test_structure()
    imports_ok = test_imports()

    print()
    print("=" * 60)

    if structure_ok and imports_ok:
        print("All structure tests passed! ✓")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with your API keys")
        print("3. Run the agent: python main.py")
        sys.exit(0)
    else:
        print("Some tests failed. Please review the output above.")
        print("=" * 60)
        sys.exit(1)