'use client';

import '../styles/card.component.scss';
import React, { useState, useEffect } from 'react';
import { fetchStocks, collectStocksSync } from '../services/api';
import type { StockResponse } from '../responses/StockResponse';

const StocksCard: React.FC = () => {
  const [stocks, setStocks] = useState<StockResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStocks = async () => {
      try {
        const data = await fetchStocks();
        if (data.length === 0) {
          const collectResponse = await collectStocksSync();
          if (collectResponse.success && collectResponse.stocks_collected) {
            setStocks(collectResponse.stocks_collected);
          }
        } else {
          setStocks(data);
        }
      } catch (error) {
        console.error('Error fetching stocks:', error);
        try {
          const collectResponse = await collectStocksSync();
          if (collectResponse.success && collectResponse.stocks_collected) {
            setStocks(collectResponse.stocks_collected);
          }
        } catch (e) {
          console.error('Error collecting stocks:', e);
        }
      } finally {
        setLoading(false);
      }
    };
    loadStocks();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="control-pane">
      <div className="control-section card-control-section horizontal_card_layout">
        <div className="e-card-resize-container">
          <div className="row">
            <div className="row card-layout">
              {stocks.map(stock => (
                <div key={stock.symbol} className="col-xs-12 col-sm-12 col-lg-6 col-md-6">
                  <div className="e-card e-card-horizontal" id={`horizontal_${stock.symbol}`}>
                    <div className="e-card-stacked">
                      <div className="e-card-header">
                        <div className="e-card-header-caption">
                          <div className="e-card-header-title">{stock.name_en}</div>
                          <div className="e-card-sub-title">{stock.symbol} | {stock.sector_en}</div>
                        </div>
                      </div>
                      <div className="e-card-content">
                        <p><strong>Arabic Name:</strong> {stock.name_ar}</p>
                        <p><strong>Market:</strong> {stock.market_en}</p>
                        <p><strong>Current Price:</strong> {stock.current_price ? `${stock.current_price} ${stock.currency || 'EGP'}` : 'N/A'}</p>
                        <p><strong>Change %:</strong> {stock.change_percentage ? `${stock.change_percentage}%` : 'N/A'}</p>
                        <p><strong>Last Update:</strong> {stock.last_update || 'N/A'}</p>
                      </div>
                      <div className="e-card-actions" style={{ justifyContent: 'center' }}>
                        <button className="e-btn e-outline e-primary">View Details</button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StocksCard;
