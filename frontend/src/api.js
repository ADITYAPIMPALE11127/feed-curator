const API_URL = 'http://127.0.0.1:8000';

export const fetchFeed = async () => {
  const res = await fetch(`${API_URL}/api/feed/`);
  if (!res.ok) throw new Error('Failed to fetch feed');
  return res.json();
};

export const sendFeedback = async (itemId, action, token) => {
  const res = await fetch(`${API_URL}/api/items/${itemId}/feedback/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ action })
  });
  return res.json();
};