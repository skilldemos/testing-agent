#!/usr/bin/env python3
"""
Test Generation and Evaluation Pipeline

This script demonstrates how to:
1. Analyze code files for testing needs
2. Generate comprehensive test suites using AI
3. Evaluate existing test quality
4. Generate structured test reports

Usage:
    python generate_tests.py                     # Analyze all Python files in sample-code/
    python generate_tests.py user_service.py     # Generate tests for a single file
    python generate_tests.py --evaluate tests/   # Evaluate existing tests
    python generate_tests.py --help              # Show help

Requirements:
    pip install anthropic ast

Environment:
    Set ANTHROPIC_API_KEY environment variable
"""

import ast
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def analyze_code_file(file_path: str) -> Dict:
    """
    Analyze a Python file to identify testable components.
    
    Args:
        file_path: Path to Python file
        
    Returns:
        Dictionary with analysis results
    """
    with open(file_path, 'r') as f:
        code = f.read()
    
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {
            'file': file_path,
            'error': f'Syntax error: {e}',
            'testable': False
        }
    
    # Extract functions and classes
    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Skip private methods
            if not node.name.startswith('_'):
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'docstring': ast.get_docstring(node)
                })
        elif isinstance(node, ast.ClassDef):
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                    methods.append(item.name)
            
            classes.append({
                'name': node.name,
                'line': node.lineno,
                'methods': methods,
                'docstring': ast.get_docstring(node)
            })
    
    # Calculate complexity score (simple heuristic)
    complexity = len(functions) + len(classes) * 2
    
    return {
        'file': file_path,
        'functions': functions,
        'classes': classes,
        'complexity': complexity,
        'lines': len(code.split('\n')),
        'testable': True
    }


def load_agent_instructions(agent_path: str = "AGENTS.md") -> str:
    """Load the agent instructions from AGENTS.md."""
    if os.path.exists(agent_path):
        with open(agent_path, 'r') as f:
            return f.read()
    return ""


def load_skill_rubric(skill_path: str = ".github/skills/test-strategy/SKILL.md") -> str:
    """Load the test strategy skill rubric."""
    if os.path.exists(skill_path):
        with open(skill_path, 'r') as f:
            return f.read()
    return ""


def create_test_generation_prompt(
    code_path: str,
    code_content: str,
    analysis: Dict,
    agent_instructions: str,
    skill_rubric: str,
    test_framework: str = "pytest"
) -> str:
    """
    Create a prompt for AI to generate comprehensive tests.
    
    Args:
        code_path: Path to the code file
        code_content: Content of the code file
        analysis: Analysis results from analyze_code_file
        agent_instructions: Instructions from AGENTS.md
        skill_rubric: Rubric from SKILL.md
        test_framework: Testing framework to use
        
    Returns:
        Complete prompt for LLM
    """
    functions_list = "\n".join(f"- {f['name']}()" for f in analysis['functions'])
    classes_list = "\n".join(
        f"- {c['name']} with methods: {', '.join(c['methods'])}" 
        for c in analysis['classes']
    )
    
    return f"""{agent_instructions}

## TEST GENERATION GUIDELINES
{skill_rubric}

## CODE TO TEST

**File**: {code_path}
**Complexity**: {analysis['complexity']} (functions + classes)
**Framework**: {test_framework}

### Functions to Test:
{functions_list if functions_list else "None"}

### Classes to Test:
{classes_list if classes_list else "None"}

### Full Code:
```python
{code_content}
```

## YOUR TASK

Generate a comprehensive test suite for this code that:

1. **Test Completeness** (30/30 points):
   - Test all critical paths (happy path + error cases)
   - Cover edge cases and boundary conditions
   - Test error handling and exceptions
   - Test input validation

2. **Test Quality** (25/25 points):
   - Follow AAA pattern (Arrange, Act, Assert)
   - Use descriptive test names
   - Ensure test isolation
   - Use fixtures for common setup
   - Make tests deterministic

3. **Test Reliability** (20/20 points):
   - Mock external dependencies appropriately
   - Add proper timeouts where needed
   - Ensure tests fail for the right reasons

4. **Testing Layers** (15/15 points):
   - Provide comprehensive unit tests
   - Include integration tests where components interact
   - Balance coverage vs execution time

5. **Best Practices** (10/10 points):
   - Follow {test_framework} conventions
   - Add clear documentation
   - Include realistic test data
   - Note any security testing

Generate the complete test file with:
- Import statements
- Fixtures for common setup
- Comprehensive test classes
- Detailed test methods with docstrings
- Comments explaining complex test scenarios

Target: 90+ quality score on the rubric above.
"""


def create_test_evaluation_prompt(
    test_code: str,
    source_code: Optional[str],
    agent_instructions: str,
    skill_rubric: str
) -> str:
    """
    Create a prompt for AI to evaluate existing tests.
    
    Args:
        test_code: Content of the test file
        source_code: Content of the source file being tested (if available)
        agent_instructions: Instructions from AGENTS.md
        skill_rubric: Rubric from SKILL.md
        
    Returns:
        Complete prompt for LLM
    """
    source_section = ""
    if source_code:
        source_section = f"""
### Source Code Being Tested:
```python
{source_code}
```
"""
    
    return f"""{agent_instructions}

## TEST EVALUATION RUBRIC
{skill_rubric}

## TEST CODE TO EVALUATE

```python
{test_code}
```

{source_section}

## YOUR TASK

Evaluate this test suite using the rubric above. Provide:

1. **Detailed Scores** for each category:
   - Test Completeness (X/30)
   - Test Quality & Maintainability (X/25)
   - Test Reliability (X/20)
   - Testing Layers (X/15)
   - Best Practices (X/10)

2. For each category:
   - State the score and why
   - Quote specific evidence from the tests
   - Note what's missing or could be improved

3. **Overall Assessment**:
   - Total score (X/100)
   - Quality tier
   - 2-3 key strengths
   - 2-3 critical gaps

4. **Prioritized Recommendations**:
   - High priority (do first)
   - Medium priority (next sprint)
   - Low priority (technical debt)

Be specific with examples and quote code where relevant.
"""


def generate_tests_with_ai(
    prompt: str,
    api_key: str,
    model: str = "claude-sonnet-4-20250514"
) -> str:
    """Send prompt to Claude API and get generated tests."""
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text


def process_code_file(
    code_path: str,
    output_dir: str = "generated-tests",
    api_key: Optional[str] = None,
    agent_path: str = "AGENTS.md",
    skill_path: str = ".github/skills/test-strategy/SKILL.md"
) -> Dict:
    """
    Process a code file and generate tests.
    
    Args:
        code_path: Path to code file
        output_dir: Where to save generated tests
        api_key: Anthropic API key
        agent_path: Path to agent instructions
        skill_path: Path to skill rubric
        
    Returns:
        Dictionary with processing results
    """
    print(f"\n{'='*60}")
    print(f"Processing: {code_path}")
    print('='*60)
    
    # Read code file
    print("  [1/6] Reading code file...")
    with open(code_path, 'r') as f:
        code_content = f.read()
    print(f"        Read {len(code_content)} characters")
    
    # Analyze code
    print("  [2/6] Analyzing code structure...")
    analysis = analyze_code_file(code_path)
    
    if not analysis['testable']:
        print(f"        ✗ Error: {analysis['error']}")
        return {'status': 'error', 'error': analysis['error']}
    
    print(f"        Found {len(analysis['functions'])} functions, "
          f"{len(analysis['classes'])} classes")
    
    # Load agent and skill
    print("  [3/6] Loading agent instructions and rubric...")
    agent_instructions = load_agent_instructions(agent_path)
    skill_rubric = load_skill_rubric(skill_path)
    
    # Create prompt
    print("  [4/6] Creating test generation prompt...")
    prompt = create_test_generation_prompt(
        code_path,
        code_content,
        analysis,
        agent_instructions,
        skill_rubric
    )
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    basename = Path(code_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save analysis
    analysis_file = f"{output_dir}/{basename}_analysis.txt"
    with open(analysis_file, 'w') as f:
        f.write(f"# Code Analysis: {basename}\n\n")
        f.write(f"**File**: {code_path}\n")
        f.write(f"**Lines**: {analysis['lines']}\n")
        f.write(f"**Complexity**: {analysis['complexity']}\n\n")
        f.write(f"## Functions ({len(analysis['functions'])})\n")
        for func in analysis['functions']:
            f.write(f"- {func['name']}() at line {func['line']}\n")
        f.write(f"\n## Classes ({len(analysis['classes'])})\n")
        for cls in analysis['classes']:
            f.write(f"- {cls['name']} at line {cls['line']}\n")
            f.write(f"  Methods: {', '.join(cls['methods'])}\n")
    
    print(f"        Analysis saved to: {analysis_file}")
    
    # Generate tests with AI or save prompt
    if api_key:
        print("  [5/6] Generating tests with AI...")
        try:
            generated_tests = generate_tests_with_ai(prompt, api_key)
            
            # Save generated tests
            test_file = f"{output_dir}/test_{basename}_{timestamp}.py"
            with open(test_file, 'w') as f:
                f.write(f'"""\nGenerated Tests for {basename}\n')
                f.write(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
                f.write(f'Source: {code_path}\n"""\n\n')
                f.write(generated_tests)
            
            print(f"  [6/6] ✓ Tests generated successfully!")
            print(f"        Saved to: {test_file}")
            
            return {
                'status': 'completed',
                'code_path': code_path,
                'test_file': test_file,
                'analysis_file': analysis_file,
                'analysis': analysis
            }
            
        except Exception as e:
            print(f"  [5/6] ✗ Error generating tests: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    else:
        # Save prompt for manual use
        prompt_file = f"{output_dir}/{basename}_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        print("  [5/6] No API key - saving prompt for manual use")
        print(f"  [6/6] Prompt saved to: {prompt_file}")
        
        return {
            'status': 'prompt_only',
            'code_path': code_path,
            'prompt_file': prompt_file,
            'analysis_file': analysis_file
        }


def evaluate_test_file(
    test_path: str,
    source_path: Optional[str] = None,
    output_dir: str = "test-evaluations",
    api_key: Optional[str] = None,
    agent_path: str = "AGENTS.md",
    skill_path: str = ".github/skills/test-strategy/SKILL.md"
) -> Dict:
    """
    Evaluate an existing test file.
    
    Args:
        test_path: Path to test file
        source_path: Path to source code file (optional)
        output_dir: Where to save evaluation
        api_key: Anthropic API key
        agent_path: Path to agent instructions
        skill_path: Path to skill rubric
        
    Returns:
        Dictionary with evaluation results
    """
    print(f"\n{'='*60}")
    print(f"Evaluating: {test_path}")
    print('='*60)
    
    # Read test file
    print("  [1/5] Reading test file...")
    with open(test_path, 'r') as f:
        test_code = f.read()
    
    # Read source file if provided
    source_code = None
    if source_path and os.path.exists(source_path):
        print("  [2/5] Reading source code file...")
        with open(source_path, 'r') as f:
            source_code = f.read()
    else:
        print("  [2/5] No source code provided")
    
    # Load agent and skill
    print("  [3/5] Loading agent instructions and rubric...")
    agent_instructions = load_agent_instructions(agent_path)
    skill_rubric = load_skill_rubric(skill_path)
    
    # Create evaluation prompt
    print("  [4/5] Creating evaluation prompt...")
    prompt = create_test_evaluation_prompt(
        test_code,
        source_code,
        agent_instructions,
        skill_rubric
    )
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    basename = Path(test_path).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if api_key:
        print("  [5/5] Evaluating with AI...")
        try:
            evaluation = generate_tests_with_ai(prompt, api_key)
            
            # Save evaluation
            eval_file = f"{output_dir}/{basename}_evaluation_{timestamp}.md"
            with open(eval_file, 'w') as f:
                f.write(f"# Test Suite Evaluation: {basename}\n")
                f.write(f"**Evaluated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Test File:** {test_path}\n")
                if source_path:
                    f.write(f"**Source File:** {source_path}\n")
                f.write("\n---\n\n")
                f.write(evaluation)
            
            print(f"        ✓ Evaluation saved to: {eval_file}")
            
            return {
                'status': 'completed',
                'test_path': test_path,
                'evaluation_file': eval_file
            }
            
        except Exception as e:
            print(f"        ✗ Error: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    else:
        # Save prompt
        prompt_file = f"{output_dir}/{basename}_eval_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        print("  [5/5] No API key - prompt saved for manual use")
        print(f"        {prompt_file}")
        
        return {
            'status': 'prompt_only',
            'test_path': test_path,
            'prompt_file': prompt_file
        }


def batch_process_directory(
    directory: str = "sample-code",
    output_dir: str = "generated-tests",
    api_key: Optional[str] = None,
    agent_path: str = "AGENTS.md",
    skill_path: str = ".github/skills/test-strategy/SKILL.md"
) -> List[Dict]:
    """Process all Python files in a directory."""
    
    py_files = sorted(Path(directory).glob("*.py"))
    
    if not py_files:
        print(f"No Python files found in {directory}/")
        return []
    
    print(f"\nFound {len(py_files)} Python file(s) to process")
    
    results = []
    for py_file in py_files:
        result = process_code_file(
            str(py_file),
            output_dir=output_dir,
            api_key=api_key,
            agent_path=agent_path,
            skill_path=skill_path
        )
        results.append(result)
    
    return results


def print_summary(results: List[Dict], mode: str = "generate"):
    """Print summary of processing results."""
    print("\n" + "=" * 60)
    print(f"{'TEST GENERATION' if mode == 'generate' else 'TEST EVALUATION'} SUMMARY")
    print("=" * 60)
    
    completed = [r for r in results if r.get('status') == 'completed']
    prompt_only = [r for r in results if r.get('status') == 'prompt_only']
    errors = [r for r in results if r.get('status') == 'error']
    
    print(f"\nTotal processed: {len(results)}")
    print(f"  ✓ Completed:    {len(completed)}")
    print(f"  ○ Prompt only:  {len(prompt_only)}")
    print(f"  ✗ Errors:       {len(errors)}")
    
    if completed:
        print("\n" + "-" * 60)
        print("COMPLETED:")
        print("-" * 60)
        for r in completed:
            if mode == "generate":
                print(f"\n  {Path(r['code_path']).name}")
                print(f"  → {r['test_file']}")
            else:
                print(f"\n  {Path(r['test_path']).name}")
                print(f"  → {r['evaluation_file']}")
    
    if prompt_only:
        print("\n" + "-" * 60)
        print("PROMPTS SAVED (no API key):")
        print("-" * 60)
        print("\nTo complete, either:")
        print("  1. Set ANTHROPIC_API_KEY and re-run")
        print("  2. Copy prompt to claude.ai manually")
        for r in prompt_only:
            key = 'code_path' if mode == 'generate' else 'test_path'
            print(f"\n  {Path(r[key]).name}")
            print(f"  → {r['prompt_file']}")
    
    if errors:
        print("\n" + "-" * 60)
        print("ERRORS:")
        print("-" * 60)
        for r in errors:
            key = 'code_path' if 'code_path' in r else 'test_path'
            if key in r:
                print(f"\n  {Path(r[key]).name}")
            print(f"  → {r.get('error', 'Unknown error')}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate and evaluate tests using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate tests for all files in sample-code/
  python generate_tests.py
  
  # Generate tests for a specific file
  python generate_tests.py sample-code/user_service.py
  
  # Evaluate existing tests
  python generate_tests.py --evaluate tests/test_user.py
  
  # Evaluate with source file for context
  python generate_tests.py --evaluate tests/test_user.py --source user.py

Environment:
  ANTHROPIC_API_KEY    Your Claude API key (required for automated generation)
        """
    )
    
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to a single code file to process"
    )
    parser.add_argument(
        "--dir", "-d",
        default="sample-code",
        help="Directory containing code files (default: sample-code/)"
    )
    parser.add_argument(
        "--output", "-o",
        default="generated-tests",
        help="Output directory (default: generated-tests/)"
    )
    parser.add_argument(
        "--evaluate", "-e",
        metavar="TEST_FILE",
        help="Evaluate an existing test file instead of generating"
    )
    parser.add_argument(
        "--source", "-s",
        help="Source code file for test evaluation (optional)"
    )
    parser.add_argument(
        "--agent", "-a",
        default="AGENTS.md",
        help="Path to agent instructions (default: AGENTS.md)"
    )
    parser.add_argument(
        "--skill", "-k",
        default=".github/skills/test-strategy/SKILL.md",
        help="Path to skill rubric (default: .github/skills/test-strategy/SKILL.md)"
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    
    # Check for anthropic library
    if api_key and not HAS_ANTHROPIC:
        print("Error: anthropic library not installed")
        print("Run: pip install anthropic")
        sys.exit(1)
    
    print("=" * 60)
    print("SPECIALIZED TESTING AGENT")
    print("=" * 60)
    print(f"Agent:  {args.agent}")
    print(f"Skill:  {args.skill}")
    print(f"Output: {args.output}/")
    print(f"API:    {'Claude API (automated)' if api_key else 'None (prompt-only mode)'}")
    
    # Evaluate mode
    if args.evaluate:
        if not os.path.exists(args.evaluate):
            print(f"\nError: Test file not found: {args.evaluate}")
            sys.exit(1)
        
        results = [evaluate_test_file(
            args.evaluate,
            source_path=args.source,
            output_dir=args.output if args.output != "generated-tests" else "test-evaluations",
            api_key=api_key,
            agent_path=args.agent,
            skill_path=args.skill
        )]
        print_summary(results, mode="evaluate")
    
    # Generate mode
    elif args.file:
        if not os.path.exists(args.file):
            print(f"\nError: File not found: {args.file}")
            sys.exit(1)
        
        results = [process_code_file(
            args.file,
            output_dir=args.output,
            api_key=api_key,
            agent_path=args.agent,
            skill_path=args.skill
        )]
        print_summary(results, mode="generate")
    
    else:
        if not os.path.exists(args.dir):
            print(f"\nError: Directory not found: {args.dir}")
            sys.exit(1)
        
        results = batch_process_directory(
            directory=args.dir,
            output_dir=args.output,
            api_key=api_key,
            agent_path=args.agent,
            skill_path=args.skill
        )
        print_summary(results, mode="generate")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
