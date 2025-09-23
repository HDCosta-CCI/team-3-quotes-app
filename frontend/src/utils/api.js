const URL = "http://localhost:8000/";

export async function login({ email, password }) {
  try {
    const response = await fetch(`${URL}auth/sign-in`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const result = await response.json();
    console.log(result);

    if (!response.ok) {
      return {
        success: false,
        message: result.detail || "Login failed",
        data: null,
      };
    }
    if (result.data?.access_token) {
      localStorage.setItem("access_token", result.data.access_token);
      localStorage.setItem("refresh_token", result.data.refresh_token);
    }

    return { success: true, data: result.data };
  } catch (err) {
    return { success: false, message: err.message || "Unknown error", data: null };
  }
}