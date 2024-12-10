import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import { createTask, approveTask, manageUsers } from '../api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [taskData, setTaskData] = useState({ task_name: '', description: '' });
  const [taskId, setTaskId] = useState('');
  const [approvalStatus, setApprovalStatus] = useState('');
  const [users, setUsers] = useState([]);

  const handleLogout = () => {
    // Clear any stored authentication (if using localStorage, etc.)
    // Redirect to the login page
    navigate('/login');
  };

  const handleCreateTask = async () => {
    try {
      const response = await createTask(taskData);
      console.log('Task created:', response);
      setTaskData({ task_name: '', description: '' });
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  const handleApproveTask = async () => {
    try {
      const response = await approveTask(taskId, approvalStatus);
      console.log('Task approved:', response);
      setTaskId('');
      setApprovalStatus('');
    } catch (error) {
      console.error('Error approving task:', error);
    }
  };

  const handleManageUsers = async () => {
    try {
      const response = await manageUsers();
      setUsers(response);
      console.log('Users managed:', response);
    } catch (error) {
      console.error('Error managing users:', error);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome to Your Dashboard!</h1>
        <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>

      <section className="dashboard-stats">
        <div className="stat-card">
          <h3>Departments</h3>
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

      <section className="dashboard-actions">
        <div>
          <h3>Create Task</h3>
          <input
            type="text"
            placeholder="Task Name"
            value={taskData.task_name}
            onChange={(e) => setTaskData({ ...taskData, task_name: e.target.value })}
          />
          <input
            type="text"
            placeholder="Description"
            value={taskData.description}
            onChange={(e) => setTaskData({ ...taskData, description: e.target.value })}
          />
          <button onClick={handleCreateTask} className="action-button">Create Task</button>
        </div>

        <div>
          <h3>Approve Task</h3>
          <input
            type="text"
            placeholder="Task ID"
            value={taskId}
            onChange={(e) => setTaskId(e.target.value)}
          />
          <input
            type="text"
            placeholder="Approval Status"
            value={approvalStatus}
            onChange={(e) => setApprovalStatus(e.target.value)}
          />
          <button onClick={handleApproveTask} className="action-button">Approve Task</button>
        </div>

        <div>
          <h3>Manage Users</h3>
          <button onClick={handleManageUsers} className="action-button">Manage Users</button>
          <ul>
            {users.map((user, index) => (
              <li key={index}>{user.email}</li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
