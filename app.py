from flask import Flask, render_template, request
from pulp import *
from sudoku import solve_sudoku

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    solution = None
    if request.method == "POST":
        try:
            puzzle = [[int(request.form.get(f"cell{i}{j}", 0) or 0) for j in range(1, 10)] for i in range(1, 10)]
        except ValueError:
            # Handle the case where conversion fails
            puzzle = [[0]*9 for _ in range(9)]
        solution = solve_sudoku(puzzle)
    return render_template("index.html", solution=solution)

@app.route("/reset")
def reset():
    # Render the template with an empty solution or initial grid
    return render_template("index.html", solution=None)

if __name__ == "__main__":
    app.run(debug=True)
