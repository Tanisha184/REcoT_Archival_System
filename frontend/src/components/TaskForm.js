import React, { useState } from 'react';
import { createTask } from '../api';

const TaskForm = () => {
    const [departmentId, setDepartmentId] = useState('');
    const [title, setTitle] = useState('');
    const [status, setStatus] = useState('Pending');
    const [description, setDescription] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        await createTask(departmentId, title, status, description);
        // Optionally reset the form or provide feedback
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Department ID" value={departmentId} onChange={(e) => setDepartmentId(e.target.value)} required />
            <input type="text" placeholder="Task Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
            <textarea placeholder="Task Description" value={description} onChange={(e) => setDescription(e.target.value)} required />
            <button type="submit">Create Task</button>
        </form>
    );
};

export default TaskForm;
