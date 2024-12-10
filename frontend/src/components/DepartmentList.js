import React, { useEffect, useState } from 'react';

function DepartmentList() {
    const [departments, setDepartments] = useState([]);

    useEffect(() => {
        // Fetch department data from the API
        fetch("http://localhost:5000/api/departments")
            .then(response => response.json())
            .then(data => {
                setDepartments(data); // Store the department list in the state
            })
            .catch(error => {
                console.error("Error fetching departments:", error);
            });
    }, []);

    return (
        <div>
            <h2>Departments</h2>
            <ul>
                {departments.length > 0 ? (
                    departments.map(department => (
                        <li key={department.id}>
                            <strong>{department.name}</strong>: {department.description}
                        </li>
                    ))
                ) : (
                    <li>No departments found</li>
                )}
            </ul>
        </div>
    );
}

export default DepartmentList;
