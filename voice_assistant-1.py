import threading
import subprocess
import queue
from text_speech_module import recognise_speech, text_to_speech


class Assistant(object):
    def __init__(self):
        self.running = True
        self.process = subprocess.Popen(
            ["ollama", "run", "llama3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.data_queue = queue.Queue()

        # Start a thread to read from stdout and stderr
        self.reader_thread = threading.Thread(target=self.read_from_pipes)
        self.reader_thread.start()

    def run_assistant(self, text):
        # Provide input
        input_data = text

        # Send input to the subprocess (without closing stdin)
        self.process.stdin.write(input_data.encode())

    def read_from_pipes(self):
        while self.running:
            data = self.process.stdout.read()
            if data:
                self.data_queue.put(data)

            data = self.process.stderr.read()
            if data:
                # Handle stderr data if needed (e.g., print error messages)
                print(f"Error from ollama: {data.decode('utf-8')}")

    def listen_and_process(self):
        while self.running:
            text = recognise_speech("Hi", 1)
            self.run_assistant(text)

            # Get data from the queue and process it (your logic)
            try:
                data = self.data_queue.get(timeout=1)  # Set a timeout to avoid blocking forever
                output_str = data.decode('utf-8').strip()
                text_to_speech(output_str)
            except queue.Empty:
                pass  # Handle the case where no data is available

    def stop(self):
        self.running = False
        # Terminate the subprocess (optional)
        self.process.terminate()

# Example usage
assistant = Assistant()
text_to_speech("Listening...")

listen_thread = threading.Thread(target=assistant.listen_and_process)
listen_thread.start()

# Keep the main thread running to prevent the program from exiting
while assistant.running:
    pass

assistant.stop()  # Signal the listening thread to stop
