# Side-by-Side Comparison: Resume Agent vs Testing Agent

This document shows how the testing agent mirrors the resume scoring agent structure.

## File Structure Comparison

```
Resume Scoring Agent              Testing Agent
══════════════════════            ══════════════════════
rescore/                          testing-agent-demo/
│                                 │
├── AGENTS.md                     ├── AGENTS.md
│   Purpose: Resume screening     │   Purpose: Test generation/evaluation
│   Task: Score resumes           │   Task: Generate and evaluate tests
│   Rubric: skills/resume-scoring │   Rubric: skills/test-strategy
│                                 │
├── .github/                      ├── .github/
│   └── skills/                   │   └── skills/
│       └── resume-scoring/       │       └── test-strategy/
│           └── SKILL.md          │           └── SKILL.md
│               100-point rubric  │               100-point rubric
│               5 categories      │               5 categories
│               Quality tiers     │               Quality tiers
│                                 │
├── sample-resumes/               ├── sample-code/
│   ├── sarah-chen.pdf            │   ├── user_service.py
│   └── marcus-johnson.pdf        │   └── shopping_cart.py
│   Sample input files            │   Sample input files
│                                 │
├── pipeline/                     ├── pipeline/
│   └── screen_resumes.py         │   └── generate_tests.py
│       - Extract PDF text        │       - Analyze code with AST
│       - Create prompt           │       - Create prompt
│       - Call Claude API         │       - Call Claude API
│       - Generate evaluation     │       - Generate tests/evaluation
│       - Batch processing        │       - Batch processing
│                                 │
├── requirements.txt              ├── requirements.txt
│   pdfplumber, anthropic         │   anthropic, pytest
│                                 │
└── README.md                     └── README.md
    Demo guide & docs                 Demo guide & docs
```

## AGENTS.md Comparison

### Resume Agent (rescore/AGENTS.md)
```markdown
# Resume Screening Agent

## Purpose
You are a scientific resume screening agent for a biomedical research 
organization...

## Primary Task
Review, summarize, and qualify scientific resumes/applications (PDF format)...

## Working with PDF Resumes
When given a PDF resume to review:
1. **Extract text** from the PDF using pdfplumber
2. **Parse** the extracted content
3. **Process** according to workflow

## Workflow
1. Extract - Pull text from PDF
2. Parse - Identify sections
3. Summarize - Create overview
4. Score - Apply rubric from skills/resume-scoring.md
5. Qualify - Determine tier
6. Report - Generate structured output

## Output Format
## Candidate Summary
- **Name**: [extracted]
- **Current Role**: [extracted]
...
```

### Testing Agent (testing-agent-demo/AGENTS.md)
```markdown
# Specialized Testing Agent

## Purpose
You are an intelligent testing agent specialized in automated test 
generation, test quality assessment, and test strategy development...

## Primary Task
Analyze code, generate appropriate tests, evaluate existing test suites...

## Working with Code Files
When given code to test:
1. **Analyze** the code structure
2. **Identify** critical paths
3. **Generate** appropriate test cases

## Workflow (Test Generation)
1. Understand Context
2. Analyze the Code
3. Generate Tests
4. Validate Quality

## Output Format
# Test Suite: [Module/Feature Name]
import pytest
from unittest.mock import Mock

class Test[FeatureName]:
    ...
```

**Pattern:** Both define purpose, workflow, and structured output format.

---

## SKILL.md Comparison

### Resume Scoring Rubric (resume-scoring/SKILL.md)

```markdown
---
name: resume-scoring
description: Score and evaluate scientific resumes for biomedical research positions.
---

# Scientific Resume Scoring

## Scoring Rubric (100 points total)

### 1. Educational Background (25 points max)
| Criteria | Points |
|----------|--------|
| PhD in directly relevant field | 25 |
| PhD in related field | 20 |
| Master's in relevant field | 15 |
...
| Degree from recognized institution | +2 bonus |

### 2. Research Experience (30 points max)
| Criteria | Points |
|----------|--------|
| 5+ years post-doctoral | 30 |
| 3-5 years post-doctoral | 25 |
...

### 3. Publication Record (20 points max)
### 4. Technical Skills Alignment (15 points max)
### 5. Mission Alignment & Collaboration (10 points max)

## Qualification Tiers
| Score Range | Tier | Action |
|-------------|------|--------|
| 80-100+ | Highly Qualified | Priority review |
| 65-79 | Qualified | Standard review |
| 50-64 | Potentially Qualified | Review if pool limited |
| Below 50 | Not Qualified | Archive |

## Output Format
[Structured template]

## Red Flags to Note
- Gaps in timeline
- Claims that cannot be verified
...
```

### Testing Strategy Rubric (test-strategy/SKILL.md)

```markdown
---
name: test-strategy
description: Evaluate test suite quality, generate comprehensive test cases...
---

# Specialized Testing Strategy

## Test Quality Evaluation Rubric (100 points total)

### 1. Test Completeness (30 points max)
| Criteria | Points |
|----------|--------|
| Critical paths fully tested | 12 |
| Edge cases covered | 8 |
| Error handling tested | 5 |
...
| Line coverage ≥ 80% | +3 bonus |

### 2. Test Quality & Maintainability (25 points max)
| Criteria | Points |
|----------|--------|
| AAA pattern followed | 5 |
| Descriptive test names | 5 |
...

### 3. Test Reliability (20 points max)
### 4. Testing Layers (15 points max)
### 5. Best Practices (10 points max)

## Quality Tiers
| Score Range | Tier | Action |
|-------------|------|--------|
| 85-100 | Excellent | Production-ready |
| 70-84 | Good | Minor gaps |
| 55-69 | Adequate | Improvements recommended |
| 40-54 | Needs Improvement | Major gaps |
| Below 40 | Insufficient | Significant work |

## Test Generation Guidelines
[Structured templates]

## Red Flags in Test Suites
- Flaky Tests
- Over-Mocking
- Assertion Roulette
...
```

**Pattern:** Both use 100-point system, 5 categories, bonus points, tiers, and red flags.

---

## Python Pipeline Comparison

### Resume Scorer (screen_resumes.py)

```python
#!/usr/bin/env python3
"""Resume Screening Demo Script"""

import pdfplumber
import anthropic

def extract_resume_text(pdf_path: str) -> str:
    """Extract text content from a PDF resume."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def load_scoring_rubric(rubric_path: str) -> str:
    """Load the scoring rubric from markdown file."""
    with open(rubric_path, 'r') as f:
        return f.read()

def create_scoring_prompt(resume_text, rubric, agent_instructions):
    """Create the prompt for LLM scoring."""
    return f"""{agent_instructions}
    
    ## SCORING RUBRIC
    {rubric}
    
    ## RESUME CONTENT
    {resume_text}
    
    ## YOUR TASK
    Score this resume following the rubric exactly...
    """

def score_resume_with_claude(prompt, api_key):
    """Send the prompt to Claude API."""
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def process_resume(pdf_path, output_dir, api_key):
    """Process a single resume."""
    # Extract, load rubric, create prompt, send to API
    ...

def batch_process_resumes(resume_dir, output_dir, api_key):
    """Process all PDFs in a directory."""
    ...
```

### Test Generator (generate_tests.py)

```python
#!/usr/bin/env python3
"""Test Generation and Evaluation Pipeline"""

import ast
import anthropic

def analyze_code_file(file_path: str) -> Dict:
    """Analyze a Python file to identify testable components."""
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    
    # Extract functions and classes
    functions = [node for node in ast.walk(tree) 
                 if isinstance(node, ast.FunctionDef)]
    return {'functions': functions, 'complexity': ...}

def load_skill_rubric(skill_path: str) -> str:
    """Load the test strategy skill rubric."""
    with open(skill_path, 'r') as f:
        return f.read()

def create_test_generation_prompt(code_content, analysis, 
                                  agent_instructions, skill_rubric):
    """Create a prompt for AI to generate comprehensive tests."""
    return f"""{agent_instructions}
    
    ## TEST GENERATION GUIDELINES
    {skill_rubric}
    
    ## CODE TO TEST
    {code_content}
    
    ## YOUR TASK
    Generate a comprehensive test suite...
    """

def generate_tests_with_ai(prompt, api_key):
    """Send prompt to Claude API."""
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def process_code_file(code_path, output_dir, api_key):
    """Process a code file and generate tests."""
    # Analyze, load rubric, create prompt, send to API
    ...

def batch_process_directory(directory, output_dir, api_key):
    """Process all Python files in a directory."""
    ...
```

**Pattern:** Both follow same structure:
1. Input extraction/analysis
2. Load rubric
3. Create structured prompt
4. API call
5. Output formatting
6. Batch processing

---

## Scoring Categories Comparison

### Resume Agent - 100 Points Total

| Category | Points | Measures |
|----------|--------|----------|
| Educational Background | 25 | PhD, MD, degrees, institution |
| Research Experience | 30 | Years, leadership, funding |
| Publication Record | 20 | Papers, impact, authorship |
| Technical Skills | 15 | Method alignment, expertise |
| Mission Alignment | 10 | Open science, collaboration |

### Testing Agent - 100 Points Total

| Category | Points | Measures |
|----------|--------|----------|
| Test Completeness | 30 | Coverage, edge cases, errors |
| Test Quality | 25 | Structure, naming, isolation |
| Test Reliability | 20 | No flakiness, proper mocking |
| Testing Layers | 15 | Unit, integration, E2E |
| Best Practices | 10 | Conventions, documentation |

**Pattern:** Both use 5 categories totaling 100 points with bonus systems.

---

## Demo Flow Comparison

### Resume Agent Demo

1. **Show structure** (AGENTS.md, SKILL.md, sample PDFs)
2. **Run agent** via Copilot: `@workspace Review sarah-chen.pdf`
3. **Compare results** on multiple resumes
4. **Batch processing** with Python script
5. **Discussion** of fairness, transparency, scalability

### Testing Agent Demo

1. **Show structure** (AGENTS.md, SKILL.md, sample code)
2. **Run agent** via Copilot: `@workspace Generate tests for user_service.py`
3. **Evaluate quality** against rubric
4. **Batch processing** with Python script
5. **Discussion** of consistency, coverage, ROI

**Pattern:** Same demo structure, different domain.

---

## Usage Patterns

### Resume Agent Usage

```bash
# Process all resumes
python screen_resumes.py

# Process single resume
python screen_resumes.py resume.pdf

# With API key
export ANTHROPIC_API_KEY="sk-ant-..."
python screen_resumes.py
```

### Testing Agent Usage

```bash
# Generate tests for all code
python generate_tests.py

# Generate for single file
python generate_tests.py user_service.py

# With API key
export ANTHROPIC_API_KEY="sk-ant-..."
python generate_tests.py
```

**Pattern:** Identical command-line interfaces.

---

## Customization Points

### Both Agents Support

1. **Adjust rubric weights**
   - Edit SKILL.md point values
   - Add new categories
   - Change tier thresholds

2. **Modify agent behavior**
   - Edit AGENTS.md workflow
   - Add domain-specific rules
   - Change output format

3. **Extend automation**
   - Add to CI/CD pipeline
   - Batch process directories
   - Generate reports

---

## Key Differences (Domain-Specific)

| Aspect | Resume Agent | Testing Agent |
|--------|--------------|---------------|
| **Input format** | PDF files | Python source files |
| **Input parsing** | pdfplumber | AST module |
| **Output** | Markdown evaluation | Python test code |
| **Domain** | HR/Recruiting | Software Engineering |
| **Use case** | Hiring decisions | Quality assurance |
| **Users** | Hiring managers | Developers, QA engineers |

---

## Why This Comparison Matters

The testing agent successfully demonstrates that the AI agent + skill pattern:

✅ **Is reproducible** - Same structure works for different domains
✅ **Is adaptable** - Change the rubric, change the domain
✅ **Is educational** - One example teaches the pattern
✅ **Is scalable** - Works for many use cases

### Other Potential Applications

Using this same pattern, you could build:

1. **Code Review Agent**
   - AGENTS.md: Define review standards
   - SKILL.md: Style, security, performance rubrics
   - Input: Pull request diffs
   - Output: Review comments

2. **Documentation Agent**
   - AGENTS.md: Define documentation standards
   - SKILL.md: Completeness, clarity, examples rubric
   - Input: Code files
   - Output: Generated documentation

3. **Security Audit Agent**
   - AGENTS.md: Define audit process
   - SKILL.md: Vulnerability scoring rubric
   - Input: Codebase
   - Output: Security assessment

4. **API Design Agent**
   - AGENTS.md: Define REST/GraphQL standards
   - SKILL.md: Design quality rubric
   - Input: API specs
   - Output: Design evaluation

---

## Conclusion

The testing agent successfully mirrors the resume agent structure while addressing a more common use case (software testing). The pattern is clear, reproducible, and adaptable to many domains where structured evaluation and generation are needed.

**Key Success Factors:**
1. ✅ Same file structure
2. ✅ Same rubric approach (100 points, 5 categories, tiers)
3. ✅ Same automation pattern (Python + Claude API)
4. ✅ Same demo flow
5. ✅ More common use case (testing vs HR)
6. ✅ Production-ready with complete docs

This demonstrates that the AI agent + structured skill pattern is a robust framework for building domain-specific automation tools.
