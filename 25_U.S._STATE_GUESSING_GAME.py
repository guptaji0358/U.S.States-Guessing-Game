import turtle
import pandas as pd

# ================= PATHS =================

STATES_PATH = r"E:\Program Files\RobinData\PYTHON\RawData\50_states.csv"
IMAGE_PATH = r"E:\Program Files\RobinData\PYTHON\RawData\blank_states_img.gif"

# ================= SCREEN =================

screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("🌎 U.S. States Quiz Game")
screen.addshape(IMAGE_PATH)
turtle.shape(IMAGE_PATH)

# ================= DATA =================

data = pd.read_csv(STATES_PATH)
all_states = data.state.to_list()
guessed_states = []

# ================= UI TURTLES =================

writer = turtle.Turtle()
writer.hideturtle()
writer.penup()
writer.color("black")

header = turtle.Turtle()
header.hideturtle()
header.penup()
header.color("darkblue")

message = turtle.Turtle()
message.hideturtle()
message.penup()
message.color("green")

# ================= UI FUNCTIONS =================

def draw_header():
    header.clear()
    header.goto(0, 260)
    header.write(
        "🇺🇸 U.S. STATES QUIZ GAME",
        align="center",
        font=("Arial", 22, "bold"))

def update_score():
    header.goto(0, 230)
    header.write(
        f"Score: {len(guessed_states)} / 50",
        align="center",
        font=("Arial", 14, "normal"))

def show_message(text, color="green"):
    message.clear()
    message.color(color)
    message.goto(0, -260)
    message.write(
        text,
        align="center",
        font=("Arial", 14, "bold"))

def clear_screen():
    writer.clear()
    header.clear()
    message.clear()
    turtle.clear()

def show_missing_states(missing):
    writer.goto(0, 220)
    writer.write(
        "❌ Missed States",
        align="center",
        font=("Arial", 20, "bold"))

    x = -350
    y = 180

    for state in missing:
        writer.goto(x, y)
        writer.write(state, font=("Arial", 12, "normal"))
        y -= 22
        if y < -120:
            y = 180
            x += 200

def show_summary(correct, missed):
    """Show summary at bottom-right"""
    accuracy = int((correct / 50) * 100)
    # Bottom-right corner
    writer.goto(250, -220)
    text = (
        "📊 SUMMARY\n"
        f"Correct : {correct}\n"
        f"Missed  : {missed}\n"
        f"Accuracy: {accuracy}%")

    writer.write(
        text,
        align="left",
        font=("Arial", 14, "bold"))

def ask_to_save(missing):
    choice = screen.textinput(
        title="Download File",
        prompt="Save missed states? (yes / no)") 
    
    if choice and choice.lower() == "yes":
        df = pd.DataFrame(missing, columns=["Missed States"])
        df.to_csv("states_to_learn.csv", index=False)
        writer.goto(250, -260)
        writer.write(
            "✅ File Saved",
            align="left",
            font=("Arial", 12, "bold"))
        
        screen.ontimer(screen.bye, 2500)
    else:
        writer.goto(250, -260)
        writer.write(
            "❌ File Not Saved",
            align="left",
            font=("Arial", 12, "bold"))

    screen.ontimer(screen.bye, 2500)

# ================= START =================

draw_header()
update_score()

show_message("Type state name (or type Exit)", "blue")

# ================= MAIN LOOP =================

while len(guessed_states) < 50:
    answer = screen.textinput(
        title=f"{len(guessed_states)}/50 States",
        prompt="Enter State Name (or Exit)")
    
    if answer is None:
        break

    user_guess = answer.strip().title()

    # EXIT MODE
    if user_guess == "Exit":
        missing_states = [
            state for state in all_states
            if state not in guessed_states]

        correct = len(guessed_states)
        missed = len(missing_states)

        clear_screen()
        show_missing_states(missing_states)
        show_summary(correct, missed)
        ask_to_save(missing_states)
        break

    # CORRECT
    if user_guess in all_states and user_guess not in guessed_states:
        guessed_states.append(user_guess)
        state_data = data[data.state == user_guess]
        writer.goto(
            int(state_data.x.item()),
            int(state_data.y.item()))
        
        writer.write(user_guess)

        header.clear()
        draw_header()
        update_score()
        show_message("✅ Correct!", "green")

    # WRONG / DUPLICATE
    else:
        show_message("❌ Wrong / Already Guessed", "red")

# ================= WIN =================

if len(guessed_states) == 50:
    clear_screen()
    show_summary(50, 0)
    ask_to_save([])

screen.exitonclick()
