```markdown
##  Sudoku Solver - Python (AC-3 + Backtracking + Tkinter)

This project is an interactive **Sudoku solving and playing application** developed in **Python**. The application generates a random Sudoku puzzle for the user and solves it using the AC-3 algorithm and backtracking method.

###  Features

- ✅ 3 difficulty levels: *Easy*, *Medium*, *Hard*
- ✅ Randomly generated Sudoku boards
- ✅ AC-3 algorithm for constraint propagation and domain reduction
- ✅ Backtracking algorithm to find the exact solution
- ✅ Timer and pause functionality
- ✅ User answer validation with real-time feedback
- ✅ User-friendly GUI built with Tkinter

###  Algorithms Used

#### 1. **AC-3 (Arc Consistency Algorithm 3)**

AC-3 evaluates constraints between Sudoku cells to eliminate inconsistent values early. This algorithm:
- Narrows down possible values for each cell
- Reduces the problem space
- Acts as an efficient preprocessing step before backtracking

#### 2. **Backtracking**

When AC-3 alone can't solve the puzzle:
- A value is chosen for a suitable cell
- A recursive search is conducted
- Invalid paths are rolled back (backtracking)
- The entire solution space is systematically explored

###  Application Interface

The GUI built with Tkinter provides:
- A 9x9 Sudoku grid
- Locked cells for given numbers (non-editable)
- Editable cells for user input
- "Solve" button for automatic solving
- "Check Answers" to validate user input
- "Reset" to start over
- "Pause/Resume" to control the timer

###  Project Structure

sudoku\_solver/
├── main.py           # Main Python file containing the Sudoku application
└── README.md         # Project description and documentation

###  Requirements

```bash
Python 3.x
````

No external libraries required. Uses only standard Python libraries: `tkinter`, `random`, `time`, `collections`.

### ▶ Run the Application

```bash
python main.py
```

###  References

* Arc Consistency: [https://en.wikipedia.org/wiki/AC-3\_algorithm](https://en.wikipedia.org/wiki/AC-3_algorithm)
* Backtracking: [https://en.wikipedia.org/wiki/Backtracking](https://en.wikipedia.org/wiki/Backtracking)
* Sudoku Rules: [https://sudoku.com](https://sudoku.com)

###  Developed By

**Furkan Arslan**
📅 December 2024
📧 furkan0tr0arslan@gmail.com

