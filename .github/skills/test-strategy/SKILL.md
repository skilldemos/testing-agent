---
name: test-strategy
description: Evaluate test suite quality, generate comprehensive test cases, and develop testing strategies for software projects. Use this skill when asked to write tests, review test coverage, assess test quality, or create testing plans. Applies structured criteria covering test completeness, maintainability, reliability, and performance.
---

# Specialized Testing Strategy

This skill evaluates test suites and generates high-quality tests for software projects using structured criteria.

## When to Use This Skill

Use this skill when you need to:
- Write unit, integration, or E2E tests for code
- Review and score existing test suites
- Identify gaps in test coverage
- Assess test quality and reliability
- Develop comprehensive testing strategies
- Recommend testing improvements

## Test Quality Evaluation Rubric (100 points total)

**IMPORTANT: Each category has a maximum score. The total score cannot exceed 100 points.**

### 1. Test Completeness (30 points max)

| Criteria | Points |
|----------|--------|
| Critical paths fully tested (happy + error paths) | 12 |
| Edge cases and boundary conditions covered | 8 |
| Error handling and exceptions tested | 5 |
| Input validation tested | 3 |
| Security-critical functions tested | 2 |

**Coverage Bonuses:**
- Line coverage ≥ 80%: +3 bonus
- Branch coverage ≥ 70%: +3 bonus
- All public APIs tested: +2 bonus

### 2. Test Quality & Maintainability (25 points max)

| Criteria | Points |
|----------|--------|
| Tests follow AAA pattern (Arrange, Act, Assert) | 5 |
| Descriptive test names clearly state intent | 5 |
| Tests are isolated and independent | 5 |
| No code duplication, good use of fixtures/helpers | 4 |
| Tests are deterministic (no random failures) | 3 |
| Clear documentation for complex test scenarios | 3 |

**Quality Bonuses:**
- Parameterized tests for similar scenarios: +2 bonus
- Good balance of unit vs integration tests: +2 bonus

### 3. Test Reliability (20 points max)

| Criteria | Points |
|----------|--------|
| No flaky tests (consistent pass/fail) | 8 |
| Appropriate timeouts and retries | 4 |
| Proper mocking of external dependencies | 4 |
| Tests fail for the right reasons | 2 |
| No test interdependencies | 2 |

**Reliability Bonuses:**
- Continuous integration passing consistently: +3 bonus
- Test execution time optimized: +2 bonus

### 4. Testing Layers (15 points max)

| Coverage | Points |
|----------|--------|
| Comprehensive unit tests (70%+ of suite) | 6 |
| Integration tests for component interactions | 5 |
| E2E tests for critical user flows | 2 |
| Performance/load tests (if applicable) | 2 |

**Layer Bonuses:**
- Testing pyramid respected (most unit, fewer integration, minimal E2E): +2 bonus

### 5. Best Practices (10 points max)

| Criteria | Points |
|----------|--------|
| Follows framework conventions | 3 |
| Test data is realistic but anonymized | 2 |
| Tests document expected behavior | 2 |
| Accessibility testing included (if UI) | 2 |
| Security testing (auth, validation) | 1 |

## Test Generation Guidelines

### For Unit Tests

**Structure:**
```python
def test_[function]_[scenario]_[expected_result]():
    """Test that [scenario] results in [expected result]."""
    # Arrange - Set up test data and mocks
    test_input = ...
    mock_dependency = Mock(return_value=...)
    
    # Act - Execute the code under test
    result = function_under_test(test_input, mock_dependency)
    
    # Assert - Verify the outcome
    assert result == expected_value
    mock_dependency.assert_called_once_with(expected_args)
```

**What to Test:**
- ✓ Function returns correct values for valid inputs
- ✓ Function handles edge cases (empty, null, max values)
- ✓ Function raises appropriate errors for invalid inputs
- ✓ Function correctly interacts with dependencies
- ✗ Don't test implementation details
- ✗ Don't test external libraries (trust they work)

### For Integration Tests

**Structure:**
```python
def test_[feature]_[integration_scenario]():
    """Test [components] working together for [scenario]."""
    # Arrange - Set up multiple components
    database = TestDatabase()
    api_client = RealAPIClient(test_credentials)
    service = ServiceUnderTest(database, api_client)
    
    # Act - Exercise the integration
    result = service.complex_operation(test_data)
    
    # Assert - Verify end-to-end behavior
    assert result.status == "success"
    assert database.record_count() == expected_count
```

**What to Test:**
- ✓ Components communicate correctly
- ✓ Data flows through the system properly
- ✓ Transactions and error handling work across boundaries
- ✓ Realistic data volumes don't break the system

### For End-to-End Tests

**Structure:**
```javascript
test('[User Journey] - [Expected Outcome]', async ({ page }) => {
  // Arrange - Navigate to starting point
  await page.goto('/app');
  await page.fill('[data-testid="username"]', 'test@example.com');
  
  // Act - Perform user actions
  await page.click('[data-testid="login-button"]');
  await page.waitForSelector('[data-testid="dashboard"]');
  
  // Assert - Verify user sees expected result
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

**What to Test:**
- ✓ Critical user workflows (login, purchase, checkout)
- ✓ Cross-browser compatibility for important flows
- ✓ Error states users might encounter
- ✗ Don't test every possible path (too slow and brittle)

## Quality Tiers

| Score Range | Tier | Action |
|-------------|------|--------|
| 85-100 | **Excellent** | Test suite is production-ready, minimal improvements needed |
| 70-84 | **Good** | Test suite is solid, minor gaps to address |
| 55-69 | **Adequate** | Core functionality tested, significant improvements recommended |
| 40-54 | **Needs Improvement** | Major gaps in coverage or quality issues |
| Below 40 | **Insufficient** | Test suite needs significant work before production |

## Test Quality Assessment Output Format

```markdown
## Test Suite Evaluation: [Feature/Module Name]

### Summary
- **Total Test Count**: X tests (Y unit, Z integration, W E2E)
- **Test Framework**: [pytest/jest/JUnit/etc.]
- **Execution Time**: [total time]
- **Current Coverage**: X% line, Y% branch

### Detailed Scores

#### Test Completeness: X/30
- Critical paths: [score and justification]
- Edge cases: [score and justification]
- Error handling: [score and justification]
- **Evidence**: [quote from tests or note missing tests]

#### Test Quality & Maintainability: X/25
- Test structure: [score and justification]
- Naming conventions: [score and justification]
- Test isolation: [score and justification]
- **Evidence**: [examples from test suite]

#### Test Reliability: X/20
- Flakiness: [assessment]
- Mocking strategy: [assessment]
- CI stability: [metrics if available]
- **Evidence**: [CI logs, test history, or observations]

#### Testing Layers: X/15
- Unit test coverage: [score]
- Integration tests: [score]
- E2E tests: [score]
- **Evidence**: [breakdown of test types]

#### Best Practices: X/10
- Framework conventions: [score]
- Test documentation: [score]
- Security testing: [score]
- **Evidence**: [specific examples]

### Overall Assessment
- **Total Score**: X/100
- **Quality Tier**: [tier]
- **Key Strengths**: 
  1. [strength with example]
  2. [strength with example]
- **Critical Gaps**:
  1. [gap with impact assessment]
  2. [gap with impact assessment]

### Recommendations (Prioritized)

#### High Priority (Do First)
1. [Specific recommendation with example]
2. [Specific recommendation with example]

#### Medium Priority (Next Sprint)
1. [Specific recommendation]
2. [Specific recommendation]

#### Low Priority (Technical Debt)
1. [Nice-to-have improvement]
```

## Test Generation Output Format

```python
"""
Test Suite for [Module/Feature Name]

Generated: [Date]
Framework: [pytest/jest/etc.]
Test Level: [unit/integration/e2e]
Coverage Target: [X%]
"""

import pytest
from unittest.mock import Mock, patch, MagicMock

# Test fixtures
@pytest.fixture
def sample_data():
    """Provide standard test data."""
    return {
        "id": 123,
        "name": "Test User",
        "email": "test@example.com"
    }

@pytest.fixture
def mock_database():
    """Mock database connection."""
    db = Mock()
    db.query.return_value = []
    return db


class Test[FeatureName]:
    """Comprehensive test suite for [feature description]."""
    
    # Happy path tests
    def test_[function]_with_valid_input_returns_expected_result(self, sample_data):
        """
        Test that [function] correctly processes valid input.
        
        This validates the primary use case where...
        """
        # Arrange
        input_data = sample_data
        expected_output = "processed_result"
        
        # Act
        result = function_under_test(input_data)
        
        # Assert
        assert result == expected_output
    
    # Edge case tests
    def test_[function]_with_empty_input_handles_gracefully(self):
        """Test that empty input is handled without errors."""
        # Arrange
        empty_input = {}
        
        # Act & Assert
        with pytest.raises(ValueError, match="Input cannot be empty"):
            function_under_test(empty_input)
    
    def test_[function]_with_max_size_input_succeeds(self):
        """Test that maximum allowed input size is handled."""
        # Arrange
        max_input = create_max_size_data()
        
        # Act
        result = function_under_test(max_input)
        
        # Assert
        assert result is not None
        assert len(result) <= MAX_OUTPUT_SIZE
    
    # Error handling tests
    @patch('module.external_service')
    def test_[function]_handles_external_service_failure(self, mock_service):
        """Test graceful degradation when external service fails."""
        # Arrange
        mock_service.side_effect = ConnectionError("Service unavailable")
        
        # Act & Assert
        with pytest.raises(ServiceUnavailableError):
            function_under_test(valid_input)
    
    # Integration tests (if applicable)
    def test_[function]_integrates_with_database(self, mock_database):
        """Test that function correctly queries and updates database."""
        # Arrange
        mock_database.query.return_value = [{"id": 1, "value": "test"}]
        
        # Act
        result = function_under_test(test_input, mock_database)
        
        # Assert
        assert result["success"] is True
        mock_database.query.assert_called_once()
        mock_database.save.assert_called_with(expected_data)
```

## Red Flags in Test Suites

When reviewing tests, watch for:

- **Flaky Tests**: Tests that pass/fail randomly
  - Common cause: Timing issues, shared state, external dependencies
  - Fix: Add proper waits, isolate tests, mock externals

- **Over-Mocking**: Mocking too many internals
  - Problem: Tests pass but real code breaks
  - Fix: Mock only external dependencies, test real implementations

- **Assertion Roulette**: Tests with many assertions
  - Problem: Hard to know which assertion failed
  - Fix: One logical concept per test, clear assertion messages

- **Test Code Duplication**: Copy-pasted test setup
  - Problem: Hard to maintain, inconsistent patterns
  - Fix: Extract fixtures, use parameterized tests

- **Slow Tests**: Test suite takes > 5 minutes
  - Problem: Developers skip running tests
  - Fix: Parallelize, optimize, move slow tests to separate suite

- **Mystery Tests**: No comments explaining complex setups
  - Problem: Future developers can't understand intent
  - Fix: Add docstrings explaining what and why

## Framework-Specific Patterns

### pytest (Python)
```python
# Fixtures for reusable setup
@pytest.fixture
def user():
    return User(name="Test", email="test@example.com")

# Parametrize for multiple test cases
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_double(input, expected):
    assert double(input) == expected
```

### Jest (JavaScript/TypeScript)
```javascript
// beforeEach for common setup
describe('UserService', () => {
  let service;
  
  beforeEach(() => {
    service = new UserService();
  });
  
  // Use descriptive nested describes
  describe('createUser', () => {
    it('should create user with valid data', () => {
      const user = service.createUser({name: 'Test'});
      expect(user).toBeDefined();
      expect(user.name).toBe('Test');
    });
  });
});
```

### JUnit (Java)
```java
class UserServiceTest {
    
    private UserService service;
    
    @BeforeEach
    void setUp() {
        service = new UserService();
    }
    
    @Test
    @DisplayName("Should create user with valid name")
    void testCreateUser_ValidName_ReturnsUser() {
        // Arrange
        String name = "Test User";
        
        // Act
        User result = service.createUser(name);
        
        // Assert
        assertNotNull(result);
        assertEquals(name, result.getName());
    }
}
```

## Testing Anti-Patterns to Avoid

1. **Testing Private Methods** - Test through public interface
2. **Testing External Libraries** - Trust they work, mock instead
3. **Testing Multiple Things** - One logical concept per test
4. **Brittle E2E Selectors** - Use data-testid attributes
5. **No Arrange/Act/Assert** - Follow clear structure
6. **Unclear Test Names** - Name should describe the scenario
7. **Shared Mutable State** - Each test should be isolated
8. **Testing Implementation** - Test behavior, not how it works
