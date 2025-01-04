import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Registration from './components/Registration';
import DepartmentTasksPage from './components/DepartmentTasksPage';

const App = () => {
  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Registration />} />
        
        {/* Route for dynamic department tasks page */}
        <Route path="/departments/:department" element={<DepartmentTasksPage />} />
      </Routes>
    </Box>
  );
}

export default App;
