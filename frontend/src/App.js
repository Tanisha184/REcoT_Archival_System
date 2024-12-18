import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UserProvider } from './UserContext';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Registration from './components/Registration';
import DepartmentsPage from './components/DepartmentsPage';
import DepartmentTasksPage from './components/DepartmentTasksPage';
import TaskForm from './components/TaskForm';
import QueryManagement from './components/QueryManagement';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <UserProvider>
      <Router>
        <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Registration />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/departments"
          element={
            <ProtectedRoute>
              <DepartmentsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/departments/:department/tasks"
          element={
            <ProtectedRoute>
              <DepartmentTasksPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/create-task"
          element={
            <ProtectedRoute>
              <TaskForm />
            </ProtectedRoute>
          }
        />
        <Route
          path="/query-management"
          element={
            <ProtectedRoute>
              <QueryManagement />
            </ProtectedRoute>
          }
        />
        </Routes>
      </Router>
    </UserProvider>
  );
}

export default App;
