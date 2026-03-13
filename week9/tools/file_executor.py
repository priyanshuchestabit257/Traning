import os

async def file_executor(input_query: str, model_client):
    """
    Day 3 Tool: Directly inspects the filesystem to prevent LLM hallucinations.
    Uses dictionary-based messaging to satisfy the local model client requirements.
    """
    # 1. Get the absolute path to your project root (week9)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 2. Identify target directory
    query_lower = input_query.lower()
    target_dir = "." # Default to week9 root
    
    if "tools" in query_lower:
        target_dir = "tools"
    elif "src" in query_lower:
        target_dir = "src"
    elif "data" in query_lower:
        target_dir = "data"

    target_path = os.path.join(root_dir, target_dir)

    # 3. Perform ACTUAL system call
    try:
        if os.path.exists(target_path):
            files = os.listdir(target_path)
            # Filter hidden files (like .venv, .git)
            files = [f for f in files if not f.startswith('.')]
            file_list_str = ", ".join(files) if files else "The directory is empty."
            
            # 4. Ground the AI with the truth
            prompt = (
                f"You are a file assistant. The actual files in '{target_dir}' are: {file_list_str}. "
                f"User asked: '{input_query}'. Answer based ONLY on this list. Do not make up files."
            )
            
            # FIX: Send a simple list of dictionaries instead of TextMessage objects
            # This is the most compatible format for LlamaCpp clients
            messages = [
                {"role": "user", "content": prompt}
            ]
            
            response = await model_client.create(messages=messages)
            
            # Extract content (handling both object and dict responses)
            if hasattr(response, 'content'):
                return response.content
            return str(response)
            
        else:
            return f"Error: Folder '{target_dir}' not found."
            
    except Exception as e:
        return f"System Error while reading files: {str(e)}"