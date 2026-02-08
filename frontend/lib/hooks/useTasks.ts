import { useState, useEffect } from 'react';
import { Task } from '@/types/task';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load auth token from localStorage
  const getToken = () => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('authToken');
    }
    return null;
  };

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const token = getToken();
      
      // In a real app, this would be: const response = await fetch('/api/tasks/', {...})
      // For now, we'll simulate the API call
      console.log('Fetching tasks with token:', token);
      
      // Simulated response
      setTimeout(() => {
        setTasks([
          { id: '1', title: 'Sample Task 1', description: 'This is a sample task', completed: false, user_id: 'user1' },
          { id: '2', title: 'Sample Task 2', description: 'This is another sample task', completed: true, user_id: 'user1' }
        ]);
        setLoading(false);
      }, 500);
    } catch (err) {
      setError('Failed to fetch tasks');
      setLoading(false);
    }
  };

  const createTask = async (taskData: Omit<Task, 'id' | 'user_id'>) => {
    try {
      const token = getToken();
      
      // In a real app, this would be: const response = await fetch('/api/tasks/', {...})
      console.log('Creating task with token:', token, 'data:', taskData);
      
      // Simulated response
      const newTask: Task = {
        id: Date.now().toString(),
        ...taskData,
        user_id: 'user1'
      };
      
      setTasks([...tasks, newTask]);
    } catch (err) {
      setError('Failed to create task');
    }
  };

  const updateTask = async (task: Task) => {
    try {
      const token = getToken();
      
      // In a real app, this would be: const response = await fetch(`/api/tasks/${task.id}`, {...})
      console.log('Updating task with token:', token, 'data:', task);
      
      setTasks(tasks.map(t => t.id === task.id ? task : t));
    } catch (err) {
      setError('Failed to update task');
    }
  };

  const deleteTask = async (id: string) => {
    try {
      const token = getToken();
      
      // In a real app, this would be: const response = await fetch(`/api/tasks/${id}`, {...})
      console.log('Deleting task with token:', token, 'id:', id);
      
      setTasks(tasks.filter(task => task.id !== id));
    } catch (err) {
      setError('Failed to delete task');
    }
  };

  const toggleTask = async (id: string) => {
    try {
      const token = getToken();
      
      // In a real app, this would be: const response = await fetch(`/api/tasks/${id}/toggle`, {...})
      console.log('Toggling task with token:', token, 'id:', id);
      
      setTasks(tasks.map(task => 
        task.id === id ? { ...task, completed: !task.completed } : task
      ));
    } catch (err) {
      setError('Failed to toggle task');
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return {
    tasks,
    loading,
    error,
    createTask,
    updateTask,
    deleteTask,
    toggleTask
  };
};