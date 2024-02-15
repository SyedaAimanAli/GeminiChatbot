import google.generativeai as genai

class GeniAIException(Exception):
    """GeniAI exception base class"""

class ChatBot:
    CHATBOT_NAME = 'My Gemini Ai'

    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.conversation = None
        self._conversation_history = []

    def send_prompt(self, prompt, temperature=0.1):
        if not (0 <= temperature <= 1):
            raise GeniAIException('Temperature must be between 0 and 1')
        if not prompt:
            raise GeniAIException('Prompt cannot be empty')
        
        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature)
            )
            response.resolve()
            return f'{response.text}\n' + '---' * 20
        except Exception as e:
            raise GeniAIException(str(e))

    def clear_conversation(self):
        self.conversation = self.model.start_chat(history=[])

    def start_conversation(self, history=None):
        self.conversation = self.model.start_chat(history=history or self._conversation_history)

    def _generation_config(self, temperature):
        return genai.types.GenerationConfig(
            temperature=temperature
        )

    def preload_conversation(self, conversation_history=None):
        self._conversation_history = conversation_history or [
            {'role': 'user', 'parts': ['From now on, return the output as JSON object that can be loaded with the key as \'text\'. For example, {"text": "<output goes here>"}']},
            {'role': 'user', 'parts': ['Sure, I can return the output as a regular JSON object with the key as `text`. Here is an example: {"text": "your output"}']}
        ]

    def _construct_message(self, text, role='user'):
        return {
            'role': role,
            'parts': [text]
        }