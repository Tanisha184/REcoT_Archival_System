import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../api';
import { useUser } from '../UserContext';
import '../App.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { setUser } = useUser();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(email, password);
      console.log('Login response data:', data); // Log the response data
      if (data.success) {
        setUser(data.user); // Set the user state
        navigate('/dashboard');
      } else {
        setError(data.message);
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('An error occurred. Please try again later.');
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        {error && <p className="error-message">{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
