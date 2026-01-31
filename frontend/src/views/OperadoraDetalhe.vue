const fetchHistorico = async (cnpj) => {
  const res = await axios.get(`/api/operadoras/${cnpj}/despesas`);
  historico.value = res.data.historico;
};