import turtle

# Set up the Turtle screen
screen = turtle.Screen()
screen.title("ShopImpact - Turtle Eco Graphics")
screen.bgcolor("#EAF5E9")
screen.setup(width=800, height=600)

pen = turtle.Turtle()
pen.speed(5)
pen.pensize(3)


def draw_leaf(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    pen.color("#176B3A", "#8FE3A0")
    pen.begin_fill()

    pen.setheading(45)

    for _ in range(2):
        pen.circle(50, 90)
        pen.circle(25, 90)

    pen.end_fill()

    # Draw the leaf vein
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color("#176B3A")
    pen.setheading(45)
    pen.forward(85)


def draw_footprint(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    pen.color("#176B3A", "#8FE3A0")
    pen.begin_fill()
    pen.setheading(0)
    pen.circle(30)
    pen.end_fill()

    # Draw five toes
    toe_positions = [
        (x - 20, y + 40),
        (x, y + 55),
        (x + 20, y + 50),
        (x + 35, y + 35),
        (x + 40, y + 15)
    ]

    for toe_x, toe_y in toe_positions:
        pen.penup()
        pen.goto(toe_x, toe_y)
        pen.pendown()
        pen.begin_fill()
        pen.circle(9)
        pen.end_fill()


def draw_title():
    pen.penup()
    pen.goto(0, 220)
    pen.color("#176B3A")
    pen.write(
        "SHOPIMPACT - GO GREEN!",
        align="center",
        font=("Arial", 22, "bold")
    )


# Draw the graphics
draw_title()
draw_leaf(-150, 20)
draw_footprint(120, -80)

pen.hideturtle()

# Keep the Turtle window open
screen.mainloop()
