from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from typing import Any

from flask import Flask, jsonify, request


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)

    db_path = os.path.join(app.instance_path, "aceest_fitness.db")
    app.config.from_mapping(
        DATABASE=db_path,
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    def get_db() -> sqlite3.Connection:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db() -> None:
        with closing(get_db()) as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    age INTEGER NOT NULL,
                    program TEXT NOT NULL,
                    membership_status TEXT NOT NULL DEFAULT 'Active'
                );

                CREATE TABLE IF NOT EXISTS workouts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_id INTEGER NOT NULL,
                    workout_type TEXT NOT NULL,
                    duration_minutes INTEGER NOT NULL,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY(client_id) REFERENCES clients(id)
                );
                """
            )
            conn.commit()

    @app.get("/health")
    def health() -> tuple[dict[str, str], int]:
        return {"status": "ok"}, 200

    @app.post("/clients")
    def create_client() -> tuple[Any, int]:
        payload = request.get_json(silent=True) or {}
        required = ("name", "age", "program")
        missing = [field for field in required if field not in payload]
        if missing:
            return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400

        try:
            with closing(get_db()) as conn:
                cursor = conn.execute(
                    """
                    INSERT INTO clients(name, age, program, membership_status)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        payload["name"],
                        int(payload["age"]),
                        payload["program"],
                        payload.get("membership_status", "Active"),
                    ),
                )
                conn.commit()
                client_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            return jsonify({"error": "client already exists"}), 409
        except (TypeError, ValueError):
            return jsonify({"error": "age must be an integer"}), 400

        return jsonify({"id": client_id, "message": "client created"}), 201

    @app.get("/clients")
    def list_clients() -> tuple[Any, int]:
        with closing(get_db()) as conn:
            rows = conn.execute(
                "SELECT id, name, age, program, membership_status FROM clients ORDER BY name"
            ).fetchall()

        clients = [dict(row) for row in rows]
        return jsonify(clients), 200

    @app.post("/workouts")
    def create_workout() -> tuple[Any, int]:
        payload = request.get_json(silent=True) or {}
        required = ("client_id", "workout_type", "duration_minutes")
        missing = [field for field in required if field not in payload]
        if missing:
            return jsonify({"error": f"missing fields: {', '.join(missing)}"}), 400

        try:
            client_id = int(payload["client_id"])
            duration = int(payload["duration_minutes"])
        except (TypeError, ValueError):
            return jsonify({"error": "client_id and duration_minutes must be integers"}), 400

        with closing(get_db()) as conn:
            existing = conn.execute(
                "SELECT id FROM clients WHERE id = ?",
                (client_id,),
            ).fetchone()
            if not existing:
                return jsonify({"error": "client not found"}), 404

            cursor = conn.execute(
                """
                INSERT INTO workouts(client_id, workout_type, duration_minutes, notes)
                VALUES (?, ?, ?, ?)
                """,
                (
                    client_id,
                    payload["workout_type"],
                    duration,
                    payload.get("notes", ""),
                ),
            )
            conn.commit()
            workout_id = cursor.lastrowid

        return jsonify({"id": workout_id, "message": "workout logged"}), 201

    @app.get("/clients/<int:client_id>/workouts")
    def get_client_workouts(client_id: int) -> tuple[Any, int]:
        with closing(get_db()) as conn:
            rows = conn.execute(
                """
                SELECT id, client_id, workout_type, duration_minutes, notes
                FROM workouts
                WHERE client_id = ?
                ORDER BY id DESC
                """,
                (client_id,),
            ).fetchall()

        return jsonify([dict(row) for row in rows]), 200

    init_db()
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
