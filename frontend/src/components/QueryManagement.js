import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const QueryManagement = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({
    department_id: '',
    title: '',
    status: '',
    start_date: '',
    end_date: ''
  });
  const [tasks, setTasks] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch departments and report templates on component mount
    const fetchInitialData = async () => {
      try {
        const [deptsResponse, templatesResponse] = await Promise.all([
          axios.get('http://localhost:5000/api/departments'),
          axios.get('http://localhost:5000/api/report-templates')
        ]);
        setDepartments(deptsResponse.data.departments);
        setTemplates(templatesResponse.data.templates);
      } catch (error) {
        console.error('Error fetching initial data:', error);
      }
    };
    fetchInitialData();
  }, []);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:5000/api/tasks/search', filters);
      setTasks(response.data.tasks);
    } catch (error) {
      console.error('Error searching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    if (!selectedTemplate) {
      alert('Please select a report template');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/api/reports/generate', {
        template_name: selectedTemplate,
        filters
      });
      
      // Handle the report data - could be displayed in a new window or downloaded
      const reportWindow = window.open('', '_blank');
      reportWindow.document.write(`
        <html>
          <head>
            <title>Task Report</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; }
              table { border-collapse: collapse; width: 100%; }
              th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
              th { background-color: #f4f4f4; }
            </style>
          </head>
          <body>
            <h1>Task Report</h1>
            <p>Generated at: ${response.data.report.generated_at}</p>
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Department</th>
                  <th>Status</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                ${response.data.report.data.map(task => `
                  <tr>
                    <td>${task.title}</td>
                    <td>${task.department_id}</td>
                    <td>${task.status}</td>
                    <td>${task.description}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </body>
        </html>
      `);
      reportWindow.document.close();
    } catch (error) {
      console.error('Error generating report:', error);
      alert('Error generating report');
    }
  };

  return (
    <div className="query-management">
      <h2>Query Management</h2>
      
      <div className="filters">
        <select 
          name="department_id" 
          value={filters.department_id}
          onChange={handleFilterChange}
        >
          <option value="">Select Department</option>
          {departments.map(dept => (
            <option key={dept._id} value={dept._id}>
              {dept.name}
            </option>
          ))}
        </select>

        <input
          type="text"
          name="title"
          placeholder="Search by title"
          value={filters.title}
          onChange={handleFilterChange}
        />

        <select 
          name="status" 
          value={filters.status}
          onChange={handleFilterChange}
        >
          <option value="">Select Status</option>
          <option value="Not Started">Not Started</option>
          <option value="In Progress">In Progress</option>
          <option value="Pending Approval">Pending Approval</option>
          <option value="Done">Done</option>
        </select>

        <input
          type="date"
          name="start_date"
          value={filters.start_date}
          onChange={handleFilterChange}
        />

        <input
          type="date"
          name="end_date"
          value={filters.end_date}
          onChange={handleFilterChange}
        />

        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="results">
        <h3>Search Results</h3>
        {tasks.length > 0 ? (
          <div>
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Department</th>
                  <th>Status</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {tasks.map(task => (
                  <tr key={task._id}>
                    <td>{task.title}</td>
                    <td>{task.department_id}</td>
                    <td>{task.status}</td>
                    <td>{task.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div className="report-generation">
              <select
                value={selectedTemplate}
                onChange={(e) => setSelectedTemplate(e.target.value)}
              >
                <option value="">Select Report Template</option>
                {templates.map(template => (
                  <option key={template._id} value={template.name}>
                    {template.name}
                  </option>
                ))}
              </select>

              <button onClick={handleGenerateReport}>
                Generate Report
              </button>
            </div>
          </div>
        ) : (
          <p>No tasks found matching your criteria.</p>
        )}
      </div>
    </div>
  );
};

export default QueryManagement;
