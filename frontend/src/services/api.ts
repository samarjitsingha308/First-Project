import axios from 'axios';
import { PredictionResult, ModelInfo, HealthStatus } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  async checkHealth(): Promise<HealthStatus> {
    const response = await api.get<HealthStatus>('/health');
    return response.data;
  },

  async getModelInfo(): Promise<ModelInfo> {
    const response = await api.get<ModelInfo>('/model/info');
    return response.data;
  },

  async predict(features: Record<string, number>): Promise<PredictionResult> {
    const response = await api.post<PredictionResult>('/predict', {
      data: features
    });
    return response.data;
  },

  async getTopDrivers(features: Record<string, number>): Promise<{ top_drivers: Record<string, number> }> {
    const response = await api.post('/explanations/top-drivers', {
      data: features
    });
    return response.data;
  },
};

export default api;
