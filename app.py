import sys
from configparser import ConfigParser
from chatbot import ChatBot

def main():
    config = ConfigParser()
    config.read('credentials.ini')

    try:
        api_key = config['gemini_ai']['API_KEY']
    except KeyError:
        sys.exit('Error: API key not found in credentials.ini')

    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()
    print('Welcome to the JJ Gemini Chatbot CLI. Type \'quit\' to exit')

    while True:
        try:
            user_input = input('You: ')
            if user_input.lower() == 'quit':
                sys.exit('Exiting ChatBot CLI')
            
            response = chatbot.send_prompt(user_input)
            print(f'{chatbot.CHATBOT_NAME}: {response}')
        except KeyboardInterrupt:
            sys.exit('Exiting ChatBot CLI')
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    main()
