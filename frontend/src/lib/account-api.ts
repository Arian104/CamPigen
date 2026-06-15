const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  (typeof window !== "undefined"
    ? window.localStorage.getItem("platform_api_base") || "http://127.0.0.1:8000/api"
    : "http://127.0.0.1:8000/api");

function getStoredToken() {
  if (typeof window === "undefined") return "";

  const possibleKeys = [
    "platform_access_token",
    "access",
    "access_token",
    "accessToken",
    "token",
    "auth_token",
    "jwt",
  ];

  for (const key of possibleKeys) {
    const value = window.localStorage.getItem(key);
    if (value) return value;
  }

  return "";
}

function authHeaders() {
  const token = getStoredToken();

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}

export async function uploadAccountAvatar(file: File) {
  const formData = new FormData();
  formData.append("avatar", file);

  const response = await fetch(`${API_BASE.replace(/\/$/, "")}/v1/accounts/me/avatar/`, {
    method: "POST",
    headers: authHeaders(),
    body: formData,
  });

  const body = await response.json().catch(() => null);

  return {
    ok: response.ok,
    status: response.status,
    body,
  };
}

export async function removeAccountAvatar() {
  const response = await fetch(`${API_BASE.replace(/\/$/, "")}/v1/accounts/me/avatar/remove/`, {
    method: "DELETE",
    headers: authHeaders(),
  });

  const body = await response.json().catch(() => null);

  return {
    ok: response.ok,
    status: response.status,
    body,
  };
}
