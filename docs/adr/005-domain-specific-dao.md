# Architecture Decision Record (No date)
Domain-specific DAOs

# Context
Previously, DAOs represented database tables. 

# Problem
It was hard for the developer to find methods and queries and the table separation was not synchronized with the domain separation, this caused coupling in the data access layer, undermining the previous efforts to decouple the other layers such as **business-logic** or **controllers**.

# Solution
Now, they represent business contexts and are associated with the module they work with, promoting decoupling at the data access layer. This avoids mixing queries from different modules in a single file and it complements ADR 004: complete isolation between functionalities.

# Benefits
- Less coupling in the data access layer.
- More readable code, organized by business context.
