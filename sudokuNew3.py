import tkinter as tk  
from tkinter import messagebox, ttk
from collections import deque  
import random  
import time 

#Her hücrenin olası değerlerinin kümesini oluşturur
def initialize_domains(board):
    domains = {}  
    for row in range(9):  
        for col in range(9): 
            if board[row][col] == 0: 
                domains[(row, col)] = set(range(1, 10))  
            else: 
                domains[(row, col)] = {board[row][col]}  
    return domains

#Bir hücrenin tüm komşularını bulur
def neighbor_cells(cell):
    row, col = cell  
    neighbors = set() 
    
    for i in range(9):
        if i != col: 
            neighbors.add((row, i))
            
    for i in range(9):
        if i != row:  
            neighbors.add((i, col))
            
    start_row, start_col = 3 * (row // 3), 3 * (col // 3) 
    for i in range(3):
        for j in range(3):
            r, c = start_row + i, start_col + j
            if (r, c) != cell: 
                neighbors.add((r, c))
    return neighbors

#Hücreye gelemeyecek değerleri siler
def revise(domains, cell, neighbor):
    revised = False  
    to_remove = set()
    
  
    for value in domains[cell]:
        if not any(value != n_value for n_value in domains[neighbor]):
         to_remove.add(value)  
    
    if to_remove:
        domains[cell] -= to_remove  
        revised = True  
    return revised

# AC3
def ac3(board, domains):
    queue = deque([(x, y) for x in domains for y in neighbor_cells(x)])
    
    while queue:  
        cell, neighbor = queue.popleft()  
        if revise(domains, cell, neighbor): 
            if not domains[cell]:  
                return False 
            for n in neighbor_cells(cell):
                if n != neighbor:
                    queue.append((n, cell))
    return True

def solve_with_ac3(board):
    domains = initialize_domains(board) 
    if not ac3(board, domains):  
        return False
    return backtrack(board, domains)

# Backtracking
def backtrack(board, domains):
    if all(len(domains[cell]) == 1 for cell in domains):
        for (row, col), values in domains.items():
            board[row][col] = next(iter(values))
        return True
    
    cell = min((c for c in domains if len(domains[c]) > 1), key=lambda x: len(domains[x]))
    
    for value in domains[cell]:
        new_domains = {k: v.copy() for k, v in domains.items()} 
        new_domains[cell] = {value} 
        if ac3(board, new_domains): 
            if backtrack(board, new_domains): 
                return True
    return False

# Rastgele Sudoku tahtası
def generate_random_sudoku(level):
    # Bir sayının yerleştirilebilir olup olmadığını kontrol etme
    def is_valid(board, row, col, num):
        for i in range(9):
            if board[row][i] == num:
                return False
                
        for i in range(9):
            if board[i][col] == num:
                return False
                
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True

    # Tahtayı dolduran iç fonksiyon
    def fill_board(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0: 
                    random_nums = list(range(1, 10)) 
                    random.shuffle(random_nums)
                    for num in random_nums: 
                        if is_valid(board, row, col, num):
                            board[row][col] = num  
                            if fill_board(board):  
                                return True
                            board[row][col] = 0  
                    return False
        return True

    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_board(board) 

    levels = {"easy": 30, "medium": 40, "hard": 50} 
    cells_to_remove = random.sample(range(81), k=levels[level])
    for cell in cells_to_remove:
        row, col = divmod(cell, 9)  
        board[row][col] = 0 

    return board

# Yeni oyun başlatan fonksiyon
def initialize_game(level):
    sudoku_board = generate_random_sudoku(level) 
    solution_board = [row[:] for row in sudoku_board] 
    solve_with_ac3(solution_board)
    return sudoku_board, solution_board

sudoku_board, solution_board = initialize_game("medium")

# GUI 
def create_gui():
    root = tk.Tk() 
    root.title("Sudoku Solver") 
    root.geometry("600x700")  
    root.configure(bg="#f7f7f7") 

    title_label = tk.Label(root, text="Sudoku Solver", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333")
    title_label.pack(pady=10)

    top_right_frame = tk.Frame(root, bg="#f7f7f7")
    top_right_frame.place(relx=1, y=5, anchor="ne")

    timer_label = tk.Label(top_right_frame, text="00:00", font=("Arial", 16), bg="#f7f7f7", fg="#333")
    timer_label.pack(side="top", pady=5)

    pause_button = ttk.Button(top_right_frame, text="Pause", command=lambda: pause_game(timer_label))
    pause_button.pack(side="top", pady=5)

    main_frame = tk.Frame(root, bg="#f7f7f7")
    main_frame.pack(pady=10)

    cells = {}
    user_board = [[0] * 9 for _ in range(9)]
    is_paused = [False]

    # Girdi doğrulama
    def validate_input(P):
        return P == "" or (len(P) == 1 and P in "123456789")

    def update_board(new_board):
        for row in range(9):
            for col in range(9):
                cells[(row, col)].config(state="normal")
                cells[(row, col)].delete(0, tk.END)
                if new_board[row][col] != 0:
                    cells[(row, col)].insert(tk.END, str(new_board[row][col]))
                    cells[(row, col)].config(state="disabled", disabledbackground="#d9ead3")
                else:
                    cells[(row, col)].config(state="normal", disabledbackground="white")
                cells[(row, col)].config(fg="black")

    sub_grids = {}
    for sub_row in range(3):
        for sub_col in range(3):
            frame = tk.Frame(main_frame, bg="#f7f7f7", bd=1, relief="solid")
            frame.grid(row=sub_row, column=sub_col, padx=0, pady=0)
            sub_grids[(sub_row, sub_col)] = frame

    for row in range(9):
        for col in range(9):
            vcmd = (main_frame.register(validate_input), '%P')
            entry = tk.Entry(
                sub_grids[(row // 3, col // 3)],
                width=2,
                font=("Arial", 18),
                justify="center",
                validate="key",
                validatecommand=vcmd,
            )
            entry.grid(row=row % 3, column=col % 3, ipadx=10, ipady=10, sticky="nsew")

            if sudoku_board[row][col] != 0:
                entry.insert(tk.END, str(sudoku_board[row][col]))
                entry.config(state="disabled", disabledbackground="#d9ead3")

            cells[(row, col)] = entry

    def reset_timer(timer_label):
        timer_label.config(text="00:00")

    def solve_gui():
        is_paused[0] = True
        pause_button.config(text="Resume")

        start_time = time.time()
        temp_board = [row[:] for row in sudoku_board]
        if solve_with_ac3(temp_board):
            solve_time = time.time() - start_time
            for row in range(9):
                for col in range(9):
                    cells[(row, col)].delete(0, tk.END)
                    cells[(row, col)].insert(tk.END, str(temp_board[row][col]))
            messagebox.showinfo("Solve Time", f"Solved in {solve_time:.2f} seconds!")
        else:
            solve_time = time.time() - start_time
            messagebox.showerror("Error", f"No solution exists! Solving attempted for {solve_time:.2f} seconds.")

    def check_answers():
        numbers_entered = False
        # Girilen sayı var mı kontrol et
        for row in range(9):
            for col in range(9):
                if sudoku_board[row][col] == 0:
                    cell_value = cells[(row, col)].get()
                    if cell_value.isdigit():
                        numbers_entered = True
                        break
            if numbers_entered:
                break

        if not numbers_entered:
            messagebox.showwarning("No Answers", "Please enter some numbers before checking.")
            return

        # Cevapları kontrol et
        correct = True
        for row in range(9):
            for col in range(9):
                cell_value = cells[(row, col)].get()
                if cell_value.isdigit():
                    value = int(cell_value)
                    if value != solution_board[row][col]:
                        cells[(row, col)].config(fg="red")
                        correct = False
                    else:
                        cells[(row, col)].config(fg="green")

        if correct:
            messagebox.showinfo("Success", "All answers entered are correct!")
        else:
            messagebox.showerror("Error", "Some answers are incorrect. Please try again.")

    # Easy-medium-hard 
    def reroll_game():
        level = level_var.get()  
        new_board, new_solution = initialize_game(level)  
        for row in range(9):
            for col in range(9):
                sudoku_board[row][col] = new_board[row][col]  
                solution_board[row][col] = new_solution[row][col] 
        update_board(sudoku_board) 

 
    def set_difficulty():
        reset_timer(timer_label)  
        reroll_game()  

    def reset_timer(timer_label):
        timer_label.config(text="00:00") 
        is_paused[0] = False  
        update_timer(timer_label) 

    def reset_timer(timer_label):
        global timer_id 
        
        if timer_id:
            root.after_cancel(timer_id)
            timer_id = None
        
        timer_label.config(text="00:00") 
        is_paused[0] = False 
        update_timer(timer_label) 

    def update_timer(label):
            global timer_id

            if not is_paused[0]:  # Eğer oyun duraklatılmadıysa
                current_time = label["text"]  # Mevcut zamanı al
                minutes, seconds = map(int, current_time.split(":"))  # Dakika ve saniyeyi ayır
                seconds += 1  # Saniyeyi 1 artır

                if seconds == 60:  # Eğer saniye 60 olursa
                    seconds = 0  # Saniyeyi sıfırla
                    minutes += 1  # Dakikayı artır

                label["text"] = f"{minutes:02}:{seconds:02}"  # Formatlanmış şekilde etiketi güncelle
                timer_id = root.after(1000, update_timer, label)  # 1 saniye sonra tekrar çağır

    def pause_game(timer_label):
        if is_paused[0]: 
            is_paused[0] = False
            pause_button.config(text="Pause")
            update_timer(timer_label) 
            
            # Mevcut Tahtayı geri yükle
            for row in range(9):
                for col in range(9):
                    if sudoku_board[row][col] != 0: 
                        cells[(row, col)].config(state="disabled", disabledbackground="#d9ead3")
                        cells[(row, col)].delete(0, tk.END)
                        cells[(row, col)].insert(tk.END, str(sudoku_board[row][col]))
                    elif user_board[row][col] != 0:  
                        cells[(row, col)].config(state="normal")
                        cells[(row, col)].delete(0, tk.END)
                        cells[(row, col)].insert(tk.END, str(user_board[row][col]))
        else: 
            is_paused[0] = True
            pause_button.config(text="Resume")
            
            # Kullanıcı girişlerini kaydet ve tahtayı temizle
            for row in range(9):
                for col in range(9):
                    if sudoku_board[row][col] == 0: 
                        cell_value = cells[(row, col)].get()
                        user_board[row][col] = int(cell_value) if cell_value.isdigit() else 0
                    cells[(row, col)].delete(0, tk.END)

    button_frame = tk.Frame(root, bg="#f7f7f7")
    button_frame.pack(pady=10)

    solve_button = ttk.Button(button_frame, text="Solve", command=solve_gui)
    solve_button.grid(row=0, column=0, padx=5)

    check_button = ttk.Button(button_frame, text="Check Answers", command=check_answers)
    check_button.grid(row=0, column=1, padx=5)

    reset_button = ttk.Button(button_frame, text="Reset", command=lambda: [update_board(sudoku_board), reset_timer(timer_label)])
    reset_button.grid(row=0, column=2, padx=5)

    quit_button = ttk.Button(button_frame, text="Quit", command=root.quit)
    quit_button.grid(row=0, column=3, padx=5)

    level_var = tk.StringVar(value="medium")
    level_frame = tk.Frame(root)
    level_frame.pack(pady=10)
    tk.Label(level_frame, text="Difficulty:", font=("Arial", 14)).pack(side="left")
    for level in ["easy", "medium", "hard"]:
        tk.Radiobutton(level_frame, text=level.capitalize(), variable=level_var, value=level, 
                      font=("Arial", 12), command=set_difficulty).pack(side="left")

    update_timer(timer_label)
    root.mainloop()  

create_gui()