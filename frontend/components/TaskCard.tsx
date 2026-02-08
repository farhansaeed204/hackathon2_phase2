import { useState } from 'react';
import { Task } from '@/types/task';

interface TaskCardProps {
  task: Task;
  onUpdate: (task: Task) => void;
  onDelete: (id: string) => void;
  onToggle: (id: string) => void;
}

export default function TaskCard({ task, onUpdate, onDelete, onToggle }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || '');

  const handleSave = () => {
    onUpdate({ ...task, title, description });
    setIsEditing(false);
  };

  return (
    <div className={`rounded-lg border p-4 shadow-sm ${task.completed ? 'bg-green-50' : 'bg-white'}`}>
      {isEditing ? (
        <div className="space-y-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full rounded border px-2 py-1 text-lg font-semibold"
            autoFocus
          />
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full rounded border px-2 py-1"
            rows={3}
          />
          <div className="flex justify-end space-x-2">
            <button
              onClick={() => setIsEditing(false)}
              className="rounded bg-gray-200 px-3 py-1 text-sm hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="rounded bg-blue-500 px-3 py-1 text-sm text-white hover:bg-blue-600"
            >
              Save
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-start justify-between">
            <div>
              <h3 className={`text-lg font-semibold ${task.completed ? 'line-through text-gray-500' : ''}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="mt-1 text-gray-600">{task.description}</p>
              )}
            </div>
            <div className="flex space-x-1">
              <button
                onClick={() => setIsEditing(true)}
                className="rounded p-1 text-gray-500 hover:bg-gray-100"
                aria-label="Edit task"
              >
                ✏️
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="rounded p-1 text-gray-500 hover:bg-gray-100"
                aria-label="Delete task"
              >
                🗑️
              </button>
            </div>
          </div>
          <div className="mt-3 flex items-center justify-between">
            <span className={`text-xs ${task.completed ? 'text-green-600' : 'text-gray-500'}`}>
              {task.completed ? 'Completed' : 'Pending'}
            </span>
            <button
              onClick={() => onToggle(task.id)}
              className={`rounded px-3 py-1 text-xs ${
                task.completed
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              }`}
            >
              {task.completed ? 'Undo' : 'Complete'}
            </button>
          </div>
        </>
      )}
    </div>
  );
}