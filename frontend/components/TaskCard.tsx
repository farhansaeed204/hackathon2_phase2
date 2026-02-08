'use client';

import { Task } from '@/lib/types/task';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import { Trash2, Edit3 } from 'lucide-react';
import { useState } from 'react';
import { motion } from 'framer-motion';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onToggleComplete: (taskId: string, completed: boolean) => void;
}

export default function TaskCard({ task, onEdit, onDelete, onToggleComplete }: TaskCardProps) {
  const [expanded] = useState(false);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.2 }}
    >
      <Card className={`transition-all duration-200 hover:shadow-md ${task.completed ? 'bg-muted/30' : ''}`}>
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <Checkbox
              checked={task.completed}
              onCheckedChange={(checked) => onToggleComplete(task.id, !!checked)}
              className="mt-1"
              aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
            />
            <div className="flex-1 min-w-0">
              <h3 className={`font-medium truncate ${task.completed ? 'line-through text-muted-foreground' : ''}`}>
                {task.title}
              </h3>
              {task.description && (
                <div className="mt-2 text-sm text-muted-foreground">
                  <p>{task.description}</p>
                </div>
              )}
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-end gap-2 p-4 pt-0 border-t">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onEdit(task)}
            aria-label="Edit task"
          >
            <Edit3 className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onDelete(task.id)}
            aria-label="Delete task"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </CardFooter>
      </Card>
    </motion.div>
  );
}