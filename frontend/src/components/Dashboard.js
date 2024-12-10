
import '../App.css';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ departments: 0, totalTasks: 0, pendingTasks: 0 });
  const [userRole, setUserRole] = useState('');
  const [userDepartment, setUserDepartment] = useState('');

  useEffect(() => {
    // Fetch user role and department from localStorage
    setUserRole(localStorage.getItem('userRole'));
    setUserDepartment(localStorage.getItem('userDepartment'));

    // Fetch stats based on user role
    const fetchStats = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/dashboard-stats', {
          headers: { email: localStorage.getItem('email') },
        });
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      }
    };

    fetchStats();
  }, []);

  const handleLogout = () => {
    localStorage.clear(); // Clear user data
    navigate('/login'); // Redirect to login
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to Your Dashboard!</h1>
        {userRole === 'user' && <p>Department: {userDepartment}</p>}
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>

      <section className="dashboard-stats">
        <div className="stat-card">
          <h3>Departments</h3>
          <p>{stats.departments}</p>
        </div>
        <div className="stat-card">
          <h3>Total Tasks</h3>
          <p>{stats.totalTasks}</p>
        </div>
        <div className="stat-card">
          <h3>Pending Tasks</h3>
          <p>{stats.pendingTasks}</p>
        </div>
      </section>

      <section className="dashboard-navigation">
        <button onClick={() => navigate('/departments')} className="navigate-button">View Departments</button>
        <button onClick={() => navigate('/settings')} className="navigate-button">Settings</button>
      </section>
    </div>
  );
};

export default Dashboard;
