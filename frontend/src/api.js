const API_URL = 'http://127.0.0.1:8000';

export const fetchFeed = async (token) => {
  const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
  const res = await fetch(`${API_URL}/api/feed/`, { headers });
  if (!res.ok) throw new Error('Failed to fetch feed');
  return res.json();
};

export const loginUser = async (email, password) => {
  const res = await fetch(`${API_URL}/api/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) throw new Error('Invalid credentials');
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

export const fetchWeights = async (token) => {
  const res = await fetch(`${API_URL}/api/me/weights/`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return res.json();
};