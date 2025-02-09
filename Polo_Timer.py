import tkinter as tk
from tkinter import messagebox

# Declare global variables
timer_time = 450  # 7 minutes 30 seconds
timer_running = False
num_chukkas = 0

# Function to show results
def show_results():
    global timer_time, timer_running, num_chukkas
    num_chukkas = int(num_chukkas_var.get()) if num_chukkas_var.get().isdigit() else 0

    # Display Team 1 Name
    team_1_label = tk.Label(root, text=team_1_name.get(), font=("Impact", 18, "bold"), bg="#4CAF50")
    team_1_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Display Team 2 Name
    team_2_label = tk.Label(root, text=team_2_name.get(), font=("Impact", 18, "bold"), bg="#4CAF50")
    team_2_label.grid(row=0, column=1, columnspan=2, pady=10)

    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Create team 1 table (left side)
    team_1_frame = tk.Frame(root, bg="#4CAF50")
    team_1_frame.grid(row=0, column=0, padx=10, pady=10)
    team_1_label = tk.Label(team_1_frame, text=team_1_name.get(), width=30, height=3, font=("Impact", 18), bg="#4CAF50")
    team_1_label.grid(row=0, column=0, columnspan=2)
    team_1_goals = [0] * 4
    team_1_goal_labels = []

    def add_goal_team1(player_index, label):
        team_1_goals[player_index] += 1
        team_1_goal_labels[player_index].config(text=str(team_1_goals[player_index]))
        player_name = team_1_players[player_index].get()
        log_goal("Team 1", player_name)

    def subtract_goal_team1(player_index, label):
        if team_1_goals[player_index] > 0:
            team_1_goals[player_index] -= 1
            team_1_goal_labels[player_index].config(text=str(team_1_goals[player_index]))

    # Update game log + goal tally on goal click
    def log_goal(team, player_name):
        minutes = timer_time // 60
        seconds = timer_time % 60
        time_stamp = f"{minutes}:{seconds:02}"
        score = f"({sum(team_1_goals)}-{sum(team_2_goals)})"
        game_log_text.insert(tk.END, f"{time_stamp} - {player_name} {score}\n")
        game_log_text.see(tk.END)

    # Team 1 clickable player labels
    for i in range(4):
        player_label = tk.Label(
            team_1_frame,
            textvariable=team_1_players[i],
            width=25,
            height=2,
            font=("Impact", 16),
            anchor="w",
            pady=2,
            fg="black",
            cursor="hand2",
            bg="#4CAF50"
        )
        player_label.grid(row=i+1, column=0)
        goal_label = tk.Label(team_1_frame, text="0", width=15, height=2, font=("Impact", 16), bg="#4CAF50")
        goal_label.grid(row=i+1, column=1)
        player_label.bind("<Button-1>", lambda event, idx=i, label=goal_label: add_goal_team1(idx, label))
        player_label.bind("<Button-3>", lambda event, idx=i, label=goal_label: subtract_goal_team1(idx, label))
        team_1_goal_labels.append(goal_label)

    # Create team 2 table (right side)
    team_2_frame = tk.Frame(root, bg="#4CAF50")
    team_2_frame.grid(row=0, column=1, padx=10, pady=10)
    team_2_label = tk.Label(team_2_frame, text=team_2_name.get(), width=30, height=3, font=("Impact", 18), bg="#4CAF50")
    team_2_label.grid(row=0, column=0, columnspan=2)
    team_2_goals = [0] * 4
    team_2_goal_labels = []

    # Update goal log + goal tally on goal click
    def add_goal_team2(player_index, label):
        team_2_goals[player_index] += 1
        team_2_goal_labels[player_index].config(text=str(team_2_goals[player_index]))
        player_name = team_2_players[player_index].get()
        log_goal("Team 2", player_name)

    def subtract_goal_team2(player_index, label):
        if team_2_goals[player_index] > 0:
            team_2_goals[player_index] -= 1
            team_2_goal_labels[player_index].config(text=str(team_2_goals[player_index]))

    def log_goal(team, player_name):
        minutes = timer_time // 60
        seconds = timer_time % 60
        time_stamp = f"{minutes}:{seconds:02}"
        score = f"({sum(team_1_goals)}-{sum(team_2_goals)})"
        game_log_text.insert(tk.END, f"{time_stamp} - {player_name} {score}\n")
        game_log_text.see(tk.END)

    # Team 1 clickable player labels
    for i in range(4):
        player_label = tk.Label(
            team_2_frame,
            textvariable=team_2_players[i],
            width=25,
            height=2,
            font=("Impact", 16),
            anchor="w",
            pady=2,
            fg="black",
            cursor="hand2",
            bg="#4CAF50"
        )
        player_label.grid(row=i+1, column=0)
        goal_label = tk.Label(team_2_frame, text="0", width=15, height=2, font=("Impact", 16), bg="#4CAF50")
        goal_label.grid(row=i+1, column=1)
        player_label.bind("<Button-1>", lambda event, idx=i: add_goal_team2(idx, team_2_goal_labels[idx]))
        player_label.bind("<Button-3>", lambda event, idx=i: subtract_goal_team2(idx, team_2_goal_labels[idx]))
        team_2_goal_labels.append(goal_label)

    # Timer and chukka button frame
    chukka_frame = tk.Frame(root, bg="#4CAF50")
    chukka_frame.grid(row=1, column=0, columnspan=1, pady=10)

    def update_timer_display():
        minutes = timer_time // 60
        seconds = timer_time % 60
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        if timer_time <= 30:
            timer_label.config(fg="red")
        else:
            timer_label.config(fg="black")

    def update_timer():
        global timer_time, timer_running
        if timer_running and timer_time > 0:
            timer_time -= 1
            update_timer_display()
            root.after(1000, update_timer)
        elif timer_time == 0:
            timer_running = False

    def start_stop_timer():
        global timer_running
        if timer_running:
            timer_running = False
            timer_button.config(text="Start")
        else:
            timer_running = True
            timer_button.config(text="Stop")
            update_timer()

    def adjust_timer(seconds):
        global timer_time
        timer_time = max(0, timer_time + seconds)
        update_timer_display()

    def set_chukka_time(chukka):
        global timer_time
        if chukka == num_chukkas:
            timer_time = 420
        else:
            timer_time = 450

        update_timer_display()
        chukka_display.config(text=f"Chukka {chukka}")

        # Log chukka change in the game log
        game_log_text.insert(tk.END, f"\nChukka {chukka}\n")
        game_log_text.see(tk.END)

    timer_label = tk.Label(chukka_frame, text="07:30", font=("Impact", 24))
    timer_label.grid(row=0, column=0, columnspan=2)

    plus_button = tk.Button(chukka_frame, text="+5 secs", command=lambda: adjust_timer(5), font=("Impact", 14))
    plus_button.grid(row=1, column=0, padx=5, pady=5)

    minus_button = tk.Button(chukka_frame, text="-5 secs", command=lambda: adjust_timer(-5), font=("Impact", 14))
    minus_button.grid(row=1, column=1, padx=5, pady=5)

    timer_button = tk.Button(chukka_frame, text="Start", command=start_stop_timer, font=("Impact", 14))
    timer_button.grid(row=2, column=0, columnspan=2, pady=10)

    chukka_display = tk.Label(root, text="Chukka 1", font=("Impact", 18))
    chukka_display.grid(row=2, column=0, columnspan=1, pady=10)

    chukka_buttons_frame = tk.Frame(root)
    chukka_buttons_frame.grid(row=3, column=0, columnspan=1)

    for i in range(1, num_chukkas + 1):
        btn = tk.Button(chukka_buttons_frame, text=f"Chukka {i}", command=lambda i=i: set_chukka_time(i), width=10, height=1, font=("Impact", 14))
        btn.grid(row=(i-1)//2, column=(i-1) % 2, padx=5, pady=5)
    
    # Create game log text area with scrollbar
    game_log_frame = tk.Frame(root, bg="#4CAF50")
    game_log_frame.grid(row=1, column=1, rowspan=4, padx=1, pady=15, sticky="nw")
    game_log_scrollbar = tk.Scrollbar(game_log_frame)
    game_log_scrollbar.pack(side="right", fill="y")
    game_log_text = tk.Text(game_log_frame, width=40, height=14, font=("Impact", 16), yscrollcommand=game_log_scrollbar.set)
    game_log_text.pack(side="left", fill="both", expand=True)
    game_log_scrollbar.config(command=game_log_text.yview)
    game_log_text.insert(tk.END, "Chukka 1\n")

# Set up main window
root = tk.Tk()
root.state("zoomed")
root.configure(bg="#4CAF50")

# Pre-match page UI
tk.Label(root, text="Team 1 Name:", font=("Impact", 16), bg="#4CAF50").grid(row=0, column=0)
team_1_name = tk.StringVar()
tk.Entry(root, textvariable=team_1_name, font=("Impact", 16)).grid(row=0, column=1)

team_1_players = [tk.StringVar() for _ in range(4)]
for i in range(4):
    tk.Label(root, text=f"Player {i+1}:", font=("Impact", 16), bg="#4CAF50").grid(row=i+1, column=0)
    tk.Entry(root, textvariable=team_1_players[i], font=("Impact", 16)).grid(row=i+1, column=1)

tk.Label(root, text="Team 2 Name:", font=("Impact", 16), bg="#4CAF50").grid(row=0, column=2)
team_2_name = tk.StringVar()
tk.Entry(root, textvariable=team_2_name, font=("Impact", 16)).grid(row=0, column=3)

team_2_players = [tk.StringVar() for _ in range(4)]
for i in range(4):
    tk.Label(root, text=f"Player {i+1}:", font=("Impact", 16), bg="#4CAF50").grid(row=i+1, column=2)
    tk.Entry(root, textvariable=team_2_players[i], font=("Impact", 16)).grid(row=i+1, column=3)

tk.Label(root, text="Number of Chukkas:", font=("Impact", 16), bg="#4CAF50").grid(row=5, column=1, pady=20)
num_chukkas_var = tk.StringVar()
tk.Entry(root, textvariable=num_chukkas_var, font=("Impact", 16)).grid(row=5, column=2)

start_button = tk.Button(root, text="Start Game", command=show_results, width=15, height=1, font=("Impact", 16))
start_button.grid(row=6, column=0, columnspan=4, pady=20)

root.mainloop()
