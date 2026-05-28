const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`${res.status} ${path}: ${body}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  health: () => request<{ status: string }>("/health"),

  majors: () =>
    request<
      { id: string; name: string; department: string; total_units: number }[]
    >("/majors"),

  parseTranscript: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<unknown>("/parse-transcript", { method: "POST", body: form });
  },

  parseDar: (file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<unknown>("/parse-dar", { method: "POST", body: form });
  },

  audit: (body: unknown) =>
    request<unknown>("/audit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),

  generatePlan: (body: unknown) =>
    request<unknown>("/generate-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
};
