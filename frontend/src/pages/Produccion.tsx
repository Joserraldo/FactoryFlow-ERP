/**
 * ============================================================================
 * Página: Producción (Produccion)
 * Propósito: Visualizar, dar seguimiento y encolar lotes de fabricación 
 *            mediante un tablero Kanban de 5 columnas.
 * Rol Arquitectónico: View Component / Controller. Consume el API Gateway 
 *                     del backend y maneja de forma robusta las validaciones 
 *                     del ciclo atómico de producción (RF-02).
 * Dependencias: PageHeader (Layout), UI components (Dialog, Input, Card), 
 *               fetchAPI (Cliente HTTP centralizado).
 * ============================================================================
 */

import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Plus } from "lucide-react";
import { fetchAPI } from "@/lib/api";
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

// Define clases CSS dinámicas según el estado físico/virtual de la orden.
const tone: Record<string, string> = {
  "En proceso": "bg-primary/10 text-primary border-primary/20",
  "Planificada": "bg-secondary text-secondary-foreground border-border",
  "Liberada": "bg-accent/15 text-accent border-accent/30",
  "Completada": "bg-success/15 text-success border-success/30",
  "Detenida": "bg-destructive/10 text-destructive border-destructive/30",
};

// Columnas del tablero Kanban ERP
const cols = ["Planificada", "Liberada", "En proceso", "Detenida", "Completada"];

/**
 * Componente principal de la página de Producción.
 * Controla el Kanban, las llamadas asíncronas de datos y la creación de órdenes de fabricación.
 */
export default function Produccion() {
  const [orders, setOrders] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Estados para el formulario modal de nueva orden
  const [isOpen, setIsOpen] = useState(false);
  const [productId, setProductId] = useState("");
  const [quantity, setQuantity] = useState(10);

  /**
   * Carga concurrentemente las órdenes de producción y la lista de productos
   * del servidor para poblar el Kanban y el formulario modal.
   */
  const loadData = () => {
    Promise.all([
      fetchAPI("/production-orders/").catch(() => []),
      fetchAPI("/products/").catch(() => [])
    ]).then(([ords, prods]) => {
      setOrders(ords);
      setProducts(prods);
    }).finally(() => setLoading(false));
  };

  // Carga inicial al montar el componente
  useEffect(() => { loadData(); }, []);

  /**
   * Envía la orden de producción solicitada al Backend de FastAPI.
   * Maneja errores lógicos como falta de stock o recetas inexistentes (BOM)
   * que son regresados de forma atómica por el backend en el rollback.
   */
  const handleCreate = async () => {
    if (!productId) return alert("Selecciona un producto");
    try {
      await fetchAPI("/production-orders/", {
        method: "POST",
        body: JSON.stringify({ product_id: productId, quantity, step_assignments: [] })
      });
      setIsOpen(false);
      loadData();
      alert("¡Orden de Producción encolada!");
    } catch (e: any) {
      const msg = e.message?.toLowerCase();
      // Captura el fallo de transacción de FastAPI (Falta de stock o BOM sin items)
      if (msg?.includes("bom") || msg?.includes("insufficient") || msg?.includes("stock")) {
        alert("Error de Manufactura (RF-02):\n\n" + e.message + "\n\nAsegúrate de que este producto cuenta con una lista de materiales (BOM) y que tienes STOCK SUFICIENTE en el almacén.");
      } else {
        alert("Error: " + e.message);
      }
    }
  };

  if (loading) return <div className="p-8 text-center text-muted-foreground">Cargando producción...</div>;

  return (
    <div>
      <PageHeader
        title="Producción"
        subtitle="Tablero kanban de órdenes de fabricación"
        actions={
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90">
                <Plus className="h-4 w-4 mr-2" />Nueva orden
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader><DialogTitle>Crear orden de producción</DialogTitle></DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2">
                  <Label>ID del Producto (UUID)</Label>
                  <select 
                    className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm"
                    value={productId} 
                    onChange={e => setProductId(e.target.value)}
                  >
                    <option value="">Selecciona producto...</option>
                    {products.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
                  </select>
                </div>
                <div className="grid gap-2">
                  <Label>Cantidad a fabricar</Label>
                  <Input type="number" value={quantity} onChange={e => setQuantity(Number(e.target.value))} />
                </div>
              </div>
              <DialogFooter>
                <Button onClick={handleCreate}>Iniciar fabricación</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        }
      />

      {/* Tablero Kanban */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-4">
        {cols.map(col => {
          const items = orders.filter(o => {
            const st = o.status === "in_progress" ? "En proceso" : o.status === "completed" ? "Completada" : o.status === "cancelled" ? "Detenida" : "Planificada";
            return st === col;
          });
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
                        <span className="font-mono text-[11px] text-muted-foreground w-16 truncate" title={o.id}>{o.id.split("-")[0]}</span>
                        <span className={`text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border ${tone[col] || tone["En proceso"]}`}>{col}</span>
                      </div>
                      <div className="font-medium text-sm mt-2">{products.find(p => p.id === o.product_id)?.name || "Producto Desconocido"}</div>
                      <div className="text-xs text-muted-foreground">{o.quantity} unidades</div>
                      <div className="text-xs text-primary/80 mt-1">Gasto total: Calculado · {o.steps?.length} fases</div>
                      <div className="text-xs text-muted-foreground">👤 API Tracked</div>
                      <Progress value={col === "Completada" ? 100 : col === "En proceso" ? 60 : 0} className="h-1.5 mt-2" />
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
