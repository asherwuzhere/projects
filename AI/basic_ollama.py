# Simple local AI chatbot using Ollama's model Llama 3.2.

import ollama

def chat_with_llama():
    print("Welcome to the Llama 3.2 chat! Type 'exit' to end the conversation.\n")
    
    # Start the conversation loop
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if the user wants to exit
        if user_input.lower() == 'exit':
            print("Goodbye! Ending the chat.")
            break
        prompt = f"{user_input}"
        # Send the user input to the Llama 3.2 model
        response = ollama.chat(
            model="llama3.2",  # Specify the locally downloaded model
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Access the 'content' of the 'message' directly
        try:
            llama_response = response.message.content
            print(f"Llama 3.2: {llama_response}\n")
        except AttributeError:
            print("Error: Could not retrieve the response content. Please check the response structure.")

if __name__ == "__main__":
    chat_with_llama()
