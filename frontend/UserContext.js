
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
    return useContext(UserContext);
};

// Example of conditional rendering based on role
const TaskManagement = () => {
    const { user } = useUser();

    return (
        <div>
            {user && user.role === 'Admin' && <AdminComponent />}
            {user && user.role === 'Department Head' && <DepartmentHeadComponent />}
            {user && user.role === 'Regular User' && <RegularUserComponent />}
        </div>
    );
};

export default TaskManagement;
