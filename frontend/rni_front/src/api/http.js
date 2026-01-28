import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000/",
  timeout: 5000,
});

/* ===============================
   INTERCEPTORES DE LOGGING
   =============================== */

// Request
api.interceptors.request.use(
  (config) => {
    console.debug("[API REQUEST]", {
      method: config.method,
      url: config.baseURL + config.url,
    });
    return config;
  },
  (error) => {
    console.error("[API REQUEST ERROR]", error);
    return Promise.reject(error);
  }
);

// Response
api.interceptors.response.use(
  (response) => {
    console.debug("[API RESPONSE]", {
      url: response.config.url,
      status: response.status,
      data: response.data,
    });
    return response;
  },
  (error) => {
    if (error.response) {
      console.error("[API RESPONSE ERROR]", {
        url: error.config?.url,
        status: error.response.status,
        data: error.response.data,
      });
    } else {
      console.error("[API NETWORK ERROR]", error.message);
    }
    return Promise.reject(error);
  }
);

