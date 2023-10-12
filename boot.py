import sys
import os
import requests

NEWS_API_KEY = '0c261d1464c34297acc3e2c1439676c0'

# Console Colors
G = '\033[92m'  # Green
Y = '\033[93m'  # Yellow
B = '\033[94m'  # Blue
R = '\033[91m'  # Red
W = '\033[0m'   # Reset (White)
X = '\033[90m'  # Grey

def banner():
    print(f"""{R}
          
 ██████  ███████ ██   ██ █ ███████     ███████  █████   ██████  ███████ 
██    ██ ██      ██   ██   ██          ██      ██   ██ ██       ██      
██    ██ ███████ ███████   ███████     ███████ ███████ ██   ███ ██████   
██    ██      ██ ██   ██        ██          ██ ██   ██ ██    ██ ██      
 ██████  ███████ ██   ██   ███████     ███████ ██   ██  ██████  ███████ \n{W}""")

def open_sites():
    sites = ["https://coursera.org", "https://github.com", "https://youtube.com", "https://notion.so"]
    for site in sites:
        os.system(f'explorer.exe {site}')

def open_mail_client():
    os.system('mutt')

def open_weather_forecast():
    weather_data = os.popen('curl -s "wttr.in/$1?m1"').read()
    watermark = 'Follow [46m[30m@igor_chubin[0m for wttr.in updates'
    weather_data = weather_data.replace(watermark, '')
    print(weather_data)

def get_news():
    sources = {
        'bbc-news': R + 'News from bbc-news:' + W,
        'the-hindu': R + 'News from the-hindu:' + W,
        'time': R + 'News from time:' + W,
        'the-times-of-india': R + 'News from the-times-of-india:' + W
    }

    for source, source_name in sources.items():
        url = f'https://newsapi.org/v2/top-headlines'
        params = {
            'sources': source,
            'apiKey': NEWS_API_KEY
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(source_name)
            for article in articles:
                print(f"{Y}Title: {article['title']} {W}")
                print(f"{X}URL:{article['url']}{W}")
                print(f"Description: {article['description']}")
                print()
        else:
            print(f'Failed to fetch news from {source}')

command_file = "data.txt"

def load_commands():
    commands = {}
    current_command_flow = None

    with open(command_file, "r") as f:
        for line in f:
            line = line.strip()  # Remove leading and trailing whitespace

            if line.startswith("[") and line.endswith("]"):
                current_command_flow = line[1:-1]
                commands[current_command_flow] = []
            elif line.startswith("[+]"):
                if current_command_flow:
                    commands[current_command_flow].append(line[3:])
    
    return commands

# Function to display command flows
def display_command_flows(commands):
    if not commands:
        print("No command flows found.")
        return

    print(f"{B}\nCommand Flows:{W}")
    for i, (flow_name, flow_commands) in enumerate(commands.items(), start=1):
        print(f"[{Y}{i}{W}] {flow_name}")
        for j, command in enumerate(flow_commands, start=1):
            print(f"[{B}+{W}] {command}")
        # print(f"[{B}#{W}] ____________")

# Function to add a new command flow
def add_command_flow(commands, name, command_list):
    if name in commands:
        print(f"Command flow '{name}' already exists.")
        return

    commands[name] = command_list
    print(f"Added command flow '{name}' with {len(command_list)} command(s.")

    # Write the new command flow to the data.txt file
    with open(command_file, "a") as f:
        f.write(f"[{name}]\n")
        for command in command_list:
            f.write(f"[+] {command}\n")

# Function to delete a command flow
def delete_command_flow(commands, name):
    if name in commands:
        del commands[name]
        print(f"Deleted command flow '{name}'.")

        # Remove the command flow from the data.txt file
        with open(command_file, "r") as f:
            lines = f.readlines()

        with open(command_file, "w") as f:
            for line in lines:
                if line.strip().startswith("[") and line.strip().endswith("]"):
                    current_command_flow = line.strip()[1:-1]
                    if current_command_flow != name:
                        f.write(line)
                elif current_command_flow == name:
                    continue
                else:
                    f.write(line)
    else:
        print(f"Command flow '{name}' not found.")


# Function to execute a command flow with optional input
def execute_command_flow(commands, name, input_args):
    if name in commands:
        command_list = commands[name]
        for i, command in enumerate(command_list, start=1):
            if "{input:" in command:
                input_placeholder = command.split("{input:")[1].split("}")[0]
                input_value = input(f"Enter {input_placeholder}: ")
                command = command.replace(f"{{input:{input_placeholder}}}", input_value)
            os.system(command)
    else:
        print(f"Command flow '{name}' not found.")

# Main function
def comm_manager():
    commands = load_commands()

    while True:
        print(f"\n{Y}Menu Options:{W}")
        print("[1] Display Command Flows")
        print("[2] Add Command Flow")
        print("[3] Delete Command Flow")
        print("[4] Execute Command Flow")
        print(f"{X} Press ⏎ to exit{W}")

        choice = input(f"{G} Enter your choice: {W}")
        
        if choice == "1":
            display_command_flows(commands)
        elif choice == "2":
            name = input("Enter the name for the new command flow: ")
            command_list = []

            while True:
                command = input("Enter a command (or leave empty to finish): ")
                if not command:
                    break
                command_list.append(command)

            add_command_flow(commands, name, command_list)
        elif choice == "3":
            name = input("Enter the name of the command flow to delete: ")
            delete_command_flow(commands, name)
        elif choice == "4":
            name = input("Enter the name of the command flow to execute: ")
            execute_command_flow(commands, name, {})
        elif choice == "5":
            # Save the updated commands to the file before exiting
            with open(command_file, "w") as f:
                for name, command_list in commands.items():
                    f.write(f"[{name}]\n")
                    for command in command_list:
                        f.write(f"[+] {command}\n")
            print("Command flows saved to 'data.txt'. Exiting.")
            break
        elif choice == '':
            break
        else:
            print("Invalid choice. Please try again.")

def display_menu(commands):
    commands = load_commands()  # Load the commands every time the menu is displayed
    menuhead = f"\n{R}Menu Options:{W}"
    print(menuhead)
    print("[0] Command Manager")

    for i, flow_name in enumerate(commands.keys(), start=1):
        print(f"[{i}] {flow_name}")

    # Calculate the starting index for the new options
    starting_index = len(commands) + 1

    print("[{}] Morning Briefing (Weather Forecast + News)".format(starting_index))
    print("[{}] Open Workflow in Browser (GitHub, Notion, Coursera, YouTube etc)".format(starting_index + 1))
    print("[{}] Open Mail Client".format(starting_index + 2))
    print("[{}] Open Weather Forecast".format(starting_index + 3))
    print("[{}] Get News".format(starting_index + 4))
    print(f"{X} Press ⏎ to exit{W}")


def main():
    banner()
    prompt = f"{G}Enter your choice:{W} "

    while True:
        commands = load_commands()  # Load the commands at the beginning of the loop
        display_menu(commands)
        user_input = input(prompt)

        if user_input == '':
            print("Portal Exited. Launch a new term with Ctrl + Shift + 4 to relaunch.")
            break
        elif user_input == '0':
            comm_manager()
        elif user_input in map(str, range(1, len(commands) + 1)):
            execute_command_flow(commands, list(commands.keys())[int(user_input) - 1], {})
        elif user_input == str(len(commands) + 1):
            open_weather_forecast()
            get_news()
        elif user_input == str(len(commands) + 2):
            open_sites()
        elif user_input == str(len(commands) + 3):
            open_mail_client()
        elif user_input == str(len(commands) + 4):
            open_weather_forecast()
        elif user_input == str(len(commands) + 5):
            get_news()
        else:
            print("Incorrect option. Please try again.")

if __name__ == "__main__":
    main()
