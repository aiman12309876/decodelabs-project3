import random
import string

def generate_password(length, use_special=False):
    if length < 4:
        print(" Password length should be at least 4 characters!")
        return None

    characters = string.ascii_letters + string.digits

    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    if not any(c.islower() for c in password):
        password = password[:-1] + random.choice(string.ascii_lowercase)
    if not any(c.isupper() for c in password):
        password = password[:-1] + random.choice(string.ascii_uppercase)
    if not any(c.isdigit() for c in password):
        password = password[:-1] + random.choice(string.digits)
    if use_special and not any(c in string.punctuation for c in password):
        password = password[:-1] + random.choice(string.punctuation)

    return password

def check_password_strength(password):
    score = 0

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 2

    if score >= 6:
        return "STRONG"
    elif score >= 4:
        return "MEDIUM"
    else:
        return "WEAK"

def main():
    print("\n" + "=" * 50)
    print("   RANDOM PASSWORD GENERATOR")
    print("=" * 50)

    try:
        length = int(input("Enter password length: "))
        if length < 4:
            print(" Minimum length is 4 characters.")
            return

        include_special = input("Include special characters? (y/n): ").lower() == 'y'

        password = generate_password(length, include_special)

        if password:
            print("\n" + "-" * 40)
            print(" Generated Password:")
            print(f"   {password}")
            print("-" * 40)

            strength = check_password_strength(password)
            print(f" Password Strength: {strength}")

            if strength == "WEAK":
                print("   Tip: Use 8+ characters with uppercase, lowercase, numbers, and symbols.")
            elif strength == "MEDIUM":
                print("   Tip: Add more characters or special symbols for better security.")

            print("-" * 40)
        else:
            print(" Password generation failed. Please try again.")

    except ValueError:
        print(" Please enter a valid number!")

    print("\n" + "=" * 50)
    print("   PASSWORD GENERATOR COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()