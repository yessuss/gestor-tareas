import { Component, OnInit } from '@angular/core';
import { TaskService } from './services/task.service';
import { Task, TaskStatus } from './models/task.model';

@Component({
  selector: 'app-root',
  standalone: false,
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  tasks: Task[] = [];

  newTitle = '';
  newDescription = '';
  newPriority ='';

  statusLabels: Record<string, string> = {
    pending: 'Pendiente',
    in_progress: 'En progreso',
    completed: 'Completada'
  };

  priorityLabels: Record<string, string> = {
    low: 'Baja',
    medium: 'Media',
    high: 'Alta'
  };
  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.fetchTasks();
  }

  fetchTasks(): void {
    this.taskService.list().subscribe({
      next: (tasks) => (this.tasks = tasks),
      error: (err) => console.error('Error al obtener la tarea:', err)
    });
  }

  addTask(): void {
    if (!this.newTitle.trim()) {
      alert('Titulo no puede ir vacio');
      return;
    }

    if (!this.newPriority) {
      alert('Por favor seleccione una prioridad');
      return;
    }
    this.taskService.create(this.newTitle, this.newDescription, this.newPriority).subscribe({
      next: () => {
        this.newTitle = '';
        this.newDescription = '';
        this.newPriority='';
        this.fetchTasks(); // recarga la lista para mostrar la nueva tarea
      },
      error: (err) => console.error('Error al crear tarea:', err)
    });
  }

  advanceStatus(task: Task): void {
    let next: TaskStatus | null = null;
    if (task.status === 'pending') next = 'in_progress';
    else if (task.status === 'in_progress') next = 'completed';

    if (!next) return;

    this.taskService.changeStatus(task.id, next).subscribe({
      next: () => this.fetchTasks(),
      error: (err) => console.error('Error al cambiar estado:', err)
    });
  }

  deleteTask(task: Task): void {
    this.taskService.delete(task.id).subscribe({
      next: () => this.fetchTasks(),
      error: (err) => console.error('Error al eliminar:', err)
    });
  }

}