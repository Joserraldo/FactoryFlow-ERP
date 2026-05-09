# FactoryFlow ERP 🏭

FactoryFlow es un sistema ERP de grado industrial enfocado en la trazabilidad total, diseñado para gestionar desde la entrada de materias primas hasta la producción, almacenamiento y venta de productos finales. Esta arquitectura ha sido modernizada a la **Versión 1.3** integrando un stack sólido:

*   **Frontend:** React (Vite) + TypeScript + Tailwind CSS (shadcn/ui).
*   **Backend:** FastAPI (Python) + SQLAlchemy (SQLite).
*   **Paradigma:** Trazabilidad basada en BOM (Listas de Materiales) y procesos de fabricación.

---

## 🚀 Guía de Inicio Rápido (Local)

### 1. Requisitos Previos
*   Python 3.10+
*   Node.js 18+

### 2. Levantar el Backend (FastAPI)
Abre un terminal en la raíz del proyecto y ejecuta:
```bash
# 1. Crear y activar tu entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # En Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Arrancar el servidor
uvicorn app.main:app --reload
```
*La API estará disponible en `http://localhost:8000`*.

### 3. Levantar el Frontend (React/Vite)
Abre un segundo terminal desde la raíz y ejecuta:
```bash
cd frontend
npm install
npm run dev
```
*El sistema estará disponible en `http://localhost:5173`*.

---

## 🛠️ Gestión de Datos y Base de Datos (Seeder)

El proyecto incluye un script robusto llamado `seed.py` (Versión 1.3 - Demo Ready) que purga la base de datos y la vuelve a llenar con escenarios hiperrealistas (cientos de kilos de inventario, proveedores cruzados, recetas industriales exactas y decenios de facturas) para simular un ambiente productivo en tiempo real.

**¿Cómo reiniciar la base de datos y cargar la Demo?**
1. Detén el servidor de Backend temporalmente (`Ctrl + C`).
2. Ejecuta el script de semilla:
   ```bash
   python seed.py
   ```
3. Verás un mensaje de éxito: `[OK] Massive Realistic Version 1.3 Seed applied!`.
4. Vuelve a arrancar el servidor: `uvicorn app.main:app --reload`.

### 🚨 IMPORTANTE: ¿Qué hacer si "No veo datos" después de correr el Seed?
Si corres `seed.py` mientras tenías el ERP abierto en el navegador, **se purgará el usuario administrador que estabas usando** de la base de datos.
Al no existir en el backend, el sistema bloqueará tu token antiguo (Error 401) y verás la pantalla vacía o con todo en ceros.

**Solución:**
1. Haz clic en **"Cerrar Sesión"** en la esquina superior derecha o recarga la página para que el sistema te expulse automáticamente al Login.
2. Ingresa de nuevo con las credenciales maestras limpias:
   * **Usuario:** `admin`
   * **Contraseña:** `admin123`

---

## ✅ Cumplimiento SRS (System Requirements Specification)

Actualmente cubrimos fielmente las directrices del SRS:
- **Gestión de Identidad:** Login JWT implementado.
- **Trazabilidad Pura:** Integración Materias Primas -> Productos + BOM -> Manufactura -> Ventas. El costo de una venta rastrea hasta el CPP (Costo Promedio Ponderado) de los almacenes base.
- **Finanzas Dinámicas:** Todo el dashboard recalcula los márgenes brutos con base a las existencias contables consumidas.
- **UX Premium:** Interfaz implementada con el estándar Glassmorphism dictado en la etapa de planeación, soportada 100% sobre las rutas del Backend real.

---

*Desarrollado con arquitectura nivel Senior para cumplimiento MVP escalable.*
