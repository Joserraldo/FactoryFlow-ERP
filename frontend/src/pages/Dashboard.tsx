import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Download, Plus, ArrowUpRight, AlertTriangle, CheckCircle2, Factory, PackageX } from "lucide-react";
import { kpis, stockTrend, productionTrend, productionOrders, materials } from "@/data/mock";
import {
  Area, AreaChart, Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis,
} from "recharts";

const toneClass: Record<string, string> = {
  primary: "bg-primary/10 text-primary",
  success: "bg-success/10 text-success",
  warning: "bg-warning/15 text-warning-foreground",
};

export default function Dashboard() {
  return (
    <div>
      <PageHeader
        title="Centro de control"
        subtitle="Visión integral de planta · materias primas, producción y finanzas"
        actions={
          <>
            <Button variant="outline" size="sm"><Download className="h-4 w-4 mr-2" />Exportar</Button>
            <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nueva OP</Button>
          </>
        }
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((k) => (
          <Card key={k.label} className="shadow-[var(--shadow-card)] border-border/60">
            <CardContent className="p-5">
              <div className="flex items-start justify-between">
                <div>
                  <div className="text-xs uppercase tracking-wider text-muted-foreground">{k.label}</div>
                  <div className="text-3xl font-semibold mt-2">{k.value}</div>
                </div>
                <span className={`text-xs px-2 py-1 rounded-md font-medium ${toneClass[k.tone]}`}>
                  {k.delta}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-6">
        <Card className="lg:col-span-2 border-border/60">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Producción semanal</CardTitle>
              <p className="text-sm text-muted-foreground">Plan vs. real (unidades)</p>
            </div>
            <Badge variant="secondary" className="gap-1"><ArrowUpRight className="h-3 w-3" /> +6.4%</Badge>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={productionTrend}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="d" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8 }} />
                <Legend />
                <Bar dataKey="plan" fill="hsl(var(--steel))" radius={[6, 6, 0, 0]} />
                <Bar dataKey="real" fill="hsl(var(--primary))" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="border-border/60">
          <CardHeader>
            <CardTitle>Movimientos de stock</CardTitle>
            <p className="text-sm text-muted-foreground">Entradas vs. salidas (7d)</p>
          </CardHeader>
          <CardContent className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stockTrend}>
                <defs>
                  <linearGradient id="gIn" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="hsl(var(--primary))" stopOpacity={0.5} />
                    <stop offset="100%" stopColor="hsl(var(--primary))" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="gOut" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="hsl(var(--accent))" stopOpacity={0.5} />
                    <stop offset="100%" stopColor="hsl(var(--accent))" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="d" stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} />
                <Tooltip contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8 }} />
                <Area type="monotone" dataKey="in" stroke="hsl(var(--primary))" fill="url(#gIn)" />
                <Area type="monotone" dataKey="out" stroke="hsl(var(--accent))" fill="url(#gOut)" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mt-6">
        <Card className="lg:col-span-2 border-border/60">
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Órdenes de producción activas</CardTitle>
              <p className="text-sm text-muted-foreground">Trazabilidad en tiempo real</p>
            </div>
            <Factory className="h-5 w-5 text-muted-foreground" />
          </CardHeader>
          <CardContent className="space-y-4">
            {productionOrders.slice(0, 4).map((o) => (
              <div key={o.id} className="flex items-center gap-4 p-3 rounded-md border border-border/60 hover:bg-secondary/40 transition">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-muted-foreground">{o.id}</span>
                    <StatusBadge status={o.status} />
                  </div>
                  <div className="font-medium truncate">{o.product} <span className="text-muted-foreground font-normal">· {o.qty} uds</span></div>
                  <Progress value={o.progress} className="h-1.5 mt-2" />
                </div>
                <div className="text-right">
                  <div className="text-xs text-muted-foreground">Entrega</div>
                  <div className="font-medium">{o.due}</div>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="border-border/60">
          <CardHeader>
            <CardTitle>Alertas de inventario</CardTitle>
            <p className="text-sm text-muted-foreground">Reorden y quiebres</p>
          </CardHeader>
          <CardContent className="space-y-3">
            {materials.filter(m => m.status !== "ok").map(m => (
              <div key={m.id} className="flex items-start gap-3 p-3 rounded-md bg-secondary/40">
                <div className={`mt-0.5 h-8 w-8 rounded-md grid place-items-center ${m.status === "out" ? "bg-destructive/15 text-destructive" : "bg-warning/20 text-warning-foreground"}`}>
                  {m.status === "out" ? <PackageX className="h-4 w-4" /> : <AlertTriangle className="h-4 w-4" />}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-sm">{m.name}</div>
                  <div className="text-xs text-muted-foreground">Stock {m.stock} {m.unit} · reorden {m.reorder}</div>
                </div>
              </div>
            ))}
            <div className="flex items-start gap-3 p-3 rounded-md bg-success/10">
              <div className="mt-0.5 h-8 w-8 rounded-md bg-success/20 text-success grid place-items-center">
                <CheckCircle2 className="h-4 w-4" />
              </div>
              <div className="flex-1">
                <div className="font-medium text-sm">4 SKUs en niveles óptimos</div>
                <div className="text-xs text-muted-foreground">Sin acción requerida</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const map: Record<string, string> = {
    "En proceso": "bg-primary/10 text-primary",
    "Planificada": "bg-secondary text-secondary-foreground",
    "Liberada": "bg-accent/15 text-accent",
    "Completada": "bg-success/15 text-success",
    "Detenida": "bg-destructive/10 text-destructive",
    "Pagada": "bg-success/15 text-success",
    "Pendiente": "bg-warning/20 text-warning-foreground",
    "Vencida": "bg-destructive/10 text-destructive",
  };
  return <span className={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded font-semibold ${map[status] ?? "bg-secondary"}`}>{status}</span>;
}
