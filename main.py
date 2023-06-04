"""
Anki cards are a great way to learn and memorize anything. 
This program continually prompts for textbook passages and
can turn them into valid anki cards automatically.
"""
import os
from utils.anki import create_card, print_card
from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init()

def input_passage():
    print("Enter a textbook passage to be turned into an anki card then hit ENTER + CTRL-D:\n")
    contents = []
    while True:
        try:
            line = input("")
        except EOFError:
            break
        contents.append(line)
    
    return "\n".join(contents)

def save_cards(cards):
    # Ask user for output file name and ask for confirmation if file already exists
    while True:
        out_file = input("Enter the name of the output file: ")
        if os.path.exists(out_file):
            overwrite = input(
                "Output file already exists. Do you want to overwrite it? (y/n): "
            )
            overwrite = overwrite.lower()

            if overwrite == "y":
                break
        else:
            break
    
    # Write cards to file in csv format
    with open(out_file, "w") as f:
        for card in cards:
            f.write(f'"{card.question}","{card.answer}"\n')

def main():
    # Initialize OpenAI API

    # Print welcome message
    print(f"{Fore.GREEN}Welcome to Anki Card Generator! 🃏")
    print(f"Type {Fore.RED}'exit' {Fore.GREEN}to exit the program.{Style.RESET_ALL}")
    print()

    cards = []
    regenerate = False
    while True:
        if not regenerate:
            text = input_passage()

            if text.lower().strip() == "exit":
                break
            
        print(f"{Fore.YELLOW}Generating anki card... 🧞‍♂️{Style.RESET_ALL}")

        # Generate anki card
        card = create_card(text)

        # Print anki card
        print_card(card)

        # Ask user if they want to save the anki card, delete it, or generate a new one
        action = input("Press y to save, n to delete, or any other key to re-generate the card: ")
        action = action.lower()

        if action == "y":
            cards.append(card)
            print(f"{Fore.GREEN}Card saved!{Style.RESET_ALL}")
            print()
        elif action == "n":
            print(f"{Fore.RED}Card deleted!{Style.RESET_ALL}")
            print()
        else:
            print(f"{Fore.YELLOW}Re-generating card...{Style.RESET_ALL}")
            print()

    print()
    print(f"{Fore.GREEN}Here are your saved cards:{Style.RESET_ALL}")
    print()
    for card in cards:
        print_card(card)
    
    save_cards(cards)


if __name__ == "__main__":
    main()
