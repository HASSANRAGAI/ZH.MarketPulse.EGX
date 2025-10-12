import React, { useEffect, useState } from 'react';
import type { FairValueResponse } from '../responses/FairValueResponse';
import { getFairValues, collectFairValuesSync } from '../services/api';
// import './FairValuesPage.css'; // Add CSS for styling

const FairValuesPage: React.FC = () => {
  const [fairValues, setFairValues] = useState<FairValueResponse[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const getRecommendationClass = (recommendation?: string): string => {
    if (!recommendation) return '';
    const lower = recommendation.toLowerCase();
    if (lower.includes('buy') || lower.includes('شراء')) return 'recommendation-buy';
    if (lower.includes('sell') || lower.includes('بيع')) return 'recommendation-sell';
    return '';
  };

  useEffect(() => {
    const loadFairValues = async () => {
      try {
        setLoading(true);
        let data = await getFairValues();
        if (data.length === 0) {
          // No data, collect sync
          await collectFairValuesSync();
          data = await getFairValues();
        }
        setFairValues(data);
      } catch (err) {
        setError('Failed to load fair values');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadFairValues();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    // <div className="fair-values-page">
    //   <h1>Fair Values</h1>
      <div  style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', padding: '20px' }}>
        {fairValues.map((fv) => (
          <div key={fv.id} className={`e-card ${getRecommendationClass(fv.recommendation)}`} style={{ width: '300px', margin: '10px' }}>
            <div className="e-card-header">
              <div className="e-card-header-caption">
                <div className="e-card-title">{fv.symbol} - Fair Value</div>
              </div>
            </div>
            <div className="e-card-conten">
              <p><strong>Source:</strong> {fv.source} {fv.source_ar && `(${fv.source_ar})`}</p>
              <p><strong>Recommendation:</strong> <span className={getRecommendationClass(fv.recommendation)}>{fv.recommendation}</span> {fv.recommendation_ar && `(${fv.recommendation_ar})`}</p>
              <p><strong>Market:</strong> {fv.market}</p>
              <p><strong>Sector:</strong> {fv.sector}</p>
              <p><strong>Value:</strong> {fv.value ? `${fv.value}` : 'N/A'}</p>
              <p><strong>Price:</strong> {fv.price ? `${fv.price}` : 'N/A'}</p>
              <p><strong>Last Price:</strong> {fv.last_price ? `${fv.last_price}` : 'N/A'}</p>
              <p><strong>Change:</strong> {fv.change ? `${fv.change}` : 'N/A'}</p>
              <p><strong>Change %:</strong> {fv.change_percentage ? `${fv.change_percentage}%` : 'N/A'}</p>
              <p><strong>Released At:</strong> {fv.released_at || 'N/A'}</p>
            </div>
          </div>
        ))}
      </div>
    // </div>
  );
};

export default FairValuesPage;
