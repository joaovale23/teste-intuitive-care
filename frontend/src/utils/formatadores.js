/**
 * Funções utilitárias para formatação e transformação de dados
 */

export function formatarCNPJ(cnpj) {
  if (!cnpj) return "";
  return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, "$1.$2.$3/$4-$5");
}

export function formatarMoeda(valor) {
  if (valor === null || valor === undefined) return "R$ 0,00";
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(valor);
}

export function formatarData(data) {
  if (!data) return "";
  return new Intl.DateTimeFormat("pt-BR").format(new Date(data));
}

/**
 * Agrupa despesas por UF para gráfico
 * Transforma dados brutos em formato adequado para Chart.js
 */
export function agruparDespesasPorUF(operadoras) {
  const agrupado = {};

  operadoras.forEach((op) => {
    const uf = op.uf || "XX";
    if (!agrupado[uf]) {
      agrupado[uf] = 0;
    }
    agrupado[uf] += parseFloat(op.valor_despesas || 0);
  });

  const ufsOrdenadas = Object.keys(agrupado).sort();
  const cores = ufsOrdenadas.map(uf => coresUF[uf] || "rgba(200, 200, 200, 0.8)");

  return {
    labels: ufsOrdenadas,
    datasets: [
      {
        label: "Despesas por UF (R$)",
        data: ufsOrdenadas.map((uf) => agrupado[uf]),
        backgroundColor: cores,
        borderColor: "#fff",
        borderWidth: 2,
      },
    ],
  };
}

/**
 * Mapa de cores fixas para cada UF
 * Garante que cada estado sempre tenha a mesma cor
 */
const coresUF = {
  "AC": "rgba(255, 107, 107, 0.8)",  // Vermelho
  "AL": "rgba(255, 159, 64, 0.8)",   // Laranja
  "AP": "rgba(255, 205, 86, 0.8)",   // Amarelo
  "AM": "rgba(75, 192, 192, 0.8)",   // Ciano
  "BA": "rgba(54, 162, 235, 0.8)",   // Azul
  "CE": "rgba(153, 102, 255, 0.8)",  // Roxo
  "DF": "rgba(255, 159, 243, 0.8)",  // Rosa
  "ES": "rgba(201, 203, 207, 0.8)",  // Cinza
  "GO": "rgba(75, 235, 107, 0.8)",   // Verde
  "MA": "rgba(255, 99, 132, 0.8)",   // Vermelho escuro
  "MT": "rgba(255, 159, 132, 0.8)",  // Salmão
  "MS": "rgba(54, 235, 162, 0.8)",   // Verde água
  "MG": "rgba(235, 162, 54, 0.8)",   // Laranja escuro
  "PA": "rgba(162, 54, 235, 0.8)",   // Roxo escuro
  "PB": "rgba(54, 162, 235, 0.9)",   // Azul escuro
  "PR": "rgba(235, 54, 162, 0.8)",   // Magenta
  "PE": "rgba(162, 235, 54, 0.8)",   // Limão
  "PI": "rgba(99, 132, 255, 0.8)",   // Azul royal
  "RJ": "rgba(255, 132, 99, 0.8)",   // Coral
  "RN": "rgba(132, 255, 99, 0.8)",   // Verde limão
  "RS": "rgba(132, 99, 255, 0.8)",   // Lilás
  "RO": "rgba(255, 99, 255, 0.8)",   // Magenta claro
  "RR": "rgba(99, 255, 132, 0.8)",   // Menta
  "SC": "rgba(255, 198, 88, 0.8)",   // Ouro
  "SP": "rgba(88, 198, 255, 0.8)",   // Azul céu
  "SE": "rgba(198, 255, 88, 0.8)",   // Amarelo-verde
  "TO": "rgba(255, 88, 198, 0.8)",   // Rosa/Magenta
};

function gerarCoresPastel(quantidade) {
  // Esta função agora não é mais usada, mas mantida por compatibilidade
  const cores = Object.values(coresUF);
  const resultado = [];
  for (let i = 0; i < quantidade; i++) {
    resultado.push(cores[i % cores.length]);
  }
  return resultado;
}

export function ordenarPorPropriedade(array, propriedade, ordem = "asc") {
  return [...array].sort((a, b) => {
    const aVal = a[propriedade];
    const bVal = b[propriedade];

    if (typeof aVal === "string") {
      return ordem === "asc"
        ? aVal.localeCompare(bVal)
        : bVal.localeCompare(aVal);
    }

    return ordem === "asc" ? aVal - bVal : bVal - aVal;
  });
}
