# Quick Start Guide - Testing Agent Demo

## 🚀 5-Minute Setup

### Option A: GitHub Copilot (Recommended)

**Prerequisites:**
- VS Code with GitHub Copilot enabled
- This repository opened in VS Code

**Steps:**

1. **Open Copilot Chat** (`Ctrl+Alt+I` or `Cmd+Shift+I`)

2. **Try these prompts:**

   ```
   @workspace Generate comprehensive pytest tests for sample-code/user_service.py 
   following the test-strategy skill. Include fixtures for mocks, test all public 
   methods, cover edge cases, and use AAA structure.
   ```

   ```
   @workspace Analyze sample-code/shopping_cart.py and create a testing strategy. 
   What should be tested at unit level vs integration level? What are the critical 
   edge cases?
   ```

3. **Review the output** - Copilot will:
   - Read AGENTS.md for instructions
   - Apply .github/skills/test-strategy/SKILL.md rubric
   - Generate complete test suite
   - Include fixtures, mocks, assertions

4. **Refine as needed:**
   ```
   Add tests for the calculate_user_tier function with boundary value analysis
   ```

---

### Option B: Python Script (Automated)

**Prerequisites:**
- Python 3.8+
- Anthropic API key ([get one here](https://console.anthropic.com/))

**Steps:**

1. **Install dependencies:**
   ```bash
   pip install anthropic
   ```

2. **Set your API key:**
   ```bash
   # Mac/Linux
   export ANTHROPIC_API_KEY="sk-ant-your-key-here"
   
   # Windows (PowerShell)
   $env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
   ```

3. **Generate tests:**
   ```bash
   # Process all sample code
   python pipeline/generate_tests.py
   
   # Or process a specific file
   python pipeline/generate_tests.py sample-code/user_service.py
   ```

4. **Check the output:**
   ```bash
   ls generated-tests/
   # You'll see:
   # - test_user_service_<timestamp>.py  (generated tests)
   # - user_service_analysis.txt         (code analysis)
   ```

5. **Review and refine the generated tests**

---

### Option C: Manual Prompt (No API Key)

**Steps:**

1. **Generate prompts:**
   ```bash
   python pipeline/generate_tests.py
   # This creates prompt files in generated-tests/
   ```

2. **Copy a prompt file:**
   ```bash
   cat generated-tests/user_service_prompt.txt
   ```

3. **Paste into:**
   - claude.ai
   - GitHub Copilot Chat
   - Any AI assistant

4. **Copy the response back** into your project as `test_user_service.py`

---

## 📊 Demo Scenarios

### Scenario 1: Test Generation

**Goal:** Generate comprehensive tests for user registration

**Prompt:**
```
@workspace Generate tests for the register_user method in sample-code/user_service.py. 
I need:
- Happy path: valid email, password, name
- Edge cases: empty inputs, max length names, special characters in email
- Error cases: duplicate email, weak password, missing fields
- Mock the database and email service
```

**Expected output:** 15-20 test cases covering all scenarios

---

### Scenario 2: Test Evaluation

**Goal:** Evaluate existing test quality

**Prompt:**
```
@workspace Evaluate the test suite in tests/test_shopping_cart.py using the 
rubric in .github/skills/test-strategy/SKILL.md. Provide scores for each category 
and specific recommendations for improvement.
```

**Expected output:**
- Scores for all 5 categories
- Total score /100
- Quality tier (Excellent/Good/Adequate/etc.)
- Specific recommendations with examples

---

### Scenario 3: Testing Strategy

**Goal:** Plan testing for a new feature

**Prompt:**
```
@workspace I'm adding a "wishlist" feature to the shopping cart. Users can save 
items for later, share wishlists, and get notified about price drops. Create a 
comprehensive testing strategy covering unit, integration, and E2E tests.
```

**Expected output:**
- Testing layers breakdown
- Priority order for test development
- Specific test cases for each layer
- Risk areas to focus on
- Estimated effort

---

## 🎯 Expected Results

### For `user_service.py`:

**Generated tests should include:**

✅ **Registration tests:**
- Valid user registration
- Duplicate email handling
- Password validation (length, complexity)
- Email format validation
- Name length validation
- Welcome email success/failure

✅ **Authentication tests:**
- Successful login
- Wrong password
- Non-existent user
- Account lockout after 5 failed attempts
- Password hash verification

✅ **Profile update tests:**
- Update allowed fields
- Prevent updating sensitive fields
- Name length validation

✅ **Test quality:**
- Fixtures for database and email service
- Proper mocking of external dependencies
- AAA structure in all tests
- Descriptive test names
- Edge case coverage

**Expected quality score: 85-95/100**

---

### For `shopping_cart.py`:

**Generated tests should include:**

✅ **Cart operations:**
- Add item to cart
- Add existing item (quantity update)
- Remove item
- Update quantity
- Clear cart

✅ **Calculations:**
- Subtotal calculation
- Tax calculation
- Shipping cost (free over $50)
- Discount application
- Final total

✅ **Validation:**
- Quantity limits (max per product)
- Stock availability
- Invalid quantity handling

✅ **Edge cases:**
- Empty cart calculations
- Maximum quantity boundary
- Stock validation against inventory
- Discount percentage validation (0-100)

**Expected quality score: 90-98/100**

---

## 🔍 Troubleshooting

### Issue: "No module named 'anthropic'"
**Solution:**
```bash
pip install anthropic
```

---

### Issue: "ANTHROPIC_API_KEY not found"
**Solution:**
```bash
# Check if it's set
echo $ANTHROPIC_API_KEY  # Mac/Linux
echo $env:ANTHROPIC_API_KEY  # Windows PowerShell

# Set it if missing
export ANTHROPIC_API_KEY="sk-ant-..."  # Mac/Linux
$env:ANTHROPIC_API_KEY="sk-ant-..."  # Windows PowerShell
```

---

### Issue: "File not found: AGENTS.md"
**Solution:**
Make sure you're running the script from the `testing-agent-demo/` directory:
```bash
cd testing-agent-demo/
python pipeline/generate_tests.py
```

---

### Issue: Generated tests don't run
**Solution:**
```bash
# Install pytest
pip install pytest

# Run tests
pytest generated-tests/test_user_service_*.py -v
```

---

## 📈 Success Metrics

After using the testing agent, you should see:

- ✅ **Test coverage increase:** 30-50% improvement
- ✅ **Consistent patterns:** All tests follow AAA structure
- ✅ **Edge case coverage:** 80%+ edge cases identified
- ✅ **Time savings:** 3-4x faster test creation
- ✅ **Quality scores:** 85+ average on rubric

---

## 🔄 Iterative Refinement

The agent generates a "first draft". Iterate with:

1. **Review generated tests:**
   ```bash
   cat generated-tests/test_user_service_*.py
   ```

2. **Identify gaps:**
   ```
   @workspace The generated tests are missing performance tests for bulk 
   user registration. Add tests for:
   - Registering 100 users sequentially
   - Handling database connection timeout
   - Memory usage with large batch operations
   ```

3. **Refine specific tests:**
   ```
   @workspace The test_register_user_with_invalid_email test is too broad. 
   Split it into separate tests for:
   - Missing @ symbol
   - Missing domain
   - Invalid TLD
   - Special characters
   ```

4. **Update the rubric** if needed:
   Edit `.github/skills/test-strategy/SKILL.md` to add custom criteria

---

## 🎓 Learning Resources

### Understanding the Agent System

1. **AGENTS.md** - Read how the agent decides what to test
2. **SKILL.md** - Understand the 100-point rubric
3. **Generated tests** - See patterns in action
4. **Analysis files** - Learn what the agent considers

### Testing Best Practices

- [Pytest Documentation](https://docs.pytest.org/)
- [Testing Best Practices](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Mocking Guide](https://docs.python.org/3/library/unittest.mock.html)

---

## 💡 Pro Tips

1. **Be specific in prompts:**
   ❌ "Generate tests for user_service.py"
   ✅ "Generate pytest tests for user_service.py focusing on authentication edge cases, password validation rules, and database error handling"

2. **Provide business context:**
   ```
   @workspace Generate tests for calculate_user_tier(). Business rules:
   - Bronze: default tier
   - Silver: 5+ purchases OR 180+ days
   - Gold: 20+ purchases OR 730+ days  
   - Platinum: 50+ purchases AND 365+ days
   Test all boundary conditions.
   ```

3. **Review critically:**
   - AI might miss domain-specific edge cases
   - Verify mocking strategy makes sense
   - Check test data is realistic

4. **Iterate:**
   - Start with basic tests
   - Add complex scenarios incrementally
   - Refine based on actual failures

---

## 🚀 Next Steps

1. ✅ **Try the quick start** (you are here!)
2. 📖 **Read the full README** for detailed explanation
3. 🔧 **Customize AGENTS.md** for your team
4. 📊 **Customize SKILL.md** rubric for your standards
5. 🔄 **Integrate with CI/CD** for automated quality checks
6. 📈 **Track metrics** and iterate

---

**Questions or issues?** Check the main README.md for detailed documentation.

**Ready to customize?** Start with `.github/skills/test-strategy/SKILL.md` to adjust point values and add your team's conventions.
