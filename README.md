# Pickle Payload Generator

Quick Python script to generate base64 encoded Pickle payloads. The script allows you to specify a command to execute during deserialization, which can be encoded and optionally saved to a file.

## Features

- Generate a base64 encoded Pickle RCE payload.
- Specify the command to execute through command-line arguments.
- Option to save the generated payload to a file.
- Print detailed information on the screen.

## Requirements

- Python 3.x

## Usage

### Generate and Print Payload

To generate and print the payload, use the following command:

```sh
python3 pickel_payload.py "your command"
```

### Save Payload to File

To save the payload to a file, use the `-o` or `--output` option:

```sh
python3 pickel_payload.py "your command" -o "payload.txt"
```

### Example

```sh
python3 pickel_payload.py "touch test.txt" -o "payload.txt"
```

