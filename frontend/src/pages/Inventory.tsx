import { useState } from "react";
import { money, dateTime, put, todayUTC } from "../api";
import { useData, useResource, useAction } from "../state";
import {
  Card,
  Modal,
  Field,
  SelectId,
  Submit,
  Alert,
  Table,
  Badge,
  Loading,
} from "../components/ui";
import type { Stock, ReportRow } from "../types";
export default function Inventory() {
  const { catalogs } = useData(),
    action = useAction();
  const [local, setLocal] = useState(0),
    [search, setSearch] = useState(""),
    [onlyLow, setOnlyLow] = useState(false),
    [edit, setEdit] = useState<Stock | null>(null),
    [minimum, setMinimum] = useState(0);
  const resource = useResource<Stock[]>(
    "/inventario" + (local ? "?establecimiento_id=" + local : ""),
  );
  const movements = useResource<ReportRow[]>(
    "/inventario/movimientos?hasta=" +
      todayUTC() +
      (local ? "&establecimiento_id=" + local : ""),
  );
  if (!catalogs) return <Loading />;
  const rows =
    resource.data?.filter(
      (x) =>
        (!onlyLow || x.faltante > 0) &&
        (x.producto + " " + x.codigo)
          .toLocaleLowerCase()
          .includes(search.toLocaleLowerCase()),
    ) ?? [];
  return (
    <>
      <Alert message={resource.error || movements.error} />
      <Card
        title="Existencias actuales"
        description="Almacenado incluye únicamente unidades habilitadas. Disponible = almacenado − reservado."
      >
        <div className="filters">
          <Field label="Establecimiento">
            <SelectId
              required={false}
              placeholder="Todos los establecimientos"
              value={local}
              onChange={setLocal}
              options={catalogs.establecimiento}
            />
          </Field>
          <Field label="Buscar producto">
            <input
              value={search}
              placeholder="Nombre o código"
              onChange={(e) => setSearch(e.target.value)}
            />
          </Field>
          <label className="check-field">
            <input
              type="checkbox"
              checked={onlyLow}
              onChange={(e) => setOnlyLow(e.target.checked)}
            />
            Solo por debajo del mínimo
          </label>
        </div>
        <Table
          rows={rows}
          columns={[
            {
              title: "Producto",
              render: (r) => (
                <>
                  <strong>{r.producto}</strong>
                  <small className="cell-sub">{r.codigo}</small>
                </>
              ),
            },
            { title: "Establecimiento", render: (r) => r.establecimiento },
            {
              title: "Almacenado",
              className: "numeric",
              render: (r) => r.almacenado_total,
            },
            {
              title: "Reservado",
              className: "numeric",
              render: (r) => r.reservado,
            },
            {
              title: "Disponible",
              className: "numeric",
              render: (r) => <strong>{r.disponible}</strong>,
            },
            {
              title: "Mínimo",
              className: "numeric",
              render: (r) => r.minimo_permitido,
            },
            {
              title: "Estado",
              render: (r) => (
                <Badge
                  value={r.faltante ? "Faltan " + r.faltante : "En nivel"}
                />
              ),
            },
            {
              title: "Valor de referencia",
              className: "numeric",
              render: (r) => money(r.valorizacion),
            },
            {
              title: "",
              render: (r) => (
                <button
                  className="text-button"
                  onClick={() => {
                    action.clear();
                    setEdit(r);
                    setMinimum(r.minimo_permitido);
                  }}
                >
                  Editar mínimo
                </button>
              ),
            },
          ]}
        />
      </Card>
      <Card
        title="Movimientos de inventario"
        description="Entradas y salidas reconstruidas a partir de las operaciones registradas."
      >
        <Table
          rows={movements.data ?? []}
          columns={[
            { title: "Fecha", render: (r) => dateTime(String(r.fecha)) },
            { title: "Establecimiento", render: (r) => r.establecimiento },
            { title: "Producto", render: (r) => r.producto },
            {
              title: "Unidades",
              className: "numeric",
              render: (r) => (
                <span
                  className={Number(r.cantidad) > 0 ? "positive" : "negative"}
                >
                  {Number(r.cantidad) > 0 ? "+" : ""}
                  {r.cantidad}
                </span>
              ),
            },
            { title: "Concepto", render: (r) => r.concepto },
            { title: "Referencia", render: (r) => r.referencia },
          ]}
        />
      </Card>
      {edit && (
        <Modal title="Configurar nivel mínimo" onClose={() => setEdit(null)}>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              action.run(
                () =>
                  put("/inventario/minimo", {
                    establecimiento_id: edit.establecimiento_id,
                    producto_id: edit.producto_id,
                    minimo_permitido: minimum,
                  }),
                () => setEdit(null),
              );
            }}
          >
            <p>
              {edit.producto} · {edit.establecimiento}
            </p>
            <Field label="Mínimo de unidades">
              <input
                required
                type="number"
                min="0"
                step="1"
                value={minimum}
                onChange={(e) => setMinimum(Number(e.target.value))}
              />
            </Field>
            <Alert message={action.error} />
            <div className="form-footer">
              <Submit busy={action.busy} />
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}
