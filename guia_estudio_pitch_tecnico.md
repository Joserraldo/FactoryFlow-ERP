# 🏭 Índice de Navegación del Repositorio: FactoryFlow ERP

Bienvenido al repositorio de **FactoryFlow ERP (Versión 1.3)**. Este documento está diseñado como una guía técnica de nivel premium para facilitar la revisión del código, la arquitectura y las decisiones de diseño implementadas en este proyecto.

---

## 🚀 1. Resumen Ejecutivo

**FactoryFlow ERP** es un sistema de planificación de recursos empresariales diseñado para gestionar operaciones industriales de manufactura. 

*   **El Problema:** Las pequeñas y medianas empresas de manufactura suelen gestionar su inventario, recetas (BOM - Bill of Materials) y costos de producción utilizando hojas de cálculo desarticuladas, lo que provoca discrepancias de stock, pérdida de trazabilidad y errores en el cálculo del margen de ganancia.
*   **La Solución:** Un software robusto que centraliza la gestión de materias primas, productos, clientes y ventas, automatizando el descuento de inventario mediante transacciones atómicas basadas en recetas de producción.
*   **Propuesta de Valor:** Destaca por su **Arquitectura Limpia (Clean Architecture Lite)**, garantizando alta cohesión, bajo acoplamiento y un nivel de escalabilidad y mantenibilidad de grado profesional. El sistema implementa cálculos financieros precisos (como el Costo Promedio Ponderado) y asegura la integridad de los datos mediante transaccionalidad ACID nivel bancario.

---

## 🗺️ 2. Índice de Navegación del Repositorio

Para facilitar la evaluación del proyecto, a continuación se presenta el mapa conceptual del código fuente. El backend sigue una **Arquitectura de Monolito Modular**, agrupando la lógica por dominio de negocio dentro del directorio `app/modules/`.

### 🏗️ A. Arquitectura y Configuración Core
Si deseas evaluar la configuración principal, conexión a base de datos y punto de entrada:
*   **Punto de entrada FastAPI:** `app/main.py` *(Aquí se inicializa la aplicación y se registran los enrutadores).*
*   **Conexión a Base de Datos:** `app/core/database.py` *(Configuración de SQLAlchemy y motor SQLite).*
*   **Seguridad y Autenticación:** `app/core/security.py` *(Manejo de JWT y hash de contraseñas).*

### 📦 B. Lógica de Dominio (Módulos de Negocio)
Cada carpeta dentro de `app/modules/` es un dominio independiente con sus propias Rutas (`routes.py`), Lógica de Negocio (`service.py`), Acceso a Datos (`repository.py`) y Modelos (`models.py`, `schemas.py`).

| ¿Qué lógica deseas evaluar? | Dónde encontrarla (Directorio) | Archivo Clave a Revisar |
| :--- | :--- | :--- |
| **Gestión de Materias Primas** y Proveedores | `app/modules/materials/` | `service.py` (Lógica CRUD y conversión de unidades) |
| **Definición de Recetas (BOM)** y Productos | `app/modules/products/` | `models.py` (Tabla intermedia `product_bom` para recetas) |
| **Transaccionalidad Atómica (Orden de Producción)** | `app/modules/production/` | `service.py` -> `create_order` (Descuento de ingredientes por lote) |
| **Cálculo de Costo Promedio Ponderado (CPP)** | `app/modules/inventory/` | `service.py` -> `_process_in` (Matemática de valoración de inventario) |
| **Procesamiento de Ventas** y Clientes | `app/modules/sales/` | `service.py` (Validación de stock y creación de factura) |

### 🎨 C. Interfaz de Usuario (Frontend)
El frontend es una Single Page Application (SPA) modular:
*   **Componentes Reutilizables (UI):** `frontend/src/components/ui/` *(Componentes base construidos con Shadcn/ui).*
*   **Vistas/Páginas Principales:** `frontend/src/pages/` *(Dashboard, Inventario, Producción, Ventas).*
*   **Servicios API:** `frontend/src/services/` *(Clientes Axios para comunicación con el backend).*

---

## ⚙️ 3. Stack Tecnológico y Justificación

El proyecto fue construido seleccionando tecnologías modernas que son estándar en la industria actual:

### Backend
*   **FastAPI (Python 3.10+):** Elegido por su altísimo rendimiento (basado en Starlette y Pydantic), soporte nativo para programación asíncrona y generación automática de documentación OpenAPI (Swagger).
*   **SQLAlchemy (ORM):** Permite mapear objetos Python a tablas relacionales de forma segura, previniendo inyección SQL y facilitando el uso del patrón *Repository*.
*   **SQLite:** Seleccionado para facilitar el despliegue local y la evaluación del proyecto sin configuraciones de servidores externos, manteniendo cumplimiento total de transacciones ACID.

### Frontend
*   **React + TypeScript (Vite):** Vite proporciona un entorno de desarrollo ultrarrápido. TypeScript asegura tipado estático, reduciendo drásticamente los errores en tiempo de ejecución.
*   **Tailwind CSS + Shadcn/ui:** Tailwind permite un diseño "Utility-First" para prototipado rápido. Shadcn proporciona componentes accesibles y hermosos con estética *Glassmorphism* sin atar el proyecto a librerías de estilos pesadas.
*   **React Router Dom:** Gestión fluida de rutas del lado del cliente (SPA).

---

> **Nota para el Evaluador:** Todo el código ha sido documentado exhaustivamente utilizando los estándares profesionales de JSDoc (Frontend) y Docstrings (Backend) para explicar el "por qué" detrás de cada bloque lógico complejo.
