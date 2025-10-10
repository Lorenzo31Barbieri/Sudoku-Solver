from flask import Flask, render_template, request
from sudoku import solve_sudoku

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    solution = None
    status = None
    if request.method == "POST":
        try:
            puzzle = [[int(request.form.get(f"cell{i}{j}", 0) or 0) for j in range(1, 10)] for i in range(1, 10)]
        except ValueError:
            puzzle = [[0]*9 for _ in range(9)]
            
        result, status = solve_sudoku(puzzle)
        
        if status == "Optimal":
            solution = result
        
    return render_template("index.html", solution=solution, status=status)

@app.route("/reset")
def reset():
    return render_template("index.html", solution=None, status=None)

if __name__ == "__main__":
    app.run(debug=True)