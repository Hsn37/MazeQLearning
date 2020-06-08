import tkinter
from tkinter import messagebox
from time import sleep


class tkWindow():

    def __init__(self):
        self.window = None

        # first window
        self.label1 = None
        self.label2 = None
        self.label3 = None
        self.var_theme = None
        self.heading = None
        self.entry1 = None
        self.entry2 = None
        self.theme = None
        self.button = None

        # second window
        self.redefine_button = None
        self.regenerate = None
        self.go_back = None
        self.train_AI = None

        # third window
        self.entry_alpha = None
        self.entry_gamma = None
        self.entry_neg_reward = None
        self.entry_pos_reward = None
        self.entry_epsilon = None
        self.alpha_label = None
        self.gamma_label = None
        self.neg_reward = None
        self.pos_reward = None
        self.epsilon_label = None
        self.start_training_button = None
        self.var_alpha = None
        self.var_gamma = None
        self.var_epsilon = None
        self.var_neg = None
        self.var_pos = None
        self.back3 = None

        # fourth window
        self.c1 = None
        self.c2 = None
        self.var1 = None
        self.var2 = None
        self.speed_up = None
        self.slowdown = None
        self.pause_button = None
        self.back4 = None
        self.end = None

        # variables
        self.maze_height = None
        self.maze_width = None
        self.color = None
        self.button_text = None

        # flags
        self.create = False
        self.back = False
        self.close_flag = False
        self.redefine_flag = False
        self.regen_flag = False
        self.training_flag = False
        self.inc_flag = False
        self.dec_flag = False
        self.reward_flag = False
        self.q_values_flag = False
        self.pause_flag = False
        self.redo = False
        self.end_training_flag = False

    def origin(self):
        self.window = tkinter.Tk()
        self.window.title("Maze Generator")
        self.window.resizable(width=False, height=False)
        self.window.geometry("300x400+500+200")
        self.window.protocol("WM_DELETE_WINDOW", self.callback)

        # first window contents
        self.label1 = tkinter.Label(self.window, text="Width:")
        self.label2 = tkinter.Label(self.window, text="Height:")
        self.label3 = tkinter.Label(self.window, text="Theme")

        self.heading = tkinter.Label(self.window, text="Maze Generator")
        self.heading.config(font=("Times New Roman", 20))

        self.var_theme = tkinter.StringVar(self.window)
        self.var_theme.set("Classic")  # default value

        self.theme = tkinter.OptionMenu(self.window, self.var_theme, "Classic", "Retro", "Fiery", "Argonzo")

        self.entry1 = tkinter.Entry()
        self.entry2 = tkinter.Entry()

        self.entry1.insert(0, "13")
        self.entry2.insert(0, "13")

        self.button = tkinter.Button(self.window, text="Create Maze", command=self.create_maze)
        self.button.config(font=("Times New Roman", 11))

        # second window contents
        self.redefine_button = tkinter.Button(self.window, text="Redefine Goal", command=self.redefine_goal)
        self.regenerate = tkinter.Button(self.window, text="Regenerate Maze", command=self.regen)
        self.go_back = tkinter.Button(self.window, text="<-Back", command=self.back2_command)
        self.train_AI = tkinter.Button(self.window, text="Train AI", command=self.train)
        self.train_AI.config(font=("Times New Roman", 12))

        # third window contents
        self.entry_alpha = tkinter.Entry(self.window)
        self.entry_gamma = tkinter.Entry(self.window)
        self.entry_neg_reward = tkinter.Entry(self.window)
        self.entry_pos_reward = tkinter.Entry(self.window)
        self.entry_epsilon = tkinter.Entry(self.window)

        self.back3 = tkinter.Button(self.window, text="<-Back", command=self.back3_command)

        self.entry_alpha.insert(0, "1")
        self.entry_gamma.insert(0, "0.8")
        self.entry_neg_reward.insert(0, "-10")
        self.entry_pos_reward.insert(0, "50")
        self.entry_epsilon.insert(0, "0")

        self.alpha_label = tkinter.Label(self.window, text="Alpha")
        self.gamma_label = tkinter.Label(self.window, text="Gamma")
        self.neg_reward = tkinter.Label(self.window, text="Reward for Walls")
        self.pos_reward = tkinter.Label(self.window, text="Reward for Goal")
        self.epsilon_label = tkinter.Label(self.window, text="Epsilon")

        self.start_training_button = tkinter.Button(self.window, text="Start Training", command=self.start_training)
        self.start_training_button.config(font=("Times New Roman", 15))

        # fourth window contents
        self.var1 = tkinter.IntVar()
        self.c1 = tkinter.Checkbutton(self.window, text='Show rewards', variable=self.var1, onvalue=1, offvalue=0,
                                 command=self.reward_command)

        self.var2 = tkinter.IntVar()
        self.c2 = tkinter.Checkbutton(self.window, text='Show Q Values', variable=self.var2, onvalue=1, offvalue=0,
                                      command=self.q_value_command)
        self.speed_up = tkinter.Button(self.window, text="Speed Up", command=self.speed_inc)
        self.slowdown = tkinter.Button(self.window, text="Slow Down", command=self.speed_dec)

        self.button_text = tkinter.StringVar()
        self.button_text.set("Pause")
        self.pause_button = tkinter.Button(self.window, textvariable=self.button_text, command=self.pause_command)
        self.pause_button.config(font=("Times New Roman", 12))

        self.back4 = tkinter.Button(self.window, text="Interrupt training", command=self.back4_command)

        self.end = tkinter.Button(self.window, text="Finish Training", command=self.end_command)
        self.end.config(font=("Times New Roman", 12))

        # starting first window
        self.first_window()
        self.window.mainloop()

    def first_window(self):

        self.heading.pack()

        self.label1.place(x=60, y=60)
        self.entry1.place(x=110, y=60)
        self.label2.place(x=60, y=90)
        self.entry2.place(x=110, y=90)

        self.label3.place(x=135, y=140)
        self.theme.place(x=117, y=160)

        self.button.pack(side=tkinter.BOTTOM, pady=50)

    def second_window(self):

        self.go_back.pack(side=tkinter.BOTTOM, pady=50)
        self.redefine_button.pack(pady=5)
        self.regenerate.pack(pady=5)
        self.train_AI.pack(pady=10)

    def third_window(self):

        self.alpha_label.pack()
        self.entry_alpha.pack()
        self.gamma_label.pack()
        self.entry_gamma.pack()
        self.epsilon_label.pack()
        self.entry_epsilon.pack()
        self.neg_reward.pack()
        self.entry_neg_reward.pack()
        self.pos_reward.pack()
        self.entry_pos_reward.pack()
        self.start_training_button.pack(pady=25)
        self.back3.pack(side=tkinter.BOTTOM, pady=30)

    def fourth_window(self):

        self.c1.pack(pady=5)
        self.c2.pack(pady=5)

        self.speed_up.pack(pady=5)
        self.slowdown.pack(pady=5)
        self.pause_button.pack(pady=10)
        self.end.pack()
        self.back4.pack(side=tkinter.BOTTOM, pady=20)

    # all the event handling functions
    def create_maze(self):
        try:
            self.maze_width = int(self.entry1.get())
            self.maze_height = int(self.entry2.get())

            if self.maze_height % 2 == 0 or self.maze_width % 2 == 0:
                messagebox.showinfo(title="Error", message="Please Enter Odd Numbers.")
                return

            self.color = self.var_theme.get()

        except Exception:
            print(Exception)
            messagebox.showinfo("Error", "Invalid Input. Please Try again.")
            return
        self.create = True

        self.label1.place_forget()
        self.label2.place_forget()
        self.label3.place_forget()
        self.heading.pack_forget()
        self.theme.place_forget()
        self.entry1.place_forget()
        self.entry2.place_forget()
        self.button.pack_forget()

        self.second_window()

        sleep(1.5)
        self.window.after(1, lambda: self.window.focus_force())

    def back2_command(self):
        self.back = True
        self.go_back.pack_forget()
        self.train_AI.pack_forget()
        self.redefine_button.pack_forget()
        self.regenerate.pack_forget()

        self.first_window()

    def back3_command(self):
        self.alpha_label.pack_forget()
        self.entry_alpha.pack_forget()
        self.gamma_label.pack_forget()
        self.entry_gamma.pack_forget()
        self.epsilon_label.pack_forget()
        self.entry_epsilon.pack_forget()
        self.neg_reward.pack_forget()
        self.entry_neg_reward.pack_forget()
        self.pos_reward.pack_forget()
        self.entry_pos_reward.pack_forget()
        self.start_training_button.pack_forget()
        self.back3.pack_forget()

        self.second_window()

    def back4_command(self):
        self.c1.pack_forget()
        self.c2.pack_forget()

        self.speed_up.pack_forget()
        self.slowdown.pack_forget()
        self.pause_button.pack_forget()
        self.end.pack_forget()
        self.back4.pack_forget()

        self.third_window()
        self.training_flag = False
        self.redo = True

    def callback(self):
        self.close_flag = True

    def regen(self):
        self.regen_flag = True

    def train(self):
        self.go_back.pack_forget()
        self.train_AI.pack_forget()
        self.redefine_button.pack_forget()
        self.regenerate.pack_forget()

        self.third_window()

    def redefine_goal(self):
        self.redefine_flag = True

    def reward_command(self):
        self.var2.set(0)
        self.q_values_flag = False
        self.reward_flag = not self.reward_flag

    def end_command(self):
        self.window.withdraw()
        self.end_training_flag = True
        self.close_flag = True

    def speed_inc(self):
        self.inc_flag = True

    def speed_dec(self):
        self.dec_flag = True

    def q_value_command(self):
        self.var1.set(0)
        self.reward_flag = False
        self.q_values_flag = not self.q_values_flag

    def start_training(self):
        try:
            self.var_alpha = self.entry_alpha.get()
            self.var_gamma = self.entry_gamma.get()
            self.var_epsilon = self.entry_epsilon.get()
            self.var_neg = self.entry_neg_reward.get()
            self.var_pos = self.entry_pos_reward.get()
        except Exception:
            messagebox.showinfo(title="Error", message="Invalid Arguments")
            return

        self.alpha_label.pack_forget()
        self.entry_alpha.pack_forget()
        self.gamma_label.pack_forget()
        self.entry_gamma.pack_forget()
        self.epsilon_label.pack_forget()
        self.entry_epsilon.pack_forget()
        self.neg_reward.pack_forget()
        self.entry_neg_reward.pack_forget()
        self.pos_reward.pack_forget()
        self.entry_pos_reward.pack_forget()
        self.start_training_button.pack_forget()
        self.back3.pack_forget()

        self.training_flag = True
        self.fourth_window()

    def pause_command(self):

        val = self.button_text.get()
        if val == "Pause":
            self.pause_flag = True
            self.button_text.set("Resume")
        if val == "Resume":
            self.pause_flag = False
            self.button_text.set("Pause")