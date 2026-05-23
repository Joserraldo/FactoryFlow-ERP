/**
 * ============================================================================
 * Archivo: api.ts
 * Propósito: Cliente HTTP ligero y centralizado para la comunicación con el Backend.
 * Rol Arquitectónico: Service Layer / API Gateway Wrapper. Abstrae la inyección 
 *                     automática de tokens JWT en las cabeceras de autorización y 
 *                     gestiona de forma reactiva la expiración de sesión (401).
 * ============================================================================
 */

export const API_URL = "http://localhost:8000";

/**
 * Realiza peticiones HTTP autenticadas al servidor de FactoryFlow ERP.
 * 
 * @param endpoint - Ruta relativa del endpoint (ej. "/api/v1/materials/")
 * @param options - Opciones estándar de RequestInit (método, body, headers extra)
 * @returns Promesa que se resuelve con los datos decodificados en JSON
 * @throws Error conteniendo el detalle del fallo enviado por el backend
 */
export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const token = localStorage.getItem("token");
  
  // Combina cabeceras por defecto (JSON, Auth JWT) con cabeceras personalizadas de la petición.
  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  // Manejo robusto de errores de red y HTTP
  if (!response.ok) {
    // Si la sesión expiró (401), se borra el token local y se fuerza el redireccionamiento al login.
    if (response.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
    }
    
    // Intenta extraer el detalle del error estructurado de FastAPI (detail)
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Error en la petición API");
  }

  return response.json();
}
