import { useEffect, useState } from 'react';
import { fetchFeed } from './api';

export default function Feed() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchFeed()
      .then(data => setItems(data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Waking up the server...</div>;

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Your Feed</h1>
      <div className="space-y-6">
        {items.map(item => (
          <div key={item.id} className="border border-gray-200 p-4 rounded-lg shadow-sm">
            <div className="text-xs text-blue-600 font-semibold mb-1">
              {item.category_name} • {item.source_name}
            </div>
            <a href={item.url} target="_blank" rel="noreferrer" className="text-xl font-semibold hover:underline">
              {item.title}
            </a>
            <p className="text-gray-600 mt-2">{item.snippet}</p>
            
            <div className="mt-4 flex space-x-4">
              <button className="text-sm font-medium text-gray-500 hover:text-green-600">👍 Like</button>
              <button className="text-sm font-medium text-gray-500 hover:text-red-600">👎 Dislike</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}