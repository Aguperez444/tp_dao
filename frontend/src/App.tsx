import { useEffect, useState } from "react";
import { DataProvider } from "./state";
import { Icon } from "./components/ui";
import Dashboard from "./pages/Dashboard";
import Catalog from "./pages/Catalog";
import Purchases from "./pages/Purchases";
import Logistics from "./pages/Logistics";
import Sales, { SaleReceipt } from "./pages/Sales";
import Inventory from "./pages/Inventory";
import Reports from "./pages/Reports";
const navigation = [
  {
    path: "/",
    label: "Resumen",
    icon: "home",
    title: "Tu operación, en un vistazo.",
    subtitle: "Inventario, distribución y ventas conectados.",
  },
  {
    path: "/catalogo",
    label: "Catálogo",
    icon: "box",
    title: "La base de tu operación.",
    subtitle: "Productos, proveedores y establecimientos.",
  },
  {
    path: "/compras",
    label: "Compras",
    icon: "cart",
    title: "Abastecer para seguir.",
    subtitle: "Compras y recepción de mercadería en el CD.",
  },
  {
    path: "/logistica",
    label: "Reposición y bultos",
    icon: "truck",
    title: "Cada bulto, bajo control.",
    subtitle:
      "Desde la necesidad del local hasta la verificación de su entrega.",
  },
  {
    path: "/ventas",
    label: "Ventas y devoluciones",
    icon: "sale",
    title: "Del stock al comprobante.",
    subtitle: "Ventas verificadas, cobros y devoluciones vinculadas.",
  },
  {
    path: "/inventario",
    label: "Inventario",
    icon: "stock",
    title: "Existencias claras.",
    subtitle: "Stock disponible, reservas y niveles mínimos.",
  },
  {
    path: "/reportes",
    label: "Reportes",
    icon: "chart",
    title: "Los números de tu negocio.",
    subtitle: "Cinco perspectivas para entender las operaciones.",
  },
];
export default function App() {
  const [path, setPath] = useState(window.location.hash.slice(1) || "/");
  useEffect(() => {
    const handler = () => {
      setPath(window.location.hash.slice(1) || "/");
      window.scrollTo(0, 0);
    };
    window.addEventListener("hashchange", handler);
    return () => window.removeEventListener("hashchange", handler);
  }, []);
  const section =
    navigation.find((x) => x.path !== "/" && path.startsWith(x.path)) ??
    navigation[0];
  const receipt = /^\/ventas\/(\d+)$/.exec(path);
  let page = receipt ? (
    <SaleReceipt id={Number(receipt[1])} />
  ) : path === "/" ? (
    <Dashboard />
  ) : path === "/catalogo" ? (
    <Catalog />
  ) : path === "/compras" ? (
    <Purchases />
  ) : path === "/logistica" ? (
    <Logistics />
  ) : path === "/ventas" ? (
    <Sales />
  ) : path === "/inventario" ? (
    <Inventory />
  ) : path === "/reportes" ? (
    <Reports />
  ) : (
    <div className="card">
      <h2>Página inexistente</h2>
      <a href="#/">Volver al resumen</a>
    </div>
  );
  return (
    <DataProvider>
      <aside className="sidebar">
        <a href="#/" className="brand">
          ne<span>x</span>o<span className="brand-dot">.</span>
        </a>
        <p className="brand-sub">DISTRIBUCIÓN Y VENTAS</p>
        <div className="sidebar-section">ESPACIO DE TRABAJO</div>
        <nav>
          {navigation.map((item) => (
            <a
              href={"#" + item.path}
              key={item.path}
              className={section.path === item.path ? "active" : ""}
            >
              <Icon name={item.icon} />
              <span>{item.label}</span>
              {section.path === item.path && <span className="nav-dot" />}
            </a>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <span className="workspace-symbol">40</span>
          <div>
            <strong>Grupo 40</strong>
            <small>DAO · TP integrador 2026</small>
          </div>
        </div>
      </aside>
      <div className="app-shell">
        <header className="topbar">
          <span className="breadcrumb">
            Nexo <span>/</span> {section.label}
          </span>
          <div className="topbar-status">
            <span />
            Entorno académico
          </div>
        </header>
        <main>
          <div className="page-heading">
            <div>
              <div className="eyebrow">
                {receipt ? "COMPROBANTES" : section.label.toLocaleUpperCase()}
              </div>
              <h1>{receipt ? "Detalle de la venta." : section.title}</h1>
              <p>
                {receipt
                  ? "Comprobante original y reintegros asociados."
                  : section.subtitle}
              </p>
            </div>
            <span className="date-chip">
              {new Intl.DateTimeFormat("es-AR", {
                day: "numeric",
                month: "long",
                year: "numeric",
              }).format(new Date())}
            </span>
          </div>
          {page}
        </main>
        <footer className="app-footer">
          <span>Nexo · Centro de distribución a locales</span>
          <span>Tema 3 / Desarrollo de Aplicaciones con Objetos</span>
        </footer>
      </div>
    </DataProvider>
  );
}
