import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api"
});

export function listarOperadoras(page = 1, limit = 10) {
  return api.get("/operadoras", {
    params: { page, limit }
  });
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