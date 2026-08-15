import streamlit as st
import random
import os

st.set_page_config(
    page_title = "Guess Game",
    page_icon = "🤔",
    layout = "centered"
)
st.title("🎯 Simple Number Guessing Game")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 50)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "next_stage" not in st.session_state:
    st.session_state.next_stage = False

if "third_stage" not in st.session_state:
    st.session_state.third_stage = False

if "final_stage" not in st.session_state:
    st.session_state.final_stage = False

if "final_won" not in st.session_state:
    st.session_state.final_won = False

def reset_game():
    st.session_state.secret_number = random.randint(1, 50)
    st.session_state.attempts = 0
    st.session_state.game_over = False

if not st.session_state.logged_in:
    st.subheader("Welcome! Please enter your name to play.")

    with st.form("login_form"):
        username_input = st.text_input("Username:")
        submit_login = st.form_submit_button("Submit")

        if submit_login:
            if username_input.strip() != "":
                st.session_state.username = username_input.strip()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter a valid username to continue.")

elif not st.session_state.next_stage :

    st.success(f"Login successfully, **{st.session_state.username}**! ")
    st.write("I have picked a random number between **1 and 50**. Try to guess it!")

    guess = st.number_input(
        "Enter your guess:",
        min_value = 1,
        max_value = 50,
        step = 1,
    )

    if st.button("Submit Guess"):
        st.session_state.attempts += 1

        if guess < st.session_state.secret_number:
            st.warning("📉 Too low! Try a higher number.")
        elif guess > st.session_state.secret_number:
            st.warning("📈 Too high! Try a lower number.")
        else:
            st.success(
                f"🎉 Congratulations {st.session_state.username}! You guessed the"
                f" number in {st.session_state.attempts} attempts."
            )
            st.session_state.game_over = True
            st.balloons()

    if st.session_state.game_over:
        col1,col2 = st.columns(2)

        with col1:
            if st.button("Play Again"):
                reset_game()
                st.rerun()
        with col2:
            if st.button("Next Stage"):
                st.session_state.next_stage = True
                st.rerun()

elif not st.session_state.third_stage:
    st.success("🎉Congratulations ! Your moving to the next level," \
    "Your next opponent is you")

    with st.form("Instructions"):
        st.subheader("⚠️**CRITICAL WARNING READ BEFORE YOU ENTER**⚠️")
        st.write("***1. You have successfully survied the first stage.***")
        st.write("***2. Now, Your officially entered in this game.***")
        st.write("***3. The puzzels are getting harder.***")
        st.write("***4. One wrong decision could end your run. Think carefully before you act.***")
        st.write("***5. Your next opponent is not computer... it is YOU.***")
        st.write("***6. Stay focused. Stay calm. Trust nothinng.***")
        st.write("***7. You chose to be on this stage and play your part right now.***")
        st.write("***8."f" GOOD LUCK **{st.session_state.username}**... YOU'RE GOING TO NEED IT.***")

        agree_checkbox = st.checkbox("I Understand the risk. I accept resposibility and choose to continue")
        agree = st.form_submit_button("I AGREE - ENTER IF YOU DARE")

        if agree:
            if agree_checkbox:
                st.session_state.third_stage = True
                st.rerun()
            else:
                st.error("You must check the box before entering the next stage !")

elif not st.session_state.final_stage:
    st.subheader("👁️ Now the real challenge begins.")
    with st.form("Risk"):
        st.write("**1.GO to Command Prompt C:\> on your laptop/PC💻.**")
        st.write("**2.For Linux/Unix/macOs:Open terminal.**")
        st.write("**2.systeminfo run this command.**")
        st.write("**3.Copy the System Directory : path and paste here⬇️.**")

    with st.form("Path"):
        user_enter = st.text_input("Paste Your System Directory (path):",placeholder = r"C:\Users\JohnDoe\Documents\report")
        submit = st.form_submit_button("Submit")

        if submit:
            if os.path.isdir(user_enter):
                st.session_state.final_stage = True

                st.session_state.secret_number = random.randint(1, 30)
                st.session_state.attempts = 0
                st.session_state.game_over = False
                st.session_state.final_won = False
                                                                    
                st.rerun()

            else:
                st.error("Invalid Path..! Please check the system path again ")

else:
    st.subheader("💀 FINAL STAGE")
    st.warning("⚠️ You have ONLY 3 chances to guess the number!")
    st.write("I have selected a number between **1 and 30**.")

    if not st.session_state.game_over:
        new_guess = st.number_input(
            "Enter your guess:",
            min_value=1,
            max_value=30,
            step=1
        )

        if st.button("☠️ GUESS"):
            st.session_state.attempts += 1
            if new_guess == st.session_state.secret_number:

                st.session_state.final_won = True
                st.session_state.game_over = True

                st.success(
                    f"🎉🏆 CONGRATULATIONS "
                    f"{st.session_state.username}! "
                    f"YOU COMPLETED THIS GAME!"
                )
                st.balloons()

            elif st.session_state.attempts == 3:
                st.session_state.game_over = True

                st.error("💀 YOU FAILED THE FINAL STAGE.")
                st.write(f"The number was **"f"{st.session_state.secret_number}**.")

            elif new_guess < st.session_state.secret_number:
                remaining = 3 - st.session_state.attempts

                st.warning(f"📉 Too low! You have **{remaining} chances** left.")

            else:
                remaining = 3 - st.session_state.attempts
                st.warning(f"📈 Too high! You have **{remaining} chances** left.")

    else:
        if st.session_state.final_won:
            st.success(
                f"🎉🏆 CONGRATULATIONS "
                f"{st.session_state.username}! "
                f"YOU COMPLETED THIS GAME!"
            )
        else:
            st.error(" GAME OVER!")
            st.write(f"Attempts used: "f"**{st.session_state.attempts}/3**")
            st.divider()

            st.subheader(f"{st.session_state.username} ! BETTER LUCK NEXT TIME")
            st.error("SYSTEM FAILURE")

            if st.button("Restart Game"):
                st.session_state.secret_number = random.randint(1, 50)
                st.session_state.attempts = 0
                st.session_state.game_over = False
                st.session_state.next_stage = False
                st.session_state.third_stage = False
                st.session_state.final_stage = False
                st.session_state.final_won = False

                st.rerun()


    