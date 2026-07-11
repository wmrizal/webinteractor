const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export class ApiClientError extends Error {
  status: number;
  code: string;

  constructor(message: string, status: number, code = "request_failed") {
    super(message);
    this.name = "ApiClientError";
    this.status = status;
    this.code = code;
  }
}

export type RequestOptions = Omit<RequestInit, "body"> & {
  body?: unknown;
};

async function parseResponse(response: Response) {
  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) {
    return response.json();
  }

  return response.text();
}

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
  });

  const payload = await parseResponse(response);
  if (!response.ok) {
    const code = typeof payload === "object" && payload && "code" in payload ? String(payload.code) : "request_failed";
    const message = typeof payload === "object" && payload && "message" in payload ? String(payload.message) : `Request failed with status ${response.status}`;
    throw new ApiClientError(message, response.status, code);
  }

  return payload as T;
}
