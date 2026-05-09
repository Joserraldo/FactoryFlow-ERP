import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Layers, Coins, Tag, Boxes, Trash2 } from "lucide-react";
import { formatCOP } from "@/lib/format";
import { fetchAPI } from "@/lib/api";
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";

export default function Productos() {
  const [products, setProducts] = useState<any[]>([]);
  const [materials, setMaterials] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [viewProduct, setViewProduct] = useState<any>(null);
  
  const [formData, setFormData] = useState({ name: "", sale_price: 0 });
  const [bomItems, setBomItems] = useState([{ material_id: "", quantity_required: 1 }]);
  const [processes, setProcesses] = useState([{ name: "", order_index: 0 }]);

  const loadData = () => {
    Promise.all([
      fetchAPI("/products/").catch(() => []),
      fetchAPI("/materials/").catch(() => [])
    ]).then(([prods, mats]) => {
      setProducts(prods);
      setMaterials(mats);
    }).finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, []);

  const handleCreate = async () => {
    if (!formData.name) return alert("Completa el nombre");
    if (bomItems.some(b => !b.material_id)) return alert("Selecciona un material para todos los elementos del BOM.");
    if (processes.some(p => !p.name)) return alert("Agrega un nombre para cada proceso.");

    try {
      await fetchAPI("/products/", {
        method: "POST",
        body: JSON.stringify({
          name: formData.name,
          sale_price: formData.sale_price,
          bom_items: bomItems.filter(b => b.material_id),
          processes: processes.filter(p => p.name).map((p, i) => ({ name: p.name, order_index: i }))
        })
      });
      setIsOpen(false);
      setFormData({ name: "", sale_price: 0 });
      setBomItems([{ material_id: "", quantity_required: 1 }]);
      setProcesses([{ name: "", order_index: 0 }]);
      loadData();
    } catch (e: any) { alert("Error: " + e.message); }
  };

  if (loading) return <div className="p-8 text-center text-muted-foreground">Cargando productos...</div>;

  return (
    <div>
      <PageHeader
        title="Ingeniería de producto"
        subtitle="Catálogo de productos terminados y BOM (recetas de fabricación)"
        actions={
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nuevo producto</Button>
            </DialogTrigger>
            <DialogContent className="max-w-2xl">
              <DialogHeader><DialogTitle>Registrar nuevo producto final</DialogTitle></DialogHeader>
              <ScrollArea className="max-h-[70vh]">
                <div className="grid gap-6 py-4 px-1">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="grid gap-2"><Label>Nombre del producto</Label><Input value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="Ej: Mesa de Roble" /></div>
                    <div className="grid gap-2"><Label>Precio de venta (COP)</Label><Input type="number" value={formData.sale_price} onChange={e => setFormData({...formData, sale_price: Number(e.target.value)})} /></div>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label>Lista de Materiales (BOM)</Label>
                      <Button variant="outline" size="sm" onClick={() => setBomItems([...bomItems, { material_id: "", quantity_required: 1 }])}>+ Agregar Componente</Button>
                    </div>
                    {bomItems.map((bom, index) => (
                      <div key={index} className="flex gap-2 items-center">
                        <select className="flex h-10 w-full rounded-md border border-input bg-background px-3 text-sm" value={bom.material_id} onChange={e => {
                          const newBOM = [...bomItems]; newBOM[index].material_id = e.target.value; setBomItems(newBOM);
                        }}>
                          <option value="">Selecciona materia prima...</option>
                          {materials.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                        </select>
                        <Input type="number" step="any" className="w-24" value={bom.quantity_required} onChange={e => {
                          const newBOM = [...bomItems]; newBOM[index].quantity_required = Number(e.target.value); setBomItems(newBOM);
                        }} placeholder="Cant" />
                        <Button variant="ghost" size="icon" className="text-destructive w-10 shrink-0" onClick={() => setBomItems(bomItems.filter((_, i) => i !== index))}><Trash2 className="h-4 w-4" /></Button>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <Label>Procesos de Fabricación</Label>
                      <Button variant="outline" size="sm" onClick={() => setProcesses([...processes, { name: "", order_index: processes.length }])}>+ Agregar Paso</Button>
                    </div>
                    {processes.map((proc, index) => (
                      <div key={index} className="flex gap-2 items-center">
                        <span className="w-6 text-sm font-medium text-muted-foreground text-center shrink-0">{index + 1}.</span>
                        <Input className="flex-1" value={proc.name} onChange={e => {
                          const newProc = [...processes]; newProc[index].name = e.target.value; setProcesses(newProc);
                        }} placeholder="Ej: Corte, Ensamblaje..." />
                        <Button variant="ghost" size="icon" className="text-destructive w-10 shrink-0" onClick={() => setProcesses(processes.filter((_, i) => i !== index))}><Trash2 className="h-4 w-4" /></Button>
                      </div>
                    ))}
                  </div>
                </div>
              </ScrollArea>
              <DialogFooter><Button onClick={handleCreate}>Guardar producto y modelo BOM</Button></DialogFooter>
            </DialogContent>
          </Dialog>
        }
      />

      {/* Visor Avanzado de BOM (Actualización 1.2) */}
      <Dialog open={!!viewProduct} onOpenChange={(o) => !o && setViewProduct(null)}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Trazabilidad: {viewProduct?.name}</DialogTitle>
          </DialogHeader>
          <div className="grid gap-6 py-4">
            <div>
              <Label className="text-muted-foreground mb-2 block uppercase tracking-wider text-xs">Lista de Materiales (BOM)</Label>
              <div className="rounded-md border bg-secondary/20 p-4 space-y-3">
                {viewProduct?.bom_items?.length === 0 && <span className="text-sm">No tiene materiales asignados.</span>}
                {viewProduct?.bom_items?.map((b: any, idx: number) => {
                  const mat = materials.find(m => m.id === b.material_id);
                  return (
                    <div key={idx} className="flex justify-between items-center text-sm border-b pb-2 last:border-0 last:pb-0">
                      <div className="font-medium">{mat?.name || "Material desconocido"}</div>
                      <div className="tabular-nums opacity-80">{b.quantity_required} unidades req.</div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div>
              <Label className="text-muted-foreground mb-2 block uppercase tracking-wider text-xs">Ruta de Procesos de Fabricación</Label>
              <div className="rounded-md border bg-secondary/20 p-4 space-y-3">
                {viewProduct?.processes?.length === 0 && <span className="text-sm">No tiene procesos asignados.</span>}
                {viewProduct?.processes?.sort((a:any, b:any) => a.order_index - b.order_index).map((p: any, idx: number) => (
                  <div key={idx} className="flex gap-3 items-center text-sm border-b pb-2 last:border-0 last:pb-0">
                    <span className="bg-primary/20 text-primary font-bold h-6 w-6 rounded-full flex items-center justify-center text-xs">{p.order_index}</span>
                    <div className="font-medium">{p.name}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          <DialogFooter>
            <Button variant="secondary" onClick={() => setViewProduct(null)}>Cerrar Visor</Button>
            <Button onClick={() => window.location.href = '/produccion'}>Pasar a Producción</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {products.map(p => {
          return (
            <Card key={p.id} className="border-border/60 hover:shadow-[var(--shadow-elegant)] transition">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-mono text-xs text-muted-foreground w-16 truncate" title={p.id}>{p.id.split("-")[0]}</span>
                    <CardTitle className="mt-1 text-lg">{p.name}</CardTitle>
                  </div>
                  <Badge className="bg-primary/10 text-primary hover:bg-primary/15">{p.bom_items?.length || 0} Insumos</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <Row icon={<Layers className="h-4 w-4" />} label="Procesos" value={`${p.processes?.length || 0} pasos`} />
                <Row icon={<Tag className="h-4 w-4" />}    label="Precio de venta" value={formatCOP(p.sale_price || 0)} />
                <Row icon={<Boxes className="h-4 w-4" />}  label="Stock disponible" value={`${p.current_stock || 0} uds`} />
                <div className="flex gap-2 pt-2">
                  <Button variant="outline" size="sm" className="flex-1" onClick={() => setViewProduct(p)}>Ver Trazabilidad BOM</Button>
                  <Button size="sm" className="flex-1" onClick={() => alert("Por integridad ACID, no puedes editar la receta de un producto existente si ya hay OP generadas. Crea una nueva Revisión del producto.")}>Editar</Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
        {products.length === 0 && <div className="col-span-full p-8 text-center text-muted-foreground border border-dashed rounded-lg">No hay productos registrados con BOM en la base de datos. Crea uno.</div>}
      </div>
    </div>
  );
}

function Row({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-muted-foreground flex items-center gap-2">{icon}{label}</span>
      <span className="font-medium tabular-nums">{value}</span>
    </div>
  );
}
