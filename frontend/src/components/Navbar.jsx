import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/authContext';

export default function Navbar() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-3xl mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex space-x-6">
          <Link to="/" className="text-xl font-bold text-gray-900">FeedCurator</Link>
          {token && (
            <Link to="/interests" className="text-gray-600 hover:text-gray-900 mt-1">My Interests</Link>
          )}
        </div>
        <div>
          {token ? (
            <button onClick={handleLogout} className="text-sm font-medium text-red-600 hover:text-red-800">Logout</button>
          ) : (
            <Link to="/login" className="text-sm font-medium text-blue-600 hover:text-blue-800">Login</Link>
          )}
        </div>
      </div>
    </nav>
  );
}