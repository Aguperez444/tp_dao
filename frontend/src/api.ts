export async function api<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch("/api" + path, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    let message = "No se pudo completar la operación.";
    if (typeof data?.detail === "string") message = data.detail;
    else if (Array.isArray(data?.detail))
      message = data.detail
        .map(
          (x: { loc: (string | number)[]; msg: string }) =>
            `${x.loc.slice(1).join(" → ")}: ${x.msg}`,
        )
        .join(". ");
    throw new Error(message);
  }
  return data as T;
}
export const post = <T>(path: string, data: unknown = {}) =>
  api<T>(path, { method: "POST", body: JSON.stringify(data) });
export const put = <T>(path: string, data: unknown) =>
  api<T>(path, { method: "PUT", body: JSON.stringify(data) });
export function money(cents: number) {
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    maximumFractionDigits: 2,
  }).format(cents / 100);
}
export function decimal(cents: number) {
  return (cents / 100).toFixed(2);
}
export function dateTime(value: string) {
  return new Intl.DateTimeFormat("es-AR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(new Date(value));
}
export const todayUTC = () => new Date().toISOString().slice(0, 10);
