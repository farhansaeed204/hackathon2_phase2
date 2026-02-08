// Mock API functions for authentication
export async function signup(email: string, password: string) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock response
  return {
    success: true,
    user: {
      id: '1',
      email,
    },
    token: 'mock-jwt-token'
  };
}

export async function login(email: string, password: string) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock response
  return {
    success: true,
    user: {
      id: '1',
      email,
    },
    token: 'mock-jwt-token'
  };
}

// Mock API functions for tasks
export async function getTasks() {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock response
  return [
    { id: '1', title: 'Sample Task', description: 'This is a sample task', completed: false },
    { id: '2', title: 'Another Task', description: 'This is another sample task', completed: true }
  ];
}

export async function createTask(task: { title: string; description?: string; completed: boolean }) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock response
  return {
    id: Math.random().toString(36).substring(7),
    ...task
  };
}

export async function updateTask(id: string, task: { title?: string; description?: string; completed?: boolean }) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock response
  return {
    id,
    title: task.title || 'Updated Task',
    description: task.description,
    completed: task.completed || false
  };
}

export async function deleteTask(id: string) {
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 500));
  
  // Mock response
  return { success: true };
}