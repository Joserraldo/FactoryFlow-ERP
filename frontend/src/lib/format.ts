// Formatos de moneda y números — COP por defecto
export const formatCOP = (value: number, opts: { decimals?: boolean; compact?: boolean } = {}) => {
  const { decimals = false, compact = false } = opts;
  return new Intl.NumberFormat("es-CO", {
    style: "currency",
    currency: "COP",
    minimumFractionDigits: decimals ? 2 : 0,
    maximumFractionDigits: decimals ? 2 : 0,
    notation: compact ? "compact" : "standard",
  }).format(value);
};

export const formatNumber = (value: number) =>
  new Intl.NumberFormat("es-CO").format(value);