
from flask import Flask, jsonify, render_template, request, redirect, url_for
from datetime import datetime
from pathlib import Path
import sqlite3

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE = DATA_DIR / "deployments.db"


# Database initialization
def init_db():
    DATA_DIR.mkdir(exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            status TEXT NOT NULL,
            duration_seconds REAL NOT NULL,
            failure_reason TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # Add deployment_type to an existing database safely
    columns = [
        row[1] for row in conn.execute(
            "PRAGMA table_info(deployments)"
        ).fetchall()
    ]

    if "deployment_type" not in columns:
        conn.execute("""
            ALTER TABLE deployments
            ADD COLUMN deployment_type TEXT NOT NULL
            DEFAULT 'Not specified'
        """)

    conn.commit()
    conn.close()


# Home dashboard
@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    deployments = conn.execute(
        "SELECT * FROM deployments ORDER BY id DESC"
    ).fetchall()

    total = conn.execute(
        "SELECT COUNT(*) FROM deployments"
    ).fetchone()[0]

    successful = conn.execute(
        "SELECT COUNT(*) FROM deployments WHERE status = 'Success'"
    ).fetchone()[0]

    failed = conn.execute(
        "SELECT COUNT(*) FROM deployments WHERE status = 'Failed'"
    ).fetchone()[0]

    failure_rate = round(
        (failed / total) * 100, 2
    ) if total > 0 else 0

    failure_analysis = conn.execute("""
        SELECT
            COALESCE(NULLIF(failure_reason, ''), 'Reason not provided') AS reason,
            COUNT(*) AS occurrences
        FROM deployments
        WHERE status = 'Failed'
        GROUP BY reason
        ORDER BY occurrences DESC
    """).fetchall()

    # Average deployment time by deployment method
    manual_avg = conn.execute("""
        SELECT AVG(duration_seconds)
        FROM deployments
        WHERE deployment_type = 'Manual'
    """).fetchone()[0]

    automated_avg = conn.execute("""
        SELECT AVG(duration_seconds)
        FROM deployments
        WHERE deployment_type = 'Automated'
    """).fetchone()[0]

    conn.close()

    manual_avg = round(manual_avg, 2) if manual_avg is not None else None
    automated_avg = round(automated_avg, 2) if automated_avg is not None else None

    return render_template(
        "index.html",
        deployments=deployments,
        total=total,
        successful=successful,
        failed=failed,
        failure_rate=failure_rate,
        failure_analysis=failure_analysis,
        manual_avg=manual_avg,
        automated_avg=automated_avg
    )


# Record deployment
@app.route("/record", methods=["POST"])
def record_deployment():
    version = request.form.get("version", "").strip()
    status = request.form.get("status", "").strip()
    duration = request.form.get("duration", "").strip()
    deployment_type = request.form.get("deployment_type", "").strip()
    failure_reason = request.form.get("failure_reason", "").strip()

    if not version or status not in ["Success", "Failed"]:
        return "Invalid deployment details", 400

    if deployment_type not in ["Manual", "Automated"]:
        return "Invalid deployment type", 400

    try:
        duration = float(duration)
        if duration < 0:
            raise ValueError
    except ValueError:
        return "Invalid deployment duration", 400

    if status == "Success":
        failure_reason = None

    conn = sqlite3.connect(DATABASE)

    conn.execute("""
        INSERT INTO deployments
        (version, status, duration_seconds, failure_reason,
         created_at, deployment_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        version,
        status,
        duration,
        failure_reason,
        datetime.now().isoformat(timespec="seconds"),
        deployment_type
    ))

    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# Deployment history API
@app.route("/api/deployments")
def deployment_history():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    records = conn.execute(
        "SELECT * FROM deployments ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([dict(record) for record in records])


# Failure analysis API
@app.route("/api/failure-analysis")
def failure_analysis_api():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    analysis = conn.execute("""
        SELECT
            COALESCE(NULLIF(failure_reason, ''), 'Reason not provided') AS reason,
            COUNT(*) AS occurrences
        FROM deployments
        WHERE status = 'Failed'
        GROUP BY reason
        ORDER BY occurrences DESC
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in analysis])


# Deployment time comparison API
@app.route("/api/deployment-comparison")
def deployment_comparison():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    results = conn.execute("""
        SELECT
            deployment_type,
            COUNT(*) AS total_deployments,
            ROUND(AVG(duration_seconds), 2) AS average_duration
        FROM deployments
        WHERE deployment_type IN ('Manual', 'Automated')
        GROUP BY deployment_type
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in results])


# Health check API
@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "BCA CI/CD Monitoring System",
        "timestamp": datetime.now().isoformat()
    }), 200


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
