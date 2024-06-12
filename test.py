
import threading
import subprocess
import queue


class Jarvis(object):
    def __init__(self):
        self.process = subprocess.Popen(
            ["Ollama", "run", "llama3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.data = queue.Queue()

        self.reader_thread = threading.Thread(target=self.read_from_pipes)
        self.reader_thread.start()

    def read_from_pipes(self):
        self.running = True
        while self.running:
            # Read from stdout
            data = self.process.stdout.readline()
            if data:
                self.data.put(data)

            # Read from stderr (optional handling)
            err = self.process.stderr.readline()
            if err:
                print(f"Error from Ollama: {err.decode('utf-8')}")

    def run_assistant(self, text):
        # Send input to the subprocess (without closing stdin)
        self.process.stdin.write(text.encode() + b'\n')
        self.process.stdin.flush()  # Ensure the data is sent immediately

    def stop(self):
        self.running = False
        self.process.terminate()
        self.reader_thread.join()


if __name__ == "__main__":
    # Example usage
    assistant = Jarvis()
    try:
        while not assistant.running :
            continue
        assistant.run_assistant("Hello, how are you?")

        # Wait for the response
        response = assistant.data.get(timeout=30)  # Wait up to 10 seconds for a response
        print("Response from Jarvis:", response.decode('utf-8'))
    except Exception or assistant.data.empty():
        print("No response received within the timeout period.")
    finally:
        assistant.stop()