import random

def human_move(piles):
    print(f"Current piles - Red: {piles['red']}, Blue: {piles['blue']}")
    while True:
        color = input("Choose a color to take from (red/blue): ").strip().lower()
        if color in piles:
            num = int(input(f"How many {color} marbles to take (1 or 2)? "))
            if num == 1 or num == 2:
                if num > piles[color]:
                    print(f"Not enough marbles in {color} pile. Try again.")
                    continue
                else:
                    piles[color] -= num
                    return
            else:
                print("Invalid number! Try again.")
        else:
            print("Invalid color. Try again!")

def get_computer_move(piles):
    print(f"Current piles - Red: {piles['red']}, Blue: {piles['blue']}")
    while True:
        color = random.choice(['red', 'blue'])
        if piles[color] > 0:
            num = random.randint(1, 2)
            if num <= piles[color]:
                piles[color] -= num
                print(f"Computer takes {num} {color} marble(s).")
                return

def calculate_score(piles):
    red_score = piles['red'] * 2
    blue_score = piles['blue'] * 3
    return red_score + blue_score

def main():
    num_red = int(input("Enter number of red marbles: "))
    num_blue = int(input("Enter number of blue marbles: "))
    version = input("Enter game version (standard/misere): ").strip().lower()
    first_player = input("Enter first player (computer/human): ").strip().lower()
    
    # Validate game version
    if version != "standard" and version != "misere":
        print("Invalid version. Choose 'standard' or 'misere'.")
        return
    # Validate first player
    elif first_player != "human" and first_player != "computer":
        print("Invalid first player. Choose 'computer' or 'human'.")
        return

    piles = {"red": num_red, "blue": num_blue}
    turn = first_player
    
    while True:
        if turn == 'human':
            human_move(piles)
            turn = 'computer'
        else:
            get_computer_move(piles)
            turn = 'human'
        
        # Check if game is over
        if piles['red'] == 0 or piles['blue'] == 0:
            print(f"Game Over! Final piles - Red: {piles['red']}, Blue: {piles['blue']}")
            player_score = calculate_score(piles)
            computer_score = calculate_score(piles)
            print(f"Player score: {player_score}")
            print(f"Computer score: {computer_score}")
            
            # Determine winner based on game version
            if version == 'standard':
                if player_score > computer_score:
                    print("Human wins!")
                elif computer_score > player_score:
                    print("Computer wins!")
                else:
                    print("It's a draw!")
            elif version == 'misere':
                if player_score < computer_score:
                    print("Human wins!")
                elif computer_score < player_score:
                    print("Computer wins!")
                else:
                    print("It's a draw!")
            break

if __name__ == "__main__":
    main()
