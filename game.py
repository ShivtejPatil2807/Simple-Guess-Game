import streamlit as st
import random
import os

# STREAMLIT PAGE CONFIGURATION
st.set_page_config(
    page_title = "Guess Game",
    page_icon = "🤔",
    layout = "centered"
)
st.title("🎯 Simple Number Guessing Game")

# SESSION STATE INITIALIZATION

# Login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Game
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 50)

# count the number of guesses
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# controls movement from Stage 1 to Stage 2
if "next_stage" not in st.session_state:
    st.session_state.next_stage = False

# controls movement from Stage 2 to Stage 3
if "third_stage" not in st.session_state:
    st.session_state.third_stage = False

# controls movement to the final Stage
if "final_stage" not in st.session_state:
    st.session_state.final_stage = False

if "final_won" not in st.session_state:
    st.session_state.final_won = False

#===== RESET GAME =====
def reset_game():
    st.session_state.secret_number = random.randint(1, 50)
    st.session_state.attempts = 0
    st.session_state.game_over = False

#===== LOGIN PAGE =====
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

#===== GAME PAGE =====
    st.success(f"Login successfully, **{st.session_state.username}**! ")
    st.write("I have picked a random number between **1 and 50**. Try to guess it!")

#===== GUESS INPUT =====
    guess = st.number_input(
        "Enter your guess:",
        min_value = 1,
        max_value = 50,
        step = 1,
    )

#===== SUBMIT GUESS =====
    if st.button("Submit Guess"):
        # Increase Attempts
        st.session_state.attempts += 1

        # Check guess
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

#===== BUTTONS AFTER WINING THE STAGE =====

    if st.session_state.game_over:
        col1,col2 = st.columns(2)

        # Play Again Button
        with col1:
            if st.button("Play Again"):
                reset_game()
                st.rerun()

        # Next Stage Button
        with col2:
            if st.button("Next Stage"):
                # Move to stage 2 
                st.session_state.next_stage = True
                st.rerun()

#===== STAGE 2 - WARNING AND INSTRUCTIONS =====
elif not st.session_state.third_stage:
    st.success("🎉Congratulations ! Your moving to the next level," \
    "Your next opponent is you")

    # instructions form
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

        # Checkbox that the player must select
        agree_checkbox = st.checkbox("I Understand the risk. I accept resposibility and choose to continue")
        # Button to enter next stage
        agree = st.form_submit_button("I AGREE - ENTER IF YOU DARE")

        # Check whether button was clicked
        if agree:
            # Make sure checkbox was selected
            if agree_checkbox:
                # Move to the third stage
                st.session_state.third_stage = True
                st.rerun()
            else:
                # checkbox was not selected
                st.error("You must check the box before entering the next stage !")

#===== STAGE 3 - PATH VERIFICATION =====
elif not st.session_state.final_stage:
    st.subheader("👁️ Now the real challenge begins.")
    with st.form("Risk"):
        # instructions for the player
        st.write("**1.GO to Command Prompt C:\> on your laptop/PC💻.**")
        st.write("**2.For Linux/Unix/macOs:Open terminal.**")
        st.write("**2.systeminfo run this command.**")
        st.write("**3.Copy the System Directory : path and paste here⬇️.**")

    # Path input form
    with st.form("Path"):
        user_enter = st.text_input("Paste Your System Directory (path):",placeholder = r"C:\Users\JohnDoe\Documents\report")
        # Submit Path
        submit = st.form_submit_button("Submit")

        # Check if path submit
        if submit:
            if os.path.isdir(user_enter):
                # Move to final stage
                st.session_state.final_stage = True

                # Create a new secret number for the final game
                st.session_state.secret_number = random.randint(1, 30)
                st.session_state.attempts = 0
                st.session_state.game_over = False
                st.session_state.final_won = False

                # Reload application                                        
                st.rerun()

            else:
                # Invalid directory
                st.error("Invalid Path..! Please check the system path again ")

#===== FINAL STAGE - ONLY 3 CHANCES =====
else:
    st.subheader("💀 FINAL STAGE")
    # Tell player they have only 3 chances
    st.warning("⚠️ You have ONLY 3 chances to guess the number!")
    # Tell player the number range
    st.write("I have selected a number between **1 and 30**.")

#===== FINAL GAME STILL ACTIVE =====
    if not st.session_state.game_over:
        new_guess = st.number_input(
            "Enter your guess:",
            min_value=1,
            max_value=30,
            step=1
        )
        # Guess Button
        if st.button("☠️ GUESS"):
            #increase attempts
            st.session_state.attempts += 1

            # The number is gueed 
            if new_guess == st.session_state.secret_number:

                # Store that player won
                st.session_state.final_won = True
                # End Game
                st.session_state.game_over = True

                # Show Wining
                st.success(
                    f"🎉🏆 CONGRATULATIONS "
                    f"{st.session_state.username}! "
                    f"YOU COMPLETED THIS GAME!"
                )
                st.balloons()

            # Player used all 3 attempts
            elif st.session_state.attempts == 3:

                # End the final game
                st.session_state.game_over = True

                # Show failure message
                st.error("💀 YOU FAILED THE FINAL STAGE.")

                # Reveal the secret number
                st.write(f"The number was **"f"{st.session_state.secret_number}**.")

            # Guess to Low
            elif new_guess < st.session_state.secret_number:

                # Attempts - 1 chance
                remaining = 3 - st.session_state.attempts

                st.warning(f"📉 Too low! You have **{remaining} chances** left.")

            # Guess to High
            else:
                # Calculate remaining attempts 
                remaining = 3 - st.session_state.attempts
                st.warning(f"📈 Too high! You have **{remaining} chances** left.")

#===== FINAL GAME OVER SCREEN =====
    else:
        # Player successfully completed the game
        if st.session_state.final_won:
            st.success(
                f"🎉🏆 CONGRATULATIONS "
                f"{st.session_state.username}! "
                f"YOU COMPLETED THIS GAME!"
            )

        # Player failed the final stage
        else:
            st.error(" GAME OVER!")

            # Show the number of attempt used
            st.write(f"Attempts used: "f"**{st.session_state.attempts}/3**")
            st.divider()

            # Game over messege 
            st.subheader(f"{st.session_state.username} ! BETTER LUCK NEXT TIME")
            st.error("SYSTEM FAILURE")

            # Restart Button 
            if st.button("Restart Game"):

                # Create new stage 1 number
                st.session_state.secret_number = random.randint(1, 50)
                st.session_state.attempts = 0
                st.session_state.game_over = False
                st.session_state.next_stage = False
                st.session_state.third_stage = False
                st.session_state.final_stage = False
                st.session_state.final_won = False

                st.rerun()


    