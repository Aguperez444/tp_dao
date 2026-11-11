import { useState } from "react";
import { post, dateTime } from "../api";
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
  Empty,
} from "../components/ui";
import type { Order, Delivery, Package, CartLine } from "../types";
type Dialog =
  | { kind: "order" }
  | { kind: "delivery"; order: Order }
  | { kind: "package"; order: Order; delivery: Delivery }
  | {
      kind: "transition";
      package: Package;
      delivery: Delivery;
      action: string;
    };
export default function Logistics() {
  const { catalogs } = useData(),
    resource = useResource<Order[]>("/reposiciones");
  const [dialog, setDialog] = useState<Dialog | null>(null);
  if (!catalogs) return <Loading />;
  const product = (id: number) =>
    catalogs.producto.find((x) => x.id === id)?.nombre ?? `Producto #${id}`;
  return (
    <>
      <Alert message={resource.error} />
      <div className="section-toolbar">
        <div className="quiet-note compact">
          <Icon name="truck" />
          <span>
            Consolidá las necesidades de un local en una orden y distribuí su
            contenido en uno o más remitos.
          </span>
        </div>
        <button className="button" onClick={() => setDialog({ kind: "order" })}>
          <Icon name="plus" size={17} />
          Nueva reposición
        </button>
      </div>
      {resource.data?.length === 0 && (
        <Card>
          <Empty>
            No hay órdenes de reposición. Creá la primera para abastecer un
            local.
          </Empty>
        </Card>
      )}
      {resource.data?.map((order) => (
        <Card
          key={order.id}
          title={`Orden #${order.id} · ${order.destino}`}
          description={`${order.origen} → ${order.destino} · ${dateTime(order.fecha)}`}
          action={<Badge value={order.estado} />}
        >
          <Table
            rows={order.detalles}
            columns={[
              { title: "Producto", render: (r) => product(r.producto_id) },
              { title: "Solicitado", render: (r) => r.cantidad },
              { title: "Asignado a bultos", render: (r) => r.asignada },
              {
                title: "Pendiente de armar",
                render: (r) => <strong>{r.cantidad - r.asignada}</strong>,
              },
            ]}
          />
          <div className="delivery-list">
            {order.remitos.map((delivery) => (
              <div className="delivery" key={delivery.id}>
                <div className="delivery-heading">
                  <div>
                    <span className="eyebrow">REMITO</span>
                    <h3>{delivery.numero_remito}</h3>
                  </div>
                  <Badge value={delivery.estado} />
                  {delivery.estado === "Pendiente" && (
                    <button
                      className="button subtle small"
                      onClick={() =>
                        setDialog({ kind: "package", order, delivery })
                      }
                    >
                      <Icon name="plus" size={15} />
                      Preparar bulto
                    </button>
                  )}
                </div>
                {delivery.bultos.length === 0 && (
                  <p className="muted small-copy">
                    Este remito todavía no tiene bultos.
                  </p>
                )}
                <div className="packages">
                  {delivery.bultos.map((pack) => (
                    <div className="package" key={pack.id}>
                      <div className="package-heading">
                        <span className="package-icon">
                          <Icon name="box" />
                        </span>
                        <strong>Bulto #{pack.id}</strong>
                        <Badge value={pack.estado} />
                      </div>
                      <ul className="package-items">
                        {pack.detalles.map((l) => (
                          <li key={l.producto_id}>
                            <span>{product(l.producto_id)}</span>
                            <strong>× {l.cantidad}</strong>
                          </li>
                        ))}
                      </ul>
                      <p className="small-copy muted">
                        Precinto:{" "}
                        <strong>{pack.codigo_precinto ?? "Pendiente"}</strong> ·{" "}
                        {pack.estado_precinto}
                      </p>
                      {(
                        {
                          Preparado: "precintar",
                          Precintado: "despachar",
                          "En tránsito": "recibir",
                          Recibido: "inspeccionar",
                        } as Record<string, string>
                      )[pack.estado] && (
                        <button
                          className="button small"
                          onClick={() =>
                            setDialog({
                              kind: "transition",
                              package: pack,
                              delivery,
                              action: (
                                {
                                  Preparado: "precintar",
                                  Precintado: "despachar",
                                  "En tránsito": "recibir",
                                  Recibido: "inspeccionar",
                                } as Record<string, string>
                              )[pack.estado],
                            })
                          }
                        >
                          {
                            (
                              {
                                Preparado: "Colocar precinto",
                                Precintado: "Registrar despacho",
                                "En tránsito": "Registrar recepción",
                                Recibido: "Inspeccionar recepción",
                              } as Record<string, string>
                            )[pack.estado]
                          }
                          <Icon name="arrow" size={14} />
                        </button>
                      )}
                      <details className="history">
                        <summary>
                          Ver trazabilidad · {pack.historial.length} eventos
                        </summary>
                        <ol>
                          {pack.historial.map((ev) => (
                            <li key={ev.id}>
                              <strong>{ev.estado}</strong>
                              <span>
                                {dateTime(ev.fecha)} · {ev.responsable}
                              </span>
                              <small>{ev.observacion}</small>
                            </li>
                          ))}
                        </ol>
                      </details>
                    </div>
                  ))}
                </div>
                {delivery.estado === "Rechazado" && (
                  <div className="quiet-note warning">
                    Remito rechazado: ningún bulto de este remito habilita stock
                    vendible. La mercadería queda en cuarentena.
                  </div>
                )}
              </div>
            ))}
          </div>
          {order.detalles.some((x) => x.asignada < x.cantidad) &&
            !order.remitos.some((r) => r.estado === "Pendiente") && (
              <button
                className="button subtle small"
                onClick={() => setDialog({ kind: "delivery", order })}
              >
                <Icon name="plus" size={15} />
                Generar remito
              </button>
            )}
        </Card>
      ))}
      {dialog && (
        <LogisticsDialog dialog={dialog} onClose={() => setDialog(null)} />
      )}
    </>
  );
}
function LogisticsDialog({
  dialog,
  onClose,
}: {
  dialog: Dialog;
  onClose: () => void;
}) {
  const { catalogs } = useData(),
    action = useAction();
  const [local, setLocal] = useState(0),
    [cd, setCd] = useState(
      catalogs?.establecimiento.find((x) => x.es_central)?.id ?? 0,
    ),
    [number, setNumber] = useState(""),
    [responsible, setResponsible] = useState(""),
    [seal, setSeal] = useState(""),
    [observedDelivery, setObservedDelivery] = useState(""),
    [intact, setIntact] = useState(false),
    [conforming, setConforming] = useState(false),
    [note, setNote] = useState(""),
    [lines, setLines] = useState<CartLine[]>([{ producto_id: 0, cantidad: 1 }]);
  const titles = {
    order: "Consolidar necesidades del local",
    delivery: "Generar remito de despacho",
    package: "Preparar y reservar un bulto",
    transition:
      dialog.kind === "transition"
        ? (
            {
              precintar: "Colocar precinto",
              despachar: "Registrar despacho",
              recibir: "Registrar recepción física",
              inspeccionar: "Inspeccionar remito y bulto",
            } as Record<string, string>
          )[dialog.action]
        : "",
  };
  const validInspection =
    dialog.kind === "transition" &&
    intact &&
    conforming &&
    seal.trim().toUpperCase() === dialog.package.codigo_precinto &&
    observedDelivery.trim().toUpperCase() === dialog.delivery.numero_remito;
  async function submit() {
    if (dialog.kind === "order")
      return post("/reposiciones", {
        establecimiento_solicitante_id: local,
        establecimiento_proveedor_id: cd,
        detalles: lines,
      });
    if (dialog.kind === "delivery")
      return post(`/reposiciones/${dialog.order.id}/remitos`, {
        numero_remito: number,
      });
    if (dialog.kind === "package")
      return post(`/remitos/${dialog.delivery.id}/bultos`, {
        responsable: responsible,
        detalles: lines,
      });
    return post(`/bultos/${dialog.package.id}/${dialog.action}`, {
      responsable: responsible,
      codigo_precinto: seal,
      numero_remito: observedDelivery,
      precinto_intacto: intact,
      contenido_conforme: conforming,
      observacion: note,
    });
  }
  return (
    <Modal title={titles[dialog.kind]} onClose={onClose}>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          action.run(submit, onClose);
        }}
      >
        {dialog.kind === "order" && (
          <>
            <div className="form-grid">
              <Field label="Origen · centro de distribución">
                <SelectId
                  value={cd}
                  onChange={setCd}
                  options={catalogs!.establecimiento.filter(
                    (x) => x.es_central,
                  )}
                />
              </Field>
              <Field label="Destino · local solicitante">
                <SelectId
                  value={local}
                  onChange={setLocal}
                  options={catalogs!.establecimiento.filter(
                    (x) => !x.es_central,
                  )}
                />
              </Field>
            </div>
            <p className="small-copy muted">
              Cargá aquí las cantidades totales que necesita ese local, con una
              sola línea por producto.
            </p>
            <LineEditor value={lines} onChange={setLines} />
          </>
        )}
        {dialog.kind === "delivery" && (
          <>
            <p className="muted">
              Orden #{dialog.order.id} · {dialog.order.destino}
            </p>
            <Field label="Número único de remito">
              <input
                required
                maxLength={50}
                value={number}
                onChange={(e) => setNumber(e.target.value)}
                placeholder="Ej. R-0001"
              />
            </Field>
          </>
        )}
        {dialog.kind === "package" && (
          <>
            <p className="muted">
              {dialog.delivery.numero_remito} → {dialog.order.destino}
            </p>
            <Field label="Responsable">
              <input
                required
                maxLength={150}
                value={responsible}
                onChange={(e) => setResponsible(e.target.value)}
              />
            </Field>
            <LineEditor
              value={lines}
              onChange={setLines}
              products={catalogs!.producto.filter(
                (p) =>
                  p.esta_activo &&
                  dialog.order.detalles.some(
                    (d) => d.producto_id === p.id && d.asignada < d.cantidad,
                  ),
              )}
            />
            <p className="quiet-note">
              Preparar reserva las unidades en el CD. El stock físico se
              descuenta al despachar.
            </p>
          </>
        )}
        {dialog.kind === "transition" && (
          <>
            <p className="muted">
              Bulto #{dialog.package.id} · {dialog.delivery.numero_remito}
            </p>
            <Field label="Responsable">
              <input
                required
                maxLength={150}
                value={responsible}
                onChange={(e) => setResponsible(e.target.value)}
              />
            </Field>
            {["precintar", "inspeccionar"].includes(dialog.action) && (
              <Field
                label={
                  dialog.action === "precintar"
                    ? "Código único de precinto"
                    : "Código de precinto observado"
                }
              >
                <input
                  required
                  maxLength={60}
                  value={seal}
                  onChange={(e) => setSeal(e.target.value)}
                />
              </Field>
            )}
            {dialog.action === "inspeccionar" && (
              <>
                <Field label="Número de remito observado">
                  <input
                    required
                    maxLength={50}
                    value={observedDelivery}
                    onChange={(e) => setObservedDelivery(e.target.value)}
                  />
                </Field>
                <label className="check-field">
                  <input
                    type="checkbox"
                    checked={intact}
                    onChange={(e) => setIntact(e.target.checked)}
                  />
                  El precinto está intacto
                </label>
                <label className="check-field">
                  <input
                    type="checkbox"
                    checked={conforming}
                    onChange={(e) => setConforming(e.target.checked)}
                  />
                  Contenido y documentación conformes
                </label>
                <div
                  className={"quiet-note " + (validInspection ? "" : "warning")}
                >
                  {validInspection
                    ? "La inspección es conforme. El stock se habilitará cuando todos los bultos del remito estén verificados."
                    : "Si hay un incumplimiento, se registrará el rechazo y se bloqueará el stock de este remito."}
                </div>
              </>
            )}
            {dialog.action === "recibir" && (
              <p className="quiet-note">
                Esta operación registra la recepción física. La verificación se
                realiza en el siguiente paso.
              </p>
            )}
            <Field
              label={
                dialog.action === "inspeccionar" && !validInspection
                  ? "Motivo del rechazo (obligatorio)"
                  : "Observación (opcional)"
              }
            >
              <textarea
                required={dialog.action === "inspeccionar" && !validInspection}
                maxLength={500}
                value={note}
                onChange={(e) => setNote(e.target.value)}
              />
            </Field>
          </>
        )}
        <Alert message={action.error} />
        <div className="form-footer">
          <button type="button" className="button subtle" onClick={onClose}>
            Cancelar
          </button>
          <Submit busy={action.busy}>
            {dialog.kind === "transition" && dialog.action === "inspeccionar"
              ? validInspection
                ? "Verificar recepción"
                : "Registrar rechazo"
              : "Confirmar"}
          </Submit>
        </div>
      </form>
    </Modal>
  );
}
