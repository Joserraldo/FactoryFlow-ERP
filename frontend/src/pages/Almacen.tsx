import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { materials } from "@/data/mock";
import { Plus, Filter, Download } from "lucide-react";
import { formatCOP } from "@/lib/format";

const dot = (s: string) =>
  s === "ok" ? "bg-success" : s === "low" ? "bg-warning" : "bg-destructive";
const label = (s: string) => (s === "ok" ? "Óptimo" : s === "low" ? "Bajo" : "Quiebre");

export default function Almacen() {
  return (
    <div>
      <PageHeader
        title="Almacén"
        subtitle="Gestión de materias primas, CPP y puntos de reorden"
        actions={
          <>
            <Button variant="outline" size="sm"><Filter className="h-4 w-4 mr-2" />Filtros</Button>
            <Button variant="outline" size="sm"><Download className="h-4 w-4 mr-2" />Exportar</Button>
            <Button size="sm" className="bg-accent text-accent-foreground hover:bg-accent/90"><Plus className="h-4 w-4 mr-2" />Nuevo material</Button>
          </>
        }
      />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {[
          { l: "SKUs totales", v: materials.length },
          { l: "Óptimo", v: materials.filter(m => m.status === "ok").length, t: "text-success" },
          { l: "Stock bajo", v: materials.filter(m => m.status === "low").length, t: "text-warning-foreground" },
          { l: "Quiebre", v: materials.filter(m => m.status === "out").length, t: "text-destructive" },
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
                <TableHead className="text-right">Stock</TableHead>
                <TableHead className="text-right">Punto de reorden</TableHead>
                <TableHead className="text-right">CPP</TableHead>
                <TableHead className="text-right">Valor</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {materials.map((m) => (
                <TableRow key={m.id} className="hover:bg-secondary/40">
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className={`h-2.5 w-2.5 rounded-full ${dot(m.status)}`} />
                      <span className="text-xs text-muted-foreground">{label(m.status)}</span>
                    </div>
                  </TableCell>
                  <TableCell className="font-mono text-xs">{m.id}</TableCell>
                  <TableCell className="font-medium">{m.name}</TableCell>
                  <TableCell className="text-right tabular-nums">{m.stock} {m.unit}</TableCell>
                  <TableCell className="text-right tabular-nums text-muted-foreground">{m.reorder} {m.unit}</TableCell>
                  <TableCell className="text-right tabular-nums">{formatCOP(m.cpp)}</TableCell>
                  <TableCell className="text-right tabular-nums font-medium">{formatCOP(m.stock * m.cpp)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
