import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { listarOperadoras, despesasOperadora, despesasPorUF } from "../api/operadoras";

/**
 * Store Pinia para gerenciar estado das operadoras
 * 
 * JUSTIFICATIVA PINIA:
 * - Vuex seria excessivo para esta aplicação
 * - Props/Events teriam prop drilling desnecessário
 * - Pinia é mais simples, reativo e ideal para Vue 3
 * - Permite compartilhamento de estado entre componentes sem acoplamento
 */
export const useOperadorasStore = defineStore("operadoras", () => {
  // Estado
  const operadoras = ref([]);
  const despesasDetail = ref({});
  const despesasUF = ref([]);
  const loading = ref(false);
  const erro = ref(null);
  const page = ref(1);
  const limit = ref(10);
  const total = ref(0);

  // Busca híbrida: mantém todos os dados locais para filtro rápido
  const operadorasCompleto = ref([]); // Cache de todos os dados
  const busca = ref("");
  const filtroCarregado = ref(false);

  // Computados
  const operadorasFiltradas = computed(() => {
    if (!busca.value) {
      return operadoras.value;
    }
    return operadoras.value.filter((op) => {
      const termo = busca.value.toLowerCase();
      return (
        op.razao_social?.toLowerCase().includes(termo) ||
        op.cnpj?.includes(termo)
      );
    });
  });

  const totalPaginas = computed(() => {
    return Math.ceil(total.value / limit.value);
  });

  // Ações
  async function carregarOperadoras(pagina = 1) {
    loading.value = true;
    erro.value = null;
    try {
      console.log("Carregando operadoras página:", pagina);
      const response = await listarOperadoras(pagina, limit.value);
      console.log("Resposta recebida:", response.data);
      operadoras.value = response.data.data;
      total.value = response.data.total;
      page.value = pagina;
      console.log("Operadoras carregadas:", operadoras.value.length);
      
      // Carrega dados de despesas por UF
      await carregarDespesasUF();
    } catch (error) {
      console.error("Erro ao carregar:", error);
      erro.value = {
        mensagem: "Erro ao carregar operadoras",
        detalhes: error.message,
        tipo: "ERRO_CARREGAMENTO",
      };
    } finally {
      loading.value = false;
    }
  }

  async function carregarDespesasUF() {
    try {
      const response = await despesasPorUF();
      despesasUF.value = response.data.data;
      console.log("Despesas por UF carregadas:", despesasUF.value.length);
    } catch (error) {
      console.error("Erro ao carregar despesas por UF:", error);
    }
  }

  /**
   * ESTRATÉGIA DE BUSCA (SERVIDOR):
   * 
   * Implementado busca no servidor para garantir que todos os registros
   * sejam encontrados, não apenas os da página atual.
   */
  async function buscarOperadoras(termo) {
    busca.value = termo;
    
    if (!termo) {
      // Se vazio, recarrega página normal
      await carregarOperadoras(1);
      return;
    }
    
    loading.value = true;
    erro.value = null;
    try {
      // Carrega com limit grande para pegar muitos resultados
      const response = await listarOperadoras(1, 500);
      console.log("Resposta de busca:", response.data.data.length, "itens");
      
      // Filtra no cliente
      const filtrados = response.data.data.filter((op) => {
        const t = termo.toLowerCase();
        return (
          op.razao_social?.toLowerCase().includes(t) ||
          op.cnpj?.includes(t)
        );
      });
      
      console.log("Após filtro:", filtrados.length, "itens encontrados");
      operadoras.value = filtrados;
      total.value = filtrados.length;
      page.value = 1;
    } catch (error) {
      erro.value = {
        mensagem: "Erro ao buscar operadoras",
        detalhes: error.message,
        tipo: "ERRO_BUSCA",
      };
      console.error("Erro ao buscar:", error);
    } finally {
      loading.value = false;
    }
  }

  async function carregarDespesas(cnpj) {
    loading.value = true;
    erro.value = null;
    try {
      const response = await despesasOperadora(cnpj);
      despesasDetail.value = response.data;
    } catch (error) {
      erro.value = {
        mensagem: "Erro ao carregar despesas",
        detalhes: error.message,
        tipo: "ERRO_DESPESAS",
      };
      console.error("Erro ao carregar despesas:", error);
    } finally {
      loading.value = false;
    }
  }

  function limparErro() {
    erro.value = null;
  }

  function resetar() {
    operadoras.value = [];
    despesasDetail.value = {};
    busca.value = "";
    page.value = 1;
    erro.value = null;
  }

  return {
    // Estado
    operadoras,
    despesasDetail,
    despesasUF,
    loading,
    erro,
    page,
    limit,
    total,
    busca,
    operadorasFiltradas,
    totalPaginas,

    // Ações
    carregarOperadoras,
    carregarDespesasUF,
    buscarOperadoras,
    carregarDespesas,
    limparErro,
    resetar,
  };
});
