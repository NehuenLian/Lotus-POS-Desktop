# Lotus POS with Fiscal Integration

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.32-red?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green?logo=qt&logoColor=white)
![dotenv](https://img.shields.io/badge/python--dotenv-1.1.0-lightgrey?logo=python&logoColor=white)
![Zeep](https://img.shields.io/badge/Zeep-4.3.1-yellow)
![lxml](https://img.shields.io/badge/lxml-5.4.0-orange)

**Lotus POS** is a desktop Point of Sale system designed for small and medium-sized businesses, with a built-in module for electronic fiscal invoicing compliant with Argentinian regulations (AFIP/ARCA). It allows you to manage sales, inventory, pricing, and database configuration in a simple way, while also handling the complexities of fiscal integration.

---

## Tech Stack

- **Python**: Core language.
- **PySide6**: For the desktop GUI.
- **SQLAlchemy**: For database interaction (ORM).
- **Zeep & lxml**: For SOAP client and XML processing for fiscal integration.
- **python-dotenv**: For managing environment variables.
- **OpenSSL**: Used via command line for cryptographic operations.
- **tenacity**: For retry logic on web requests.
- **ntplib**: For time synchronization, critical for token generation.

---

## Main Features

- **Sales Management:** Fast sales registration, product selection by barcode, automatic total calculation, and payment method selection.
- **Inventory Control:** Instant stock lookup by product.
- **Price Management:** Search and update product prices.
- **Flexible Configuration:** Change the database URL from the interface and restart the app to apply changes.
- **Architecture:** Clear separation between business logic, data access, controllers, and views.
- **Logging:** Log management for auditing and debugging.
- **Fiscal Integration (AFIP/ARCA):**
    - Generates electronic invoices (CAE).
    - Handles communication with AFIP web services using SOAP.
    - Manages authentication tokens (TA) and their validity.
    - Signs requests using a digital certificate and private key.
    - Builds and validates XML requests and responses.

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

## Project Structure

The project has a modular architecture, separating the core POS application from the fiscal integration service.

```
.
├── bin/                    # OpenSSL binaries for cryptographic operations.
├── integration/            # Bridge connecting the POS application with the fiscal service.
│   └── bridge.py
├── service/                # Fiscal Invoicing Service (AFIP/ARCA integration).
│   ├── certificates/       # Directory for digital certificates.
│   ├── controllers/        # Manages the flow of token generation and invoicing.
│   ├── crypto/             # Handles cryptographic signing of requests.
│   ├── payload_builder/    # Constructs the XML payload for SOAP requests.
│   ├── soap_management/    # Manages the SOAP client and communication.
│   ├── xml_management/     # Handles XML creation and parsing.
│   └── ...                 # Other utilities for logging, error handling, etc.
├── src/                    # Core POS Desktop Application.
│   ├── business_logic/     # Business rules for sales, stock, etc.
│   ├── controllers/        # Application-level controllers.
│   ├── data_access/        # Database connection and repositories.
│   ├── views/              # GUI components (PySide6).
│   └── ...
├── main.py                 # Application entry point.
├── requirements.txt        # Python dependencies.
└── .env.example            # Example environment variables file.
```

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/NehuenLian/Lotus-POS-Fiscal-Integration
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
   - Copy the `.env.example` file to `.env` and fill in the required values. This includes the database URL and paths for the fiscal integration certificates and other parameters.
     ```
     # .env file
     DB_URL="sqlite:///src/data_access/sample_database.db"
     
     # Paths for AFIP integration
     CERT_PATH="service/certificates/your_cert.crt"
     PRIVATE_KEY_PATH="service/certificates/your_private_key.key"
     WSDL_URL_WSAA="https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl"
     WSDL_URL_WSFE="https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
     # ... and other variables from .env.example
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
- **Fiscal Integration (SOAP/XML)**: [zeep](https://pypi.org/project/zeep/), [lxml](https://pypi.org/project/lxml/)
- **Utilities**: [tenacity](https://pypi.org/project/tenacity/) (for retries), [ntplib](https://pypi.org/project/ntplib/) (for time sync)

---

## License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute the software.

---

## Author

Developed by Nehuen Lian.

---
You can contact me for any question or suggestion.