import time
import random
import curses

def snake_game():
    # Initialize curses
    screen = curses.initscr()
    curses.curs_set(0)  # Hide cursor
    screen_height, screen_width = screen.getmaxyx()
    window = curses.newwin(screen_height, screen_width, 0, 0)
    window.keypad(1)
    window.timeout(100)  # Refresh every 100ms

    # Initial snake position and food
    snake = [[10, 10], [10, 9], [10, 8]]
    food = [screen_height // 2, screen_width // 4]
    window.addch(food[0], food[1], curses.ACS_PI)

    # Initial direction
    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = window.getch()
        key = key if next_key == -1 else next_key

        # Determine the new head of the snake
        head = snake[0]
        if key == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif key == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif key == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif key == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]
        else:
            new_head = head  # Keep moving in the same direction

        # Check if the snake hits the wall or itself
        if (
            new_head[0] in [0, screen_height]
            or new_head[1] in [0, screen_width]
            or new_head in snake
        ):
            curses.endwin()
            print(f"Game Over! Your Score: {score}")
            break

        # Add the new head to the snake
        snake.insert(0, new_head)

        # Check if snake eats the food
        if new_head == food:
            score += 1
            food = None
            while food is None:
                nf = [
                    random.randint(1, screen_height - 2),
                    random.randint(1, screen_width - 2),
                ]
                food = nf if nf not in snake else None
            window.addch(food[0], food[1], curses.ACS_PI)
        else:
            # Remove the last segment if no food is eaten
            tail = snake.pop()
            window.addch(tail[0], tail[1], " ")

        # Update the snake on the screen
        window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

if __name__ == "__main__":
    snake_game()
