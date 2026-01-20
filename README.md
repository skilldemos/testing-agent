# Specialized Testing Agent Demo

An intelligent AI agent system for automated test generation, test quality evaluation, and testing strategy development using GitHub Copilot.

## Overview

This demo shows how to use AI agents with structured skills to:
- **Generate comprehensive test suites** for Python code
- **Evaluate existing tests** against quality metrics
- **Develop testing strategies** for features and systems
- **Ensure consistent testing standards** across teams

## Setup Time: ~2 minutes

## Files Included

```
testing-agent-demo/
├── AGENTS.md                           # Agent definition for GitHub Copilot
├── .github/
│   └── skills/
│       └── test-strategy/
│           └── SKILL.md                # Testing skill with 100-point rubric
├── sample-code/
│   ├── user_service.py                 # E-commerce user management module
│   └── shopping_cart.py                # Shopping cart with complex logic
├── pipeline/
│   └── generate_tests.py               # Automated test generation script
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Three Demo Options

### Option 1: GitHub Copilot Agent Mode (Quick, 5 min)

Best for: Showing AI-powered test generation with minimal setup

```
User prompt → Copilot reads AGENTS.md → Reads skill → Analyzes code → Generates tests
```

**Steps:**
1. Open project in VS Code with GitHub Copilot
2. Ask: `@workspace Generate comprehensive unit tests for sample-code/user_service.py using skills/test-strategy.md`
3. Watch Copilot:
   - Analyze the code structure
   - Apply the testing rubric
   - Generate complete test suite with fixtures, mocks, and assertions
   - Include edge cases and error handling

**Example prompts:**
```
@workspace Generate tests for user_service.py that cover all edge cases

@workspace Evaluate the test quality of tests/test_shopping_cart.py using the rubric in skills/test-strategy.md

@workspace Create a testing strategy for the shopping cart module
```

### Option 2: Python Script (Production-Ready, 10 min)

Best for: Showing automated pipeline for batch test generation

```
generate_tests.py → Analyze code → Call Claude API → Generate test suite → Save to file
```

**Setup:**
```bash
# Install dependencies
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Generate tests for all sample code
python pipeline/generate_tests.py
```

**Output:**
- `generated-tests/test_user_service_<timestamp>.py` - Complete test suite
- `generated-tests/user_service_analysis.txt` - Code analysis report
- Test quality target: 85+/100 on rubric

**Advanced usage:**
```bash
# Generate tests for a specific file
python pipeline/generate_tests.py sample-code/shopping_cart.py

# Evaluate existing tests
python pipeline/generate_tests.py --evaluate tests/test_user.py --source sample-code/user_service.py

# Process a different directory
python pipeline/generate_tests.py --dir src/ --output test-output/
```

### Option 3: Manual Prompt Mode (No API Key, 5 min)

Best for: Demos where you don't want to expose API keys

```bash
# Run without API key - generates prompts only
python pipeline/generate_tests.py
```

**Output:**
- Prompt files saved to `generated-tests/`
- Copy prompts to claude.ai or GitHub Copilot
- Paste generated tests back into your project

---

## Demo Flow (10-15 minutes)

### 1. Show the Structure (2 min)

- **Open `AGENTS.md`** - Explain this defines the agent's testing capabilities
- **Open `.github/skills/test-strategy/SKILL.md`** - Show the 100-point rubric
- **Open `sample-code/user_service.py`** - Show realistic code that needs testing

**Key points:**
- ✓ Rubric is auditable and adjustable by technical leads
- ✓ Agent follows consistent testing patterns
- ✓ Works with any testing framework (pytest, Jest, JUnit, etc.)

### 2. Generate Tests with Copilot (5 min)

In GitHub Copilot Chat:

```
@workspace Generate comprehensive unit tests for sample-code/user_service.py 
following the test-strategy skill. Include:
- Test fixtures for database and email service mocks
- Happy path tests for registration and authentication
- Edge case tests (empty inputs, max lengths, special characters)
- Error handling tests (duplicate users, invalid passwords)
- Use pytest framework with proper AAA structure
```

**Watch it:**
- Analyze the code structure (classes, methods, dependencies)
- Identify critical paths and edge cases
- Generate complete test file with:
  - Fixtures for mocks
  - Descriptive test names
  - AAA pattern (Arrange, Act, Assert)
  - Edge case coverage
  - Error handling tests

### 3. Evaluate Test Quality (3 min)

After generating tests, evaluate them:

```
@workspace Evaluate the test quality of the generated tests using 
the rubric in .github/skills/test-strategy/SKILL.md. Provide:
- Scores for each category
- What's covered well
- What's missing
- Specific recommendations
```

**Expected output:**
- Completeness: 28/30 (missing performance test edge case)
- Quality: 24/25 (excellent naming and structure)
- Reliability: 20/20 (proper mocking, no flaky tests)
- Layers: 15/15 (good unit test coverage)
- Best Practices: 9/10 (could add more docstrings)
- **Total: 96/100 - Excellent tier**

### 4. Show Batch Processing (2 min)

Run the Python script:

```bash
python pipeline/generate_tests.py
```

**Demonstrate:**
- Processes multiple files automatically
- Analyzes code complexity
- Generates comprehensive tests
- Creates analysis reports
- Scalable to hundreds of files

### 5. Compare to Manual Testing (3 min)

**Traditional approach:**
- Developer writes tests manually: 2-4 hours per module
- Inconsistent patterns across team
- Often skips edge cases
- May miss error handling scenarios

**AI Agent approach:**
- Generates comprehensive tests: 5 minutes per module
- Consistent patterns (follows rubric)
- Systematically covers edge cases
- Includes error handling by default
- Developer reviews and refines: 30 minutes

**ROI:**
- 3-4x faster test creation
- Higher quality coverage
- Consistent across team
- Frees developers for complex scenarios

---

## Key Talking Points

### Why This Approach Works

1. **Structured Rubric**
   - 100-point scoring system ensures completeness
   - Categories cover all aspects of test quality
   - Easy for teams to customize weights

2. **Consistent Patterns**
   - AAA structure (Arrange, Act, Assert)
   - Descriptive test names
   - Proper mocking strategies
   - Framework best practices

3. **Scalable**
   - Works for any codebase size
   - Batch process entire directories
   - CI/CD integration ready
   - Multi-language support (adapt SKILL.md)

4. **Educational**
   - Junior developers learn from generated tests
   - Documents testing patterns
   - Shows edge cases they might miss
   - Teaches mocking strategies

5. **Auditable**
   - Every test decision is traceable
   - Rubric explains the "why"
   - Easy to review and improve
   - Compliance-friendly

### When to Use This

✓ **Good fit:**
- New feature development (generate tests as you code)
- Legacy code (add tests to untested code)
- Test quality audits (evaluate and improve existing tests)
- Team consistency (standardize testing patterns)
- Junior developer onboarding (learn by example)

✗ **Not ideal for:**
- Ultra-performance-critical code (needs manual optimization)
- Highly specialized domains (may need custom rubrics)
- Very simple code (manual tests might be faster)

---

## Technical Details

### Requirements

```bash
pip install anthropic  # For AI test generation
# Code analysis uses built-in ast module
```

### Python Script Features

The `generate_tests.py` script provides:

1. **Code Analysis**
   - Parses Python files with AST
   - Identifies functions, classes, methods
   - Calculates complexity scores
   - Detects dependencies

2. **Test Generation**
   - Uses Claude API for generation
   - Applies structured rubric
   - Generates pytest-format tests
   - Includes fixtures and mocks

3. **Test Evaluation**
   - Scores existing tests against rubric
   - Identifies gaps and issues
   - Provides specific recommendations
   - Generates improvement plans

4. **Batch Processing**
   - Process entire directories
   - Parallel execution ready
   - Progress tracking
   - Summary reports

### Command Line Usage

```bash
# Show help
python pipeline/generate_tests.py --help

# Generate tests for all files in sample-code/
python pipeline/generate_tests.py

# Generate tests for a specific file
python pipeline/generate_tests.py sample-code/user_service.py

# Evaluate existing tests
python pipeline/generate_tests.py --evaluate tests/test_user.py

# Evaluate with source code context
python pipeline/generate_tests.py --evaluate tests/test_user.py --source sample-code/user_service.py

# Use different agent/skill files
python pipeline/generate_tests.py --agent custom-agent.md --skill custom-skill.md

# Save to different output directory
python pipeline/generate_tests.py --output my-tests/
```

---

## Customization for Your Team

### Adapt the Rubric

Edit `.github/skills/test-strategy/SKILL.md` to:

1. **Adjust point weights**
   ```markdown
   # Emphasize security testing
   Security-critical functions tested | 5 points  # was 2
   ```

2. **Add framework-specific patterns**
   ```markdown
   # For React/Jest
   - Use data-testid for selectors
   - Mock useContext hooks
   - Test loading and error states
   ```

3. **Include domain requirements**
   ```markdown
   # Healthcare applications
   - HIPAA compliance checks
   - PHI data masking in tests
   - Audit trail validation
   ```

### Extend the Agent

Edit `AGENTS.md` to:

1. **Add specialized capabilities**
   ```markdown
   ## Performance Testing
   When generating tests for performance-critical code:
   - Include benchmark tests
   - Test with realistic data volumes
   - Measure memory usage
   ```

2. **Include company conventions**
   ```markdown
   ## Our Testing Standards
   - All tests must run in < 5 seconds
   - Use factory_boy for test data
   - Follow naming: test_<method>_<scenario>_<expected>
   ```

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Test Quality Check

on: [pull_request]

jobs:
  evaluate-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Evaluate test quality
        run: |
          pip install anthropic
          python pipeline/generate_tests.py --evaluate tests/ --output reports/
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      
      - name: Check quality threshold
        run: |
          # Parse reports and fail if score < 70
          python scripts/check_test_quality.py reports/
```

---

## Cost Comparison

| Approach | Per-Module Cost | Quality | Consistency |
|----------|-----------------|---------|-------------|
| Manual (Senior Dev) | 2-4 hours ($100-200) | High | Variable |
| **AI Agent** | **5 min + 30 min review ($5-10)** | **High** | **Excellent** |
| Junior Dev | 4-8 hours ($50-150) | Medium | Variable |
| Outsourced | 1-2 weeks ($500-2000) | Variable | Low |

**Break-even: ~10 modules** (saves 20-40 hours of development time)

---

## Common Questions

**Q: Can the AI generate tests for languages other than Python?**  
A: Yes! Update the SKILL.md with framework-specific patterns (Jest, JUnit, RSpec) and the agent will adapt.

**Q: What about flaky tests?**  
A: The rubric explicitly penalizes flaky tests. The agent generates deterministic tests with proper mocking.

**Q: How do I integrate this with our existing test suite?**  
A: Generate tests to a review directory, have developers review/refine, then merge. Treat AI as a "first draft" author.

**Q: Can it test complex business logic?**  
A: Yes, but works best when you provide context. Example: "Generate tests for the discount calculation logic. The business rule is: orders > $100 get 10% off, VIP customers get 15% off, and discounts stack."

**Q: What about test data privacy?**  
A: Generated tests use synthetic data. For sensitive domains, review and anonymize before committing.

**Q: How often should we regenerate tests?**  
A: When code changes significantly, or every 6 months to adopt new testing patterns and improve coverage.

---

## Next Steps

1. **Try the demo** with your own codebase
2. **Customize the rubric** for your team's standards
3. **Integrate into CI/CD** for automated test quality checks
4. **Train your team** on reviewing and refining AI-generated tests
5. **Track metrics** (test coverage, bug detection, development time)

---

## Support and Feedback

This demo was created to showcase AI agents with structured skills for software testing. Adapt it freely for your needs!

**Related Resources:**
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

---

**Built with:**
- GitHub Copilot for agent interactions
- Claude API for automated generation
- Python AST for code analysis
- Structured prompting for consistent results
