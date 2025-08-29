import streamlit as st
import random
import math

# Clear questions if query param _rerun is set
query_params = st.experimental_get_query_params()
if "_rerun" in query_params:
    for key in ["questions", "answers", "last_topic", "last_count"]:
        st.session_state.pop(key, None)
    # Clear the param so it doesn’t keep clearing
    st.experimental_set_query_params()


def rerun():
    # Change a query param to force rerun
    st.experimental_set_query_params(_rerun=str(random.random()))



st.write("Your Streamlit version is:", st.__version__)

st.set_page_config(page_title="📘 Grade 7 math quiz for JS", layout="centered")

st.title("📘 Interactive Geometry & Time Quiz")
st.subheader("Where stupid meets genius")
st.write("Made by the one and only Maahin ofc")

# Topics available
topics = [
    "Area of Circle", "Perimeter of Circle",
    "Area of Square", "Perimeter of Square", "Volume of Cube",
    "Area of Rectangle", "Perimeter of Rectangle", "Volume of Cuboid",
    "Area of Triangle", "Perimeter of Triangle",
    "Area of Parallelogram",
    "Area of Trapezium",
    "Time: Elapsed Time", "Time: Convert Minutes & Hours"
]

# User picks topic and question count
topic = st.selectbox("Choose a topic:", topics)
num_questions = st.slider("How many questions?", 5, 15, 5)



# Geometry/time generators
def area_circle():
    r = random.randint(1, 20)
    q = f"Find the area of a circle with radius {r} cm."
    a = round(math.pi * r ** 2, 2)
    return q, a


def perimeter_circle():
    r = random.randint(1, 20)
    q = f"Find the perimeter (circumference) of a circle with radius {r} cm."
    a = round(2 * math.pi * r, 2)
    return q, a


def area_square():
    s = random.randint(2, 30)
    q = f"Find the area of a square with side {s} cm."
    a = s ** 2
    return q, a


def perimeter_square():
    s = random.randint(2, 30)
    q = f"Find the perimeter of a square with side {s} cm."
    a = 4 * s
    return q, a


def volume_cube():
    s = random.randint(2, 15)
    q = f"Find the volume of a cube with side {s} cm."
    a = s ** 3
    return q, a


def area_rectangle():
    l = random.randint(5, 40)
    w = random.randint(5, 40)
    q = f"Find the area of a rectangle with length {l} cm and width {w} cm."
    a = l * w
    return q, a


def perimeter_rectangle():
    l = random.randint(5, 40)
    w = random.randint(5, 40)
    q = f"Find the perimeter of a rectangle with length {l} cm and width {w} cm."
    a = 2 * (l + w)
    return q, a


def volume_cuboid():
    l = random.randint(3, 15)
    w = random.randint(3, 15)
    h = random.randint(3, 15)
    q = f"Find the volume of a cuboid with length {l} cm, width {w} cm, and height {h} cm."
    a = l * w * h
    return q, a


def area_triangle():
    b = random.randint(5, 30)
    h = random.randint(5, 30)
    q = f"Find the area of a triangle with base {b} cm and height {h} cm."
    a = 0.5 * b * h
    return q, round(a, 2)


def perimeter_triangle():
    a = random.randint(5, 20)
    b = random.randint(5, 20)
    c = random.randint(5, 20)
    q = f"Find the perimeter of a triangle with sides {a} cm, {b} cm, and {c} cm."
    return q, a + b + c


def area_parallelogram():
    b = random.randint(5, 25)
    h = random.randint(5, 25)
    q = f"Find the area of a parallelogram with base {b} cm and height {h} cm."
    a = b * h
    return q, a


def area_trapezium():
    a = random.randint(5, 25)
    b = random.randint(5, 25)
    h = random.randint(5, 20)
    q = f"Find the area of a trapezium with bases {a} cm and {b} cm and height {h} cm."
    area = ((a + b) / 2) * h
    return q, round(area, 2)


def time_elapsed():
    start_hour = random.randint(1, 10)
    duration = random.randint(30, 180)
    end_hour = (start_hour * 60 + duration) // 60
    end_min = (start_hour * 60 + duration) % 60
    q = f"If an event starts at {start_hour}:00 and lasts for {duration} minutes, what time does it end? (Format: HH:MM)"
    a = f"{end_hour}:{str(end_min).zfill(2)}"
    return q, a


def time_convert():
    mins = random.randint(60, 600)
    q = f"Convert {mins} minutes to hours and minutes. (Format: H hours M minutes)"
    a = f"{mins // 60} hours {mins % 60} minutes"
    return q, a


question_bank = {
    "Area of Circle": area_circle,
    "Perimeter of Circle": perimeter_circle,
    "Area of Square": area_square,
    "Perimeter of Square": perimeter_square,
    "Volume of Cube": volume_cube,
    "Area of Rectangle": area_rectangle,
    "Perimeter of Rectangle": perimeter_rectangle,
    "Volume of Cuboid": volume_cuboid,
    "Area of Triangle": area_triangle,
    "Perimeter of Triangle": perimeter_triangle,
    "Area of Parallelogram": area_parallelogram,
    "Area of Trapezium": area_trapezium,
    "Time: Elapsed Time": time_elapsed,
    "Time: Convert Minutes & Hours": time_convert
}

st.markdown("### 📝 Your Quiz")

if st.button("🔁 Reset Questions"):
    for key in ["questions", "answers", "last_topic", "last_count"]:
        st.session_state.pop(key, None)
    rerun()


# Generate questions once and store in session state
if "questions" not in st.session_state or "answers" not in st.session_state or st.session_state.get("last_topic") != topic or st.session_state.get("last_count") != num_questions:
    questions = []
    answers = []
    for _ in range(num_questions):
        q, a = question_bank[topic]()
        questions.append(q)
        answers.append(a)
    st.session_state.questions = questions
    st.session_state.answers = answers
    st.session_state.last_topic = topic
    st.session_state.last_count = num_questions
else:
    questions = st.session_state.questions
    answers = st.session_state.answers


# Student answers and feedback
score = 0
for i in range(num_questions):
    st.markdown(f"**{i + 1}. {questions[i]}**")

    if isinstance(answers[i], (int, float)):
        user_input = st.number_input(f"Your answer for Q{i + 1}:", key=f"input_{i}")
    else:
        user_input = st.text_input(f"Your answer for Q{i + 1}:", key=f"input_{i}")

    # Evaluate
    if st.button(f"Check Q{i + 1}", key=f"check_{i}"):
        if isinstance(answers[i], float):
            if abs(user_input - answers[i]) < 0.1:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {answers[i]}")
        elif isinstance(answers[i], int):
            if user_input == answers[i]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {answers[i]}")
        else:
            if str(user_input).strip().lower() == str(answers[i]).strip().lower():
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. Correct answer: {answers[i]}")


import datetime  # Add this at the top of your file if not already

# Feedback Section
st.markdown("---")
with st.expander("💬 Give Feedback"):
    st.write("We’d love to hear your thoughts!")

    name = st.text_input("Your name or email (optional):")
    feedback = st.text_area("Type your feedback here:")

    if st.button("Submit Feedback"):
        if feedback.strip() == "":
            st.warning("Please type something before submitting.")
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"{timestamp}\nName: {name}\nFeedback: {feedback}\n---\n"

            # Save to file
            with open("feedback.txt", "a", encoding="utf-8") as f:
                f.write(entry)

            st.success("Thanks! Your feedback has been received.")

with st.expander("📂 View All Feedback (Admin Only)"):
    admin_password = st.text_input("Enter admin password to view feedback:", type="password")

    if admin_password == "letmein123":  # <- change this to your own secret password
        try:
            with open("feedback.txt", "r", encoding="utf-8") as f:
                feedback_data = f.read()
                st.text_area("Feedback received so far:", value=feedback_data, height=300)
        except FileNotFoundError:
            st.info("No feedback has been submitted yet.")
    elif admin_password != "":
        st.error("Incorrect password.")


