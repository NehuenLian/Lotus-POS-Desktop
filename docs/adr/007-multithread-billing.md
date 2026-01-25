## Architecture Decision Record (No date)
Multithreaded Billing

### Problem
After registering a sale, the system is designed to optionally invoice the sale immediately with the corresponding fiscal authority. This involves network I/O to an external server, which may fail or become unresponsive for various reasons.

### Solution
This task is executed on a secondary thread to avoid blocking the UI while the invoice is being processed and to prevent the application from crashing in case of failure.

### Benefits
Separates external network-related tasks from the core application contract.