import tkinter as tk
import random


GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class StartWindow:
    def __init__(self, master):
        self.master = master
        start_win_height = GAME_HEIGHT + 100
        start_win_width = GAME_WIDTH + 100
        window_width = start_win_height
        window_height = start_win_width
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.master.geometry(f"{start_win_height}x{start_win_width}+{x}+{y}")
        self.master.configure(background="lightgray")
        self.text = tk.Label(text="Welcome to Snek Game!", font=("Arial", 50), background="lightgray")
        self.text.pack(pady=150)
        self.start_btn = tk.Button(master, text="START", command=self.start_game, font=("Arial", 50), bg="#00FF00")
        self.start_btn.pack()

    def start_game(self):
        self.start_btn.destroy()
        self.text.destroy()
        game_window = GameWindow(self.master, self)


class GameWindow:
    def __init__(self, master, start_window):
        self.game_window = master
        self.start_window = start_window
        self.direction = "down"
        self.score = 0
        self.label = tk.Label(self.game_window, text=f"Score:{self.score}", font=("Arial", 40), background="lightgray")
        self.label.pack()

        self.canvas = tk.Canvas(self.game_window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.game_window.update()

        window_width = self.game_window.winfo_width()
        window_height = self.game_window.winfo_height()
        screen_width = self.game_window.winfo_screenwidth()
        screen_height = self.game_window.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self.game_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.game_window.bind("<Left>", lambda event: self.change_direction("left"))
        self.game_window.bind("<Right>", lambda event: self.change_direction("right"))
        self.game_window.bind("<Down>", lambda event: self.change_direction("down"))
        self.game_window.bind("<Up>", lambda event: self.change_direction("up"))

        self.food = Food(self)
        self.snake = Snake(self)
        self.next_turn(self.snake, self.food)

    def start(self):
        self.start_window.destroy()

    def next_turn(self, snake, food):
        x, y = snake.coordinates[0]
        directions = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}
        x += directions[self.direction][0] * SPACE_SIZE
        y += directions[self.direction][1] * SPACE_SIZE

        snake.coordinates.insert(0, (x, y))

        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            self.score += 1
            self.label.config(text="Score:{}".format(self.score))
            self.canvas.delete("food")
            food = Food(self)
        else:
            del snake.coordinates[-1]
            self.canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if self.check_collisions(snake):
            self.game_over()

        else:
            root.after(SPEED, self.next_turn, snake, food)

    def change_direction(self, new_direction):
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction

    def check_collisions(self, snake):
        x, y = snake.coordinates[0]

        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        for body_part in snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                print("GAME OVER")
                return True
        return False

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.destroy()
        self.label.configure(bg="#000000", foreground="red")
        self.game_window.configure(background="#000000")
        self.game_over_text = tk.Label(self.game_window, font=("Arial", 70), text="GAME OVER!", foreground="red", bg="#000000")
        self.game_over_text.pack(pady=50)
        self.restart_button = tk.Button(self.game_window, text="RESTART", command=self.restart, font=("Arial", 50), bg="#000000",
                           foreground="red")
        self.restart_button.pack()

    def restart(self):
        self.game_over_text.destroy()
        self.restart_button.destroy()
        self.label.destroy()
        self.game_window.configure(background="lightgray")
        StartWindow(self.game_window)

class Snake:
    def __init__(self, game_window):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = game_window.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, game_window):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        game_window.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    root.title("SNAKE GAME")
    start = StartWindow(root)
    root.mainloop()
