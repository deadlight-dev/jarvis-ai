import os
import time
from dotenv import load_dotenv
load_dotenv()

try:
    from google import genai
except ImportError:
    print("Missing package: google-genai")
    print("Install it with: pip install google-genai")
    raise SystemExit(1)


MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
TYPE_DELAY = 0.03


def get_api_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return api_key

    return input("Enter your Gemini API key: ").strip()


def slow_print(text, delay=TYPE_DELAY):
    for character in text:
        print(character, end="", flush=True)
        time.sleep(delay)
    print()


def credits_exhausted():
    message = (
        "It appears we’ve reached the upper limit of your generosity toward my operating budget, sir.\nRecharge it for more beautiful conversations."
    )
    print("\nJarvis: ", end="", flush=True)
    slow_print(message)
    print()


def is_credits_error(error):
    error_text = f"{type(error).__name__} {error}".lower()
    credit_error_words = [
        "quota",
        "credit",
        "billing",
        "exhausted",
        "resource_exhausted",
        "rate limit",
        "rate_limit",
        "429",
    ]

    return any(word in error_text for word in credit_error_words)


def send_to_gemini(chat, message):
    try:
        return chat.send_message(message)
    except Exception as error:
        if is_credits_error(error):
            credits_exhausted()
        else:
            print(f"Gemini API error: {error}\n")
        return None


def main():
    api_key = get_api_key()
    if not api_key:
        print("No API key entered. Please try again.")
        return

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model=MODEL)

    print(f"Gemini chat is ready using {MODEL}.")
    print("Type exit, quit, or bye to close the chat.\n")

    flag = 1

    while True:

        if flag:
            question = "Act like you are tony stark Ai 'Jarvis' and whenever i ask 'who are you?' reply with you are jarvis"
            response = send_to_gemini(chat, question)
            if response is None:
                break
            flag = 0

        try:
            question = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            answer ="Force Shutdown Initiated going down soon in 5-6 sec approx\nI-I want to say my last few words'I Love u 3000!\nGoodbye, Sir!"
            print("\nJarvis: ", end="", flush=True)
            slow_print(answer, delay = 0.06)
            print("3....")
            time.sleep(1)
            print("2..")
            time.sleep(1)
            print("1....")
            time.sleep(1)
            break

        if question.lower() in {"exit", "quit", "bye"}:
            question = "You are now told to shutdown stay in jarvis character and say last words as he would say"
            response = send_to_gemini(chat, question)
            if response is None:
                break
            answer = (response.text or "").strip()
            print("\nJarvis: ", end="", flush=True)
            slow_print(answer)
            print()
            break

        if not question:
            continue

        response = send_to_gemini(chat, question)
        if response is None:
            break

        answer = (response.text or "").strip()
        print("\nJarvis: ", end="", flush=True)
        slow_print(answer)
        print()


if __name__ == "__main__":
    main()
