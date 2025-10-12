import React, { useEffect, useState } from 'react';
import { fetchStocks, collectStocksSync } from '../services/api';
import type { StockResponse } from '../responses/StockResponse';
import './StocksPage.css'; // Add CSS for styling

const StocksPage: React.FC = () => {
  const [stocks, setStocks] = useState<StockResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStocks = async () => {
      try {
        setLoading(true);
        let data = await fetchStocks();
        if (data.length === 0) {
          // No data, collect sync
          await collectStocksSync();
          data = await fetchStocks();
        }
        setStocks(data);
      } catch (err) {
        setError('Failed to load stocks');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadStocks();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="stocks-page">
      <h1>Stocks</h1>
      <div className="cards-container">
        {stocks.map((stock) => (
          <div key={stock.symbol} className="stock-card">
            <div className="card-header">
              <h3>{stock.symbol} - {stock.name_en}</h3>
            </div>
            <div className="card-content">
              <p><strong>Arabic Name:</strong> {stock.name_ar}</p>
              <p><strong>Sector:</strong> {stock.sector_en} ({stock.sector_ar})</p>
              <p><strong>Market:</strong> {stock.market_en} ({stock.market_ar})</p>
              <p><strong>Currency:</strong> {stock.currency || 'N/A'}</p>
              <p><strong>Current Price:</strong> {stock.current_price ? `${stock.current_price} ${stock.currency}` : 'N/A'}</p>
              <p><strong>Change %:</strong> {stock.change_percentage ? `${stock.change_percentage}%` : 'N/A'}</p>
              <p><strong>Last Update:</strong> {stock.last_update || 'N/A'}</p>
              <p><strong>Active:</strong> {stock.is_active ? 'Yes' : 'No'}</p>
              {stock.profile_url && <p><a href={stock.profile_url} target="_blank" rel="noopener noreferrer">Profile</a></p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default StocksPage;
