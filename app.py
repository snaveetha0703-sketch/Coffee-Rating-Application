
from flask import Flask, render_template, jsonify
import sqlite3
import json

app = Flask(__name__)

# Database connection
def connect_db():
    return sqlite3.connect("coffee.db")


# Create database and table
def create_database():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS coffee (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            image TEXT,
            votes INTEGER DEFAULT 0
        )
    """)

    cur.execute("SELECT COUNT(*) FROM coffee")

    if cur.fetchone()[0] == 0:
        with open("coffee_seed_data.json", "r") as file:
            data = json.load(file)

        for item in data:
            cur.execute("""
                INSERT INTO coffee
                VALUES (?, ?, ?, ?, ?)
            """, (
                item["id"],
                item["name"],
                item["description"],
                item["image"],
                item["votes"]
            ))

    con.commit()
    con.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Get all coffees
@app.route("/api/coffees")
def get_coffees():
    con = connect_db()
    con.row_factory = sqlite3.Row

    data = con.execute(
        "SELECT * FROM coffee ORDER BY votes DESC"
    ).fetchall()

    con.close()

    return jsonify([dict(row) for row in data])


# Vote for coffee
@app.route("/api/vote/<int:id>", methods=["POST"])
def vote(id):
    con = connect_db()
    cur = con.cursor()

    cur.execute(
        "UPDATE coffee SET votes = votes + 1 WHERE id = ?",
        (id,)
    )

    con.commit()

    if cur.rowcount == 0:
        con.close()
        return jsonify({"error": "Coffee not found"}), 404

    con.close()

    return jsonify({"message": "Vote added successfully"})


# Leaderboard
@app.route("/api/leaderboard")
def leaderboard():
    con = connect_db()
    con.row_factory = sqlite3.Row

    data = con.execute("""
        SELECT name, votes FROM coffee
        ORDER BY votes DESC
        LIMIT 5
    """).fetchall()

    con.close()

    return jsonify([dict(row) for row in data])


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
