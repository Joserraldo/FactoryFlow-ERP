/**
 * ============================================================================
 * Archivo: main.tsx
 * Propósito: Punto de montaje DOM de la aplicación React.
 * Rol Arquitectónico: Bootstrap. Enlaza el componente <App /> con el nodo
 *                     HTML #root del index.html, iniciando el Virtual DOM.
 * ============================================================================
 */

import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// Monta la aplicación React en el nodo raíz del HTML
createRoot(document.getElementById("root")!).render(<App />);
