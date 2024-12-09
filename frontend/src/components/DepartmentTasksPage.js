import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom'; // To access the dynamic route params

const DepartmentTasksPage = () => {
  const { department } = useParams(); // Access department name (e.g., cs, ee)
  const [tasks, setTasks] = useState([]);

  // Fetch department-specific tasks when the component mounts
  useEffect(() => {
    // Assuming you have an API endpoint to fetch tasks for a department
    const fetchTasks = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/departments/${department}/tasks`);
        const data = await response.json();
        setTasks(data.tasks); // Assuming the response contains a "tasks" array
      } catch (error) {
        console.error('Error fetching tasks:', error);
      }
    };

    fetchTasks();
  }, [department]); // Fetch tasks when department changes

  return (
    <div>
      <h1>{department} Department Tasks</h1>
      {tasks.length > 0 ? (
        <ul>
          {tasks.map((task, index) => (
            <li key={index}>
              <strong>{task.title}</strong>
              <p>Status: {task.status}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No tasks available for this department.</p>
      )}
    </div>
  );
};

export default DepartmentTasksPage;
