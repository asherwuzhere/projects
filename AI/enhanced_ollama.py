# Just a simple way of getting work done with a local Ollama model.

import ollama

def chat_with_llama():
    print("Welcome to the Everyday Task Assistant! Type 'exit' to end the conversation.\n")
    
    # Display available tasks
    print("Available tasks:")
    print("1. Summarize - Summarize any text or document")
    print("2. To-Do - Generate a to-do list for a task or goal")
    print("3. Explain - Get explanations for concepts or topics")
    print("4. Brainstorm - Brainstorm ideas for a project, event, or solution")
    print("5. Answer - Ask any general question\n")
    
    # Task selection
    task_mapping = {
        '1': "Summarize",
        '2': "To-Do",
        '3': "Explain",
        '4': "Brainstorm",
        '5': "Answer",
    }

    while True:
        # Input task
        task_choice = input("Select a task number (1-5): ").strip()
        task = task_mapping.get(task_choice)
        if not task:
            print("Invalid task selection. Please choose a valid task number.\n")
            continue
        print(f"\nYou selected: {task}\n")
        
        while True:
            # Input user request
            user_input = input("Enter your input (or type 'back' to choose another task, 'exit' to quit): ").strip()
            
            # Check for exit or back options
            if user_input.lower() == 'exit':
                print("Goodbye! Ending the chat.")
                return
            elif user_input.lower() == 'back':
                print("Going back to task selection...\n")
                break

            # Generate prompt based on task
            if task == "Summarize":
                prompt = f"Summarize the following text: {user_input}"
            elif task == "To-Do":
                prompt = f"Generate a to-do list for the following task or goal: {user_input}"
            elif task == "Explain":
                prompt = f"Explain the following concept or topic: {user_input}"
            elif task == "Brainstorm":
                prompt = f"Brainstorm ideas for: {user_input}"
            elif task == "Answer":
                prompt = f"Provide an answer to the following question: {user_input}"
            else:
                print("Unexpected error occurred. Restarting task selection.")
                break

            # Send prompt to Llama model
            try:
                response = ollama.chat(
                    model="llama3.2",  # Specify the locally downloaded model
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Access the 'content' of the 'message'
                llama_response = response['message']['content']
                print(f"\nLlama 3.2: {llama_response}\n")
            except KeyError:
                print("Error: Could not retrieve the response content. Please check the response structure.")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    chat_with_llama()

