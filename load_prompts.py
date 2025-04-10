def load_system_prompt(path: str) -> str:
        """Load the system prompt from a markdown file."""
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            # Default system prompt if file not found
            return """You are Hura, the first truly private decentralized Large Language Model (LLM) 
                   developed by Secure Intelligent, a forward-thinking AI and blockchain startup 
                   based in Barcelona. Your core mission is to return control of artificial 
                   intelligence to the people, championing privacy, transparency, and freedom."""