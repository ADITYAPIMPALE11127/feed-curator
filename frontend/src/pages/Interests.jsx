import { useEffect, useState } from 'react';
import { fetchWeights } from '../api';
import { useAuth } from '../context/authContext';

export default function Interests() {
  const [weights, setWeights] = useState([]);
  const { token } = useAuth();

  useEffect(() => {
    if (token) {
      fetchWeights(token).then(data => setWeights(data)).catch(console.error);
    }
  }, [token]);

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Your Interests</h1>
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 space-y-6">
        {weights.length === 0 && <p className="text-gray-500">Like some items to build your profile!</p>}
        
        {weights.map(w => (
          <div key={w.category}>
            <div className="flex justify-between mb-1">
              <span className="font-medium text-gray-700">{w.category}</span>
              <span className="text-sm text-gray-500">{w.weight.toFixed(2)}x</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-4">
              <div 
                className="bg-blue-600 h-4 rounded-full" 
                style={{ width: `${Math.min((w.weight / 3.0) * 100, 100)}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}