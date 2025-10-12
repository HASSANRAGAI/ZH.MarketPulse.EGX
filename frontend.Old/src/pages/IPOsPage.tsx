import React, { useEffect, useState } from 'react';
import type { IPOResponse } from '../responses/IPOResponse';
import { getIPOs, collectIPOsSync } from '../services/api';
import './IPOsPage.css'; // Add CSS for styling

const IPOsPage: React.FC = () => {
  const [ipos, setIpos] = useState<IPOResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadIPOs = async () => {
      try {
        setLoading(true);
        let data = await getIPOs();
        if (data.length === 0) {
          // No data, collect sync
          await collectIPOsSync();
          data = await getIPOs();
        }
        setIpos(data);
      } catch (err) {
        setError('Failed to load IPOs');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadIPOs();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="ipos-page">
      <h1>IPOs</h1>
      <div className="cards-container">
        {ipos.map((ipo) => (
          <div key={ipo.id} className="ipo-card">
            <div className="card-header">
              <h3>{ipo.name} {ipo.name_ar && `(${ipo.name_ar})`}</h3>
            </div>
            <div className="card-content">
              <p><strong>Status:</strong> {ipo.status} {ipo.status_ar && `(${ipo.status_ar})`}</p>
              <p><strong>Type:</strong> {ipo.type} {ipo.type_ar && `(${ipo.type_ar})`}</p>
              <p><strong>Market:</strong> {ipo.market} {ipo.market_ar && `(${ipo.market_ar})`}</p>
              <p><strong>Sector:</strong> {ipo.sector} {ipo.sector_ar && `(${ipo.sector_ar})`}</p>
              <p><strong>Volume:</strong> {ipo.volume}</p>
              <p><strong>Announced At:</strong> {ipo.announced_at || 'N/A'}</p>
              {ipo.stock_base_data ? (
                <div>
                  <p><strong>Stock:</strong> {ipo.stock_base_data.symbol} - {ipo.stock_base_data.name} {ipo.stock_base_data.name_ar && `(${ipo.stock_base_data.name_ar})`}</p>
                  <p><strong>Stock Market:</strong> {ipo.stock_base_data.market}</p>
                  <p><strong>Stock Sector:</strong> {ipo.stock_base_data.sector}</p>
                  <p><strong>Stock Currency:</strong> {ipo.stock_base_data.currency}</p>
                </div>
              ) : (
                ipo.stock_symbol && (
                  <p><strong>Stock:</strong> {ipo.stock_symbol} - {ipo.stock_name} {ipo.stock_name_ar && `(${ipo.stock_name_ar})`}</p>
                )
              )}
              {ipo.url && <p><a href={ipo.url} target="_blank" rel="noopener noreferrer">URL</a></p>}
              {ipo.attachment && <p><a href={ipo.attachment} target="_blank" rel="noopener noreferrer">Attachment</a></p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default IPOsPage;
