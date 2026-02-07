'use client';

import { useState, useEffect } from 'react';
import { Task, CreateTaskInput, UpdateTaskInput } from '@/lib/types/task';
import TaskCard from '@/components/TaskCard';
import TaskForm from '@/components/TaskForm';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Search, Plus, Grid3X3, List, Table } from 'lucide-react';
import { toast } from 'sonner';

// Mock API functions - these would be replaced with actual API calls
const mockGetTasks = async (): Promise<Task[]> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Return mock tasks
  return [
    {
      id: '1',
      title: 'Sample Task',
      description: 'This is a sample task to demonstrate the UI.',
      completed: false,
      userId: 'user-1',
      createdAt: new Date(),
      updatedAt: new Date(),
    },
    {
      id: '2',
      title: 'Another Sample Task',
      description: 'This is another sample task with a longer description to test the read more functionality. It contains more text to see how the expansion works when the description is lengthy.',
      completed: true,
      userId: 'user-1',
      createdAt: new Date(Date.now() - 86400000), // 1 day ago
      updatedAt: new Date(Date.now() - 43200000), // 12 hours ago
    },
  ];
};

const mockCreateTask = async (taskData: CreateTaskInput): Promise<Task> => {
  await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API delay

  return {
    id: Math.random().toString(36).substring(7),
    ...taskData,
    completed: false,
    userId: 'user-1', // Add the missing userId
    createdAt: new Date(),
    updatedAt: new Date(),
  };
};

const mockUpdateTask = async (taskData: UpdateTaskInput): Promise<Task> => {
  await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API delay
  
  return {
    id: taskData.id,
    title: taskData.title || 'Untitled Task',
    description: taskData.description,
    completed: taskData.completed ?? false,
    userId: 'user-1', // In a real app, this would come from auth context
    createdAt: new Date(Date.now() - 86400000), // 1 day ago
    updatedAt: new Date(),
  };
};

const mockDeleteTask = async (taskId: string): Promise<void> => {
  await new Promise(resolve => setTimeout(resolve, 500)); // Simulate API delay
};

const mockToggleTaskCompletion = async (taskId: string, completed: boolean): Promise<Task> => {
  await new Promise(resolve => setTimeout(resolve, 300)); // Simulate API delay
  
  return {
    id: taskId,
    title: 'Updated Task',
    description: 'This task was updated',
    completed,
    userId: 'user-1',
    createdAt: new Date(Date.now() - 86400000),
    updatedAt: new Date(),
  };
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'title' | 'date'>('date');
  const [viewMode, setViewMode] = useState<'card' | 'list' | 'table'>('card');

  // Load tasks on component mount
  useEffect(() => {
    const loadTasks = async () => {
      try {
        const loadedTasks = await mockGetTasks();
        setTasks(loadedTasks);
        setFilteredTasks(loadedTasks);
      } catch (error) {
        console.error('Failed to load tasks:', error);
        toast.error('Failed to load tasks');
      } finally {
        setIsLoading(false);
      }
    };

    loadTasks();
  }, []);

  // Apply search and sorting filters
  useEffect(() => {
    let result = [...tasks];

    // Apply search filter
    if (searchQuery) {
      result = result.filter(task =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchQuery.toLowerCase()))
      );
    }

    // Apply sorting
    result.sort((a, b) => {
      if (sortBy === 'title') {
        return a.title.localeCompare(b.title);
      } else {
        return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
      }
    });

    setFilteredTasks(result);
  }, [tasks, searchQuery, sortBy]);

  const handleCreateTask = async (taskData: CreateTaskInput) => {
    setIsSubmitting(true);
    try {
      const newTask = await mockCreateTask(taskData);
      setTasks(prev => [newTask, ...prev]);
      setIsFormOpen(false);
      toast.success('Task created successfully!');
    } catch (error) {
      console.error('Failed to create task:', error);
      toast.error('Failed to create task');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateTask = async (taskData: UpdateTaskInput) => {
    setIsSubmitting(true);
    try {
      const updatedTask = await mockUpdateTask(taskData);
      setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
      setEditingTask(null);
      setIsFormOpen(false);
      toast.success('Task updated successfully!');
    } catch (error) {
      console.error('Failed to update task:', error);
      toast.error('Failed to update task');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    try {
      await mockDeleteTask(taskId);
      setTasks(prev => prev.filter(t => t.id !== taskId));
      toast.success('Task deleted successfully!');
    } catch (error) {
      console.error('Failed to delete task:', error);
      toast.error('Failed to delete task');
    }
  };

  const handleToggleTaskCompletion = async (taskId: string, completed: boolean) => {
    try {
      const updatedTask = await mockToggleTaskCompletion(taskId, completed);
      setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
    } catch (error) {
      console.error('Failed to update task completion:', error);
      toast.error('Failed to update task status');
    }
  };

  const handleFormSubmit = (data: CreateTaskInput | UpdateTaskInput) => {
    if ('id' in data && data.id) {
      // This is an update operation
      handleUpdateTask(data as UpdateTaskInput);
    } else {
      // This is a create operation
      handleCreateTask(data as CreateTaskInput);
    }
  };

  const openEditTask = (task: Task) => {
    setEditingTask(task);
    setIsFormOpen(true);
  };

  const openCreateTask = () => {
    setEditingTask(null);
    setIsFormOpen(true);
  };

  // Listen for the custom event to open the task modal
  useEffect(() => {
    const handleOpenTaskModal = () => {
      openCreateTask();
    };

    window.addEventListener('openTaskModal', handleOpenTaskModal);

    return () => {
      window.removeEventListener('openTaskModal', handleOpenTaskModal);
    };
  }, []);

  return (
    <div className="container mx-auto py-6 px-4">
      {/* Header with search, sort, and add button */}
      <div className="mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <h1 className="text-3xl font-bold">My Tasks</h1>
          
          <div className="flex items-center gap-2">
            <div className="relative">
              <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 text-muted-foreground h-4 w-4" />
              <Input
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-8 w-full md:w-64"
              />
            </div>
            
            <Select value={sortBy} onValueChange={(value: 'title' | 'date') => setSortBy(value)}>
              <SelectTrigger className="w-32">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="title">Title</SelectItem>
                <SelectItem value="date">Date</SelectItem>
              </SelectContent>
            </Select>
            
            <div className="flex border rounded-md p-1 bg-secondary">
              <Button
                variant={viewMode === 'card' ? 'secondary' : 'ghost'}
                size="icon"
                onClick={() => setViewMode('card')}
                className="h-8 w-8"
                aria-label="Card view"
              >
                <Grid3X3 className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'secondary' : 'ghost'}
                size="icon"
                onClick={() => setViewMode('list')}
                className="h-8 w-8"
                aria-label="List view"
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
            
            <Button onClick={openCreateTask}>
              <Plus className="mr-2 h-4 w-4" />
              Add Task
            </Button>
          </div>
        </div>
      </div>

      {/* Task list */}
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
        </div>
      ) : filteredTasks.length === 0 ? (
        <div className="text-center py-12">
          <h3 className="text-xl font-medium mb-2">No tasks yet</h3>
          <p className="text-muted-foreground mb-4">Get started by creating your first task</p>
          <Button onClick={openCreateTask}>
            <Plus className="mr-2 h-4 w-4" />
            Create Task
          </Button>
        </div>
      ) : (
        <div className={`grid ${
          viewMode === 'card' 
            ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' 
            : 'grid-cols-1 gap-2'
        }`}>
          {filteredTasks.map(task => (
            <div key={task.id} className={viewMode === 'list' ? 'border rounded-lg' : ''}>
              <TaskCard
                task={task}
                onUpdate={(taskId, data) => {
                  // Convert the update data to the format expected by handleUpdateTask
                  handleUpdateTask({ id: taskId, ...data });
                }}
                onDelete={handleDeleteTask}
                onToggleComplete={handleToggleTaskCompletion}
              />
            </div>
          ))}
        </div>
      )}

      {/* Task Form Modal */}
      <TaskForm
        isOpen={isFormOpen}
        onClose={() => {
          setIsFormOpen(false);
          setEditingTask(null);
        }}
        onSubmit={handleFormSubmit}
        task={editingTask}
        isSubmitting={isSubmitting}
      />
    </div>
  );
}