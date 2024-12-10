import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null); // Store user info including role

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

// Example of conditional rendering based on role
const TaskManagement = () => {
  const { user } = useUser();

  return (
    <div>
      {user && user.role === 'Admin' && <div>Admin Component</div>}
      {user && user.role === 'Department Head' && <div>Department Head Component</div>}
      {user && user.role === 'Regular User' && <div>Regular User Component</div>}
    </div>
  );
};

export default TaskManagement;