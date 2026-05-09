import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Building2, Bell, Globe2, ShieldCheck } from "lucide-react";

export default function Configuracion() {
  return (
    <div>
      <PageHeader title="Configuración" subtitle="Empresa, parámetros regionales y preferencias del sistema" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="border-border/60">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="h-9 w-9 rounded-md bg-primary/10 text-primary grid place-items-center">
                <Building2 className="h-4 w-4" />
              </div>
              <div>
                <CardTitle>Información de la empresa</CardTitle>
                <CardDescription>Datos legales y de identificación</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-1.5">
              <Label>Razón social</Label>
              <Input placeholder="Nombre de la empresa" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="grid gap-1.5">
                <Label>NIT</Label>
                <Input placeholder="000.000.000-0" />
              </div>
              <div className="grid gap-1.5">
                <Label>Sector</Label>
                <Select defaultValue="manufactura">
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="manufactura">Manufactura</SelectItem>
                    <SelectItem value="metalmecanica">Metalmecánica</SelectItem>
                    <SelectItem value="alimentos">Alimentos</SelectItem>
                    <SelectItem value="textil">Textil</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid gap-1.5">
              <Label>Dirección de la planta</Label>
              <Input placeholder="Ciudad, departamento" />
            </div>
            <div className="flex justify-end pt-2">
              <Button>Guardar cambios</Button>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="h-9 w-9 rounded-md bg-primary/10 text-primary grid place-items-center">
                <Globe2 className="h-4 w-4" />
              </div>
              <div>
                <CardTitle>Parámetros regionales</CardTitle>
                <CardDescription>Moneda, idioma y zona horaria</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-1.5">
              <Label>Moneda base</Label>
              <Select defaultValue="COP">
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="COP">COP — Peso colombiano ($)</SelectItem>
                  <SelectItem value="USD">USD — Dólar estadounidense</SelectItem>
                  <SelectItem value="EUR">EUR — Euro</SelectItem>
                  <SelectItem value="MXN">MXN — Peso mexicano</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">Todos los costos, precios y reportes financieros se mostrarán en esta moneda.</p>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div className="grid gap-1.5">
                <Label>Idioma</Label>
                <Select defaultValue="es-CO">
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="es-CO">Español (Colombia)</SelectItem>
                    <SelectItem value="es-MX">Español (México)</SelectItem>
                    <SelectItem value="en-US">English (US)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid gap-1.5">
                <Label>Zona horaria</Label>
                <Select defaultValue="bog">
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="bog">America/Bogotá (GMT-5)</SelectItem>
                    <SelectItem value="mex">America/México (GMT-6)</SelectItem>
                    <SelectItem value="mad">Europe/Madrid (GMT+1)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid gap-1.5">
              <Label>Formato de fecha</Label>
              <Select defaultValue="dmy">
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="dmy">DD/MM/AAAA</SelectItem>
                  <SelectItem value="ymd">AAAA-MM-DD</SelectItem>
                  <SelectItem value="mdy">MM/DD/AAAA</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border/60">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="h-9 w-9 rounded-md bg-primary/10 text-primary grid place-items-center">
                <Bell className="h-4 w-4" />
              </div>
              <div>
                <CardTitle>Notificaciones</CardTitle>
                <CardDescription>Alertas operativas y resúmenes</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-1">
            {[
              ["Alertas de stock bajo", "Avisar cuando un material caiga bajo el punto de reorden", true],
              ["Notificaciones de OP detenidas", "Notificar cuando una orden de producción se pause", true],
              ["Resumen diario por correo", "Recibir KPIs y movimientos del día", false],
              ["Doble validación al cerrar OP", "Requiere confirmación al cerrar una OP", true],
            ].map(([l, d, v]) => (
              <div key={l as string} className="flex items-center justify-between py-2.5 border-b last:border-0">
                <div className="pr-4">
                  <div className="text-sm font-medium">{l}</div>
                  <div className="text-xs text-muted-foreground">{d}</div>
                </div>
                <Switch defaultChecked={v as boolean} />
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="border-border/60">
          <CardHeader>
            <div className="flex items-center gap-2">
              <div className="h-9 w-9 rounded-md bg-primary/10 text-primary grid place-items-center">
                <ShieldCheck className="h-4 w-4" />
              </div>
              <div>
                <CardTitle>Seguridad</CardTitle>
                <CardDescription>Política de acceso y sesiones</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-1">
            {[
              ["Autenticación en dos pasos", "Solicitar código adicional al iniciar sesión", false],
              ["Cierre de sesión automático", "Después de 30 minutos de inactividad", true],
              ["Bitácora de auditoría", "Registrar acciones críticas por usuario", true],
            ].map(([l, d, v]) => (
              <div key={l as string} className="flex items-center justify-between py-2.5 border-b last:border-0">
                <div className="pr-4">
                  <div className="text-sm font-medium">{l}</div>
                  <div className="text-xs text-muted-foreground">{d}</div>
                </div>
                <Switch defaultChecked={v as boolean} />
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
