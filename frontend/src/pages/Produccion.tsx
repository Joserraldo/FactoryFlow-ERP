import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Plus } from "lucide-react";
import { productionOrders } from "@/data/mock";

const tone: Record<string, string> = {
  "En proceso": "bg-primary/10 text-primary border-primary/20",
  "Planificada": "bg-secondary text-secondary-foreground border-border",
  "Liberada": "bg-accent/15 text-accent border-accent/30",
  "Completada": "bg-success/15 text-success border-success/30",
  "Detenida": "bg-destructive/10 text-destructive border-destructive/30",
};

const cols = ["Planificada", "Liberada", "En proceso", "Detenida", "Completada"];

export default function Produccion() {
  return (
    <div>
      <PageHeader
        title="Producción"
        subtitle="Tablero kanban de órdenes de fabricación"
        actions={<Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nueva orden</Button>}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">
        {cols.map(col => {
          const items = productionOrders.filter(o => o.status === col);
          return (
            <div key={col} className="bg-secondary/40 rounded-lg p-3 border border-border/60">
              <div className="flex items-center justify-between mb-3 px-1">
                <span className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">{col}</span>
                <span className="text-xs bg-card border rounded-full h-5 min-w-5 px-1.5 grid place-items-center">{items.length}</span>
              </div>
              <div className="space-y-2">
                {items.map(o => (
                  <Card key={o.id} className="border-border/60 cursor-pointer hover:shadow-[var(--shadow-card)] transition">
                    <CardContent className="p-3">
                      <div className="flex items-center justify-between">
                        <span className="font-mono text-[11px] text-muted-foreground">{o.id}</span>
                        <span className={`text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border ${tone[o.status]}`}>{o.status}</span>
                      </div>
                      <div className="font-medium text-sm mt-2">{o.product}</div>
                      <div className="text-xs text-muted-foreground">{o.qty} unidades · {o.due}</div>
                      <Progress value={o.progress} className="h-1.5 mt-2" />
                    </CardContent>
                  </Card>
                ))}
                {items.length === 0 && (
                  <div className="text-xs text-muted-foreground text-center py-6">Sin órdenes</div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
