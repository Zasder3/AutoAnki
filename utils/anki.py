from .openai import init_openai_api, complete_request
from dataclasses import dataclass
from colorama import Fore, Style

init_openai_api()

@dataclass
class AnkiCard:
    question: str
    answer: str

    def __repr__(self) -> str:
        return f"AnkiCard(question={self.question}, answer={self.answer})"

def append_anki_prompt(prompt: str) -> str:
    # Append information that will explain the function of the Anki and generate a high-quality card
    injected_prompt = """Anki is a flashcard program that uses spaced repetition to help you memorize information. 
    For example, if you have a card that asks you "What is the capital of France?" and you answer "Paris", the card would look like this:
    [QUESTION]: What is the capital of France?
    [ANSWER]: Paris

    Using the following textbook snippet, generate a quality question and answer pair in the format above:
    """

    return injected_prompt + prompt

def strip_response(response: dict) -> AnkiCard:
    # Strip the response from OpenAI and return a valid AnkiCard
    response_text = response["choices"][0]["message"]["content"]

    q_begin = response_text.find("[QUESTION]: ") + len("[QUESTION]: ")
    q_end = response_text.find("[ANSWER]: ")

    a_begin = q_end + len("[ANSWER]: ")

    question = response_text[q_begin:q_end]
    answer = response_text[a_begin:]

    return AnkiCard(question, answer)
    

def create_card(prompt: str) -> AnkiCard:
    prompt = append_anki_prompt(prompt)
    response = complete_request(prompt)
    return strip_response(response)

def print_card(card: AnkiCard) -> None:
    print("=========================================")
    print(f"{Fore.BLUE}[Question]: {Style.RESET_ALL}{card.question.strip()}")
    print(f"{Fore.BLUE}[Answer]: {Style.RESET_ALL}{card.answer.strip()}")
    print("=========================================")
    print()
