# Architecture Decision Record (No date)
Domain-specific MVC

# Context
Initially, the app was separated into modules for business logic and views but still had a single controller.py with a class for each controller.

# Problem
When each class for each module started to grow in lines of code I considered creating one .py file for each business domain as a solution.

# Solution
Each system module (Sales, Prices, Stock) has its own Model, View, and Controller, functioning as independent mini-applications.

# Benefits
This allows complete isolation between functionalities, so if a domain breaks or is removed, the others remain unaffected.
It promotes scalability and maintainability, as the flows of different modules never intersect at any point in the lifecycle.
