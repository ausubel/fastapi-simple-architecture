import { useState } from 'react';
import { AuthService } from '../api/AuthService';
import type { LoginDto } from '../api/types';

interface LoginProps {
  onLogin: (token: string, userId: number) => void;
}

const API_URL = 'http://localhost:8000';

export function Login({ onLogin }: LoginProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const service = new AuthService(API_URL);
      const credentials: LoginDto = { email, password };
      
      const response = await service.login(credentials);
      if (response.success && response.data?.access_token) {
        // Decode JWT to get user_id from payload
        const payload = JSON.parse(atob(response.data.access_token.split('.')[1]));
        const userId = payload.user_id || 1;
        onLogin(response.data.access_token, userId);
      } else {
        setError(response.message || 'Login failed');
      }
    } catch (err) {
      setError('Invalid credentials or server error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login">
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="your@email.com"
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="••••••••"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p className="hint">
        Try: admin@admin.com / borntofeel
      </p>
    </div>
  );
}
