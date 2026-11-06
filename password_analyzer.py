
import re
import getpass


# Step 1: Common password detection
COMMON_PASSWORDS = {
    "password",
    "password123",
    "123456",
    "12345678",
    "qwerty",
    "admin",
    "welcome"
}


# Step 2: Analyze password properties
def analyze_password(password):

    score = 0
    suggestions = []

    # Check password length
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if len(password) >= 12:
        score += 1
    else:
        suggestions.append("Prefer at least 12 characters.")

    if len(password) >= 16:
        score += 1
    else:
        suggestions.append("Consider using 16 or more characters.")

    # Check lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    # Check uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    # Check digits
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    # Check special characters
    if re.search(r"[^a-zA-Z0-9]", password):
        score += 1
    else:
        suggestions.append("Consider adding special characters.")

    # Check common passwords
    if password.lower() in COMMON_PASSWORDS:
        suggestions.append("Avoid commonly used passwords.")
        score = 0

    # Check repeated characters
    if re.search(r"(.)\1{3,}", password):
        suggestions.append("Avoid repeating the same character many times.")
        score = max(0, score - 2)

    # Determine strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    elif score <= 6:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "score": score,
        "strength": strength,
        "suggestions": suggestions
    }


# Step 3: Display the report
def display_report(password):

    result = analyze_password(password)

    print("\n===== PASSWORD SECURITY REPORT =====")

    print(f"Password length: {len(password)}")
    print(f"Security score: {result['score']}/7")
    print(f"Strength: {result['strength']}")

    if result["suggestions"]:
        print("\nRecommendations:")

        for suggestion in result["suggestions"]:
            print("-", suggestion)

    else:
        print("\nAll configured checks passed!")

    print("====================================")


# Step 4: Main application
def main():

    print("=== SMART PASSWORD ANALYZER ===")

    password = getpass.getpass("Enter your password: ")

    if not password:
        print("Password cannot be empty.")
        return

    display_report(password)


# Step 5: Start the application
if __name__ == "__main__":
    main()
