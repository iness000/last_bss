import {
  useQuery,
  useMutation as useMutationRQ,
  useQueryClient,
  QueryKey,
  UseQueryResult,
  UseMutationResult,
} from '@tanstack/react-query';

import api from '../utils/api'; // Ton instance axios configurée

interface ApiOptions<TData> {
  immediate?: boolean; // Lancer automatiquement le fetch
  dependencies?: QueryKey; // Dépendances pour le refetch
  onSuccess?: (data: TData) => void;
  onError?: (error: Error) => void;
}

/**
 * Hook GET générique
 */
export function useApi<TData = unknown>(
  url: string | null,
  options: ApiOptions<TData> = {}
): UseQueryResult<TData, Error> {
  const { immediate = true, dependencies = [], onSuccess, onError } = options;
  const queryKey: QueryKey = [url, ...(Array.isArray(dependencies) ? dependencies : [dependencies])];

  const query = useQuery<TData, Error, TData, QueryKey>({
    queryKey: queryKey,
    queryFn: async () => {
      if (!url) {
        return Promise.reject(new Error("URL is null, skipping fetch."));
      }
      const response = await api.get<TData>(url);
      return response.data;
    },
    enabled: immediate && !!url,
  });

  // Handle success and error callbacks using useEffect if provided
  if (onSuccess && query.data && query.isSuccess) {
    onSuccess(query.data);
  }
  
  if (onError && query.error && query.isError) {
    onError(query.error);
  }

  return query;
}

/**
 * Hook de mutation (POST, PUT, PATCH, DELETE) avec invalidation automatique
 */
export function useAppMutation<TData = unknown, TVariables = unknown>(
  mutationFn: (variables: TVariables) => Promise<TData>,
  queryKeyToInvalidate?: QueryKey | QueryKey[]
): UseMutationResult<TData, Error, TVariables, unknown> {
  const queryClient = useQueryClient();

  return useMutationRQ<TData, Error, TVariables, unknown>({
    mutationFn,
    onSuccess: () => {
      if (queryKeyToInvalidate) {
        queryClient.invalidateQueries({
          queryKey: Array.isArray(queryKeyToInvalidate)
            ? queryKeyToInvalidate
            : [queryKeyToInvalidate],
        });
      }
    },
  });
}
