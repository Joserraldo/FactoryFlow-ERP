/**
 * ============================================================================
 * Archivo: format.ts
 * Propósito: Utilidades de formateo de moneda y números.
 * Rol Arquitectónico: Utility Layer. Centraliza la localización (i18n) del
 *                     formato monetario colombiano (COP) para que todos los
 *                     componentes del frontend usen una única fuente.
 * ============================================================================
 */

/**
 * Formatea un valor numérico a Pesos Colombianos (COP).
 * 
 * @param value - Valor numérico a formatear
 * @param opts.decimals - Mostrar decimales (por defecto: false)
 * @param opts.compact - Usar notación compacta (ej. $1.2M) (por defecto: false)
 * @returns Cadena formateada con símbolo de moneda COP
 */
export const formatCOP = (value: number, opts: { decimals?: boolean; compact?: boolean } = {}) => {
  const { decimals = false, compact = false } = opts;
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: decimals ? 2 : 0,
    maximumFractionDigits: decimals ? 2 : 0,
    notation: compact ? "compact" : "standard",
  }).format(value);
};

/**
 * Formatea un número con separadores de miles al estilo colombiano.
 * 
 * @param value - Número a formatear
 * @returns Cadena con separadores (ej. 1.234.567)
 */
export const formatNumber = (value: number) =>
  new Intl.NumberFormat("es-CO").format(value);