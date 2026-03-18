
import os

async def file_executor(input_query: str, model_client):

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    query = input_query.lower()

    try:
        if "list" in query or "files" in query:

            target_dir = root_dir

            if "tools" in query:
                target_dir = os.path.join(root_dir, "tools")
            elif "src" in query:
                target_dir = os.path.join(root_dir, "src")
            elif "data" in query:
                target_dir = os.path.join(root_dir, "data")

            if not os.path.exists(target_dir):
                return "Directory not found."

            files = [f for f in os.listdir(target_dir) if not f.startswith(".")]

            return "\n".join(files) if files else "No files found."

        elif "find" in query:

            words = input_query.split()
            filename = words[-1]

            matches = []

            for root, _, files in os.walk(root_dir):
                for f in files:
                    if f.lower() == filename.lower():
                        matches.append(os.path.join(root, f))

            return "\n".join(matches) if matches else "File not found."

        elif "create" in query or "write" in query:

            parts = input_query.split("with")
            file_part = parts[0]
            content = parts[1] if len(parts) > 1 else ""

            filename = file_part.split()[-1]
            full_path = os.path.join(root_dir, filename)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())

            return f"File created: {full_path}"

        elif "append" in query:

            parts = input_query.split("with")
            file_part = parts[0]
            content = parts[1] if len(parts) > 1 else ""

            filename = file_part.split()[-1]
            full_path = os.path.join(root_dir, filename)

            with open(full_path, "a", encoding="utf-8") as f:
                f.write(content.strip())

            return f"Content appended to: {full_path}"

        else:

            files = []
            for root, _, fs in os.walk(root_dir):
                for f in fs:
                    files.append(f)

            file_list = ", ".join(files[:50])

            prompt = (
                f"Files available: {file_list}\n"
                f"User question: {input_query}\n"
                f"Answer ONLY based on these files."
            )

            response = await model_client.create(
                messages=[{"role": "user", "content": prompt}]
            )

            return response.content if hasattr(response, "content") else str(response)

    except Exception as e:
        return f"System Error: {str(e)}"
