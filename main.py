"""
Anki cards are a great way to learn and memorize anything. 
This program continually prompts for textbook passages and
can turn them into valid anki cards automatically.
"""
import os
from utils.anki import create_card, print_card
from colorama import Fore, Style
from colorama import init as colorama_init
from bs4 import BeautifulSoup

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

def add_card_to_html(question, answer, filename='cards.html'):
    html_doc = """
    <html>
    <head>
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f5f5f5;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        padding: 20px;
    }
    h1 {
        width: 100%;
        text-align: center;
        color: #333;
        margin: 20px 0;
    }
    .card {
        background-color: #fff;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        width: 30%;
        border-radius: 10px;
        margin: 10px;
        padding: 20px;
        box-sizing: border-box;
    }
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
    }
    </style>
    </head>
    <body>
    <h1>AutoAnki</h1>
    </body>
    </html>
    """

    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    else:
        soup = BeautifulSoup(html_doc, 'html.parser')

    new_card = soup.new_tag('div')
    new_card.attrs.update({'class': 'card'})
    question_tag = soup.new_tag('h3')
    question_tag.string = question
    answer_tag = soup.new_tag('p')
    answer_tag.string = answer
    new_card.append(question_tag)
    new_card.append(answer_tag)

    soup.body.append(new_card)

    with open(filename, 'w', encoding='utf-8') as f_out:
        f_out.write(str(soup.prettify()))

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
            add_card_to_html(card.question, card.answer)

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
        else:
            regenerate = False
            
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
            regenerate = True

    print()
    print(f"{Fore.GREEN}Here are your saved cards:{Style.RESET_ALL}")
    print()
    for card in cards:
        print_card(card)
    
    save_cards(cards)


if __name__ == "__main__":
    main()
