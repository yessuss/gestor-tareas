from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import enum
from datetime import datetime, timezone
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
db_user = os.getenv("DB_USER", "taskuser")
db_password = os.getenv("DB_PASSWORD", "taskpassword")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "taskmanager")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

db = SQLAlchemy(app)

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(db.Model):
    __tablename__= "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(
        db.Enum(TaskPriority, name="task_priority"),
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    status = db.Column(
        db.Enum(TaskStatus, name="task_status"),
        nullable=False,
        default=TaskStatus.PENDING,
    )
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }
    

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error":"El campo title es obligatorio"}), 400
    
    priority_value = data.get("priority", "MEDIUM")
    try:
        priority = TaskPriority(priority_value)
    except ValueError:
        return jsonify({"error": f"priority inválido: {priority_value}"}), 400
    
    task = Task(title=title, description=data.get("description",""), priority = priority)
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()),201

@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks]), 200

@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    if "title" in data:
        task.title = data["title"]
    if "description" in data:
        task.description = data["description"]

    db.session.commit()
    return jsonify(task.to_dict()), 200

@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada"}), 200

@app.route("/api/tasks/<int:task_id>/status", methods=["PATCH"])
def change_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()

    new_status = data.get("status")
    try:
        task.status = TaskStatus(new_status)
    except ValueError:
        return jsonify({"error": f"status inválido: {new_status}"}), 400

    db.session.commit()
    return jsonify(task.to_dict()), 200

@app.route("/")
def home():
    return "Hola el servidor Flask esta funcionando"

@app.route("/test-db")
def test_db():
    db.session.execute(db.text("SELECT 1"))
    return "¡Conexión a la base de datos exitosa!"


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
    
