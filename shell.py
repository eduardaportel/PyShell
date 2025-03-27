#!/usr/bin/env python3
"""
Shell Simples em Python 
Nome: Eduarda Portel
RA: 23.00292-0
"""

import os
import sys
import platform
import subprocess
import shlex

def display_prompt():
    """Exibe o prompt personalizado"""
    sys.stdout.write("shell> ")
    sys.stdout.flush() #força a exibição

def execute_unix_command(command):
    """Executa comandos em sistemas Unix/Linux"""

    # Divide preservando strings entre aspas
    parts = shlex.split(command)
    try:
        # Cria um processo filho
        pid = os.fork()
        if pid == 0:
            # Processo filho - executa o comando
            os.execvp(parts[0], parts)
        elif pid > 0:
            # Processo pai - espera o filho terminar
            _, status = os.wait()
            # Converte o status para código de saída
            return os.waitstatus_to_exitcode(status)
        else:
            # Erro no fork()
            print("Erro ao criar processo filho", file=sys.stderr)
            return 1
        
    except FileNotFoundError:
        print(f"{parts[0]}: comando não encontrado", file=sys.stderr)
        return 127
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1

def execute_windows_command(command):
    """Executa comandos no Windows com tratamento especial para ls"""
    if command.startswith('ls'):
        # Tenta usar o WSL se estiver disponível
        try:
            # Executa via WSL (Windows Subsystem for Linux)
            result = subprocess.run(['wsl'] + command.split(), 
                                  stdout=sys.stdout, 
                                  stderr=sys.stderr)
            return result.returncode
        except:
            print("Para usar 'ls' no Windows, instale o WSL ou Git Bash", file=sys.stderr)
            return 1
    else:
        try:
            result = subprocess.run(command, 
                                  shell=True,
                                  stdout=sys.stdout,
                                  stderr=sys.stderr)
            return result.returncode
        except FileNotFoundError:
            print(f"Comando não encontrado", file=sys.stderr)
            return 127

def execute_command(command):
    """Seleciona o método de execução baseado no SO"""
    if not command.strip():
        return 0
    
    # Tratamento especial para echo
    if command.startswith('echo '):
        text = command[5:].strip()
        # Remove aspas apenas se estiverem no início e no fim
        if len(text) >= 2 and text[0] == text[-1] and text[0] in ('"', "'"):
            text = text[1:-1]
        print(text)  # Imprime sem aspas
        return 0

    if platform.system() == "Windows":
        return execute_windows_command(command)
    else:
        return execute_unix_command(command)

def main():
    """Função principal que implementa o loop REPL"""
    print("Shell Python - Digite 'help' para ajuda")
    
    while True: #loop principal infinito
        try:
            display_prompt() #Mostra o prompt
            command = input().strip() #Lê o comando
            
            if not command:
                continue
                
            if command.lower() in ("exit", "quit"):
                print("Saindo do shell...")
                break
                
            if command.lower() == "help":
                print("\nComandos disponíveis:")
                print("- ls -l: Lista arquivos com detalhes")
                print("- echo: Exibe mensagens")
                print("- exit/quit: Sair do shell")
                print("- help: Mostra esta ajuda\n")
                continue
                
            # Executa comandos do sistema
            return_code = execute_command(command)

            # Exibe código de erro se necessário
            if return_code != 0:
                print(f"[Código de saída: {return_code}]", file=sys.stderr)
                
        except KeyboardInterrupt:
            print("\nDica: Digite 'exit' para sair")
        except EOFError:
            print("\nSaindo...")
            break
        except Exception as e:
            print(f"Erro inesperado: {e}", file=sys.stderr)
            break

if __name__ == "__main__":
    main()