export type TaskStatus = 'pending' | 'in_progress' | 'completed';
export type TaskSPriority = 'low' | 'medium' | 'high';

export interface Task {
  id: number;
  title: string;
  description: string;
  priority: TaskSPriority;
  status: TaskStatus;
  created_at: string;
}