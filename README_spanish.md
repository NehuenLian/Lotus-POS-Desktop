![human-coded](https://badgen.net/static/Human%20Coded/100%25/green)
# Lotus POS | Integración fiscal

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.32-red?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green?logo=qt&logoColor=white)
![dotenv](https://img.shields.io/badge/python--dotenv-1.1.0-lightgrey?logo=python&logoColor=white)
![Zeep](https://img.shields.io/badge/Zeep-4.3.1-yellow)
![lxml](https://img.shields.io/badge/lxml-5.4.0-orange)

**Lotus POS** es una aplicación de escritorio creada para pequeños-medianos negocios, con un servicio de facturación con AFIP/ARCA integrado, cumpliendo con las regulaciones Argentinas. Te permite manejar ventas, inventario, precios y configurar una base de datos de fforma simple.

## Offline-first: resiliente

El software esta diseñado para ser "offline-first", asegurando que el sistema continúe funcionando incluso si hay problemas de internet o si este se cae, no dependa de él.

La parte de facturación también está preparada para este escenario: si una factura no puede ser aprobada inmediatamente, la venta se marca como **pendiente** en el registro de ventas, y todos los datos necesarios para generar la factura son guardados. Más tarde las facturas pendientes pueden ser enviadas en lote, asegurando la integridad fiscal del negocio.

---

## Stack

- **Python**: Lenguaje principal.
- **PySide6**: Interfaz de usuario
- **SQLAlchemy**: Interacción con base de datos.
- **Zeep & lxml**: Para la comunicación con el cliente SOAP y el procesamiento de archivos XML.
- **python-dotenv**: Manejo de variables de entorno.
- **OpenSSL**: Utilizado vía CLI para tareas criptográficas.
- **tenacity**: Para reintentos de peticiones SOAP.
- **ntplib**: Sincronización de tiempo, importante para la generación de tokens.

---

## Funciones principales

- **Manejo de ventas:** Registro rápido de ventas, selección de productos por código de barras, cálculo de totales, subtotales automáticos, selección de método de pago.
- **Control de inventario:** Consultar stock de forma instantánea.
- **Gestión de precios:** Buscar y actualizar/modificar precios de productos.
- **Configuración flexible:** Se puede cambiar de base de datos colocando simplemente otra URL y reiniciando el software aplicando los cambios.
- **Arquitecture:** Separación limpia entre capas de negocio, acceso a datos, controladores y vistas.
- **Logging:** Sistema de logs para debugging sencillo.
- **Integración fiscal (AFIP/ARCA):**
    - Genera facturas electrónicas (CAE).
    - Maneja la comunicación con los servicios WEB de AFIP usando SOAP.
    - Maneja tokens de autenticación (TA) y su validez.
    - Firma solicitudes de token de acceso con certificados digitales y claves privadas.
    - Construye y valida solicitudes y respuestas XML.

<h3 align="center">Screenshot del frontend</h3>
<p align="center">
  <img src="images/frontend_screenshot.jpg" alt="Lotus POS Frontend" width="700">
  <br>
</p>

---

## 🏗 Decisiones Arquitectónicas
Durante el desarrollo, se tomaron varias decisiones para priorizar la **mantenibilidad**, **escalabilidad** del código y el **bajo acoplamiento**.

---

### MVC con dominios
Cada módulo del sistema (Ventas, Precios, Stock) tiene su propia `lógica de negocio`, su propia `Vista` y su propio `controlador`, funcionando de forma independiente.

- Esto permite un desacoplamiento completo entre cada funcionalidad. Si uno se rompe, o es removido, los otros modulos nunca se verán afectados porque no se "conocen" entre sí.
- Promueve la escalabilidad y mantenibilidad, el flujo de ninguno de los módulos nunca se cruza con el flujo de los otros.

---

### DAOs divididos por dominio.
Previamente, los DAOs representaban las tablas de la base de datos. Es decir, un DAO por tabla. Ahora, representan contextos de negocio y estan asociados al módulo con el que trabajan. Promoviendo aún más el desacoplamiento completo también en la capa de acceso a datos. Esto evita tener consultas de distintos módulos mezcladas en el mismo DAO.

- Menos acoplamiento en la capa de acceso a datos.
- Código mas legible y organizado por contexto de negocio.

---

### Objetos “espejo” en el frontend
Los datos están duplicados: el backend se queda con los datos originales para todos los cálculos y el frontend recibe una copia de ellos para poder modificar la vista en tiempo real sin comprometer los datos críticos de la venta.

- Desacopla la capa de presentación y la lógica de negocio.
- Más seguro, los datos del backend no tienen que ser modificados o tratados en otro punto del flujo para cumplir con lo que se debe mostrar en el frontend.
* Esta solución soluciona el problema donde los cálculos como subtotal o total se hacen al   final del flujo. Para mostrar en tiempo real la actualización de los datos win comprometer al backend, esta técnica fue implementada exitosamente.

---- 

# Estructura del Proyecto

El proyecto tiene una arquitectura modular, separando la aplicación principal del POS del servicio de integración fiscal.

```
.
├── bin/                    # Binarios de OpenSSL para operaciones criptográficas.
├── integration/            # Puente que conecta la aplicación POS con el servicio fiscal.
│   └── bridge.py
├── service/                # Servicio de Facturación Fiscal (integración AFIP/ARCA).
│   ├── certificates/       # Directorio para certificados digitales.
│   ├── controllers/        # Maneja el flujo de generación de tokens y facturación.
│   ├── crypto/             # Se encarga de la firma criptográfica de las solicitudes.
│   ├── payload_builder/    # Construye el payload XML para las solicitudes SOAP.
│   ├── soap_management/    # Administra el cliente SOAP y la comunicación.
│   ├── xml_management/     # Maneja la creación y el parsing de XML.
│   └── ...                 # Otras utilidades para logging, manejo de errores, etc.
├── src/                    # Aplicación principal POS de Escritorio.
│   ├── business_logic/     # Reglas de negocio para ventas, stock, etc.
│   ├── controllers/        # Controladores a nivel de aplicación.
│   ├── data_access/        # Conexión a la base de datos y repositorios.
│   ├── views/              # Componentes de la interfaz gráfica (PySide6).
│   └── ...
├── main.py                 # Punto de entrada de la aplicación.
├── requirements.txt        # Dependencias de Python.
└── .env.example            # Archivo de ejemplo con variables de entorno.
```

---

## Instalación

1.  **Clonar el repositorio:**
    ```sh
    git clone https://github.com/NehuenLian/Lotus-POS-Fiscal-Integration
    ```

2.  **Crear y activar un entorno virtual:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # En Windows, usar `venv\Scripts\activate`
    ```

3.  **Instalar dependencias:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    -   Copia el archivo `.env.example` a `.env` y completa los valores requeridos. Esto incluye la URL de la base de datos y las rutas para los certificados de integración fiscal y otros parámetros.
    ```
    # archivo .env
    DB_URL="sqlite:///src/data_access/sample_database.db"
    
    # Rutas para la integración con AFIP
    CERT_PATH="service/certificates/your_cert.crt"
    PRIVATE_KEY_PATH="service/certificates/your_private_key.key"
    WSDL_URL_WSAA="[https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl](https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl)"
    WSDL_URL_WSFE="[https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL](https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL)"
    # ... y otras variables de .env.example
    ```

---

## Uso

1.  Ejecutar la aplicación:
    ```sh
    python main.py
    ```

2.  Se puede navegar por las secciones desde la barra lateral:
    -   **Consulta de Stock**
    -   **Gestión de Precios**
    -   **Registro de Ventas**
    -   **Configuración**

---

## Dependencias

Todas las dependencias están listadas en `requirements.txt`.

-   **Interfaz Gráfica (GUI)**: [PySide6](https://pypi.org/project/PySide6/)
-   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
-   **Entorno**: [python-dotenv](https://pypi.org/project/python-dotenv/)
-   **Integración Fiscal (SOAP/XML)**: [zeep](https://pypi.org/project/zeep/), [lxml](https://pypi.org/project/lxml/)
-   **Utilidades**: [tenacity](https://pypi.org/project/tenacity/) (para reintentos), [ntplib](https://pypi.org/project/ntplib/) (para sincronización de tiempo)

---

## Licencia

Este proyecto está bajo la Licencia MIT.
Eres libre de usar, modificar y distribuir el software.

---

## Autor

Desarrollado por Nehuen Lián.

---

Contactarme para cualquier pregunta o sugerencia.