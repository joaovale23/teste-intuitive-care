/**
 * Composable para gerenciar estados de loading
 * Centraliza lógica de loading para evitar repetição
 */

import { ref, computed } from "vue";

export function useLoading() {
  const loadingStates = ref({});

  const setLoading = (chave, valor) => {
    loadingStates.value[chave] = valor;
  };

  const isLoading = (chave) => {
    return loadingStates.value[chave] ?? false;
  };

  const qualquerCarregamento = computed(() => {
    return Object.values(loadingStates.value).some((v) => v === true);
  });

  return {
    setLoading,
    isLoading,
    qualquerCarregamento,
  };
}
