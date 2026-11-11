import { post, money, dateTime } from "../api";
import { useData, useResource, useAction } from "../state";
import { Card, Icon, Badge, Table, Alert, Loading } from "../components/ui";
import type { Order, Sale, Stock } from "../types";
export default function Dashboard() {
  const { catalogs } = useData(),
    sales = useResource<Sale[]>("/ventas"),
    orders = useResource<Order[]>("/reposiciones"),
    stock = useResource<Stock[]>("/inventario");
  const action = useAction();
  if (!catalogs) return <Loading />;
  const shipped =
    orders.data
      ?.flatMap((o) => o.remitos.flatMap((r) => r.bultos))
      .filter((b) => b.estado === "En tránsito").length ?? 0;
  const alerts = stock.data?.filter((x) => x.faltante > 0).length ?? 0;
  const values = [
    {
      title: "Ventas registradas",
      value: sales.data?.length ?? 0,
      icon: "sale",
      caption: "Comprobantes emitidos",
    },
    {
      title: "Locales conectados",
      value: catalogs.establecimiento.filter((x) => !x.es_central).length,
      icon: "home",
      caption: "Abastecidos desde el CD",
    },
    {
      title: "Bultos en tránsito",
      value: shipped,
      icon: "truck",
      caption: "Pendientes de recepción",
    },
    {
      title: "Alertas de existencia",
      value: alerts,
      icon: "stock",
      caption: "Por debajo del mínimo",
    },
  ];
  return (
    <>
      <Alert
        message={sales.error || orders.error || stock.error || action.error}
      />
      {catalogs.establecimiento.length === 0 && (
        <div className="welcome">
          <div>
            <span className="eyebrow">TU PRIMER RECORRIDO</span>
            <h2>Todo comienza en el centro de distribución.</h2>
            <p>
              Creá los establecimientos y productos en Catálogo, o explorá un
              circuito completo con datos ficticios.
            </p>
          </div>
          <button
            className="button"
            disabled={action.busy}
            onClick={() => action.run(() => post("/demo"))}
          >
            Cargar demostración <Icon name="arrow" size={17} />
          </button>
        </div>
      )}
      <div className="metrics">
        {values.map((x) => (
          <div className="metric" key={x.title}>
            <div className="metric-top">
              <span>{x.title}</span>
              <Icon name={x.icon} />
            </div>
            <strong>{x.value}</strong>
            <small>{x.caption}</small>
          </div>
        ))}
      </div>
      <div className="dashboard-grid">
        <Card
          title="Del origen al mostrador"
          description="Una cadena de abastecimiento con trazabilidad."
        >
          <div className="journey">
            {[
              ["cart", "Compra", "Ingreso al CD"],
              ["box", "Preparación", "Reserva y precinto"],
              ["truck", "Traslado", "Despacho y recepción"],
              ["check", "Verificación", "Stock habilitado"],
            ].map(([icon, title, sub], i) => (
              <div className="journey-step" key={title}>
                <span className="journey-number">0{i + 1}</span>
                <span className="journey-icon">
                  <Icon name={icon} size={26} />
                </span>
                <strong>{title}</strong>
                <small>{sub}</small>
              </div>
            ))}
          </div>
          <div className="quiet-note">
            <Icon name="check" size={18} />
            <span>
              Recibir un bulto no habilita su venta: primero se verifica el
              remito y su contenido.
            </span>
          </div>
        </Card>
        <Card title="Accesos rápidos">
          <div className="quick-links">
            {[
              [
                "/compras",
                "cart",
                "Registrar una compra",
                "Abastecer el centro de distribución",
              ],
              [
                "/logistica",
                "truck",
                "Gestionar reposición",
                "Preparar y seguir los bultos",
              ],
              [
                "/ventas",
                "sale",
                "Registrar una venta",
                "Cobrar y emitir comprobante",
              ],
            ].map(([href, icon, title, sub]) => (
              <a href={"#" + href} key={href}>
                <Icon name={icon} />
                <span>
                  <strong>{title}</strong>
                  <small>{sub}</small>
                </span>
                <Icon name="arrow" size={17} />
              </a>
            ))}
          </div>
        </Card>
      </div>
      <Card
        title="Últimas ventas"
        description="Operaciones recientes de tus locales."
        action={
          <a className="text-link" href="#/ventas">
            Ver todas →
          </a>
        }
      >
        <Table
          rows={sales.data?.slice(0, 6) ?? []}
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
            {
              title: "Medio de pago",
              render: (r) => <Badge value={r.metodo_pago} />,
            },
            {
              title: "Importe",
              className: "numeric",
              render: (r) => <strong>{money(r.total)}</strong>,
            },
          ]}
        />
      </Card>
    </>
  );
}
