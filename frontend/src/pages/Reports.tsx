import { useState } from "react";
import { money, dateTime, todayUTC } from "../api";
import { useData, useResource } from "../state";
import { Card, Field, SelectId, Alert, Table, Loading } from "../components/ui";
import type { Reports as ReportData, ReportRow } from "../types";
const definitions = [
  {
    key: "ventas",
    title: "Ventas e ingresos",
    description:
      "Cobros y reintegros imputados en su propia fecha, agrupados por local y medio.",
    columns: ["local", "medio_pago", "bruto", "reintegros", "neto"],
  },
  {
    key: "productos",
    title: "Productos y margen estimado",
    description:
      "Unidades e ingresos netos de devoluciones. El costo corresponde al momento de la venta; no incluye gastos ni impuestos.",
    columns: [
      "codigo",
      "producto",
      "unidades_netas",
      "ingreso_neto",
      "costo_neto",
      "margen_estimado",
    ],
  },
  {
    key: "existencias",
    title: "Existencias y mínimos",
    description:
      "Situación actual: el período no aplica. Valorización al costo de referencia vigente.",
    columns: [
      "establecimiento",
      "producto",
      "almacenado_total",
      "reservado",
      "disponible",
      "minimo_permitido",
      "faltante",
      "valorizacion",
    ],
  },
  {
    key: "rechazos",
    title: "Rechazos logísticos",
    description:
      "Bultos rechazados en el período. El valor de referencia no equivale a una merma definitiva.",
    columns: [
      "destino",
      "bulto_id",
      "numero_remito",
      "fecha",
      "motivo",
      "unidades",
      "valor_referencia",
    ],
  },
  {
    key: "transito",
    title: "Tiempo de tránsito",
    description:
      "Bultos despachados en el período. Promedio entre despacho y recepción física, expresado en horas.",
    columns: ["destino", "recibidos", "horas_promedio", "en_transito"],
  },
] as const;
const monetary = new Set([
  "bruto",
  "reintegros",
  "neto",
  "ingreso_neto",
  "costo_neto",
  "margen_estimado",
  "valorizacion",
  "valor_referencia",
]);
export default function Reports() {
  const { catalogs } = useData();
  const [filters, setFilters] = useState({
      desde: todayUTC().slice(0, 8) + "01",
      hasta: todayUTC(),
      local: 0,
    }),
    [applied, setApplied] = useState(filters);
  const [selected, setSelected] = useState("ventas");
  const query = new URLSearchParams({
    desde: applied.desde,
    hasta: applied.hasta,
    ...(applied.local ? { establecimiento_id: String(applied.local) } : {}),
  });
  const resource = useResource<ReportData>("/reportes?" + query.toString());
  if (!catalogs) return <Loading />;
  const definition = definitions.find((x) => x.key === selected)!;
  const data = resource.data?.[definition.key] ?? [];
  const income =
    resource.data?.ventas.reduce((sum, row) => sum + Number(row.neto), 0) ?? 0;
  const margin =
    resource.data?.productos.reduce(
      (sum, row) => sum + Number(row.margen_estimado),
      0,
    ) ?? 0;
  return (
    <>
      <Card title="Período y establecimiento">
        <form
          className="filters"
          onSubmit={(e) => {
            e.preventDefault();
            setApplied({ ...filters });
          }}
        >
          <Field label="Desde (UTC)">
            <input
              required
              type="date"
              value={filters.desde}
              onChange={(e) =>
                setFilters((x) => ({ ...x, desde: e.target.value }))
              }
            />
          </Field>
          <Field label="Hasta inclusive (UTC)">
            <input
              required
              type="date"
              min={filters.desde}
              value={filters.hasta}
              onChange={(e) =>
                setFilters((x) => ({ ...x, hasta: e.target.value }))
              }
            />
          </Field>
          <Field label="Establecimiento">
            <SelectId
              required={false}
              placeholder="Todos los establecimientos"
              value={filters.local}
              onChange={(local) => setFilters((x) => ({ ...x, local }))}
              options={catalogs.establecimiento}
            />
          </Field>
          <button className="button">Consultar</button>
        </form>
      </Card>
      <Alert message={resource.error} />
      <div className="metrics reports-metrics">
        <div className="metric">
          <span>Ingresos netos del período</span>
          <strong>{money(income)}</strong>
          <small>Cobros menos reintegros</small>
        </div>
        <div className="metric">
          <span>Margen bruto estimado</span>
          <strong>{money(margin)}</strong>
          <small>Con costo histórico de venta</small>
        </div>
        <div className="metric">
          <span>Bultos rechazados</span>
          <strong>{resource.data?.rechazos.length ?? 0}</strong>
          <small>Por fecha del rechazo</small>
        </div>
      </div>
      <div className="tabs report-tabs">
        {definitions.map((d, i) => (
          <button
            className={selected === d.key ? "selected" : ""}
            key={d.key}
            onClick={() => setSelected(d.key)}
          >
            <span>0{i + 1}</span>
            {d.title}
          </button>
        ))}
      </div>
      <Card title={definition.title} description={definition.description}>
        {resource.loading ? (
          <Loading />
        ) : (
          <Table<ReportRow>
            rows={data}
            columns={definition.columns.map((key) => ({
              title: key.replaceAll("_", " "),
              className: monetary.has(key) ? "numeric" : undefined,
              render: (row) =>
                row[key] === null
                  ? "—"
                  : monetary.has(key)
                    ? money(Number(row[key]))
                    : key === "fecha"
                      ? dateTime(String(row[key]))
                      : row[key],
            }))}
          />
        )}
      </Card>
    </>
  );
}
