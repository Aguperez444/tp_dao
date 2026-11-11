import { useEffect, useRef, type ReactNode } from "react";
import { useData } from "../state";
import { decimal } from "../api";
import type { CartLine, Product } from "../types";

export function Icon({ name, size = 20 }: { name: string; size?: number }) {
  const paths: Record<string, ReactNode> = {
    home: (
      <>
        <path d="M3 10 12 3l9 7v10H3Z" />
        <path d="M9 20v-7h6v7" />
      </>
    ),
    box: (
      <>
        <path d="m3 7 9-4 9 4-9 4Z" />
        <path d="M3 7v10l9 4 9-4V7M12 11v10M7 5l10 4" />
      </>
    ),
    truck: (
      <>
        <path d="M3 5h11v12H3ZM14 9h4l3 4v4h-7" />
        <circle cx="7" cy="18" r="2" />
        <circle cx="18" cy="18" r="2" />
      </>
    ),
    sale: (
      <>
        <path d="M5 3h14v18l-3-2-4 2-4-2-3 2Z" />
        <path d="M8 8h8M8 12h8M8 16h4" />
      </>
    ),
    stock: (
      <>
        <path d="M3 4h18v16H3ZM3 10h18M9 4v16M15 4v16" />
      </>
    ),
    chart: (
      <>
        <path d="M4 3v18h17M8 16v-4M13 16V7M18 16V4" />
      </>
    ),
    cart: (
      <>
        <path d="M3 3h2l3 12h11l2-8H6" />
        <circle cx="9" cy="20" r="1" />
        <circle cx="18" cy="20" r="1" />
      </>
    ),
    arrow: <path d="M4 12h16m-6-6 6 6-6 6" />,
    plus: <path d="M12 4v16M4 12h16" />,
    check: <path d="m5 12 4 4L19 6" />,
    close: <path d="m6 6 12 12M6 18 18 6" />,
    search: (
      <>
        <circle cx="10" cy="10" r="6" />
        <path d="m15 15 6 6" />
      </>
    ),
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.65"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {paths[name] || paths.box}
    </svg>
  );
}
export function Card({
  title,
  description,
  children,
  action,
  className = "",
}: {
  title?: string;
  description?: string;
  children: ReactNode;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <section className={"card " + className}>
      {title && (
        <div className="card-heading">
          <div>
            <h2>{title}</h2>
            {description && <p>{description}</p>}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  );
}
export function Empty({
  children = "Todavía no hay registros para mostrar.",
}: {
  children?: ReactNode;
}) {
  return (
    <div className="empty">
      <Icon name="box" size={30} />
      <p>{children}</p>
    </div>
  );
}
export function Alert({ message }: { message?: string }) {
  return message ? (
    <div className="alert" role="alert">
      {message}
    </div>
  ) : null;
}
export function Loading() {
  return (
    <div className="loading" role="status">
      Cargando operaciones…
    </div>
  );
}
export function Badge({ value }: { value: string }) {
  const danger = /rechaz|violado|no coincide|inactivo/i.test(value),
    good = /verificado|completada|recibida|activo|intacto/i.test(value);
  return (
    <span
      className={"badge " + (danger ? "danger" : good ? "good" : "neutral")}
    >
      {value}
    </span>
  );
}
export function Submit({
  busy,
  children = "Guardar",
}: {
  busy: boolean;
  children?: ReactNode;
}) {
  return (
    <button type="submit" className="button" disabled={busy}>
      {busy ? "Guardando…" : children}
      {!busy && <Icon name="arrow" size={16} />}
    </button>
  );
}
export function Field({
  label,
  children,
  hint,
}: {
  label: string;
  children: ReactNode;
  hint?: string;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
      {hint && <small>{hint}</small>}
    </label>
  );
}
export function SelectId({
  value,
  onChange,
  options,
  placeholder = "Seleccionar…",
  required = true,
}: {
  value: number | string;
  onChange: (id: number) => void;
  options: { id: number; nombre: string }[];
  placeholder?: string;
  required?: boolean;
}) {
  return (
    <select
      required={required}
      value={value || ""}
      onChange={(e) => onChange(Number(e.target.value))}
    >
      <option value="">{placeholder}</option>
      {options.map((x) => (
        <option key={x.id} value={x.id}>
          {x.nombre}
        </option>
      ))}
    </select>
  );
}
export type Column<T> = {
  title: string;
  render: (row: T) => ReactNode;
  className?: string;
};
export function Table<T>({
  rows,
  columns,
  empty,
}: {
  rows: T[];
  columns: Column<T>[];
  empty?: string;
}) {
  return rows.length ? (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((c, i) => (
              <th className={c.className} key={i}>
                {c.title}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i}>
              {columns.map((c, j) => (
                <td className={c.className} key={j}>
                  {c.render(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  ) : (
    <Empty>{empty}</Empty>
  );
}
export function Modal({
  title,
  children,
  onClose,
}: {
  title: string;
  children: ReactNode;
  onClose: () => void;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    ref.current?.showModal();
  }, []);
  return (
    <dialog
      ref={ref}
      onCancel={(e) => {
        e.preventDefault();
        onClose();
      }}
    >
      <div className="modal-heading">
        <h2>{title}</h2>
        <button className="icon-button" aria-label="Cerrar" onClick={onClose}>
          <Icon name="close" />
        </button>
      </div>
      {children}
    </dialog>
  );
}
export function LineEditor({
  value,
  onChange,
  cost = false,
  products,
}: {
  value: CartLine[];
  onChange: (v: CartLine[]) => void;
  cost?: boolean;
  products?: Product[];
}) {
  const { catalogs } = useData();
  const options =
    products ?? catalogs?.producto.filter((p) => p.esta_activo) ?? [];
  function update(index: number, changes: Partial<CartLine>) {
    onChange(value.map((x, i) => (i === index ? { ...x, ...changes } : x)));
  }
  return (
    <div className="line-editor">
      {value.map((line, index) => (
        <div className={"cart-line " + (cost ? "with-cost" : "")} key={index}>
          <Field label="Producto">
            <SelectId
              value={line.producto_id}
              options={options}
              onChange={(id) => {
                const p = options.find((x) => x.id === id);
                update(index, {
                  producto_id: id,
                  ...(cost && p ? { costo: decimal(p.costo_referencia) } : {}),
                });
              }}
            />
          </Field>
          <Field label="Unidades">
            <input
              aria-label={`Unidades de la línea ${index + 1}`}
              type="number"
              min="1"
              max="1000000"
              step="1"
              required
              value={line.cantidad}
              onChange={(e) =>
                update(index, { cantidad: Number(e.target.value) })
              }
            />
          </Field>
          {cost && (
            <Field label="Costo unitario $">
              <input
                type="number"
                required
                min="0"
                step="0.01"
                value={line.costo ?? ""}
                onChange={(e) => update(index, { costo: e.target.value })}
              />
            </Field>
          )}
          <button
            type="button"
            className="icon-button remove-line"
            disabled={value.length === 1}
            aria-label={`Quitar línea ${index + 1}`}
            onClick={() => onChange(value.filter((_, i) => i !== index))}
          >
            <Icon name="close" size={17} />
          </button>
        </div>
      ))}
      <button
        type="button"
        className="button subtle small"
        onClick={() =>
          onChange([
            ...value,
            { producto_id: 0, cantidad: 1, ...(cost ? { costo: "0" } : {}) },
          ])
        }
      >
        <Icon name="plus" size={16} />
        Agregar producto
      </button>
    </div>
  );
}
