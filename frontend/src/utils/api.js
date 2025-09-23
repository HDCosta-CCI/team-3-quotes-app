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


export async function signup({ first_name, last_name, email, password }) {
  try {
    const response = await fetch(`${URL}auth/sign-up`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ first_name, last_name, email, password }),
    });
    const result = await response.json();
    console.log(result);

    if (!response.ok) {
      return {
        success: false,
        message: result.detail || "Sign-up failed",
        data: null,
      };
    }
    return { success: true, data: result.data };
  } catch (err) {
    return { success: false, message: err.message || "Unknown error", data: null };
  }
}


export async function fetchQuotes() {
  try {
    const response = await fetch(URL + "quotes", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${localStorage.getItem("access_token")}`, 
      },
    });

    if (!response.ok) {
      throw new Error("Failed to fetch quotes");
    }
    const result = await response.json();
    console.log("Quotes:", result);
    return result.data;
  } catch (err) {
    console.error(err);
  }
}

