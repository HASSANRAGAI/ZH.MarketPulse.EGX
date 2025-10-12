import type { StockResponse } from './StockResponse';

export interface StockCollectionResponse {
  success: boolean;
  message: string;
  stocks_collected?: StockResponse[];
  timestamp: string;
  service: string;
}
