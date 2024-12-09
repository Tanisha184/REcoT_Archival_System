import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const Dashboard = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear any stored authentication (if using localStorage, etc.)
    // Redirect to the login page
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to Your Dashboard!</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>

      <section className="dashboard-stats">
        <div className="stat-card">
          <h3>Deparmnets</h3>
          <p>10</p>
        </div>
        <div className="stat-card">
          <h3>Total Tasks</h3>
          <p>5</p>
        </div>
        <div className="stat-card">
          <h3>Pending Tasks</h3>
          <p>5</p>
        </div>
      </section>

      <section className="dashboard-navigation">
        <button onClick={() => navigate('/todo')} className="navigate-button">Go to Task</button>
        <button onClick={() => navigate('/settings')} className="navigate-button">Settings</button>
      </section>
    </div>
  );
};

export default Dashboard;
