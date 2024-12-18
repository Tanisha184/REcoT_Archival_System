import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const DepartmentList = () => {
  const [departments, setDepartments] = useState([]);

  // Fetch departments from the server when the component mounts
  useEffect(() => {
    fetch('/api/departments')
      .then((response) => response.json())
      .then((data) => setDepartments(data)) // Set departments from API response
      .catch((error) => console.error('Error fetching departments:', error));
  }, []); // Empty dependency array ensures this runs once when the component mounts

  return (
    <div className="department-list-container">
      <h1>Department List</h1>
      <Link to="/departments/add">
        <button>Add New Department</button>
      </Link>
      <ul>
        {departments.length > 0 ? (
          departments.map((department) => (
            <li key={department.id}>
              <Link to={`/departments/${department.id}`}>{department.name}</Link>
            </li>
          ))
        ) : (
          <p>No departments available.</p>
        )}
      </ul>
    </div>
  );
};

export default DepartmentList;
