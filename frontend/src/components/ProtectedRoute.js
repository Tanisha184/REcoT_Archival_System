import React from 'react';
import { Navigate } from 'react-router-dom';

import '../App.css';


const ProtectedRoute = ({ children, allowedRoles }) => {
  const userRole = localStorage.getItem('userRole');

  return allowedRoles.includes(userRole) ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
