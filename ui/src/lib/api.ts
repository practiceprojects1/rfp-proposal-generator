import axios, { AxiosInstance } from 'axios';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          localStorage.removeItem('authToken');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }

  async chat(message: string, threadId: string = 'default') {
    const response = await this.client.post('/chat', {
      message,
      thread_id: threadId,
      stream: false,
    });
    return response.data;
  }

  async searchRfps(keywords: string, daysBack: number = 30, limit: number = 10) {
    const response = await this.client.post('/rfp/search', null, {
      params: {
        keywords,
        days_back: daysBack,
        limit,
      },
    });
    return response.data;
  }

  async analyzeRfp(rfpDetails: any) {
    const response = await this.client.post('/rfp/analyze', rfpDetails);
    return response.data;
  }

  async generateProposal(rfpDetails: any) {
    const response = await this.client.post('/proposal/generate', rfpDetails);
    return response.data;
  }
}

export const apiClient = new ApiClient();