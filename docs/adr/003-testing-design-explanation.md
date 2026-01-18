# Architecture Decision Record 16/01/2026  
Design of POS Tests

## General Testing Approach
- Both unit tests and integration tests focus only on business logic. UI testing is explicitly excluded.
- The test structure follows one `.py` file per class to test.

### conftest.py Explanation:

#### Unit Test Settings
- Business logic classes are designed to work with a single instance per individual sale. During testing, this caused shared state between tests (for example, adding a product when previous tests had already populated products).  
  To avoid this, a `clear_instance` function is used. This function runs via an `autouse=True` fixture and resets the state of the relevant classes by calling a special cleanup method implemented in each class.
- Although these are unit tests, some methods require pre-existing state in other classes. For this reason, a general setup function was created to prepare the required class state in a way that is closer to real usage.  
  For example, in order to register a sale, a product must already exist in the cart.
- Fake DAOs were used, matching the structure of the real DAOs but with methods that do not access any database. This allows each method to behave as if it were querying a DAO, without introducing external dependencies, keeping the tests purely unit-level.

#### Integration Test Settings
- Integration tests depend on querying or modifying database records. Therefore, at the start of each test, data for three products is inserted into the in-memory database.
- In production, database queries use a context manager that provides a session connected to the production database. Since integration tests use an in-memory database, a dedicated testing context manager was created. This testing context manager provides a session connected to the in-memory database while maintaining the same interface as the production one.  
  In each integration test, the production context manager is patched with the testing version.
- Fake views were used, matching the structure of the original views.
