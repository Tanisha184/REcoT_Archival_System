import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const DepartmentAddPage = () => {
  const [departmentName, setDepartmentName] = useState('');
  const [departmentDescription, setDepartmentDescription] = useState('');
  const [successMessage, setSuccessMessage] = useState(''); // State for success message
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();

    const newDepartment = {
      name: departmentName,
      description: departmentDescription,
    };

    fetch('/api/departments', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newDepartment),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setSuccessMessage('Department added successfully!'); // Show success message
          setTimeout(() => {
            navigate('/departments'); // Redirect to departments page after 2 seconds
          }, 2000); // Wait for 2 seconds before redirecting
        }
      });
  };

  return (
    <div className="department-add-container">
      <h1>Add New Department</h1>
      {successMessage && <p style={{ color: 'green' }}>{successMessage}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Department Name</label>
          <input
            type="text"
            value={departmentName}
            onChange={(e) => setDepartmentName(e.target.value)}
          />
        </div>
        <div>
          <label>Department Description</label>
          <textarea
            value={departmentDescription}
            onChange={(e) => setDepartmentDescription(e.target.value)}
          />
        </div>
        <button type="submit">Add Department</button>
      </form>
    </div>
  );
};

export default DepartmentAddPage;
