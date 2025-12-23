export interface StockResponse {
  symbol: string;
  name_en: string;
  name_ar: string;
  sector_en: string;
  sector_ar: string;
  market_en: string;
  market_ar: string;
  currency?: string;
  profile_url?: string;
  current_price?: number;
  change_percentage?: number;
  last_update?: string;
  is_active: boolean;
}

