export const kpis = [
  { label: "Órdenes activas", value: 12, delta: "+3", tone: "primary" },
  { label: "SKUs en stock bajo", value: 5, delta: "-2", tone: "warning" },
  { label: "Producción hoy (uds)", value: 1480, delta: "+12%", tone: "success" },
  { label: "Margen promedio", value: "32.4%", delta: "+1.2pp", tone: "primary" },
];

export const stockTrend = [
  { d: "Lun", in: 320, out: 280 },
  { d: "Mar", in: 410, out: 360 },
  { d: "Mié", in: 280, out: 340 },
  { d: "Jue", in: 520, out: 410 },
  { d: "Vie", in: 460, out: 480 },
  { d: "Sáb", in: 300, out: 220 },
  { d: "Dom", in: 180, out: 90 },
];

export const productionTrend = [
  { d: "S1", plan: 1200, real: 1100 },
  { d: "S2", plan: 1300, real: 1280 },
  { d: "S3", plan: 1250, real: 1310 },
  { d: "S4", plan: 1400, real: 1370 },
  { d: "S5", plan: 1500, real: 1480 },
];

export const materials = [
  { id: "MP-001", name: "Acero laminado 2mm",    unit: "kg", stock: 1240, reorder: 800,  cpp: 19400, status: "ok" },
  { id: "MP-002", name: "Pintura epóxica azul",  unit: "L",  stock: 38,   reorder: 60,   cpp: 49600, status: "low" },
  { id: "MP-003", name: "Tornillo M6 inox",      unit: "ud", stock: 9800, reorder: 5000, cpp: 320,   status: "ok" },
  { id: "MP-004", name: "Empaque cartón XL",     unit: "ud", stock: 120,  reorder: 200,  cpp: 3000,  status: "low" },
  { id: "MP-005", name: "Lubricante industrial", unit: "L",  stock: 0,    reorder: 50,   cpp: 24800, status: "out" },
  { id: "MP-006", name: "Cable AWG 14",          unit: "m",  stock: 2400, reorder: 1000, cpp: 1360,  status: "ok" },
];

export const products = [
  { id: "PT-101", name: "Estructura metálica STD", bomItems: 6,  estCost: 336800,  price: 556000,  stock: 42 },
  { id: "PT-102", name: "Mesa de trabajo Pro",     bomItems: 9,  estCost: 650000,  price: 1036000, stock: 18 },
  { id: "PT-103", name: "Estante modular S",       bomItems: 4,  estCost: 154800,  price: 279600,  stock: 96 },
  { id: "PT-104", name: "Carro logístico XL",      bomItems: 12, estCost: 980000,  price: 1596000, stock: 7  },
];

export const productionOrders = [
  { id: "OP-2026-0142", product: "Mesa de trabajo Pro", qty: 50,  status: "En proceso", progress: 64, due: "08 May" },
  { id: "OP-2026-0143", product: "Estructura metálica STD", qty: 120, status: "Planificada", progress: 0, due: "11 May" },
  { id: "OP-2026-0141", product: "Estante modular S", qty: 80,  status: "Liberada", progress: 22, due: "07 May" },
  { id: "OP-2026-0140", product: "Carro logístico XL", qty: 20,  status: "Completada", progress: 100, due: "05 May" },
  { id: "OP-2026-0139", product: "Mesa de trabajo Pro", qty: 30,  status: "Detenida", progress: 48, due: "06 May" },
];

export const sales = [
  { id: "FV-9821", client: "Industrias Norte SAS", date: "2026-05-05", total: 19_480_000, status: "Pagada"    },
  { id: "FV-9822", client: "Metalúrgica Andina",   date: "2026-05-05", total: 49_800_000, status: "Pendiente" },
  { id: "FV-9823", client: "Tornillos del Sur",    date: "2026-05-04", total: 3_922_000,  status: "Pagada"    },
  { id: "FV-9824", client: "Construcciones JL",    date: "2026-05-04", total: 29_280_000, status: "Vencida"   },
  { id: "FV-9825", client: "Logística Pacífico",   date: "2026-05-03", total: 8_600_000,  status: "Pagada"    },
];

export const finance = [
  { d: "Ene", income: 168_000_000, expense: 124_000_000 },
  { d: "Feb", income: 194_000_000, expense: 134_000_000 },
  { d: "Mar", income: 204_800_000, expense: 147_200_000 },
  { d: "Abr", income: 225_600_000, expense: 155_600_000 },
  { d: "May", income: 244_000_000, expense: 164_800_000 },
];
