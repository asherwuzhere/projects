# This is just a fun little code that claims to "read your mind" with AI.

import ollama
import time
import threading

def show_loading_screen():
    loading_messages = [
        "Analysing Brain Waves",
        "Decoding Neural Patterns",
        "Accessing Subconscious Frameworks",
        "Mapping Cognitive Pathways"
    ]
    
    for message in loading_messages:
        print(message, end="", flush=True)
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(1)
        print()

def chat_with_llama():
    print("Hi! I'm Llama 3.2 and I bet I can read your mind. (type 'exit' to end)\n")
    
    # Start the conversation loop
    while True:
        # Get user input
        user_input = input("Think of a number and type it in: ")
        
        # Check if the user wants to exit
        if user_input.lower() == 'exit':
            print("Thanks for playing, goodbye!")
            break
        
        # Construct the request for Llama to extract the raw number
        prompt = f"Extract number in quotes as digits without additional words: '{user_input}'"
        
        # Start the loading screen in a separate thread
        loading_thread = threading.Thread(target=show_loading_screen)
        loading_thread.start()

        # Send the user input to the Llama 3.2 model (this will block until the response is received)
        response = ollama.chat(
            model="llama3.2",  # Specify the locally downloaded model
            messages=[{"role": "user", "content": prompt}]
        )

        # Wait for the loading thread to complete
        loading_thread.join()

        # Access the 'content' of the 'message' directly
        try:
            llama_response = response.message.content
            print(f"\nThe number you were thinking of was: {llama_response}\n")
        except AttributeError:
            print("Error: Could not retrieve the response content. Please check the response structure.")

if __name__ == "__main__":
    chat_with_llama()
