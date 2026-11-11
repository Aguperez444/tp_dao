import { useState } from "react";
import { post, money, dateTime } from "../api";
import { useData, useResource, useAction } from "../state";
import {
  Card,
  Modal,
  Field,
  SelectId,
  LineEditor,
  Submit,
  Alert,
  Table,
  Badge,
  Icon,
  Loading,
} from "../components/ui";
import type { Purchase, CartLine } from "../types";
export default function Purchases() {
  const { catalogs } = useData(),
    resource = useResource<Purchase[]>("/compras"),
    action = useAction();
  const [open, setOpen] = useState(false),
    [receiving, setReceiving] = useState<Purchase | null>(null),
    [supplier, setSupplier] = useState(0),
    [lines, setLines] = useState<CartLine[]>([
      { producto_id: 0, cantidad: 1, costo: "0" },
    ]);
  if (!catalogs) return <Loading />;
  const estimate = lines.reduce(
    (sum, l) => sum + Math.round(Number(l.costo || 0) * 100) * l.cantidad,
    0,
  );
  return (
    <>
      <Alert message={resource.error} />
      <Card
        title="Abastecimiento del CD"
        description="Registrá una compra y confirmá su recepción para ingresar la mercadería."
        action={
          <button
            className="button"
            onClick={() => {
              action.clear();
              setOpen(true);
            }}
          >
            <Icon name="plus" size={17} />
            Nueva compra
          </button>
        }
      >
        <Table
          rows={resource.data ?? []}
          columns={[
            {
              title: "Compra",
              render: (r) => <strong>C-{String(r.id).padStart(6, "0")}</strong>,
            },
            { title: "Proveedor", render: (r) => r.proveedor },
            { title: "Fecha", render: (r) => dateTime(r.fecha) },
            { title: "Estado", render: (r) => <Badge value={r.estado} /> },
            {
              title: "Total",
              className: "numeric",
              render: (r) => money(r.total),
            },
            {
              title: "",
              render: (r) => (
                <button
                  className="text-button"
                  onClick={() => {
                    action.clear();
                    setReceiving(r);
                  }}
                >
                  {r.estado === "Pendiente" ? "Recibir compra" : "Ver detalle"}
                </button>
              ),
            },
          ]}
        />
      </Card>
      {open && (
        <Modal title="Registrar compra" onClose={() => setOpen(false)}>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              action.run(
                () =>
                  post("/compras", { proveedor_id: supplier, detalles: lines }),
                () => {
                  setOpen(false);
                  setLines([{ producto_id: 0, cantidad: 1, costo: "0" }]);
                  setSupplier(0);
                },
              );
            }}
          >
            <Field label="Proveedor">
              <SelectId
                value={supplier}
                onChange={setSupplier}
                options={catalogs.proveedor.filter((x) => x.esta_activo)}
              />
            </Field>
            <LineEditor value={lines} onChange={setLines} cost />
            <div className="total-line">
              <span>Total de compra</span>
              <strong>{money(estimate)}</strong>
            </div>
            <Alert message={action.error} />
            <div className="form-footer">
              <Submit busy={action.busy}>Registrar pendiente</Submit>
            </div>
          </form>
        </Modal>
      )}
      {receiving && (
        <Modal
          title={`Compra C-${String(receiving.id).padStart(6, "0")}`}
          onClose={() => setReceiving(null)}
        >
          <p className="muted">
            {receiving.proveedor} · {dateTime(receiving.fecha)}
          </p>
          <Table
            rows={receiving.detalles}
            columns={[
              {
                title: "Producto",
                render: (r) =>
                  catalogs.producto.find((p) => p.id === r.producto_id)?.nombre,
              },
              { title: "Unidades", render: (r) => r.cantidad },
              { title: "Costo unitario", render: (r) => money(r.costo) },
              { title: "Subtotal", render: (r) => money(r.costo * r.cantidad) },
            ]}
          />
          <div className="total-line">
            <span>Total</span>
            <strong>{money(receiving.total)}</strong>
          </div>
          {receiving.estado === "Pendiente" && (
            <>
              <p className="quiet-note">
                Confirmar la recepción incrementa el stock del centro de
                distribución una sola vez.
              </p>
              <Alert message={action.error} />
              <div className="form-footer">
                <button
                  className="button"
                  disabled={action.busy}
                  onClick={() =>
                    action.run(
                      () => post("/compras/" + receiving.id + "/recepcion"),
                      () => setReceiving(null),
                    )
                  }
                >
                  Confirmar recepción
                </button>
              </div>
            </>
          )}
        </Modal>
      )}
    </>
  );
}
