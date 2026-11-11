export type Named = { id: number; nombre: string };
export type Product = Named & {
  codigo: string;
  detalle: string;
  categoria_id: number;
  precio: number;
  costo_referencia: number;
  esta_activo: boolean;
};
export type Establishment = Named & {
  es_central: boolean;
  domicilio_id: number;
};
export type Supplier = Named & { CUIT: string; esta_activo: boolean };
export type Catalogs = {
  producto: Product[];
  establecimiento: Establishment[];
  proveedor: Supplier[];
  categoria: Named[];
  provincia: Named[];
  ciudad: (Named & { provincia_id: number })[];
  domicilio: { id: number; calle: string; altura: string; ciudad_id: number }[];
  motivo: Named[];
  metodo_pago: Named[];
  estado_compra: Named[];
  estado_reposicion: Named[];
  estado_remito: Named[];
  estado_precinto: Named[];
  estado_bulto: Named[];
};
export type CartLine = {
  producto_id: number;
  cantidad: number;
  costo?: string;
};
export type Purchase = {
  id: number;
  proveedor: string;
  proveedor_id: number;
  fecha: string;
  estado: string;
  total: number;
  detalles: (CartLine & { costo: number })[];
};
export type PackageEvent = {
  id: number;
  estado: string;
  fecha: string;
  responsable: string;
  observacion: string;
};
export type Package = {
  id: number;
  remito_id: number;
  estado: string;
  estado_precinto: string;
  codigo_precinto: string | null;
  detalles: CartLine[];
  historial: PackageEvent[];
};
export type Delivery = {
  id: number;
  numero_remito: string;
  estado: string;
  fecha_emision: string;
  bultos: Package[];
};
export type Order = {
  id: number;
  origen: string;
  destino: string;
  estado: string;
  fecha: string;
  detalles: (CartLine & { asignada: number })[];
  remitos: Delivery[];
};
export type SaleLine = CartLine & {
  id: number;
  producto: string;
  precio_unitario: number;
  descuento_aplicado: number;
  costo_unitario: number;
  devuelta: number;
  subtotal: number;
};
export type Refund = {
  id: number;
  fecha: string;
  numero_comprobante: string;
  motivo: string;
  metodo_reintegro: string;
  detalle: string;
  total: number;
  detalles: (CartLine & { importe_unitario: number })[];
};
export type Sale = {
  id: number;
  local: string;
  fecha: string;
  total: number;
  metodo_pago: string;
  numero_comprobante: string;
  reintegrado: number;
};
export type SaleDetail = Sale & {
  detalles: SaleLine[];
  devoluciones: Refund[];
};
export type Stock = {
  establecimiento_id: number;
  establecimiento: string;
  producto_id: number;
  producto: string;
  codigo: string;
  almacenado_total: number;
  reservado: number;
  disponible: number;
  minimo_permitido: number;
  faltante: number;
  valorizacion: number;
};
export type ReportRow = Record<string, string | number | null>;
export type Reports = {
  desde: string;
  hasta: string;
  establecimiento_id: number | null;
  ventas: ReportRow[];
  productos: ReportRow[];
  existencias: ReportRow[];
  rechazos: ReportRow[];
  transito: ReportRow[];
};
