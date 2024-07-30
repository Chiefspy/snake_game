from tkinter import *
import random

GAME_HEIGHT = 700
GAME_WIDTH = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

score = 0
direction = "down"


class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, canvas):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def next_turn(snake, food, canvas, window, label):
    global direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text=f"Score: {score}")

        canvas.delete("food")

        food = Food(canvas)

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over(canvas)

    else:
        window.after(SPEED, next_turn, snake, food, canvas, window, label)


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    else:
        return False


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def game_over(canvas):
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=("consolas", 70), text="GAME OVER", fill="red", tag="gameover")


def play_again(window):
    window.destroy()
    main()


def main():
    global score, direction
    score = 0
    direction = "down"
    window = Tk()
    window.title("Snake game")
    window.resizable(False, False)

    # global score
    # score = 0
    # global direction
    # direction = "down"
    label = Label(window, text=f"Score:{score}", font=("consolas", 40))
    label.pack()

    play_again_button = Button(window, font=("consolas", 20), text="restart", command=lambda: play_again(window))
    play_again_button.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
    canvas.pack()

    window.focus_set()

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenheight()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind("<Up>", lambda event: change_direction("up"))
    window.bind("<Down>", lambda event: change_direction("down"))
    window.bind("<Left>", lambda event: change_direction("left"))
    window.bind("<Right>", lambda event: change_direction("right"))
    window.bind("<w>", lambda event: change_direction("up"))
    window.bind("<s>", lambda event: change_direction("down"))
    window.bind("<d>", lambda event: change_direction("right"))
    window.bind("<a>", lambda event: change_direction("left"))

    snake = Snake(canvas)

    food = Food(canvas)


    next_turn(snake, food, canvas, window, label)

    window.mainloop()


if __name__ == '__main__':
    main()
