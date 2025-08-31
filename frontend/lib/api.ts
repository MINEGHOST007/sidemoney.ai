export const API_BASE =
  (typeof window !== "undefined" && (process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000")) ||
  "http://localhost:8000"

export type HttpMethod = "GET" | "POST" | "PUT" | "DELETE"

export function getAccessToken() {
  if (typeof window === "undefined") return null
  try {
    return localStorage.getItem("access_token")
  } catch {
    return null
  }
}

export async function apiFetch<T>(path: string, options: RequestInit = {}, requireAuth = true): Promise<T> {
  const token = getAccessToken()
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  }
  if (requireAuth && token) {
    headers["Authorization"] = `Bearer ${token}`
  }
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  })
  if (!res.ok) {
    const text = await res.text().catch(() => "")
    let detail = text
    try {
      const j = JSON.parse(text)
      detail = j?.detail || text
    } catch {}
    throw new Error(detail || `Request failed: ${res.status}`)
  }
  if (res.status === 204) return undefined as unknown as T
  return (await res.json()) as T
}

export const swrFetcher = async (key: string) => apiFetch(key)

// Specialized helpers
export function apiGet<T>(path: string, requireAuth = true) {
  return apiFetch<T>(path, { method: "GET" }, requireAuth)
}
export function apiPost<T>(path: string, body?: any, requireAuth = true) {
  return apiFetch<T>(
    path,
    {
      method: "POST",
      body: body instanceof FormData ? body : JSON.stringify(body),
      headers: body instanceof FormData ? {} : { "Content-Type": "application/json" },
    },
    requireAuth,
  )
}
export function apiPut<T>(path: string, body?: any, requireAuth = true) {
  return apiFetch<T>(path, { method: "PUT", body: JSON.stringify(body) }, requireAuth)
}
export function apiDelete<T>(path: string, requireAuth = true) {
  return apiFetch<T>(path, { method: "DELETE" }, requireAuth)
}
