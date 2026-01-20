# Understanding the SKILL.md Rubric System

## The Problem This Solves

**Without a rubric, AI evaluations are:**
- Inconsistent (same code scored differently each time)
- Subjective (no clear criteria)
- Not comparable (can't compare across evaluations)
- Not actionable (vague feedback like "needs improvement")

**With a structured rubric, AI evaluations become:**
- ✅ Consistent (same code = same score)
- ✅ Objective (clear point-based criteria)
- ✅ Comparable (89/100 vs 72/100 is meaningful)
- ✅ Actionable (specific gaps identified with point values)

---

## How the Agent Uses the Rubric

### 1. The Agent Reads SKILL.md as Instructions

When you invoke the agent, it:

```
User: "Generate tests for user_service.py"
  ↓
Agent reads: AGENTS.md (what I am, what I do)
  ↓
Agent reads: .github/skills/test-strategy/SKILL.md (HOW to evaluate quality)
  ↓
Agent generates tests following the rubric criteria
  ↓
Agent self-evaluates: "Will this score 85+/100?"
  ↓
Agent outputs tests designed to meet the rubric
```

The rubric is literally part of the prompt sent to the AI. It says:
> "Generate tests that will score high on these specific criteria..."

### 2. Rubric as a Contract

Think of SKILL.md as a **contract between you and the AI**:

| You Define | AI Delivers |
|------------|-------------|
| "Edge cases are worth 8 points" | AI ensures edge cases are included |
| "AAA pattern is worth 5 points" | AI structures tests with Arrange/Act/Assert |
| "Coverage ≥80% gets +3 bonus" | AI generates enough tests for 80% coverage |

It's like hiring a contractor with a detailed specification document.

---

## The Scoring System Explained

### Base Points (100 total)

```markdown
### 1. Test Completeness (30 points max)
| Criteria | Points |
|----------|--------|
| Critical paths fully tested | 12 |
| Edge cases covered | 8 |
| Error handling tested | 5 |
| Input validation tested | 3 |
| Security functions tested | 2 |
```

**Purpose of base points:**
- Define what "complete" means
- Give AI specific targets
- Allow granular scoring
- Show what matters most (critical paths = 12 pts, security = 2 pts)

**How the agent uses this:**
```python
# Agent thinks: "I need 12 points for critical paths"
# So it generates:
def test_register_user_with_valid_data():  # Happy path ✓
def test_authenticate_user_success():       # Happy path ✓
def test_authenticate_user_wrong_password(): # Error path ✓
# All critical paths covered → 12/12 points
```

### Bonus Points (Extra credit, but capped)

```markdown
**Coverage Bonuses:**
- Line coverage ≥ 80%: +3 bonus
- Branch coverage ≥ 70%: +3 bonus
- All public APIs tested: +2 bonus
```

**Purpose of bonuses:**
- Reward going above and beyond
- Incentivize best practices
- But prevent gaming (note the cap at category max)

**Key rule:** Bonuses can help reach the category max but CANNOT exceed it.

Example:
```
Category: Test Completeness (30 points max)
Base points earned: 28
Bonus points available: +8 (coverage bonuses)
  
Final score: 30/30 (capped, not 36)
```

**How the agent uses this:**
```python
# Agent thinks: "I'm at 28/30, I can earn +3 for 80% coverage"
# So it generates extra tests:
def test_user_tier_calculation_bronze():
def test_user_tier_calculation_silver():
def test_user_tier_calculation_gold():
def test_user_tier_calculation_platinum():
# Now coverage is 85% → +3 bonus → 30/30 total (capped)
```

---

## Quality Tiers: Converting Score to Action

```markdown
| Score Range | Tier | Action |
|-------------|------|--------|
| 85-100 | Excellent | Production-ready |
| 70-84 | Good | Minor improvements needed |
| 55-69 | Adequate | Significant improvements needed |
| 40-54 | Needs Improvement | Major gaps |
| Below 40 | Insufficient | Not ready for production |
```

**Purpose:**
- Make scores actionable
- Set quality gates for CI/CD
- Give clear guidance (not just a number)

**How teams use this:**
```yaml
# In CI/CD pipeline:
- name: Check test quality
  run: |
    score=$(evaluate_tests.py)
    if [ $score -lt 70 ]; then
      echo "Test quality below threshold"
      exit 1  # Fail the build
    fi
```

---

## Real Example: How It All Works Together

### Scenario: Agent evaluates existing tests

**Input:** Test file with 10 tests

**Agent's process:**

1. **Read the rubric** (SKILL.md)
2. **Count critical paths:** 8/10 covered → 10/12 points
3. **Check edge cases:** 5 found, 3 missing → 5/8 points
4. **Check error handling:** All 5 error paths tested → 5/5 points
5. **Check validation:** 2/3 validation tests → 2/3 points
6. **Check security:** No security tests → 0/2 points
7. **Total base:** 22/30

8. **Check bonuses:**
   - Line coverage: 75% → No bonus (need 80%)
   - Branch coverage: 72% → +3 bonus ✓
   - All public APIs: No → 0
   
9. **Final score:** 22 + 3 = 25/30 for Test Completeness

10. **Repeat for other categories...**

11. **Grand total:** 72/100 → "Good" tier

**Agent's output:**
```markdown
## Test Suite Evaluation

### Test Completeness: 25/30
- Critical paths: 10/12 (missing user deactivation, password reset)
- Edge cases: 5/8 (missing: max name length, special chars, empty email)
- Error handling: 5/5 ✓
- Validation: 2/3 (missing: negative age test)
- Security: 0/2 (no SQL injection or XSS tests)
- Bonus: +3 (branch coverage 72%)

### Overall: 72/100 - Good
**Action:** Add missing critical paths and security tests to reach 85+
```

---

## Why This Design is Powerful

### 1. Consistency Through Structure

**Without rubric:**
```
User: "Review my tests"
AI: "These look pretty good, maybe add more edge cases"
```
(Vague, not measurable, not comparable)

**With rubric:**
```
User: "Review my tests"
AI: "Test Completeness: 25/30
     - Missing 2 critical paths (user deactivation, password reset)
     - Missing 3 edge cases (max length, special chars, empty email)
     - Add these to reach 30/30"
```
(Specific, measurable, actionable)

### 2. Teaching Through Example

The rubric teaches the AI (and developers) what "quality" means:

```markdown
| Descriptive test names | 5 points |
```

This tells the AI:
- "test_1" is bad (0/5 points)
- "test_register" is better (2/5 points)
- "test_register_user_with_valid_email_succeeds" is best (5/5 points)

### 3. Customizable Standards

Different teams have different priorities:

**FinTech company (security-critical):**
```markdown
| Security-critical functions tested | 10 |  # Increased from 2
| SQL injection tests | 5 |               # New category
```

**Startup (move fast):**
```markdown
| Critical paths tested | 12 |
| Edge cases covered | 3 |               # Decreased from 8
```

Just edit the point values → Agent adapts immediately.

### 4. Audit Trail

Every decision is traceable:

```markdown
Score: 72/100
- Why? Because missing 8 points in edge cases
- Which edge cases? Max length, special chars, empty input
- Why do those matter? Rubric says edge cases = 8 points
- How to fix? Add those 3 tests → score increases to 80/100
```

This is critical for:
- Code reviews (objective feedback)
- Hiring decisions (fair comparisons)
- Compliance (auditable process)

---

## The Math Behind Bonuses

### Why Cap Bonuses?

**Without cap:**
```
Base points: 15/30
Bonus points: +20
Total: 35/30 ??? This makes no sense
```

**With cap:**
```
Base points: 15/30
Bonus points available: +20
Total: 30/30 (capped - incentive to improve base first)
```

**The strategy:**
1. First, meet base criteria (get to 25-28/30)
2. Then, bonuses help reach max (28 → 30)
3. Bonuses can't compensate for missing basics

### Example: You Can't Game the System

```markdown
Test Completeness (30 max):
- Critical paths: 4/12 (barely tested)
- Edge cases: 2/8 (mostly missing)
- Bonuses: +8 (excellent coverage)

Total: 14/30 (not 14 + 8 = 22)
Why? Because bonuses can't exceed category max
And you only get bonuses ON TOP of base
So: 14 base + min(8 bonus, 30 - 14 cap) = 14 + 8 = 22? No!
Actually: 14 + 8 = 22, but 22 is less than 30, so 22/30

Wait, let me recalculate correctly:
Base: 4 + 2 = 6 points
Bonuses: +8 points
Total: 6 + 8 = 14/30 (bonuses added, but still far from max)

The point: Bonuses reward excellence, but can't fix fundamental gaps.
```

Actually, the rubric says bonuses can help reach max but not exceed:
```
If base + bonus > max → cap at max
Example: 28 base + 5 bonus = 30 (capped, noted as "capped from 33")
```

---

## How to Use This in Practice

### For Developers:

1. **Before writing tests:**
   - Read SKILL.md
   - Understand what scores points
   - Plan tests to hit high-value categories

2. **While writing tests:**
   - Check rubric: "Am I covering edge cases?" (8 points)
   - Use AAA pattern (5 points)
   - Write descriptive names (5 points)

3. **After writing tests:**
   - Self-score against rubric
   - "I have 25/30 in completeness, missing 3 edge cases"
   - Add those specific tests

### For Teams:

1. **Customize the rubric:**
   ```bash
   # Edit .github/skills/test-strategy/SKILL.md
   # Adjust point values for your priorities
   ```

2. **Set quality gates:**
   ```yaml
   # In CI/CD:
   minimum_score: 75  # Matches "Good" tier
   ```

3. **Track trends:**
   ```
   Week 1: Avg score 68/100
   Week 2: Avg score 74/100  # Improving!
   Week 3: Avg score 82/100  # "Good" tier reached
   ```

### For AI Agents:

The agent uses the rubric as its evaluation function:

```python
def evaluate_tests(test_code, source_code):
    rubric = load_skill_md()
    
    scores = {
        'completeness': score_completeness(test_code, rubric),
        'quality': score_quality(test_code, rubric),
        'reliability': score_reliability(test_code, rubric),
        'layers': score_layers(test_code, rubric),
        'practices': score_practices(test_code, rubric)
    }
    
    total = sum(scores.values())
    tier = get_tier(total, rubric)
    
    return {
        'total': total,
        'tier': tier,
        'scores': scores,
        'recommendations': generate_recommendations(scores, rubric)
    }
```

---

## Summary: The Rubric's Purpose

| Purpose | How It Works | Benefit |
|---------|--------------|---------|
| **Consistency** | Same criteria every time | Fair comparisons |
| **Objectivity** | Point-based scoring | No subjective bias |
| **Actionability** | Specific gaps identified | Clear improvement path |
| **Teaching** | Shows what quality means | Levels up team |
| **Customization** | Edit points = change priorities | Fits any team |
| **Auditability** | Every score explained | Compliance-ready |

**The rubric transforms the AI from:**
- ❌ "Your tests look okay" → Vague, useless
- ✅ "72/100 - Missing 3 edge cases worth 6 points, add these specific tests to reach 78/100" → Specific, actionable

**It's the difference between:**
- A subjective code review
- An objective quality measurement system

That's why the resume scoring agent uses it for fair hiring decisions, and the testing agent uses it for consistent test quality assessment!
