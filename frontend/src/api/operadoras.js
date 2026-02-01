import axios from "axios";

// Em produção, usa a URL do Render; em dev, usa localhost
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL
});

export function listarOperadoras(page = 1, limit = 10, busca = null) {
  const params = { page, limit };

  if (busca?.termo) {
    params.q = busca.termo;
    params.campo = busca.campo || "razao_social";
  }

  return api.get("/operadoras", { params });
}

export function obterOperadora(cnpj) {
  return api.get(`/operadoras/${cnpj}`);
}

export function despesasOperadora(cnpj) {
  return api.get(`/operadoras/${cnpj}/despesas`);
}

export function estatisticas() {
  return api.get("/estatisticas");
}

export function despesasPorUF() {
  return api.get("/operadoras/estatisticas/despesas-uf");
}