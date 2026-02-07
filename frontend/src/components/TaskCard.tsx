"use client";

import { useState } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Edit, Trash2, Save, X } from "lucide-react";
import { Task, UpdateTaskData } from "@/lib/types/task";

interface TaskCardProps {
  task: Task;
  onUpdate: (taskId: string, data: UpdateTaskData) => void;
  onDelete: (taskId: string) => void;
  onToggleComplete: (taskId: string, completed: boolean) => void;
}

export default function TaskCard({ task, onUpdate, onDelete, onToggleComplete }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description || "");
  const [isTruncated, setIsTruncated] = useState(true);

  const MAX_DESC_LENGTH = 100;

  const handleSave = () => {
    onUpdate(task.id, { title, description });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setTitle(task.title);
    setDescription(task.description || "");
    setIsEditing(false);
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  const toggleComplete = () => {
    onToggleComplete(task.id, !task.completed);
  };

  const toggleTruncate = () => {
    setIsTruncated(!isTruncated);
  };

  const formattedDate = new Date(task.createdAt).toLocaleDateString();

  return (
    <Card className={`transition-all duration-200 ${task.completed ? "opacity-70 bg-green-50" : ""}`}>
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          <Checkbox
            checked={task.completed}
            onCheckedChange={toggleComplete}
            className="mt-1"
          />

          <div className="flex-1 min-w-0">
            {isEditing ? (
              <div className="space-y-3">
                <Input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="text-lg font-semibold"
                />
                <Textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Task description..."
                  rows={3}
                />
                <div className="flex gap-2">
                  <Button onClick={handleSave} size="sm" className="flex items-center gap-1">
                    <Save className="w-4 h-4" /> Save
                  </Button>
                  <Button onClick={handleCancel} variant="outline" size="sm" className="flex items-center gap-1">
                    <X className="w-4 h-4" /> Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div>
                <h3 className={`text-lg font-semibold ${task.completed ? "line-through" : ""}`}>
                  {title}
                </h3>

                {description && (
                  <p className="text-gray-600 mt-2 text-sm">
                    {description.length > MAX_DESC_LENGTH && isTruncated
                      ? `${description.substring(0, MAX_DESC_LENGTH)}... `
                      : description}

                    {description.length > MAX_DESC_LENGTH && (
                      <button
                        onClick={toggleTruncate}
                        className="text-blue-600 hover:underline text-xs"
                      >
                        {isTruncated ? "Read more" : "Show less"}
                      </button>
                    )}
                  </p>
                )}

                <p className="text-xs text-gray-500 mt-2">
                  Created: {formattedDate}
                </p>
              </div>
            )}
          </div>

          {!isEditing && (
            <div className="flex gap-1">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEditing(true)}
                className="h-8 w-8 p-0"
              >
                <Edit className="w-4 h-4" />
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={handleDelete}
                className="h-8 w-8 p-0"
              >
                <Trash2 className="w-4 h-4" />
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}