import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Filter, Download } from "lucide-react";
import { formatCOP } from "@/lib/format";
import { fetchAPI } from "@/lib/api";
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";

const dot = (s: string) =>
  s === "ok" ? "bg-success" : s === "low" ? "bg-warning" : "bg-destructive";
const label = (s: string) => (s === "ok" ? "Óptimo" : s === "low" ? "Bajo" : "Quiebre");

export default function Almacen() {
  const [materials, setMaterials] = useState<any[]>([]);
  const [units, setUnits] = useState<any[]>([]);
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // Form State
  const [isOpen, setIsOpen] = useState(false);
  const [isMovementOpen, setIsMovementOpen] = useState(false);
  const [formData, setFormData] = useState({ name: "", primary_unit_id: "", secondary_unit_id: "", conversion_factor: 1, stock_primary: 0, cost_cpp: 0 });
  const [movementData, setMovementData] = useState({ material_id: "", supplier_id: "", quantity_primary: 0, unit_cost: 0 });

  const loadData = () => {
    Promise.all([
      fetchAPI("/materials/").catch(() => []),
      fetchAPI("/materials/units").catch(() => []),
      fetchAPI("/materials/suppliers").catch(() => [])
    ]).then(([mats, uns, sups]) => {
      setMaterials(mats);
      setUnits(uns);
      setSuppliers(sups);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, []);

  const handleCreate = async () => {
    if (!formData.name || !formData.primary_unit_id || !formData.secondary_unit_id) return alert("Completa todos los campos obligatorios");
    try {
      await fetchAPI("/materials/", {
        method: "POST",
        body: JSON.stringify(formData)
      });
      setIsOpen(false);
      loadData();
    } catch (e: any) { alert("Error: " + e.message); }
  };

  const handleMovement = async () => {
    if (!movementData.material_id || movementData.quantity_primary <= 0 || movementData.unit_cost <= 0) {
      return alert("Completa el material, cantidad (mayor a 0) y costo unitario.");
    }
    try {
      await fetchAPI("/inventory/movement", {
        method: "POST",
        body: JSON.stringify({
          type: "IN",
          ...movementData
        })
      });
      setIsMovementOpen(false);
      setMovementData({ material_id: "", supplier_id: "", quantity_primary: 0, unit_cost: 0 });
      loadData();
      alert("¡Entrada registrada! Inventario y CPP actualizados.");
    } catch(e: any) { alert("Falló la entrada: " + e.message); }
  };


  if (loading) return <div className="p-8 text-center text-muted-foreground">Cargando inventario...</div>;

  return (
    <div>
      <PageHeader
        title="Almacén"
        subtitle="Gestión de materias primas, CPP y puntos de reorden"
        actions={
          <>
            <Button variant="outline" size="sm" onClick={() => alert("Los filtros avanzados requieren plan Pro. Comunícate con soporte.")}><Filter className="h-4 w-4 mr-2" />Filtros</Button>
            
            <Dialog open={isMovementOpen} onOpenChange={setIsMovementOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm" className="bg-accent/10 border-accent/20 text-accent font-medium">Entrada Inventario</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader><DialogTitle>Registrar entrada de materia prima (IN)</DialogTitle></DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label>Material</Label>
                    <select className="flex h-10 w-full rounded-md border border-input bg-background px-3 text-sm" value={movementData.material_id} onChange={e => setMovementData({...movementData, material_id: e.target.value})}>
                      <option value="">Selecciona...</option>
                      {materials.map(m => <option key={m.id} value={m.id}>{m.name} (Stock: {m.stock_primary.toFixed(2)})</option>)}
                    </select>
                  </div>
                  <div className="grid gap-2">
                    <Label>Proveedor (Opcional)</Label>
                    <select className="flex h-10 w-full rounded-md border border-input bg-background px-3 text-sm" value={movementData.supplier_id} onChange={e => setMovementData({...movementData, supplier_id: e.target.value})}>
                      <option value="">Sin proveedor específico...</option>
                      {suppliers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                    </select>
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="grid gap-2"><Label>Cantidad (Ingreso)</Label><Input type="number" step="any" min="0.01" value={movementData.quantity_primary} onChange={e => setMovementData({...movementData, quantity_primary: Number(e.target.value)})} /></div>
                    <div className="grid gap-2"><Label>Costo Unitario ($)</Label><Input type="number" step="any" min="0.01" value={movementData.unit_cost} onChange={e => setMovementData({...movementData, unit_cost: Number(e.target.value)})} /></div>
                  </div>
                </div>
                <DialogFooter><Button onClick={handleMovement}>Procesar Entrada</Button></DialogFooter>
              </DialogContent>
            </Dialog>
            <Dialog open={isOpen} onOpenChange={setIsOpen}>
              <DialogTrigger asChild>
                <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nuevo material</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader><DialogTitle>Registrar nueva materia prima</DialogTitle></DialogHeader>
                <div className="grid grid-cols-2 gap-4 py-2">
                  <div className="col-span-2 grid gap-1.5">
                    <Label>Nombre</Label>
                    <Input value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="Ej. Acero" />
                  </div>
                  <div className="grid gap-1.5"><Label>Unidad Primaria</Label><select className="flex h-10 w-full rounded-md border border-input bg-background px-3" value={formData.primary_unit_id} onChange={e => setFormData({...formData, primary_unit_id: e.target.value})}><option value="">Selecciona...</option>{units.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}</select></div>
                  <div className="grid gap-1.5"><Label>Unidad Secundaria</Label><select className="flex h-10 w-full rounded-md border border-input bg-background px-3" value={formData.secondary_unit_id} onChange={e => setFormData({...formData, secondary_unit_id: e.target.value})}><option value="">Selecciona...</option>{units.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}</select></div>
                  <div className="grid gap-1.5"><Label>Factor Conversión</Label><Input type="number" step="any" value={formData.conversion_factor} onChange={e => setFormData({...formData, conversion_factor: Number(e.target.value)})} /></div>
                  <div className="grid gap-1.5"><Label>Costo (CPP)</Label><Input type="number" step="any" value={formData.cost_cpp} onChange={e => setFormData({...formData, cost_cpp: Number(e.target.value)})} /></div>
                  <div className="col-span-2 grid gap-1.5"><Label>Stock Inicial (+)</Label><Input type="number" step="any" value={formData.stock_primary} onChange={e => setFormData({...formData, stock_primary: Number(e.target.value)})} /></div>
                </div>
                <DialogFooter><Button onClick={handleCreate}>Guardar material</Button></DialogFooter>
              </DialogContent>
            </Dialog>
          </>
        }
      />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {[
          { l: "SKUs totales", v: materials.length },
          { l: "Óptimo", v: materials.filter(m => m.stock_primary > 50).length, t: "text-success" },
          { l: "Stock bajo", v: materials.filter(m => m.stock_primary > 0 && m.stock_primary <= 50).length, t: "text-warning-foreground" },
          { l: "Quiebre", v: materials.filter(m => m.stock_primary === 0).length, t: "text-destructive" },
        ].map((c) => (
          <Card key={c.l} className="border-border/60">
            <CardContent className="p-5">
              <div className="text-xs uppercase tracking-wider text-muted-foreground">{c.l}</div>
              <div className={`text-3xl font-semibold mt-1 ${c.t ?? ""}`}>{c.v}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="border-border/60">
        <CardContent className="p-0">
          <div className="p-4 border-b">
            <Input placeholder="Buscar por nombre o SKU…" className="max-w-sm" />
          </div>
          <Table>
            <TableHeader>
              <TableRow className="bg-secondary/50">
                <TableHead>Estado</TableHead>
                <TableHead>SKU</TableHead>
                <TableHead>Material</TableHead>
                <TableHead>Proveedor</TableHead>
                <TableHead className="text-right">Stock</TableHead>
                <TableHead className="text-right">Punto de reorden</TableHead>
                <TableHead className="text-right">CPP</TableHead>
                <TableHead className="text-right">Valor</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {materials.map((m) => {
                const status = m.stock_primary > 50 ? "ok" : m.stock_primary > 0 ? "low" : "out";
                return (
                <TableRow key={m.id} className="hover:bg-secondary/40">
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className={`h-2.5 w-2.5 rounded-full ${dot(status)}`} />
                      <span className="text-xs text-muted-foreground">{label(status)}</span>
                    </div>
                  </TableCell>
                  <TableCell className="font-mono text-[10px] w-24 truncate" title={m.id}>{m.id.split("-")[0]}</TableCell>
                  <TableCell className="font-medium">{m.name}</TableCell>
                  <TableCell className="text-muted-foreground">Múltiples</TableCell>
                  <TableCell className="text-right tabular-nums">{m.stock_primary}</TableCell>
                  <TableCell className="text-right tabular-nums text-muted-foreground">50</TableCell>
                  <TableCell className="text-right tabular-nums">{formatCOP(m.cost_cpp)}</TableCell>
                  <TableCell className="text-right tabular-nums font-medium">{formatCOP(m.stock_primary * m.cost_cpp)}</TableCell>
                </TableRow>
                )
              })}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
