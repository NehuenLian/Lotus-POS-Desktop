## Architecture Decision Record 14/07/2025  
Resolving Coupling Between Views and Controllers

### Context
Problem: views (UI) and controllers need to interact with each other.

Each view must communicate with its controller to delegate business logic, and the controller must be able to update or interact with its corresponding view.  
The problem arises during instantiation: if a view requires a controller in its constructor, and the controller also requires the view, a circular dependency is created, making the initialization flow unclear and harder to maintain.

### Decision
To resolve this coupling, a deferred dependency injection approach was adopted:

- Domain controllers are instantiated first, without a reference to their views. (see `src/controllers/main_controller.py`)
- Views are then created, receiving their corresponding controller.
- After all views are instantiated, they are explicitly linked back to their controllers using a setter.

This avoids circular dependencies while keeping a clear connection between UI and business logic.

### Benefits
- Easy to test: controllers and views can be instantiated independently or with fakes/mocks.
- Predictable domain initialization order