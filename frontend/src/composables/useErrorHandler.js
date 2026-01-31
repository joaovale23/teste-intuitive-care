/**
 * Composable para tratamento uniforme de erros
 * 
 * ESTRATÉGIA DE ERROS:
 * - Mensagens específicas: ajuda debug, melhor UX
 * - Vs Mensagens genéricas: mais segurança (menos info. sensível)
 * - ESCOLHIDA: Específica com logging
 * 
 * Tipos de erro tratados:
 * - Network: Sem conexão, timeout
 * - API: 400, 404, 500
 * - Validação: Dados inválidos
 * - Lógica: Estado inconsistente
 */

import { ref } from "vue";

export function useErrorHandler() {
  const erro = ref(null);
  const erroAnterior = ref(null);

  const mapearErro = (error) => {
    let tipo = "ERRO_DESCONHECIDO";
    let mensagem = "Ocorreu um erro inesperado";
    let detalhes = "";

    if (!error) {
      return null;
    }

    // Erro de rede
    if (error.message === "Network Error") {
      tipo = "ERRO_REDE";
      mensagem = "Não foi possível conectar ao servidor";
      detalhes = "Verifique sua conexão com a internet";
    }
    // Timeout
    else if (error.code === "ECONNABORTED") {
      tipo = "ERRO_TIMEOUT";
      mensagem = "A requisição demorou muito";
      detalhes = "Tente novamente em alguns momentos";
    }
    // Erro HTTP
    else if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      switch (status) {
        case 400:
          tipo = "ERRO_VALIDACAO";
          mensagem = data.detail || "Dados inválidos";
          break;
        case 404:
          tipo = "ERRO_NAO_ENCONTRADO";
          mensagem = data.detail || "Recurso não encontrado";
          break;
        case 500:
          tipo = "ERRO_SERVIDOR";
          mensagem = "Erro no servidor";
          detalhes = "O servidor está temporariamente indisponível";
          break;
        default:
          tipo = `ERRO_HTTP_${status}`;
          mensagem = data.detail || `Erro ${status}`;
      }
    }
    // Erro genérico
    else {
      mensagem = error.message || "Erro desconhecido";
    }

    return {
      tipo,
      mensagem,
      detalhes,
      timestamp: new Date().toISOString(),
    };
  };

  const definirErro = (error) => {
    erroAnterior.value = erro.value;
    erro.value = mapearErro(error);
    if (erro.value) {
      console.error(`[${erro.value.tipo}]`, erro.value.mensagem);
    }
  };

  const limparErro = () => {
    erro.value = null;
  };

  const temErro = () => {
    return erro.value !== null;
  };

  return {
    erro,
    definirErro,
    limparErro,
    temErro,
  };
}
