import { useState } from "react";
import { post, money, decimal, dateTime } from "../api";
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
import type { Sale, SaleDetail, CartLine } from "../types";
export default function Sales() {
  const resource = useResource<Sale[]>("/ventas");
  const [open, setOpen] = useState(false);
  return (
    <>
      <Alert message={resource.error} />
      <Card
        title="Comprobantes de venta"
        description="Cada venta confirma el cobro y descuenta stock verificado del local."
        action={
          <button className="button" onClick={() => setOpen(true)}>
            <Icon name="plus" size={17} />
            Nueva venta
          </button>
        }
      >
        <Table
          rows={resource.data ?? []}
          columns={[
            {
              title: "Comprobante",
              render: (r) => (
                <a className="text-link" href={"#/ventas/" + r.id}>
                  {r.numero_comprobante}
                </a>
              ),
            },
            { title: "Local", render: (r) => r.local },
            { title: "Fecha", render: (r) => dateTime(r.fecha) },
            { title: "Cobro", render: (r) => <Badge value={r.metodo_pago} /> },
            {
              title: "Total",
              className: "numeric",
              render: (r) => <strong>{money(r.total)}</strong>,
            },
            {
              title: "Reintegrado",
              className: "numeric",
              render: (r) => money(r.reintegrado),
            },
            {
              title: "",
              render: (r) => (
                <a className="text-link" href={"#/ventas/" + r.id}>
                  Ver detalle →
                </a>
              ),
            },
          ]}
        />
      </Card>
      {open && <SaleForm onClose={() => setOpen(false)} />}
    </>
  );
}
function SaleForm({ onClose }: { onClose: () => void }) {
  const { catalogs } = useData(),
    action = useAction();
  const stock =
    useResource<
      { establecimiento_id: number; producto_id: number; disponible: number }[]
    >("/inventario");
  const [local, setLocal] = useState(0),
    [method, setMethod] = useState(0),
    [policy, setPolicy] = useState("lista"),
    [amount, setAmount] = useState(""),
    [lines, setLines] = useState<CartLine[]>([{ producto_id: 0, cantidad: 1 }]);
  const total = lines.reduce((sum, l) => {
    const p = catalogs?.producto.find((x) => x.id === l.producto_id);
    const price = p?.precio ?? 0;
    const discount =
      policy === "descuento_10" ? Math.floor((price * 10 + 50) / 100) : 0;
    return sum + (price - discount) * l.cantidad;
  }, 0);
  if (!catalogs) return <Loading />;
  return (
    <Modal title="Registrar venta" onClose={onClose}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          action.run(
            () =>
              post<SaleDetail>("/ventas", {
                local_id: local,
                metodo_pago_id: method,
                politica: policy,
                importe_cobrado: amount || decimal(total),
                detalles: lines,
              }),
            (result) => {
              onClose();
              window.location.hash = "/ventas/" + result.id;
            },
          );
        }}
      >
        <div className="form-grid">
          <Field label="Local de venta">
            <SelectId
              value={local}
              onChange={setLocal}
              options={catalogs.establecimiento.filter((x) => !x.es_central)}
            />
          </Field>
          <Field label="Política de precio">
            <select value={policy} onChange={(e) => setPolicy(e.target.value)}>
              <option value="lista">Precio de lista</option>
              <option value="descuento_10">Descuento del 10%</option>
            </select>
          </Field>
        </div>
        <LineEditor value={lines} onChange={setLines} />
        {local > 0 && (
          <div className="availability">
            {lines
              .filter((l) => l.producto_id)
              .map((l, i) => (
                <span key={i}>
                  {
                    catalogs.producto.find((p) => p.id === l.producto_id)
                      ?.nombre
                  }
                  :{" "}
                  <strong>
                    {stock.data?.find(
                      (x) =>
                        x.establecimiento_id === local &&
                        x.producto_id === l.producto_id,
                    )?.disponible ?? 0}{" "}
                    disponibles
                  </strong>
                </span>
              ))}
          </div>
        )}
        <div className="total-line emphasis">
          <span>Total a cobrar</span>
          <strong>{money(total)}</strong>
        </div>
        <div className="form-grid">
          <Field label="Medio de pago">
            <SelectId
              value={method}
              onChange={setMethod}
              options={catalogs.metodo_pago}
            />
          </Field>
          <Field
            label="Importe cobrado $"
            hint="Debe coincidir exactamente con el total de venta."
          >
            <input
              required
              type="number"
              min="0.01"
              step="0.01"
              value={amount || decimal(total)}
              onChange={(e) => setAmount(e.target.value)}
            />
          </Field>
        </div>
        <Alert message={stock.error || action.error} />
        <p className="small-copy muted">
          Cobro simulado. Se emitirá un comprobante interno sin validez fiscal.
        </p>
        <div className="form-footer">
          <Submit busy={action.busy}>Cobrar y emitir comprobante</Submit>
        </div>
      </form>
    </Modal>
  );
}
export function SaleReceipt({ id }: { id: number }) {
  const resource = useResource<SaleDetail>("/ventas/" + id);
  const [refund, setRefund] = useState(false);
  if (resource.error) return <Alert message={resource.error} />;
  if (!resource.data) return <Loading />;
  const sale = resource.data;
  return (
    <>
      <div className="section-toolbar no-print">
        <a className="text-link" href="#/ventas">
          ← Volver a ventas
        </a>
        <div className="button-group">
          <button className="button subtle" onClick={() => window.print()}>
            Imprimir comprobante
          </button>
          <button className="button" onClick={() => setRefund(true)}>
            Registrar devolución
          </button>
        </div>
      </div>
      <Card className="receipt">
        <div className="receipt-heading">
          <div>
            <div className="brand receipt-brand">
              ne<span>x</span>o.
            </div>
            <p>Distribución y ventas</p>
          </div>
          <div>
            <span className="eyebrow">COMPROBANTE INTERNO</span>
            <h2>{sale.numero_comprobante}</h2>
            <p>{dateTime(sale.fecha)}</p>
          </div>
        </div>
        <div className="receipt-info">
          <div>
            <small>LOCAL</small>
            <strong>{sale.local}</strong>
          </div>
          <div>
            <small>MEDIO DE PAGO</small>
            <strong>{sale.metodo_pago}</strong>
          </div>
        </div>
        <Table
          rows={sale.detalles}
          columns={[
            { title: "Producto", render: (r) => r.producto },
            { title: "Unidades", render: (r) => r.cantidad },
            {
              title: "Precio unitario",
              className: "numeric",
              render: (r) => money(r.precio_unitario),
            },
            {
              title: "Descuento unitario",
              className: "numeric",
              render: (r) => money(r.descuento_aplicado),
            },
            {
              title: "Subtotal",
              className: "numeric",
              render: (r) => money(r.subtotal),
            },
            { title: "Devueltas", render: (r) => r.devuelta },
          ]}
        />
        <div className="total-line emphasis">
          <span>Total cobrado</span>
          <strong>{money(sale.total)}</strong>
        </div>
        <p className="small-copy muted">
          Documento académico. Sin validez fiscal.
        </p>
      </Card>
      {sale.devoluciones.map((d) => (
        <Card
          key={d.id}
          title={`Devolución ${d.numero_comprobante}`}
          description={`${dateTime(d.fecha)} · ${d.motivo}`}
        >
          <p>{d.detalle}</p>
          <Table
            rows={d.detalles}
            columns={[
              {
                title: "Producto",
                render: (r) =>
                  sale.detalles.find((l) => l.producto_id === r.producto_id)
                    ?.producto,
              },
              { title: "Unidades", render: (r) => r.cantidad },
              {
                title: "Reintegro unitario",
                className: "numeric",
                render: (r) => money(r.importe_unitario),
              },
              {
                title: "Subtotal",
                className: "numeric",
                render: (r) => money(r.importe_unitario * r.cantidad),
              },
            ]}
          />
          <div className="total-line">
            <span>Reintegro · {d.metodo_reintegro}</span>
            <strong>{money(d.total)}</strong>
          </div>
        </Card>
      ))}
      {refund && <RefundForm sale={sale} onClose={() => setRefund(false)} />}
    </>
  );
}
function RefundForm({
  sale,
  onClose,
}: {
  sale: SaleDetail;
  onClose: () => void;
}) {
  const { catalogs } = useData(),
    action = useAction();
  const [quantities, setQuantities] = useState<Record<number, number>>({}),
    [reason, setReason] = useState(0),
    [method, setMethod] = useState(0),
    [note, setNote] = useState(""),
    [apt, setApt] = useState(false);
  const remaining = sale.detalles.filter((x) => x.cantidad > x.devuelta);
  const total = sale.detalles.reduce(
    (sum, l) =>
      sum +
      (quantities[l.producto_id] ?? 0) *
        (l.precio_unitario - l.descuento_aplicado),
    0,
  );
  return (
    <Modal title={"Devolver · " + sale.numero_comprobante} onClose={onClose}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          const details = Object.entries(quantities)
            .filter(([, q]) => q > 0)
            .map(([product, q]) => ({
              producto_id: Number(product),
              cantidad: q,
            }));
          action.run(
            () =>
              post(`/ventas/${sale.id}/devoluciones`, {
                motivo_id: reason,
                metodo_reintegro_id: method,
                detalle: note,
                productos_aptos: apt,
                detalles: details,
              }),
            onClose,
          );
        }}
      >
        <p className="muted">
          Plazo máximo: 30 días desde la venta. Seleccioná las unidades
          inspeccionadas que van a volver al stock.
        </p>
        <Table
          rows={remaining}
          columns={[
            { title: "Producto", render: (r) => r.producto },
            { title: "Pendiente", render: (r) => r.cantidad - r.devuelta },
            {
              title: "A devolver",
              render: (r) => (
                <input
                  aria-label={"Cantidad a devolver de " + r.producto}
                  type="number"
                  min="0"
                  max={r.cantidad - r.devuelta}
                  step="1"
                  value={quantities[r.producto_id] ?? 0}
                  onChange={(e) =>
                    setQuantities((x) => ({
                      ...x,
                      [r.producto_id]: Number(e.target.value),
                    }))
                  }
                />
              ),
            },
          ]}
          empty="Todos los productos de esta venta ya fueron devueltos."
        />
        <div className="form-grid">
          <Field label="Motivo">
            <SelectId
              value={reason}
              onChange={setReason}
              options={catalogs?.motivo ?? []}
            />
          </Field>
          <Field label="Medio de reintegro">
            <SelectId
              value={method}
              onChange={setMethod}
              options={catalogs?.metodo_pago ?? []}
            />
          </Field>
        </div>
        <Field label="Detalle del motivo">
          <textarea
            required
            maxLength={500}
            value={note}
            onChange={(e) => setNote(e.target.value)}
          />
        </Field>
        <label className="check-field">
          <input
            required
            type="checkbox"
            checked={apt}
            onChange={(e) => setApt(e.target.checked)}
          />
          Los productos fueron inspeccionados y están aptos para reventa
        </label>
        <div className="total-line">
          <span>Total a reintegrar</span>
          <strong>{money(total)}</strong>
        </div>
        <Alert message={action.error} />
        <div className="form-footer">
          <Submit busy={action.busy}>Confirmar devolución y reintegro</Submit>
        </div>
      </form>
    </Modal>
  );
}
