"""
Desktop Turtle graphics companion for ShopImpact.

Run locally:
    python turtle_graphics.py

This opens a Turtle window and draws a leaf and a simple footprint.
A desktop display is required. Streamlit Cloud cannot open a Turtle GUI window.
"""

import turtle


def setup_turtle():
    screen = turtle.Screen()
    screen.title("ShopImpact — Turtle Eco Art")
    screen.bgcolor("#F3F8EF")
    screen.setup(width=760, height=520)

    pen = turtle.Turtle()
    pen.speed(0)
    pen.pensize(4)
    pen.hideturtle()
    return screen, pen


def draw_leaf(pen, x, y, size=1.0):
    """Draw a leaf using Turtle movement and arcs."""
    pen.penup()
    pen.goto(x, y)
    pen.setheading(45)
    pen.pendown()
    pen.color("#247A4B", "#8BCF9B")
    pen.begin_fill()
    pen.circle(65 * size, 90)
    pen.left(90)
    pen.circle(65 * size, 90)
    pen.end_fill()

    pen.penup()
    pen.goto(x, y)
    pen.setheading(45)
    pen.pendown()
    pen.color("#FFFFFF")
    pen.forward(90 * size)


def draw_footprint(pen, x, y, size=1.0):
    """Draw a friendly footprint badge."""
    pen.penup()
    pen.goto(x, y)
    pen.setheading(0)
    pen.pendown()
    pen.color("#1E5C3B", "#B7E4C7")
    pen.begin_fill()
    pen.circle(42 * size)
    pen.end_fill()

    # Toe pads
    toes = [(-25, 57, 13), (0, 72, 15), (25, 63, 13), (43, 42, 10)]
    for dx, dy, radius in toes:
        pen.penup()
        pen.goto(x + dx * size, y + dy * size)
        pen.pendown()
        pen.color("#1E5C3B", "#8BCF9B")
        pen.begin_fill()
        pen.circle(radius * size)
        pen.end_fill()


def main():
    screen, pen = setup_turtle()

    pen.penup()
    pen.goto(0, 190)
    pen.color("#1E5C3B")
    pen.write("SHOPIMPACT", align="center", font=("Arial", 24, "bold"))
    pen.goto(0, 155)
    pen.write("Small choices. A lighter footprint.", align="center", font=("Arial", 13, "normal"))

    draw_leaf(pen, -175, -75, 1.0)
    draw_footprint(pen, 145, -95, 1.0)

    pen.penup()
    pen.goto(0, -205)
    pen.color("#247A4B")
    pen.write("Choose thoughtfully • Reuse • Repair • Recycle",
              align="center", font=("Arial", 12, "bold"))

    screen.mainloop()


if __name__ == "__main__":
    main()
