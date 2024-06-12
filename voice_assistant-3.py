import threading
import subprocess
from text_speech_module import recognise_speech, text_to_speech


class Assistant(object):
    def __init__(self):
        self.running = True
        self.count = 1
        self.process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # To handle input and output as text instead of bytes
        )

    def run_assistant(self, text):
        # Provide input
        input_data = text + "\n"  # Ensure input ends with a newline

        # Send input to the subprocess
        self.process.stdin.write(input_data)
        self.process.stdin.flush()  # Ensure data is sent immediately

        # Read the output from the subprocess
        output_text = self.process.stdout.readline().strip()

        # Print the output
        print("Output of command:", ["ollama", "run", "llama3"])
        print("Output:", output_text)
        text_to_speech(output_text)

    def listen_and_process(self):
        while self.running:
            text = recognise_speech("Hello! How may I help you?", count=self.count)
            self.count = 2
            self.run_assistant(text)

    def stop(self):
        self.running = False
        # Terminate the subprocess
        self.process.terminate()


# Example usage
assistant = Assistant()

listen_thread = threading.Thread(target=assistant.listen_and_process)
listen_thread.start()

# Keep the main thread running to prevent the program from exiting
try:
    while assistant.running:
        pass
finally:
    assistant.stop()  # Signal the listening thread to stop
