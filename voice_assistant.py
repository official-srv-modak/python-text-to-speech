import threading
import subprocess
from text_speech_module import recognise_speech, text_to_speech

class Assistant(object):
    def __init__(self):
        self.running = True
        self.count = 1
        self.process = subprocess.Popen(
            ["ollama", "run", "llama3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run_assistant(self, text):
        # Provide input
        input_data = text

        # Send input to the subprocess (without closing stdin)
        self.process.stdin.write(input_data.encode())

        # Read the output and error from the subprocess
        output, error = self.process.communicate()

        # Decode the output and error from bytes to string
        output_str = output.decode('utf-8')
        error_str = error.decode('utf-8')

        # Print the output and error
        print("Output of command:", ["ollama", "run", "llama3"])
        output_text = output_str.strip()
        print("Output:", output_text)
        text_to_speech(output_text)

        # You can modify this section to handle potential communication issues
        # For example, check the return value of process.stdin.write()

    def listen_and_process(self):
        while self.running:
            text = recognise_speech("Hello! How may I help you?", count=self.count)
            self.count = 2
            self.run_assistant(text)

    def stop(self):
        self.running = False
        # Terminate the subprocess (optional for short-lived processes)
        self.process.terminate()

# Example usage
assistant = Assistant()

listen_thread = threading.Thread(target=assistant.listen_and_process)
listen_thread.start()

# Keep the main thread running to prevent the program from exiting
while assistant.running:
    pass

assistant.stop()  # Signal the listening thread to stop
