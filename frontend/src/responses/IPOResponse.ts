export interface StockBaseData {
  id: number;
  symbol: string;
  name?: string;
  name_ar?: string;
  market?: string;
  sector?: string;
  currency?: string;
}

export interface IPOResponse {
  id: number;
  name?: string;
  name_ar?: string;
  url?: string;
  status?: string;
  status_ar?: string;
  attachment?: string;
  type?: string;
  type_ar?: string;
  market?: string;
  market_ar?: string;
  sector?: string;
  sector_ar?: string;
  market_url?: string;
  volume?: number;
  announced_at?: string;
  stock_symbol?: string;
  stock_name?: string;
  stock_name_ar?: string;
  stock_base_data?: StockBaseData;
}
