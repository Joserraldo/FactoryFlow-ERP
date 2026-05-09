import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Cog, ShieldCheck, Activity } from "lucide-react";

export default function Login() {
  const nav = useNavigate();
  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-background">
      <div className="hidden lg:flex flex-col justify-between p-12 text-primary-foreground relative overflow-hidden" style={{ background: "var(--gradient-primary)" }}>
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-md bg-accent grid place-items-center"><Cog className="h-5 w-5 text-accent-foreground" /></div>
          <div>
            <div className="font-semibold">FactoryFlow</div>
            <div className="text-xs opacity-70 uppercase tracking-widest">ERP Industrial</div>
          </div>
        </div>
        <div className="space-y-6 max-w-md">
          <h1 className="text-4xl font-semibold leading-tight">De la planta a los datos, de los datos a las decisiones.</h1>
          <p className="opacity-80">Solución integral de manufactura para PYMES: inventario, producción, ventas y finanzas en un solo centro de control.</p>
          <div className="grid grid-cols-2 gap-4 pt-4">
            <Feature icon={<ShieldCheck className="h-5 w-5" />} title="RBAC + JWT" desc="Control de acceso por roles" />
            <Feature icon={<Activity className="h-5 w-5" />} title="Tiempo real" desc="KPIs y trazabilidad de lotes" />
          </div>
        </div>
        <div className="text-xs opacity-60">Célula Atlas · v1.0 MVP</div>
      </div>

      <div className="flex items-center justify-center p-8">
        <form
          onSubmit={(e) => { e.preventDefault(); nav("/"); }}
          className="w-full max-w-sm space-y-6"
        >
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">Bienvenido</h2>
            <p className="text-sm text-muted-foreground mt-1">Ingresa con tus credenciales corporativas</p>
          </div>
          <div className="space-y-3">
            <div className="grid gap-1.5"><Label>Usuario o correo</Label><Input placeholder="usuario@empresa.com" /></div>
            <div className="grid gap-1.5"><Label>Contraseña</Label><Input type="password" placeholder="••••••••" /></div>
          </div>
          <Button type="submit" className="w-full bg-accent text-accent-foreground hover:bg-accent/90">Ingresar</Button>
          <div className="text-center text-xs text-muted-foreground">¿Olvidaste tu contraseña? <a className="text-primary hover:underline" href="#">Recupérala</a></div>
        </form>
      </div>
    </div>
  );
}

function Feature({ icon, title, desc }: { icon: React.ReactNode; title: string; desc: string }) {
  return (
    <div className="bg-white/10 backdrop-blur rounded-lg p-4">
      <div className="h-8 w-8 rounded bg-white/15 grid place-items-center mb-2">{icon}</div>
      <div className="font-medium text-sm">{title}</div>
      <div className="text-xs opacity-75">{desc}</div>
    </div>
  );
}
