import { useState } from "react";
import { post, put, money, decimal } from "../api";
import { useData, useAction } from "../state";
import {
  Card,
  Modal,
  Field,
  SelectId,
  Submit,
  Alert,
  Table,
  Badge,
  Icon,
  Loading,
} from "../components/ui";
import type { Catalogs } from "../types";
type Tab =
  | "producto"
  | "establecimiento"
  | "proveedor"
  | "categoria"
  | "provincia"
  | "ciudad"
  | "domicilio"
  | "motivo";
type Def = {
  name: string;
  label: string;
  type?: "money" | "boolean" | "reference" | "textarea";
  reference?: keyof Catalogs;
};
const labels: Record<Tab, string> = {
  producto: "Productos",
  establecimiento: "Establecimientos",
  proveedor: "Proveedores",
  categoria: "Categorías",
  provincia: "Provincias",
  ciudad: "Ciudades",
  domicilio: "Domicilios",
  motivo: "Motivos de devolución",
};
const definitions: Record<Tab, Def[]> = {
  producto: [
    { name: "codigo", label: "Código" },
    { name: "nombre", label: "Nombre" },
    { name: "detalle", label: "Descripción", type: "textarea" },
    {
      name: "categoria_id",
      label: "Categoría",
      type: "reference",
      reference: "categoria",
    },
    { name: "precio", label: "Precio de venta $", type: "money" },
    { name: "costo_referencia", label: "Costo de referencia $", type: "money" },
    { name: "esta_activo", label: "Activo", type: "boolean" },
  ],
  establecimiento: [
    { name: "nombre", label: "Nombre" },
    { name: "es_central", label: "Es centro de distribución", type: "boolean" },
    {
      name: "domicilio_id",
      label: "Domicilio",
      type: "reference",
      reference: "domicilio",
    },
  ],
  proveedor: [
    { name: "nombre", label: "Razón social" },
    { name: "CUIT", label: "CUIT (11 dígitos)" },
    { name: "esta_activo", label: "Activo", type: "boolean" },
  ],
  categoria: [{ name: "nombre", label: "Nombre" }],
  provincia: [{ name: "nombre", label: "Nombre" }],
  ciudad: [
    { name: "nombre", label: "Nombre" },
    {
      name: "provincia_id",
      label: "Provincia",
      type: "reference",
      reference: "provincia",
    },
  ],
  domicilio: [
    { name: "calle", label: "Calle" },
    { name: "altura", label: "Altura" },
    {
      name: "ciudad_id",
      label: "Ciudad",
      type: "reference",
      reference: "ciudad",
    },
  ],
  motivo: [{ name: "nombre", label: "Nombre" }],
};
export default function Catalog() {
  const { catalogs } = useData();
  const [tab, setTab] = useState<Tab>("producto"),
    [editing, setEditing] = useState<
      Record<string, unknown> | null | undefined
    >(undefined),
    [search, setSearch] = useState("");
  if (!catalogs) return <Loading />;
  const rows = (catalogs[tab] as unknown as Record<string, unknown>[]).filter(
    (r) =>
      Object.values(r).some((v) =>
        String(v).toLocaleLowerCase().includes(search.toLocaleLowerCase()),
      ),
  );
  function reference(def: Def, id: unknown) {
    const values = catalogs![def.reference!] as unknown as Record<
      string,
      unknown
    >[];
    const row = values.find((x) => x.id === id);
    return row
      ? def.reference === "domicilio"
        ? `${row.calle} ${row.altura}`
        : String(row.nombre)
      : "—";
  }
  return (
    <>
      <div className="toolbar">
        <div className="tabs">
          {(
            ["producto", "establecimiento", "proveedor", "categoria"] as Tab[]
          ).map((t) => (
            <button
              className={tab === t ? "selected" : ""}
              key={t}
              onClick={() => {
                setTab(t);
                setSearch("");
              }}
            >
              {labels[t]}
            </button>
          ))}
        </div>
        <select
          aria-label="Otros catálogos"
          value={
            ["provincia", "ciudad", "domicilio", "motivo"].includes(tab)
              ? tab
              : ""
          }
          onChange={(e) => {
            if (e.target.value) {
              setTab(e.target.value as Tab);
              setSearch("");
            }
          }}
        >
          <option value="">Ubicación y otros catálogos</option>
          {(["provincia", "ciudad", "domicilio", "motivo"] as Tab[]).map(
            (t) => (
              <option key={t} value={t}>
                {labels[t]}
              </option>
            ),
          )}
        </select>
      </div>
      <Card
        title={labels[tab]}
        description={
          tab === "establecimiento"
            ? "Creá primero provincia, ciudad y domicilio desde los otros catálogos."
            : tab === "producto"
              ? "Precios actuales y costos de referencia. Las ventas conservan sus valores históricos."
              : "Administrá los datos de referencia de tus operaciones."
        }
        action={
          <button className="button" onClick={() => setEditing(null)}>
            <Icon name="plus" size={17} />
            Agregar
          </button>
        }
      >
        <div className="search-field">
          <Icon name="search" size={17} />
          <input
            value={search}
            placeholder="Buscar en este catálogo…"
            aria-label="Buscar"
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Table
          rows={rows}
          columns={[
            {
              title: "ID",
              render: (r) => <span className="muted">#{String(r.id)}</span>,
            },
            ...definitions[tab]
              .filter((d) => d.type !== "textarea")
              .map((d) => ({
                title: d.label.replace(" $", ""),
                render: (r: Record<string, unknown>) =>
                  d.type === "money" ? (
                    money(Number(r[d.name]))
                  ) : d.type === "boolean" ? (
                    <Badge
                      value={
                        r[d.name]
                          ? d.name === "es_central"
                            ? "Centro de distribución"
                            : "Activo"
                          : d.name === "es_central"
                            ? "Local"
                            : "Inactivo"
                      }
                    />
                  ) : d.type === "reference" ? (
                    reference(d, r[d.name])
                  ) : (
                    String(r[d.name] ?? "")
                  ),
              })),
            {
              title: "",
              render: (r) => (
                <button className="text-button" onClick={() => setEditing(r)}>
                  Editar
                </button>
              ),
            },
          ]}
        />
      </Card>
      {editing !== undefined && (
        <CatalogForm
          key={tab + String(editing?.id ?? "new")}
          tab={tab}
          value={editing}
          onClose={() => setEditing(undefined)}
        />
      )}
    </>
  );
}
function CatalogForm({
  tab,
  value,
  onClose,
}: {
  tab: Tab;
  value: Record<string, unknown> | null;
  onClose: () => void;
}) {
  const { catalogs } = useData();
  const action = useAction();
  const [form, setForm] = useState<Record<string, string | number | boolean>>(
    () =>
      Object.fromEntries(
        definitions[tab].map((d) => [
          d.name,
          d.type === "money"
            ? decimal(Number(value?.[d.name] ?? 0))
            : d.type === "boolean"
              ? Boolean(value?.[d.name] ?? d.name === "esta_activo")
              : d.type === "reference"
                ? Number(value?.[d.name] ?? 0)
                : String(value?.[d.name] ?? ""),
        ]),
      ),
  );
  function set(name: string, v: string | number | boolean) {
    setForm((x) => ({ ...x, [name]: v }));
  }
  return (
    <Modal
      title={(value ? "Editar · " : "Agregar · ") + labels[tab]}
      onClose={onClose}
    >
      <form
        onSubmit={(e) => {
          e.preventDefault();
          action.run(
            () =>
              value
                ? put("/catalogos/" + tab + "/" + value.id, form)
                : post("/catalogos/" + tab, form),
            onClose,
          );
        }}
      >
        <div className="form-grid">
          {definitions[tab].map((d) => (
            <Field key={d.name} label={d.label}>
              {d.type === "boolean" ? (
                <select
                  value={String(form[d.name])}
                  onChange={(e) => set(d.name, e.target.value === "true")}
                >
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
              ) : d.type === "reference" ? (
                <SelectId
                  value={Number(form[d.name])}
                  options={(
                    catalogs![d.reference!] as unknown as Record<
                      string,
                      unknown
                    >[]
                  ).map((x) => ({
                    id: Number(x.id),
                    nombre:
                      d.reference === "domicilio"
                        ? `${x.calle} ${x.altura}`
                        : String(x.nombre),
                  }))}
                  onChange={(id) => set(d.name, id)}
                />
              ) : d.type === "textarea" ? (
                <textarea
                  value={String(form[d.name])}
                  maxLength={1000}
                  onChange={(e) => set(d.name, e.target.value)}
                />
              ) : (
                <input
                  required
                  value={String(form[d.name])}
                  type={d.type === "money" ? "number" : "text"}
                  min={d.name === "precio" ? "0.01" : "0"}
                  step={d.type === "money" ? "0.01" : undefined}
                  maxLength={d.name === "codigo" ? 50 : 150}
                  onChange={(e) => set(d.name, e.target.value)}
                />
              )}
            </Field>
          ))}
        </div>
        <Alert message={action.error} />
        <div className="form-footer">
          <button className="button subtle" type="button" onClick={onClose}>
            Cancelar
          </button>
          <Submit busy={action.busy} />
        </div>
      </form>
    </Modal>
  );
}
