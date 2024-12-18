import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom'; // Import navigate function
import '../App.css'; // Optional: Add CSS for styling

function DepartmentsPage() {
    const [departments, setDepartments] = useState([]);
    const navigate = useNavigate(); // Initialize navigate function

    useEffect(() => {
        // Fetch department data from the backend
        fetch("http://localhost:5000/api/departments")
            .then((response) => response.json())
            .then((data) => setDepartments(data))
            .catch((error) => console.error("Error fetching departments:", error));
    }, []);

    const handleViewDepartment = (departmentId) => {
        navigate(`/departments/${departmentId}`);
    };

    // Define the handleAddDepartment function
    const handleAddDepartment = () => {
        // Redirect to the add department page
        navigate("/departments/add");
    };

    return (
        <div className="departments-container">
            <h1>University Departments</h1>
            
            {/* Button to add a department */}
            <button onClick={handleAddDepartment}>Add Department</button>

            <div className="departments-list">
                {departments.map((dept) => (
                    <div key={dept.id} className="department-card">
                        <h2>{dept.name}</h2>
                        <p>{dept.description}</p>
                        <button onClick={() => handleViewDepartment(dept.id)}>
                            View {dept.name} Department
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default DepartmentsPage;
