import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Plus, Layers, Coins, Tag, Boxes } from "lucide-react";
import { products } from "@/data/mock";
import { formatCOP } from "@/lib/format";

export default function Productos() {
  return (
    <div>
      <PageHeader
        title="Ingeniería de producto"
        subtitle="Catálogo de productos terminados y BOM (recetas de fabricación)"
        actions={<Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nuevo producto</Button>}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {products.map(p => {
          const margin = ((p.price - p.estCost) / p.price) * 100;
          return (
            <Card key={p.id} className="border-border/60 hover:shadow-[var(--shadow-elegant)] transition">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-mono text-xs text-muted-foreground">{p.id}</span>
                    <CardTitle className="mt-1 text-lg">{p.name}</CardTitle>
                  </div>
                  <Badge className="bg-primary/10 text-primary hover:bg-primary/15">{margin.toFixed(0)}% margen</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <Row icon={<Layers className="h-4 w-4" />} label="Componentes BOM" value={`${p.bomItems} ítems`} />
                <Row icon={<Coins className="h-4 w-4" />}  label="Costo estimado"  value={formatCOP(p.estCost)} />
                <Row icon={<Tag className="h-4 w-4" />}    label="Precio de venta" value={formatCOP(p.price)} />
                <Row icon={<Boxes className="h-4 w-4" />}  label="Stock disponible" value={`${p.stock} uds`} />
                <div className="flex gap-2 pt-2">
                  <Button variant="outline" size="sm" className="flex-1">Ver BOM</Button>
                  <Button size="sm" className="flex-1">Editar</Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
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
