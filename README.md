<p align="center">
  <a href="https://codecov.io/github/NehuenLian/Lotus-POS-Desktop">
    <img src="https://codecov.io/github/NehuenLian/Lotus-POS-Desktop/graph/badge.svg?token=20WL0URAGI" alt="codecov"/>
  </a>
</p>

# Lotus POS | Point of sale system

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.32-red?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green?logo=qt&logoColor=white)
![dotenv](https://img.shields.io/badge/python--dotenv-1.1.0-lightgrey?logo=python&logoColor=white)

**Lotus POS** is a desktop Point of Sale system designed for small and medium-sized businesses. It allows you to manage sales, inventory, pricing, and database configuration in a simple way.

## Offline-first and Resilient

The POS software is designed for being "offline-first", ensuring the system remains operational even when internet connectivity fails, and does not depend on it.

If electronic invoicing software/service is used and an invoice cannot be approved immediately, the sale is marked as **"pending"** in the sales record, and all necessary data to generate the invoice is saved. Later, pending invoices can be resent if desired, ensuring the business’s fiscal integrity.

---

## Tech Stack

- **Python**: Core language.
- **PySide6**: For the desktop GUI.
- **SQLAlchemy**: For database interaction (ORM).
- **python-dotenv**: For managing environment variables.

---

## Main Features

- **Sales Management:** Fast sales registration, product selection by barcode, automatic total calculation, and payment method selection.
- **Inventory Control:** Instant stock lookup by product.
- **Price Management:** Search and update product prices.
- **Flexible Configuration:** Change the database URL from the interface and restart the app to apply changes.
- **Architecture:** Clear separation between business logic, data access, controllers, and views.
- **Logging:** Log management for auditing and debugging.

---
<h3 align="center">Frontend screenshot</h3>
<p align="center">
  <img src="images/frontend_screenshot.jpg" alt="Lotus POS Frontend" width="700">
  <br>
  <em>The screenshot shows the app in Spanish, as requested by a real client.</em>
</p>

---

## 🏗 Architectural Decisions

During development, several design decisions were made to prioritize **maintainability**, **scalability**, and **low coupling**.

---

### Domain-specific MVC  
Each system module (Sales, Prices, Stock) has its own `Model`, `View`, and `Controller`, functioning as independent mini-applications.  

- This allows complete isolation between functionalities, so if a domain breaks or is removed, the others remain unaffected.  
- It promotes scalability and maintainability, as the flows of different modules never intersect at any point in the lifecycle.

---

### Domain-specific DAO
Previously, DAOs represented database tables. Now, they represent business contexts and are associated with the module they work with, also promoting decoupling at the data access layer. This avoids mixing queries from different modules in a single file.  

- Less coupling in the data access layer.  
- More readable code, organized by business context.

---

### “Mirror” objects in the frontend  
Data is duplicated: the backend keeps the original object for final calculations, while the frontend receives a copy for real-time visual calculations.  

- Decouples presentation and business logic.  
- More secure, as the backend data does not need to be modified just for frontend display purposes.  
* This solution addresses the problem that calculations like subtotal or total were done at the end of the flow. To show real-time updates to the user without relying on the backend, this technique was implemented successfully, improving the user experience.

---

### Multithreaded Billing

When entering a sale, if it is automatically sent to an external electronic invoicing service, it does not block the UI because this process runs on a separate thread, nor does it stop the program in case of an error. See the code between lines 72-88 in src/controllers/register_sale.py.

---

## Project Structure

The project has a modular architecture.

```
.
├── integration/            # Modules to connect with external services (e.g., billing services).
├── src/                    # Main source code.
│   ├── business_logic/     # Core logic: business rules, calculations, and processes.
│   ├── controllers/        # Intermediaries between the view and the logic.
│   ├── data_access/        # Persistence layer: SQL queries and database access.
│   ├── logs/
│   ├── sample_data/
│   ├── utils/              # Helper functions and reusable tools.
│   ├── views/              # User interface.
│   └── exceptions.py       # Custom error definitions.
├── .env                    # Real environment variables (credentials, local paths).
├── .env.example            # Template of environment variables for other developers.
├── .gitignore
├── LICENSE
├── main.py                 # Main entry point to run the application.
├── README_English.md
├── README_spanish.md
└── requirements.txt
```

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/NehuenLian/Lotus-POS-Desktop
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy the `.env.example` file to `.env` and fill in the required values. This includes the database URL and paths for the fiscal integration certificates (if required).
     ```
     # .env file
     DB_URL="sqlite:///src/data_access/sample_database.db"

     ```

---

## Usage

1. Run the application:
   ```sh
   python main.py
   ```

2. You can navigate through the sections from the sidebar:
   - **Stock Lookup**
   - **Price Management**
   - **Sales Registration**
   - **Settings**

---

## Dependencies

All dependencies are listed in `requirements.txt`.

- **GUI**: [PySide6](https://pypi.org/project/PySide6/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Environment**: [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute the software.

---

## Author

Developed by Nehuen Lián.

---
You can contact me for any question or suggestion.