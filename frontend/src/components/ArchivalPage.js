import React, { useState, useEffect } from 'react';

const ArchivalPage = () => {
    const [completedTasks, setCompletedTasks] = useState([]);

    useEffect(() => {
        // Simulate fetching completed tasks from the backend
        const tasksData = {
            "cs": [{"title": "CS Task 1", "status": "In Progress"}, {"title": "CS Task 2", "status": "Completed"}],
            "ee": [{"title": "EE Task 1", "status": "Not Started"}],
            "me": [{"title": "ME Task 1", "status": "In Progress"}],
            "bba": [{"title": "BBA Task 1", "status": "Completed"}],
            "eco": [{"title": "Eco Task 1", "status": "Not Started"}],
        };

        // Filter completed tasks
        const completed = Object.values(tasksData).flat().filter(task => task.status === "Completed");
        setCompletedTasks(completed);
    }, []);

    return (
        <div className="archival-container">
            <h1>Completed Tasks</h1>
            {completedTasks.length > 0 ? (
                <ul>
                    {completedTasks.map((task, index) => (
                        <li key={index}>{task.title}</li>
                    ))}
                </ul>
            ) : (
                <p>No completed tasks available.</p>
            )}
        </div>
    );
};

export default ArchivalPage;
