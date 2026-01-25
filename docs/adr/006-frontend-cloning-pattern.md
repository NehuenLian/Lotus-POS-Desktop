## Architecture Decision Record (No date)
“Mirror” sale information in the frontend

### Problem
The final sale calculations are performed when the user presses "REGISTRAR VENTA" (Register Sale) in the UI. However, there is a requirement to show the subtotal and quantity changes in real time. 
Modifying the existing business-logic flow was not an option.

### Solution
The best decision for this case was "cloning" the backend sale data on the frontend and then displaying it but making the calculations in real time when the user interacts with the UI. This is not an academic or recognized pattern.
Data is duplicated: the backend keeps the original object for final calculations and persistence, while the frontend receives a copy for real-time visual calculations.

### Benefits
- Decouples presentation and business logic. More secure, as the backend data does not need to be modified just for frontend display purposes.
- This solution addresses the problem that calculations like subtotal or total were done at the end of the flow. To show real-time updates to the user without relying on the backend.
