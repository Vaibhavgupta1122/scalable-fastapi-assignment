import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Task, TaskCreate, TaskUpdate } from '../types/auth';
import { taskService } from '../services/api';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [formData, setFormData] = useState<TaskCreate>({
    title: '',
    description: '',
    priority: 'medium'
  });

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const tasksData = await taskService.getTasks();
      setTasks(tasksData);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to fetch tasks');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const newTask = await taskService.createTask(formData);
      setTasks([...tasks, newTask]);
      setFormData({ title: '', description: '', priority: 'medium' });
      setShowCreateForm(false);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to create task');
    }
  };

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask) return;

    try {
      const updatedTask = await taskService.updateTask(editingTask.id, formData as TaskUpdate);
      setTasks(tasks.map(task => task.id === editingTask.id ? updatedTask : task));
      setEditingTask(null);
      setFormData({ title: '', description: '', priority: 'medium' });
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await taskService.deleteTask(taskId);
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.response?.data?.error?.message || 'Failed to delete task');
    }
  };

  const startEdit = (task: Task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description || '',
      priority: task.priority
    });
  };

  const cancelEdit = () => {
    setEditingTask(null);
    setFormData({ title: '', description: '', priority: 'medium' });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return '#28a745';
      case 'in_progress': return '#ffc107';
      default: return '#6c757d';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#dc3545';
      case 'medium': return '#ffc107';
      default: return '#28a745';
    }
  };

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Task Management Dashboard</h1>
          <div className="user-info">
            <span>Welcome, {user?.full_name || user?.username}!</span>
            <span className="role-badge">{user?.role}</span>
            <button onClick={logout} className="logout-btn">Logout</button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        {error && <div className="error-message">{error}</div>}

        <div className="tasks-section">
          <div className="section-header">
            <h2>Tasks</h2>
            <button 
              onClick={() => setShowCreateForm(true)} 
              className="create-btn"
            >
              Create New Task
            </button>
          </div>

          {(showCreateForm || editingTask) && (
            <div className="task-form">
              <h3>{editingTask ? 'Edit Task' : 'Create New Task'}</h3>
              <form onSubmit={editingTask ? handleUpdateTask : handleCreateTask}>
                <div className="form-group">
                  <label>Title:</label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({...formData, title: e.target.value})}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Description:</label>
                  <textarea
                    value={formData.description}
                    onChange={(e) => setFormData({...formData, description: e.target.value})}
                    rows={3}
                  />
                </div>
                <div className="form-group">
                  <label>Priority:</label>
                  <select
                    value={formData.priority}
                    onChange={(e) => setFormData({...formData, priority: e.target.value as 'low' | 'medium' | 'high'})}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
                <div className="form-actions">
                  <button type="submit" className="submit-btn">
                    {editingTask ? 'Update' : 'Create'}
                  </button>
                  <button type="button" onClick={editingTask ? cancelEdit : () => setShowCreateForm(false)} className="cancel-btn">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          <div className="tasks-list">
            {tasks.length === 0 ? (
              <p>No tasks found. Create your first task!</p>
            ) : (
              tasks.map(task => (
                <div key={task.id} className="task-card">
                  <div className="task-header">
                    <h3>{task.title}</h3>
                    <div className="task-badges">
                      <span className="status-badge" style={{ backgroundColor: getStatusColor(task.status) }}>
                        {task.status.replace('_', ' ')}
                      </span>
                      <span className="priority-badge" style={{ backgroundColor: getPriorityColor(task.priority) }}>
                        {task.priority}
                      </span>
                    </div>
                  </div>
                  {task.description && (
                    <p className="task-description">{task.description}</p>
                  )}
                  <div className="task-meta">
                    <small>Created: {new Date(task.created_at).toLocaleDateString()}</small>
                    {task.completed_at && (
                      <small>Completed: {new Date(task.completed_at).toLocaleDateString()}</small>
                    )}
                  </div>
                  <div className="task-actions">
                    <button onClick={() => startEdit(task)} className="edit-btn">Edit</button>
                    <button onClick={() => handleDeleteTask(task.id)} className="delete-btn">Delete</button>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
