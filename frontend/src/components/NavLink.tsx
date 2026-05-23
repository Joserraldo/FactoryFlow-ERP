/**
 * ============================================================================
 * Componente: NavLink (Wrapper)
 * Propósito: Adaptador de compatibilidad para react-router-dom NavLink.
 * Rol Arquitectónico: Utility Component. Permite pasar clases CSS estáticas
 *                     (`className`, `activeClassName`) en lugar de la función
 *                     render-prop nativa, simplificando el uso en el Sidebar.
 * ============================================================================
 */

import { NavLink as RouterNavLink, NavLinkProps } from "react-router-dom";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

/** Props extendidas para el wrapper de NavLink con soporte de clases activas. */
interface NavLinkCompatProps extends Omit<NavLinkProps, "className"> {
  className?: string;
  activeClassName?: string;
  pendingClassName?: string;
}

const NavLink = forwardRef<HTMLAnchorElement, NavLinkCompatProps>(
  ({ className, activeClassName, pendingClassName, to, ...props }, ref) => {
    return (
      <RouterNavLink
        ref={ref}
        to={to}
        className={({ isActive, isPending }) =>
          cn(className, isActive && activeClassName, isPending && pendingClassName)
        }
        {...props}
      />
    );
  },
);

NavLink.displayName = "NavLink";

export { NavLink };
