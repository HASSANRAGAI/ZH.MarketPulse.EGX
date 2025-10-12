import React from 'react';

interface Stock {
  name: string;
  source: string;
  recommendation: string;
  market: string;
  sector: string;
  value: string;
  price: string;
  lastPrice: string;
  change: string;
  changePercent: string;
  releasedAt: string;
}

const stocks: Stock[] = [
  {
    name: 'CLHO_r1 - Fair Value',
    source: 'Mubasher Trade',
    recommendation: 'Buy',
    market: 'Egyptian Stock Exchange',
    sector: 'Healthcare and Pharmaceuticals Sector Index',
    value: '11.6',
    price: '8.71',
    lastPrice: '11.35',
    change: '2.889',
    changePercent: '33.18%',
    releasedAt: '2025-09-01T00:00:00',
  },
  {
    name: 'CSAG - Fair Value',
    source: 'Mubasher Trade',
    recommendation: 'Buy',
    market: 'Egyptian Stock Exchange',
    sector: 'Shipping & Transportation Services',
    value: '14.2',
    price: 'N/A',
    lastPrice: '29.17',
    change: 'N/A',
    changePercent: 'N/A',
    releasedAt: '2025-03-03T00:00:00',
  },
  {
    name: 'VALU - Fair Value',
    source: 'Mubasher Trade',
    recommendation: 'Buy',
    market: 'Egyptian Stock Exchange',
    sector: 'Non-bank financial services',
    value: '7.2',
    price: 'N/A',
    lastPrice: '8',
    change: 'N/A',
    changePercent: 'N/A',
    releasedAt: 'Not specified', // From screenshot, cut off
  },
];

const NewStocksPage: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', padding: '20px' }}>
      {stocks.map((stock, index) => (
        <div key={index} className="e-card" style={{ width: '300px', margin: '10px' }}>
          <div className="e-card-header">
            <div className="e-card-header-caption">
              <div className="e-card-title">{stock.name}</div>
            </div>
          </div>
          <div className="e-card-content">
            <p><strong>Source:</strong> {stock.source}</p>
            <p><strong>Recommendation:</strong> {stock.recommendation}</p>
            <p><strong>Market:</strong> {stock.market}</p>
            <p><strong>Sector:</strong> {stock.sector}</p>
            <p><strong>Value:</strong> {stock.value}</p>
            <p><strong>Price:</strong> {stock.price}</p>
            <p><strong>Last Price:</strong> {stock.lastPrice}</p>
            <p><strong>Change:</strong> {stock.change}</p>
            <p><strong>Change %:</strong> {stock.changePercent}</p>
            <p><strong>Released At:</strong> {stock.releasedAt}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default NewStocksPage;