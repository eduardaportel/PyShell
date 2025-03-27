#!/usr/bin/env python3
"""
Simple Python Shell
Name: Eduarda Portel
ID: 23.00292-0
"""

import os
import sys
import platform
import subprocess
import shlex

def display_prompt():
    """Displays the custom shell prompt"""
    sys.stdout.write("shell> ")
    sys.stdout.flush()  # Forces immediate display

def execute_unix_command(command):
    """Executes commands on Unix/Linux systems"""
    
    # Split while preserving quoted strings
    parts = shlex.split(command)
    try:
        # Create a child process
        pid = os.fork()
        if pid == 0:
            # Child process - executes the command
            os.execvp(parts[0], parts)
        elif pid > 0:
            # Parent process - waits for child to complete
            _, status = os.wait()
            # Convert status to exit code
            return os.waitstatus_to_exitcode(status)
        else:
            # Fork error
            print("Error creating child process", file=sys.stderr)
            return 1
        
    except FileNotFoundError:
        print(f"{parts[0]}: command not found", file=sys.stderr)
        return 127
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def execute_windows_command(command):
    """Executes commands on Windows with special handling for ls"""
    if command.startswith('ls'):
        # Try using WSL if available
        try:
            # Execute via Windows Subsystem for Linux
            result = subprocess.run(['wsl'] + command.split(), 
                                  stdout=sys.stdout, 
                                  stderr=sys.stderr)
            return result.returncode
        except:
            print("To use 'ls' on Windows, install WSL or Git Bash", file=sys.stderr)
            return 1
    else:
        try:
            result = subprocess.run(command, 
                                  shell=True,
                                  stdout=sys.stdout,
                                  stderr=sys.stderr)
            return result.returncode
        except FileNotFoundError:
            print(f"Command not found", file=sys.stderr)
            return 127

def execute_command(command):
    """Selects execution method based on OS"""
    if not command.strip():
        return 0
    
    # Special handling for echo command
    if command.startswith('echo '):
        text = command[5:].strip()
        # Remove quotes only if they're at start and end
        if len(text) >= 2 and text[0] == text[-1] and text[0] in ('"', "'"):
            text = text[1:-1]
        print(text)  # Print without quotes
        return 0

    if platform.system() == "Windows":
        return execute_windows_command(command)
    else:
        return execute_unix_command(command)

def main():
    """Main function implementing the REPL loop"""
    print("Python Shell - Type 'help' for assistance")
    
    while True:  # Main infinite loop
        try:
            display_prompt()  # Show prompt
            command = input().strip()  # Read command
            
            if not command:
                continue
                
            if command.lower() in ("exit", "quit"):
                print("Exiting shell...")
                break
                
            if command.lower() == "help":
                print("\nAvailable commands:")
                print("- ls -l: List files with details")
                print("- echo: Display messages")
                print("- exit/quit: Exit the shell")
                print("- help: Show this help message\n")
                continue
                
            # Execute system commands
            return_code = execute_command(command)

            # Show error code if needed
            if return_code != 0:
                print(f"[Exit code: {return_code}]", file=sys.stderr)
                
        except KeyboardInterrupt:
            print("\nTip: Type 'exit' to quit")
        except EOFError:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            break

if __name__ == "__main__":
    main()