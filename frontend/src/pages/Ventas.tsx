import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus } from "lucide-react";
import { formatCOP } from "@/lib/format";
import { fetchAPI } from "@/lib/api";
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const tone: Record<string, string> = {
  "Pagada": "bg-success/15 text-success",
  "Pendiente": "bg-warning/20 text-warning-foreground",
  "Vencida": "bg-destructive/10 text-destructive",
};

export default function Ventas() {
  const [sales, setSales] = useState<any[]>([]);
  const [products, setProducts] = useState<any[]>([]);
  const [clients, setClients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({ client_name: "", product_id: "", quantity: 1, unit_price: 0 });

  const loadData = () => {
    Promise.all([
      fetchAPI("/sales/").catch(() => []),
      fetchAPI("/products/").catch(() => []),
      fetchAPI("/sales/clients").catch(() => [])
    ]).then(([s, p, c]) => { 
        setSales(s.sort((a:any, b:any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())); 
        setProducts(p); 
        setClients(c); 
    }).finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, []);

  const handleCreate = async () => {
    if (!formData.client_name || !formData.product_id) return alert("Completa todos los campos obligatorios");
    try {
      // 1. Resolve client (RF-03 association)
      const clientRes = await fetchAPI("/sales/clients", {
        method: "POST",
        body: JSON.stringify({ name: formData.client_name, email: `${formData.client_name.replace(/\s+/g,'').toLowerCase()}@cliente.com` })
      });
      if (!clientRes.id) throw new Error("Fallo la creación del cliente");

      // 2. Register sale globally
      await fetchAPI("/sales/", {
        method: "POST",
        body: JSON.stringify({
          client_id: clientRes.id,
          items: [{ 
            product_id: formData.product_id, 
            quantity: formData.quantity, 
            unit_price: formData.unit_price 
          }]
        })
      });
      setIsOpen(false);
      loadData();
      alert("¡Venta registrada exitosamente!");
    } catch (e: any) { alert("Error: " + (e.message || "Fallo validando IDs")); }
  };

  const total = sales.reduce((a, s) => a + (s.total || 0), 0);
  const clientsCount = clients.length;

  if (loading) return <div className="p-8 text-center text-muted-foreground">Cargando ventas...</div>;

  return (
    <div>
      <PageHeader
        title="Ventas"
        subtitle="Facturación, clientes y cuentas por cobrar"
        actions={
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nueva venta</Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader><DialogTitle>Registrar nueva venta</DialogTitle></DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2"><Label>Nombre del Cliente</Label><Input value={formData.client_name} onChange={e => setFormData({...formData, client_name: e.target.value})} placeholder="Ej. Juan Pérez" /></div>
                <div className="grid gap-2"><Label>Producto</Label><select className="flex h-10 w-full rounded-md border border-input bg-background px-3" value={formData.product_id} onChange={e => setFormData({...formData, product_id: e.target.value})}><option value="">Selecciona...</option>{products.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}</select></div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2"><Label>Cantidad</Label><Input type="number" value={formData.quantity} onChange={e => setFormData({...formData, quantity: Number(e.target.value)})} /></div>
                  <div className="grid gap-2"><Label>Precio Unitario</Label><Input type="number" value={formData.unit_price} onChange={e => setFormData({...formData, unit_price: Number(e.target.value)})} /></div>
                </div>
              </div>
              <DialogFooter><Button onClick={handleCreate}>Guardar venta</Button></DialogFooter>
            </DialogContent>
          </Dialog>
        }
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="border-border/60"><CardContent className="p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Ventas del periodo</div>
          <div className="text-3xl font-semibold mt-1">{formatCOP(total)}</div>
        </CardContent></Card>
        <Card className="border-border/60"><CardContent className="p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Por cobrar</div>
          <div className="text-3xl font-semibold mt-1 text-warning-foreground">{formatCOP(0)}</div>
        </CardContent></Card>
        <Card className="border-border/60"><CardContent className="p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Clientes activos</div>
          <div className="text-3xl font-semibold mt-1">{clientsCount}</div>
        </CardContent></Card>
      </div>

      <Card className="border-border/60">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow className="bg-secondary/50">
                <TableHead>Factura</TableHead>
                <TableHead>Cliente</TableHead>
                <TableHead>Fecha</TableHead>
                <TableHead className="text-right">Total</TableHead>
                <TableHead>Estado</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sales.length === 0 ? <TableRow><TableCell colSpan={5} className="text-center">Sin ventas registradas</TableCell></TableRow> : null}
              {sales.map(s => {
                const client = clients.find(c => c.id === s.client_id);
                return (
                <TableRow key={s.id} className="hover:bg-secondary/40">
                  <TableCell className="font-mono text-[10px] w-24 truncate" title={s.id}>{s.id.split("-")[0]}</TableCell>
                  <TableCell className="font-medium">{client ? client.name : "Cliente registrado"}</TableCell>
                  <TableCell className="text-muted-foreground">{new Date(s.created_at).toLocaleDateString()}</TableCell>
                  <TableCell className="text-right tabular-nums font-medium">{formatCOP(s.total)}</TableCell>
                  <TableCell>
                    <span className={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded font-semibold ${tone["Pagada"]}`}>Pagada</span>
                  </TableCell>
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
