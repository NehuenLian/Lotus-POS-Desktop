<p align="center">
  <a href="https://codecov.io/github/NehuenLian/Lotus-POS-Desktop">
    <img src="https://codecov.io/github/NehuenLian/Lotus-POS-Desktop/graph/badge.svg?token=20WL0URAGI" alt="codecov"/>
  </a>
</p>

# Lotus POS | Sistema de punto de venta

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.32-red?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.9.1-green?logo=qt&logoColor=white)
![dotenv](https://img.shields.io/badge/python--dotenv-1.1.0-lightgrey?logo=python&logoColor=white)

**Lotus POS** es una aplicación de escritorio creada para pequeños-medianos negocios. Te permite manejar ventas, inventario, precios y configurar una base de datos de forma simple.

## Offline-first: resiliente

El software esta diseñado para ser "offline-first", asegurando que el sistema continúe funcionando incluso si hay problemas de internet o si este se cae, no dependa de él.
En caso de usar un software/servicio de facturación electrónica si una factura no puede ser aprobada inmediatamente, la venta se marca como **pendiente** en el registro de ventas, y todos los datos necesarios para generar la factura son guardados. Más tarde las facturas pendientes pueden ser enviadas de nuevo si se desea, asegurando la integridad fiscal del negocio.

---

## Stack

- **Python**: Lenguaje principal.
- **PySide6**: Interfaz de usuario.
- **SQLAlchemy**: Interacción con base de datos.
- **python-dotenv**: Manejo de variables de entorno.

---

## Funciones principales

- **Manejo de ventas:** Registro rápido de ventas, selección de productos por código de barras, cálculo de totales, subtotales automáticos, selección de método de pago.
- **Control de inventario:** Consultar stock de forma instantánea.
- **Gestión de precios:** Buscar y actualizar/modificar precios de productos.
- **Configuración flexible:** Se puede cambiar de base de datos colocando simplemente otra URL y reiniciando el software aplicando los cambios.
- **Arquitectura:** Separación limpia entre capas de negocio, acceso a datos, controladores y vistas.
- **Logging:** Sistema de logs para debugging sencillo.

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
* Esta técnica soluciona el problema donde los cálculos como subtotal o total se hacen al final del flujo. Para mostrar en tiempo real la actualización de los datos sin comprometer al backend, esta técnica fue implementada exitosamente.

---

### Facturación multihilo
Al ingresar una venta, si esta se envía automáticamente a un servicio externo de facturación electrónica, no bloquea la UI porque este proceso se ejecuta en otro hilo, y tampoco detiene el programa en caso de error. Ver el código comprendido entre las lineas 72-88 en src/controllers/register_sale.py

---- 

# Estructura del Proyecto

El proyecto tiene una arquitectura modular.

```
.
├── integration/            # Módulos para conectar con servicios externos (ej. servicios de facturacion).
├── src/                    # Código fuente principal.
│   ├── business_logic/     # Lógica central: reglas de negocio, cálculos y procesos.
│   ├── controllers/        # Intermediarios entre la vista y la lógica.
│   ├── data_access/        # Capa de persistencia: consultas SQL y acceso a base de datos.
│   ├── logs/
│   ├── sample_data/.
│   ├── utils/              # Funciones auxiliares y herramientas reutilizables.
│   ├── views/              # Interfaz de usuario.
│   └── exceptions.py       # Definición de errores personalizados.
├── .env                    # Variables de entorno reales (credenciales, rutas locales).
├── .env.example            # Plantilla de variables de entorno para otros desarrolladores.
├── .gitignore
├── LICENSE
├── main.py                 # Punto de entrada principal para ejecutar la aplicación.
├── README_English.md
├── README_spanish.md
└── requirements.txt
```

---

## Instalación

1.  **Clonar el repositorio:**
    ```sh
    git clone https://github.com/NehuenLian/Lotus-POS-Desktop
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
    -   Copia el archivo `.env.example` a `.env` y completa los valores requeridos. Esto incluye la URL de la base de datos y las rutas para los certificados de integración fiscal (en caso de ser necesario).
    ```
    # archivo .env
    DB_URL="sqlite:///src/data_access/sample_database.db"
    
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

---

## Licencia

Este proyecto está bajo la Licencia MIT.
Eres libre de usar, modificar y distribuir el software.

---

## Autor

Desarrollado por Nehuen Lián.

---

Contactarme para cualquier pregunta o sugerencia.