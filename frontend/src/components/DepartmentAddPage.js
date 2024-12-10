import React, { useState } from 'react';

const DepartmentAddPage = () => {
  const [departmentName, setDepartmentName] = useState('');
  const [departmentDescription, setDepartmentDescription] = useState('');

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
          // Redirect to department list page after successful addition
          window.location.href = '/departments';
        }
      });
  };

  return (
    <div>
      <h1>Add New Department</h1>
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
