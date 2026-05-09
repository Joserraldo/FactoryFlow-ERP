import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus } from "lucide-react";
import { fetchAPI } from "@/lib/api";
import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";

export default function Proveedores() {
  const [suppliers, setSuppliers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({ name: "", contact_email: "", phone: "" });

  const loadData = () => {
    fetchAPI("/materials/suppliers")
      .then(setSuppliers)
      .catch(() => [])
      .finally(() => setLoading(false));
  };

  useEffect(() => { loadData(); }, []);

  const handleCreate = async () => {
    if (!formData.name) return alert("El nombre es obligatorio");
    try {
      await fetchAPI("/materials/suppliers", {
        method: "POST",
        body: JSON.stringify(formData)
      });
      setIsOpen(false);
      setFormData({ name: "", contact_email: "", phone: "" });
      loadData();
    } catch (e: any) { alert("Error: " + e.message); }
  };

  if (loading) return <div className="p-8 text-center text-muted-foreground">Cargando proveedores...</div>;

  return (
    <div>
      <PageHeader
        title="Proveedores"
        subtitle="Directorio de fuentes de abastecimiento"
        actions={
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90">
                <Plus className="h-4 w-4 mr-2" />Nuevo proveedor
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader><DialogTitle>Registrar nuevo proveedor</DialogTitle></DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid gap-2">
                  <Label>Nombre completo / Razón social</Label>
                  <Input value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} placeholder="Insumos S.A." />
                </div>
                <div className="grid gap-2">
                  <Label>Email de contacto</Label>
                  <Input type="email" value={formData.contact_email} onChange={e => setFormData({...formData, contact_email: e.target.value})} placeholder="ventas@empresa.com" />
                </div>
                <div className="grid gap-2">
                  <Label>Teléfono</Label>
                  <Input value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} placeholder="300 123 4567" />
                </div>
              </div>
              <DialogFooter>
                <Button onClick={handleCreate}>Registrar</Button>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        }
      />
      <Card className="border-border/60 mt-6">
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow className="bg-secondary/50">
                <TableHead>Nombre</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Teléfono</TableHead>
                <TableHead className="text-right">ID</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {suppliers.map(s => (
                <TableRow key={s.id} className="hover:bg-secondary/40">
                  <TableCell className="font-medium">{s.name}</TableCell>
                  <TableCell className="text-muted-foreground">{s.contact_email || '—'}</TableCell>
                  <TableCell className="text-muted-foreground">{s.phone || '—'}</TableCell>
                  <TableCell className="text-right font-mono text-[10px] text-muted-foreground w-20 truncate" title={s.id}>{s.id.split("-")[0]}</TableCell>
                </TableRow>
              ))}
              {suppliers.length === 0 && (
                <TableRow>
                  <TableCell colSpan={4} className="text-center py-6 text-muted-foreground">No hay proveedores registrados.</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
