/**
 * ============================================================================
 * Componente: PageHeader
 * Propósito: Componente reutilizable para el encabezado de cada página del ERP.
 * Rol Arquitectónico: Presentational Component. Garantiza consistencia visual
 *                     (tipografía, espaciado) entre todas las páginas del sistema.
 * ============================================================================
 */

import { ReactNode } from "react";

/**
 * Renderiza el título principal (h1), subtítulo y acciones (botones)
 * de forma estandarizada en todas las páginas del ERP.
 * 
 * @param title - Título principal de la sección
 * @param subtitle - Descripción corta debajo del título (opcional)
 * @param actions - Botones o controles alineados a la derecha (opcional)
 */
export function PageHeader({ title, subtitle, actions }: { title: string; subtitle?: string; actions?: ReactNode }) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-4 mb-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">{title}</h1>
        {subtitle && <p className="text-sm text-muted-foreground mt-1">{subtitle}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}
