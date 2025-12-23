import axios from 'axios';
import type { StockResponse } from '../responses/StockResponse';
import type { StockCollectionResponse } from '../responses/StockCollectionResponse';
import type { FairValueResponse } from '../responses/FairValueResponse';
import type { IPOResponse } from '../responses/IPOResponse';

// Assuming the backend is running on localhost:8001, adjust as needed
let apiBaseUrl: string | null = null;

const getApiBaseUrl = async (): Promise<string> => {
  if (apiBaseUrl) return apiBaseUrl;
  try {
    await axios.get('http://localhost:8001/health', { timeout: 2000 });
    apiBaseUrl = 'http://localhost:8001';
  } catch {
    apiBaseUrl = 'http://196.221.164.57:8811';
  }
  return apiBaseUrl;
};

export const fetchStocks = async (): Promise<StockResponse[]> => {
  const base = await getApiBaseUrl();
  const response = await axios.get(`${base}/stocks`);
  return response.data;
};

export const collectStocksSync = async (): Promise<StockCollectionResponse> => {
  const base = await getApiBaseUrl();
  const response = await axios.get(`${base}/collect/stocksSync`);
  return response.data;
};

export const getFairValues = async (): Promise<FairValueResponse[]> => {
  const base = await getApiBaseUrl();
  const response = await axios.get(`${base}/fairValues`);
  return response.data;
};

export const collectFairValues = async (): Promise<StockCollectionResponse> => {
  const base = await getApiBaseUrl();
  const response = await axios.post(`${base}/collect/fairValues`);
  return response.data;
};

export const collectFairValuesSync = async (): Promise<StockCollectionResponse> => {
  const base = await getApiBaseUrl();
  const response = await axios.get(`${base}/collect/fairValuesSync`);
  return response.data;
};

export const getIPOs = async (): Promise<IPOResponse[]> => {
  const base = await getApiBaseUrl();
  const response = await axios.get(`${base}/ipos`);
  return response.data;
};

export const collectIPOs = async (): Promise<StockCollectionResponse> => {
  const base = await getApiBaseUrl();
  const response = await axios.post(`${base}/collect/ipos`);
  return response.data;
};

export const collectIPOsSync = async (): Promise<StockCollectionResponse> => {
  const base = await getApiBaseUrl();
  const response = await axios.get(`${base}/collect/iposSync`);
  return response.data;
};
