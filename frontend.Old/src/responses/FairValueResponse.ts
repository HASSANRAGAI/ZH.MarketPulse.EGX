export interface FairValueResponse {
  id: number;
  symbol: string;
  released_at?: string;
  source?: string;
  source_ar?: string;
  recommendation?: string;
  recommendation_ar?: string;
  market?: string;
  sector?: string;
  market_url?: string;
  value?: number;
  price?: number;
  last_price?: number;
  change?: number;
  change_percentage?: number;
}

