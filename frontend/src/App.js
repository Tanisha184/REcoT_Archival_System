import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Registration from './components/Registration';
import DepartmentTasksPage from './components/DepartmentTasksPage';
import DepartmentsPage from './components/DepartmentsPage';
import DepartmentDetailPage from './components/DepartmentDetailPage';
import ProtectedRoute from './components/ProtectedRoute';
import DepartmentList from './components/DepartmentList';
import DepartmentAddPage from './components/DepartmentAddPage';
import ArchivalPage from './components/ArchivalPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Registration />} />
        <Route path="/departments/:departmentId" element={<DepartmentDetailPage />} />
        <Route path="/departments" element={<DepartmentsPage />} />
        <Route path="/departments/add" element={<DepartmentAddPage />} />
        <Route path="/departments/list" element={<DepartmentList />} />
        <Route path="/Archival" element={<ArchivalPage />} />
        <Route
          path="/departments/:departmentId/tasks"
          element={
            <ProtectedRoute allowedRoles={['admin', 'superuser', 'user']}>
              <DepartmentTasksPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
