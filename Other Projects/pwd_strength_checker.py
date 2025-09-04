import re

def check_password_strength(password):
    # Initialize score and feedback
    score = 0
    feedback = []

    # Criteria for password strength
    if len(password) >= 8:
        score += 2
    else:
        feedback.append("is too short")
    
    if re.search(r"[A-Za-z]", password):
        score += 2
    else:
        feedback.append("should include letters")
    
    if re.search(r"[0-9]", password):
        score += 2
    else:
        feedback.append("should include numbers")
    
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 2
    else:
        feedback.append("should include special characters")
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        feedback.append("could be longer")

    # Generate feedback and overall strength
    if score < 4:
        strength = "Weak Password"
    elif score < 8:
        strength = "Moderate Password"
    else:
        strength = "Strong Password"
    
    feedback_summary = ", ".join(feedback) if feedback else "meets all the criteria"
    return score, f"\n{strength}! Score: {score}/10\n\nFeedback: Password {feedback_summary}."

# Continuously prompt the user until the password is rated 10/10
while True:
    password = input("\nEnter a password to check strength: ")
    score, result = check_password_strength(password)
    print(result)
    if score == 10:
        print("\nCongratulations! Your password is good to go, make sure to never reuse the same password multiple times, especially for important accounts.")
        break
