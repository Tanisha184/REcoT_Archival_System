// src/components/DepartmentsPage.js
import React, { useState, useEffect } from 'react';
import '../App.css'; // Optional: Add CSS for styling

function DepartmentsPage() {
    const [departments, setDepartments] = useState([]);

    useEffect(() => {
        // Fetch department data from the backend
        fetch("http://localhost:5000/api/departments")
            .then((response) => response.json())
            .then((data) => setDepartments(data))
            .catch((error) => console.error("Error fetching departments:", error));
    }, []);

    return (
        <div className="departments-container">
            <h1>University Departments</h1>
            <div className="departments-list">
                {departments.map((dept) => (
                    <div key={dept.id} className="department-card">
                        <h2>{dept.name}</h2>
                        <p>{dept.description}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default DepartmentsPage;
