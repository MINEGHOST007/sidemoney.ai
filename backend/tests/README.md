# Tests Directory

This directory contains all test files for the SideMoney.ai backend API.

## Test Files

### `test_comprehensive.py`
- **Main test suite** combining functionality from all other test files
- Tests API health, endpoint structure, AI services, and schema validation
- Run with: `python test_comprehensive.py`

### `test_api.py`
- Basic API structure and endpoint testing
- Health checks and documentation validation
- Run with: `python test_api.py`

### `test_ai_features.py`
- Focused AI feature testing
- Tests categorization, analysis, OCR, and custom queries
- Run with: `python test_ai_features.py`

## Running Tests

1. **Start the backend server:**
   ```bash
   cd backend
   python run.py
   ```

2. **Run tests:**
   ```bash
   # Comprehensive test suite (recommended)
   python tests/test_comprehensive.py
   
   # Individual test files
   python tests/test_api.py
   python tests/test_ai_features.py
   ```

## Test Requirements

- Backend server must be running
- Database connection must be healthy
- For AI features: `GEMINI_API_KEY` environment variable
- For authenticated endpoints: Valid JWT token

## Test Organization Benefits

- ✅ **Centralized**: All tests in one location
- ✅ **Modular**: Separate files for different concerns
- ✅ **Comprehensive**: Combined test suite for full coverage
- ✅ **Documentation**: Clear usage instructions 