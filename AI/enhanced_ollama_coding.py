# Ollama enhanced for coding.

import ollama

def get_language_mapping():
    """Returns a dictionary mapping short codes to full language names."""
    return {
        'p': "Python",
        'j': "Java",
        'js': "JavaScript",
        'html': "HTML",
        'css': "CSS"
    }

def select_task():
    """Prompts the user to select a task and validates the input."""
    tasks = {
        'd': "Debug",
        'b': "Base",
        'o': "Optimize",
        'r': "Review",
        's': "Suggestions",
        'e': "Explain",
        'x': "eXamples",
        'c': "Convert"
    }
    print("\nAvailable tasks: " + ", ".join(f"{v}" for k, v in tasks.items()))
    need = input("Select a task: ").lower()
    if need not in tasks:
        print("Invalid task selection. Please restart the program.")
        return None
    return need

def select_language(prompt):
    """Prompts the user to select a language and returns the full language name."""
    lang_mapping = get_language_mapping()
    lang = input(prompt).lower()
    return lang_mapping.get(lang, None)

def generate_prompt(task, lang1, user_input, lang2=None):
    """Generates the appropriate prompt based on the task and input."""
    if task == 'd':
        return f"Debug this {lang1} code: {user_input}"
    elif task == 'b':
        return f"Write base {lang1} code for this task: {user_input}"
    elif task == 'o':
        return f"Optimize this {lang1} code: {user_input}"
    elif task == 'r':
        return f"Review this {lang1} code: {user_input}"
    elif task == 's':
        return f"Provide suggestions for how to code this in {lang1}: {user_input}"
    elif task == 'e':
        return f"Explain this {lang1} code: {user_input}"
    elif task == 'x':
        return f"Provide {lang1} code examples for: {user_input}"
    elif task == 'c' and lang2:
        return f"Convert this {lang1} code to {lang2}: {user_input}"
    else:
        raise ValueError("Invalid task or missing conversion target language.")

def chat_with_llama():
    """Main function to interact with the Llama model."""
    print("Welcome to the CodeGemma chat! Type 'exit' to end the conversation.\n")

    # Task selection
    task = select_task()
    if not task:
        return

    # Language selection
    lang1 = select_language("Select the source language (p/j/js/html/css): ")
    if not lang1:
        print("Invalid language selection. Please restart the program.")
        return

    lang2 = None
    if task == 'c':  # Conversion task
        lang2 = select_language("Convert to what language (p/j/js/html/css): ")
        if not lang2:
            print("Invalid target language selection. Please restart the program.")
            return

    # Conversation loop
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Goodbye! Ending the chat.")
            break

        try:
            # Generate and debug the prompt
            prompt = generate_prompt(task, lang1, user_input, lang2)
            print(f"Generated Prompt: {prompt}")  # Debug log

            # Send the prompt to the Llama model
            response = ollama.chat(
                model="llama3.2",  # Specify the locally downloaded model
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse and display the response
            llama_response = response['message']['content']
            print(f"Llama 3.2: {llama_response}\n")
        except KeyError:
            print("Error: Could not retrieve the response content. Please check the response structure.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    chat_with_llama()
