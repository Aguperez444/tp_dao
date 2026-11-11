import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { api } from "./api";
import type { Catalogs } from "./types";

const Context = createContext<{
  catalogs: Catalogs | null;
  version: number;
  refresh: () => void;
  notify: (message: string) => void;
}>({ catalogs: null, version: 0, refresh: () => {}, notify: () => {} });
export function DataProvider({ children }: { children: ReactNode }) {
  const [catalogs, setCatalogs] = useState<Catalogs | null>(null),
    [version, setVersion] = useState(0),
    [message, setMessage] = useState(""),
    [error, setError] = useState("");
  const refresh = useCallback(() => setVersion((v) => v + 1), []);
  useEffect(() => {
    let active = true;
    api<Catalogs>("/catalogos")
      .then((x) => {
        if (active) {
          setCatalogs(x);
          setError("");
        }
      })
      .catch((e) => {
        if (active) setError(e.message);
      });
    return () => {
      active = false;
    };
  }, [version]);
  useEffect(() => {
    if (!message) return;
    const id = setTimeout(() => setMessage(""), 5000);
    return () => clearTimeout(id);
  }, [message]);
  return (
    <Context.Provider
      value={{ catalogs, version, refresh, notify: setMessage }}
    >
      {error && (
        <div className="connection-error" role="alert">
          No se pudo conectar con el servidor. {error}{" "}
          <button onClick={refresh}>Reintentar</button>
        </div>
      )}
      {children}
      {message && (
        <div className="toast" role="status">
          ✓ {message}
          <button aria-label="Cerrar aviso" onClick={() => setMessage("")}>
            ×
          </button>
        </div>
      )}
    </Context.Provider>
  );
}
export const useData = () => useContext(Context);
export function useResource<T>(path: string) {
  const { version } = useData();
  const [data, setData] = useState<T | null>(null),
    [loading, setLoading] = useState(true),
    [error, setError] = useState("");
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    api<T>(path)
      .then((x) => {
        if (active) setData(x);
      })
      .catch((e) => {
        if (active) setError(e.message);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [path, version]);
  return { data, loading, error };
}
export function useAction() {
  const { refresh, notify } = useData();
  const [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  async function run<T>(
    action: () => Promise<T>,
    success?: (result: T) => void,
  ) {
    if (busy) return;
    setBusy(true);
    setError("");
    try {
      const result = await action();
      refresh();
      notify("Operación registrada correctamente.");
      success?.(result);
      return result;
    } catch (e) {
      setError(
        e instanceof Error ? e.message : "No se pudo guardar la operación.",
      );
    } finally {
      setBusy(false);
    }
  }
  return { busy, error, run, clear: () => setError("") };
}
