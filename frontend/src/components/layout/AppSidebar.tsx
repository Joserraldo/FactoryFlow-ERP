import { NavLink, useLocation } from "react-router-dom";
import {
  LayoutDashboard, Boxes, Package, Factory, ShoppingCart, Wallet, Settings, Cog,
} from "lucide-react";
import {
  Sidebar, SidebarContent, SidebarGroup, SidebarGroupContent, SidebarGroupLabel,
  SidebarMenu, SidebarMenuButton, SidebarMenuItem, SidebarHeader, SidebarFooter, useSidebar,
} from "@/components/ui/sidebar";

const main = [
  { title: "Dashboard", url: "/", icon: LayoutDashboard },
  { title: "Almacén", url: "/almacen", icon: Boxes },
  { title: "Productos & BOM", url: "/productos", icon: Package },
  { title: "Producción", url: "/produccion", icon: Factory },
  { title: "Ventas", url: "/ventas", icon: ShoppingCart },
  { title: "Finanzas", url: "/finanzas", icon: Wallet },
];

const admin = [
  { title: "Configuración", url: "/configuracion", icon: Settings },
];

export function AppSidebar() {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const { pathname } = useLocation();
  const isActive = (p: string) => (p === "/" ? pathname === "/" : pathname.startsWith(p));

  return (
    <Sidebar collapsible="icon" className="border-r border-sidebar-border">
      <SidebarHeader className="px-4 py-5">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-md bg-accent grid place-items-center shadow-md">
            <Cog className="h-5 w-5 text-accent-foreground" />
          </div>
          {!collapsed && (
            <div className="leading-tight">
              <div className="text-sidebar-foreground font-semibold tracking-tight">FactoryFlow</div>
              <div className="text-[11px] uppercase tracking-widest text-sidebar-foreground/60">ERP · Atlas</div>
            </div>
          )}
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Operación</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {main.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton asChild isActive={isActive(item.url)}>
                    <NavLink to={item.url} className="flex items-center gap-3">
                      <item.icon className="h-4 w-4" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarGroup>
          <SidebarGroupLabel>Sistema</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {admin.map((item) => (
                <SidebarMenuItem key={item.url}>
                  <SidebarMenuButton asChild isActive={isActive(item.url)}>
                    <NavLink to={item.url} className="flex items-center gap-3">
                      <item.icon className="h-4 w-4" />
                      {!collapsed && <span>{item.title}</span>}
                    </NavLink>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter className="p-3">
        {!collapsed && (
          <div className="rounded-md bg-sidebar-accent/40 p-3 text-xs text-sidebar-foreground/80">
            <div className="font-medium text-sidebar-foreground">Célula Atlas</div>
            <div className="opacity-70">v1.0 · MVP</div>
          </div>
        )}
      </SidebarFooter>
    </Sidebar>
  );
}
