import random

def guess_number():
    num = random.randint(1, 10)
    print("Guess a number between 1 and 10:")
    guess = int(input("> "))
    return "Correct!" if guess == num else f"Nope! It was {num}"

def rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    ai = random.choice(choices)
    user = input("rock / paper / scissors: ").lower()

    if user == ai:
        return "Tie!"
    elif (user == "rock" and ai == "scissors") or \
         (user == "paper" and ai == "rock") or \
         (user == "scissors" and ai == "paper"):
        return f"You win! I chose {ai}"
    else:
        return f"You lose! I chose {ai}"
