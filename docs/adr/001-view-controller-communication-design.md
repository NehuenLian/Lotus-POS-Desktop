## Architecture Decision Record 14/07/2026  
View–Controller Communication Design

### Context
When designing the application, a decision was made to clearly define how the user interfaces (views) communicates with the controllers. The main goal was to keep the app easy to maintain, and simple to extend over time.

### Decision
Controller methods handle the full flow of each user action. When an event is triggered from the view, such as a product search request, the view only captures user input and delegates the action to the controller.

The controller is responsible for executing all required logic, including business rules and database access, and then updating the view with the result.

### Conclusion
This keeps responsibilities well separated, the main benefit of this is that lets the developer modify a method with the certainty of not broke another different module and avoid bugs harder to track and its easy to test.
