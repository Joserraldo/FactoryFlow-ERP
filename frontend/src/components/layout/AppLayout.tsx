import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "./AppSidebar";
import { Bell, Search, ChevronRight, Settings, LogOut } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

const titles: Record<string, string> = {
  "/": "Dashboard",
  "/almacen": "Almacén · Materias primas",
  "/productos": "Ingeniería de producto",
  "/produccion": "Órdenes de producción",
  "/ventas": "Ventas & Clientes",
  "/finanzas": "Finanzas",
  "/configuracion": "Configuración",
};

const notifications = [
  { id: 1, title: "Stock crítico: Acero inoxidable 304", desc: "Por debajo del punto de reorden", time: "hace 5 min", type: "warning" as const },
  { id: 2, title: "OP-2041 completada", desc: "Línea 2 · 1.200 unidades", time: "hace 22 min", type: "success" as const },
  { id: 3, title: "Factura FV-1188 vencida", desc: "Cliente: Industrias Reyes S.A.", time: "hace 1 h", type: "danger" as const },
];

export default function AppLayout() {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const title = titles[pathname] ?? "FactoryFlow";

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-background">
        <AppSidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <header className="h-16 border-b bg-card/80 backdrop-blur flex items-center gap-3 px-4 sticky top-0 z-30">
            <SidebarTrigger />
            <div className="flex items-center text-sm text-muted-foreground gap-1">
              <span>FactoryFlow</span>
              <ChevronRight className="h-3.5 w-3.5" />
              <span className="text-foreground font-medium">{title}</span>
            </div>
            <div className="ml-auto flex items-center gap-2">
              <div className="relative hidden md:block">
                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Buscar OP, SKU, cliente…" className="pl-8 w-72 bg-background" />
              </div>

              <Popover>
                <PopoverTrigger asChild>
                  <button className="relative p-2 rounded-md hover:bg-secondary transition-colors" aria-label="Notificaciones">
                    <Bell className="h-4 w-4" />
                    <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-accent ring-2 ring-card" />
                  </button>
                </PopoverTrigger>
                <PopoverContent align="end" className="w-80 p-0">
                  <div className="flex items-center justify-between px-4 py-3 border-b">
                    <div className="font-semibold text-sm">Notificaciones</div>
                    <Badge variant="secondary" className="text-[10px]">{notifications.length} nuevas</Badge>
                  </div>
                  <div className="max-h-80 overflow-y-auto divide-y">
                    {notifications.map((n) => (
                      <div key={n.id} className="px-4 py-3 hover:bg-secondary/60 cursor-pointer">
                        <div className="flex items-start gap-2">
                          <span className={
                            "mt-1 h-2 w-2 rounded-full shrink-0 " +
                            (n.type === "warning" ? "bg-accent" : n.type === "success" ? "bg-emerald-500" : "bg-destructive")
                          } />
                          <div className="min-w-0">
                            <div className="text-sm font-medium leading-snug">{n.title}</div>
                            <div className="text-xs text-muted-foreground">{n.desc}</div>
                            <div className="text-[11px] text-muted-foreground mt-1">{n.time}</div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="p-2 border-t">
                    <Button variant="ghost" size="sm" className="w-full justify-center text-xs">Ver todas</Button>
                  </div>
                </PopoverContent>
              </Popover>

              <div className="h-6 w-px bg-border mx-1" />

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <button className="flex items-center gap-2 pl-1 pr-2 py-1 rounded-md hover:bg-secondary transition-colors">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-primary text-primary-foreground text-xs font-semibold">P1</AvatarFallback>
                    </Avatar>
                    <div className="hidden md:block text-left leading-tight">
                      <div className="text-xs font-medium">Prueba 1</div>
                      <div className="text-[10px] text-muted-foreground">Sesión demo</div>
                    </div>
                  </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-60">
                  <div className="px-2 py-3 flex items-center gap-3">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="bg-primary text-primary-foreground text-sm font-semibold">P1</AvatarFallback>
                    </Avatar>
                    <div className="min-w-0">
                      <div className="text-sm font-semibold truncate">Prueba 1</div>
                      <div className="text-xs text-muted-foreground truncate">Sesión de demostración</div>
                    </div>
                  </div>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem className="gap-2" onClick={() => navigate("/configuracion")}>
                    <Settings className="h-4 w-4" /> Configuración
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem
                    className="gap-2 text-destructive focus:text-destructive"
                    onClick={() => navigate("/login")}
                  >
                    <LogOut className="h-4 w-4" /> Cerrar sesión
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </header>
          <main className="flex-1 p-6 overflow-x-auto">
            <Outlet />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
