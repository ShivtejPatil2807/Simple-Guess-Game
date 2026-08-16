import streamlit as st
import random

ATTEMPTS = 3

st.set_page_config(
    page_title = "Guess Game",
    page_icon = "🤔",
    layout = "centered"
)

def initialize_state():
    Stages = {
        "logged_in": False,
        "username": "",
        "stage": 1,
        "secret_number": random.randint(1, 50),
        "attempts": 0,
        "game_over": False,
        "final_won": False,
        "challenge_a": random.randint(2, 10),
        "challenge_b": random.randint(2, 10),
    }
    for key, value in Stages.items():
        if key not in st.session_state:
            st.session_state[key] = value


def start_stage_one():
    st.session_state.stage = 1
    st.session_state.secret_number = random.randint(1,50)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.final_won = False


def start_final_stage():
    st.session_state.stage = 4
    st.session_state.secret_number = random.randint(1, 30)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.final_won = False


def start_stage_three():
    st.session_state.stage = 3
    st.session_state.challenge_a = random.randint(2, 10)
    st.session_state.challenge_b = random.randint(2, 10)


def restart_game():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.stage = 1
    st.session_state.secret_number = random.randint(1, 50)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.final_won = False
    st.session_state.challenge_a = random.randint(1, 10)
    st.session_state.challenge_b = random.randint(1, 10)


def show_login():
    st.subheader("Welcome! Please enter your name to play.")

    with st.form("login_form"):
        username = st.text_input("Username:")
        submit = st.form_submit_button("Start Game")

        if submit:
            username = username.strip()

            if username:
                st.session_state.username = username
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter a valid username.")


def show_stage_one():
    st.success(f"Welcome, **{st.session_state.username}**!")
    st.write(f"I have selected a number between 1 to 50.")

    guess = st.number_input(
        "Enter your guess:",
        min_value = 1,
        max_value = 50,
        step=1
    )

    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        if guess < st.session_state.secret_number:
            st.warning("📉 Too low! Try a higher number.")

        elif guess > st.session_state.secret_number:
            st.warning("📈 Too high! Try a lower number.")

        else:
            st.session_state.game_over = True 

            st.success(
                f"🎉 Congratulations **{st.session_state.username}**! "
                f"You guessed the number in "
                f"**{st.session_state.attempts} attempts**."
            )
            st.balloons()

    if st.session_state.game_over:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Play Again"):
                start_stage_one()
                st.rerun()

        with col2:
            if st.button("Next Stage"):
                st.session_state.stage = 2
                st.rerun()


def show_stage_two():
    st.success("🎉 Congratulations! You're moving to the next level,Your next opponent is You.")

    st.subheader("⚠️ CRITICAL WARNING READ BEFORE YOU ENTER ")

    st.write("**1.You have successfully completed the first stage.**" )

    st.write("**2.The challenges are getting harder.**")

    st.write("**3.One wrong decision could end your run.**")

    st.write("**4.Your next opponent is not the computer... it is YOU.**")

    st.write("**5.Stay focused. Stay calm. Trust your decisions.**")

    st.write(f"**Good luck {st.session_state.username}.**")

    with st.form("stage_two_form"):
        agree_checkbox = st.checkbox("I understand the rules and choose to continue.")

        continue_button = st.form_submit_button("I AGREE - ENTER IF YOU DARE")

        if continue_button:
            if agree_checkbox:
                start_stage_three()
                st.rerun()
            else:
                st.error("You must accept the rules before continuing.")


def show_stage_three():
    st.subheader("👁️ Now the real challenge begins")
    st.write("Before entering the final stage, solve this verification challenge.")

    a = st.session_state.challenge_a
    b = st.session_state.challenge_b

    correct_answer = (a + b) ** 2
    st.info(f"If $a = {a}$ and $b = {b}$, What is the value of **(a+b)²**?")

    with st.form("verification_form"):
        answer = st.number_input(
            "Enter your answer:",
            min_value = 0,
            step = 1
        )
        submit = st.form_submit_button("Verify")

        if submit:
        
            if answer == correct_answer:
                st.success("✅ Verification successful!")
                start_final_stage()
                st.rerun()
            else:
                st.error("❌ Incorrect answer. Try again.")


def show_final_stage():
    st.subheader("💀 FINAL STAGE")
    st.warning(f"⚠️ You have ONLY {ATTEMPTS} chances!")

    st.write(f"I have selected a number between 1 to 30")

    if not st.session_state.game_over:
        guess = st.number_input(
            "Enter your final guess:",
            min_value = 1,
            max_value = 30,
            step = 1
        )

        if st.button("☠️ GUESS"):
            st.session_state.attempts += 1

            if guess == st.session_state.secret_number:
                st.session_state.final_won = True
                st.session_state.game_over = True

                st.success(
                    f"🎉🏆 CONGRATULATIONS "
                    f"**{st.session_state.username}**!"
                )
                st.success("YOU COMPLETED THE GAME!")
                st.balloons()

            elif st.session_state.attempts >= ATTEMPTS:
                st.session_state.game_over = True

                st.error("💀 YOU FAILED THE FINAL STAGE.")

                st.write("The number was "f"**{st.session_state.secret_number}**.")

            elif guess < st.session_state.secret_number:
                remaining = (ATTEMPTS - st.session_state.attempts)

                st.warning(
                    f"📉 Too low! "
                    f"You have **{remaining} chances** left."
                )

            else:
                remaining = (ATTEMPTS - st.session_state.attempts)

                st.warning(
                    f"📈 Too high! "
                    f"You have **{remaining} chances** left."
                )

    else:
        if st.session_state.final_won:
            st.success(
                f"🎉🏆 Congratulations "
                f"**{st.session_state.username}**!"
            )
            st.success( "***You successfully completed all Stages.***")

        else:
            st.error("GAME OVER!")

            st.write(
                f"Attempts used: "
                f"**{st.session_state.attempts}/"
                f"{ATTEMPTS}**"
            )

            st.divider()

            st.subheader(f"{st.session_state.username} ! BETTER LUCK NEXT TIME")

            st.error("SYSTEM FAILURE")

            if st.button("Restart Game"):
                restart_game()
                st.rerun()

def main():
    initialize_state()

    st.title("🎯 Simple Number Guessing Game")

    if not st.session_state.logged_in:
        show_login()

    elif st.session_state.stage == 1:
        show_stage_one()

    elif st.session_state.stage == 2:
        show_stage_two()

    elif st.session_state.stage == 3:
        show_stage_three()

    elif st.session_state.stage == 4:
        show_final_stage()

if __name__ == "__main__":
    main()