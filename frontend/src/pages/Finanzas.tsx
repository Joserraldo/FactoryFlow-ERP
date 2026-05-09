import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { finance } from "@/data/mock";
import { formatCOP } from "@/lib/format";
import {
  Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis, Line, ComposedChart,
} from "recharts";

export default function Finanzas() {
  const data = finance.map(f => ({ ...f, margin: f.income - f.expense }));
  const totalIn = data.reduce((a, d) => a + d.income, 0);
  const totalOut = data.reduce((a, d) => a + d.expense, 0);
  const margin = totalIn - totalOut;

  return (
    <div>
      <PageHeader title="Finanzas" subtitle="Ingresos, egresos y margen operativo" />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {[
          { l: "Ingresos YTD", v: totalIn, t: "text-success" },
          { l: "Egresos YTD", v: totalOut, t: "text-destructive" },
          { l: "Margen", v: margin, t: "text-primary" },
        ].map(c => (
          <Card key={c.l} className="border-border/60"><CardContent className="p-5">
            <div className="text-xs uppercase tracking-wider text-muted-foreground">{c.l}</div>
            <div className={`text-3xl font-semibold mt-1 ${c.t}`}>{formatCOP(c.v, { compact: true })}</div>
          </CardContent></Card>
        ))}
      </div>

      <Card className="border-border/60">
        <CardHeader><CardTitle>Flujo financiero mensual</CardTitle></CardHeader>
        <CardContent className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
              <XAxis dataKey="d" stroke="hsl(var(--muted-foreground))" fontSize={12} />
              <YAxis stroke="hsl(var(--muted-foreground))" fontSize={12} tickFormatter={(v) => formatCOP(v, { compact: true })} />
              <Tooltip
                contentStyle={{ background: "hsl(var(--card))", border: "1px solid hsl(var(--border))", borderRadius: 8 }}
                formatter={(v: number) => formatCOP(v)}
              />
              <Legend />
              <Bar dataKey="income" name="Ingresos" fill="hsl(var(--primary))" radius={[6,6,0,0]} />
              <Bar dataKey="expense" name="Egresos" fill="hsl(var(--steel))" radius={[6,6,0,0]} />
              <Line type="monotone" dataKey="margin" name="Margen" stroke="hsl(var(--accent))" strokeWidth={3} dot={{ r: 4 }} />
            </ComposedChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
