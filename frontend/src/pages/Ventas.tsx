import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus } from "lucide-react";
import { sales } from "@/data/mock";
import { formatCOP } from "@/lib/format";

const tone: Record<string, string> = {
  "Pagada": "bg-success/15 text-success",
  "Pendiente": "bg-warning/20 text-warning-foreground",
  "Vencida": "bg-destructive/10 text-destructive",
};

export default function Ventas() {
  const total = sales.reduce((a, s) => a + s.total, 0);
  const pendiente = sales.filter(s => s.status !== "Pagada").reduce((a, s) => a + s.total, 0);

  return (
    <div>
      <PageHeader
        title="Ventas"
        subtitle="Facturación, clientes y cuentas por cobrar"
        actions={<Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nueva venta</Button>}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card className="border-border/60"><CardContent className="p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Ventas del periodo</div>
          <div className="text-3xl font-semibold mt-1">{formatCOP(total)}</div>
        </CardContent></Card>
        <Card className="border-border/60"><CardContent className="p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Por cobrar</div>
          <div className="text-3xl font-semibold mt-1 text-warning-foreground">{formatCOP(pendiente)}</div>
        </CardContent></Card>
        <Card className="border-border/60"><CardContent className="p-5">
          <div className="text-xs uppercase tracking-wider text-muted-foreground">Clientes activos</div>
          <div className="text-3xl font-semibold mt-1">{new Set(sales.map(s => s.client)).size}</div>
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
              {sales.map(s => (
                <TableRow key={s.id} className="hover:bg-secondary/40">
                  <TableCell className="font-mono text-xs">{s.id}</TableCell>
                  <TableCell className="font-medium">{s.client}</TableCell>
                  <TableCell className="text-muted-foreground">{s.date}</TableCell>
                  <TableCell className="text-right tabular-nums font-medium">{formatCOP(s.total)}</TableCell>
                  <TableCell>
                    <span className={`text-[10px] uppercase tracking-wider px-2 py-0.5 rounded font-semibold ${tone[s.status]}`}>{s.status}</span>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
