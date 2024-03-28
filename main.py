import os
import paramiko
import pandas as pd
import getpass

def authenticate():
    """
    Prompt user for password authentication.
    Returns True if authentication is successful, False otherwise.
    """
    entered_password = getpass.getpass("Enter the password: ")
    # Replace 'your_password' with the actual password
    return entered_password == '@ut#ent!c8ed'

def homacadditionscript():
    if not authenticate():
        print("Authentication failed. Exiting.")
        return

    # Read data from Excel sheet
    excel_path = "C:\\Users\\Administrator\\Desktop\\HO Firewall-Push\\mac enabled macro for script.xlsm"
    df = pd.read_excel(excel_path, sheet_name="Sheet1")

    # Format data into configuration commands
    config_data = "config firewall address\n"
    for index, row in df.iterrows():
        config_data += f'edit "{row["Name"]}"\n'
        config_data += "set type mac\n"
        config_data += f'set macaddr {row["Mac "]}\n'
        config_data += f'set comment "{row["Purpose/Group Name"]}"\n'
        config_data += f'set associated-interface "{row["Interface"]}"\n'
        config_data += "next\n"
    config_data += "end\n"
    config_data += "config firewall addrgrp\n"
    
    # Ensure there are rows in the DataFrame before accessing index 1
    if len(df) > 0:
        config_data += f'edit "{df.at[0, "Purpose/Group Name"]}"\n'
        config_data += 'append member {}\n'.format(" ".join(['"{}"'.format(row["Name"]) for index, row in df.iterrows()]))
        config_data += "next\n"
    
    config_data += "end\n"
    config_data += "exit\n"

    # Write configuration data to a Notepad file
    notepad_path = "C:\\Users\\Administrator\\Desktop\\HO Firewall-Push\\Test.txt"
    with open(notepad_path, "w", encoding="utf-8") as notepad_file:
        notepad_file.write(config_data)

    # Open the Notepad file
    os.system(f"notepad.exe {notepad_path}")
    input("Press Enter when you are done reviewing the file...")

    # Establish SSH connection to the firewall
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Replace 'firewall-ip', 'your-username', and 'your-password' with actual firewall credentials
        ssh.connect('firewall-ip', username='your-username', password='your-password')

        # Send configuration commands to the firewall
        stdin, stdout, stderr = ssh.exec_command(config_data)

        # Capture command output
        command_output = stdout.read().decode()

        # Print command output
        print("Command output:")
        print(command_output)

        # Write command output to a new text file named "output.txt"
        with open("output.txt", "w", encoding="utf-8") as output_file:
            output_file.write(command_output)

        print("Press the 'Esc' key to exit the script.")

        # Your script logic goes here
        while True:
            pass

    finally:
        ssh.close()

if __name__ == "__main__":
    homacadditionscript()
