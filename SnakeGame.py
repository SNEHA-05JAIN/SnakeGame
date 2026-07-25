"""
How to run:
    python SnakeGame.py

Controls:
    W / Up Arrow    -> Move Up
    S / Down Arrow  -> Move Down
    A / Left Arrow  -> Move Left
    D / Right Arrow -> Move Right

Rules:
    - Eat the red food to grow and increase score.
    - Avoid hitting the walls or your own body.
    - Game restarts after a short delay when you lose.
"""

import turtle
import time
import random
import tkinter

# ---------------------------------------------------------------------------
# Screen setup
# ---------------------------------------------------------------------------
WIDTH, HEIGHT = 600, 600

screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("black")
screen.setup(width=WIDTH, height=HEIGHT)
screen.tracer(0)  # Turns off automatic screen updates for smooth animation

# ---------------------------------------------------------------------------
# Snake head
# ---------------------------------------------------------------------------
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("lime")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# ---------------------------------------------------------------------------
# Food
# ---------------------------------------------------------------------------
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# List to store snake body segments
segments = []

# ---------------------------------------------------------------------------
# Score display
# ---------------------------------------------------------------------------
score = 0
high_score = 0

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(f"Score : {score}   High Score : {high_score}",
          align="center", font=("Courier", 18, "normal"))


# ---------------------------------------------------------------------------
# Movement functions
# ---------------------------------------------------------------------------
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    if head.direction == "down":
        head.sety(head.ycor() - 20)
    if head.direction == "left":
        head.setx(head.xcor() - 20)
    if head.direction == "right":
        head.setx(head.xcor() + 20)


# ---------------------------------------------------------------------------
# Keyboard bindings
# ---------------------------------------------------------------------------
screen.listen()
screen.onkeypress(go_up, "Up")
screen.onkeypress(go_down, "Down")
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")
screen.onkeypress(go_up, "w")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_right, "d")

# ---------------------------------------------------------------------------
# Main game loop
# ---------------------------------------------------------------------------
delay = 0.1

try:
    while True:
        screen.update()

        # --- Check collision with border ---
        if (head.xcor() > WIDTH / 2 - 10 or head.xcor() < -WIDTH / 2 + 10 or
                head.ycor() > HEIGHT / 2 - 10 or head.ycor() < -HEIGHT / 2 + 10):
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"

            # Hide and clear all segments
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            # Reset score
            score = 0
            delay = 0.1
            pen.clear()
            pen.write(f"Score : {score}   High Score : {high_score}",
                      align="center", font=("Courier", 18, "normal"))

        # --- Check collision with food ---
        if head.distance(food) < 20:
            # Move food to a random spot
            x = random.randint(-int(WIDTH / 2 - 20), int(WIDTH / 2 - 20))
            y = random.randint(-int(HEIGHT / 2 - 20), int(HEIGHT / 2 - 20))
            food.goto(x, y)

            # Add a new segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("dark green")
            new_segment.penup()
            segments.append(new_segment)

            # Increase score
            score += 10
            if score > high_score:
                high_score = score
            pen.clear()
            pen.write(f"Score : {score}   High Score : {high_score}",
                      align="center", font=("Courier", 18, "normal"))

            # Slightly increase speed
            delay = max(0.05, delay - 0.001)

        # --- Move the body segments in reverse order ---
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        # Move first segment to where the head is
        if segments:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # --- Check collision with own body ---
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "stop"

                for seg in segments:
                    seg.goto(1000, 1000)
                segments.clear()

                score = 0
                delay = 0.1
                pen.clear()
                pen.write(f"Score : {score}   High Score : {high_score}",
                          align="center", font=("Courier", 18, "normal"))

        time.sleep(delay)

except (turtle.Terminator, tkinter.TclError):
    # Window was closed while the game loop was running -- exit quietly.
    pass