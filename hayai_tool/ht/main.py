import argparse
import sys
import readline
import os
import pandas as pd
import pkg_resources
import pyperclip
import shutil

def process_csv_step1(file_path):
    df = pd.read_csv(file_path)
    df['CN'] = df['CN'].apply(lambda x: str(x).zfill(8))
    return df.iloc[:, [4, 5, 6]]


def tocsv(directory):
    # Step 1: Find the Excel file with the largest number
    existing_files = [f for f in os.listdir(directory) if f.endswith("_はやい.xlsx")]

    # Determine the file with the largest number
    numbers = []
    for file in existing_files:
        try:
            number = int(file.split("_")[0])  # Extract the number before "_はやい.xlsx"
            numbers.append((number, file))  # Store both the number and the file name
        except ValueError:
            pass

    if not numbers:
        print("No matching files found in the directory.")
        return

    # Get the file with the largest number
    largest_number, largest_file = max(numbers, key=lambda x: x[0])
    print(f"Found file with the largest number: {largest_file}")

    # Step 2: Convert the found Excel file to a CSV file
    excel_file_path = os.path.join(directory, largest_file)
    try:
        df = pd.read_excel(excel_file_path)
    except FileNotFoundError:
        print(f"Error: {excel_file_path} not found.")
        return

    # Create a new CSV filename (same as the Excel file but with .csv extension)
    csv_file = excel_file_path.replace(".xlsx", ".csv")

    # Save the dataframe as a CSV file
    df.to_csv(csv_file, index=False)
    print(f"Converted {excel_file_path} to {csv_file}")


def process_csv_step2(file1, file2):
    df_from_enduser = process_csv_step1(file1)

    df_from_ssms = pd.read_csv(file2, header=None)
    df_from_ssms.drop([2, 3, 4], axis=1, inplace=True)
    df_from_ssms.rename(columns={0: 'MEK', 1: 'CN_'}, inplace=True)
    df_from_ssms['CN_'] = df_from_ssms['CN_'].apply(lambda x: str(x).zfill(8))

    df_hayai = pd.concat([df_from_enduser, df_from_ssms], axis=1)
    df_hayai['MEK'] = df_hayai['MEK'].fillna(0).astype(int)

    return df_hayai


def select_database():
    """
    Prompts user to select database and returns the database name.
    """
    while True:
        db_choice = input("Do you want to store in test (t), prod (p), or other (o): ").lower()
        
        if db_choice == 't':
            return 'TEST'
        elif db_choice == 'p':
            return 'URMCCEX3'
        elif db_choice == 'o':
            custom_db = input("Enter the custom database name: ")
            return custom_db
        else:
            print("Invalid choice. Please enter t, p, or o.")

def get_meks_from_ssms(control_numbers):
    # Select database first
    database = select_database()

    case_statements = [f"        WHEN [ControlNo] = '{cn}' THEN {i+1}" for i, cn in enumerate(control_numbers)]
    case_block = "\n    ".join(case_statements)

    sql_command = f"""
    SELECT
        [EquipmentKey],
        [CN],
        [CycleDate],
        [CycleSetBy],
        [RTLSCode]
    FROM
        [{database}].[dbo].[Equipment]
    WHERE 
        [ControlNo] IN (\n{', '.join([f"'{cn}'" for cn in control_numbers])} 
        )
    ORDER BY 
        CASE\n    {case_block}  
    END;
    """.strip()

    return sql_command

def generate_sql_for_ssms(meks, dates, rtls_codes):
    # Select database first
    database = select_database()

    if not (len(meks) == len(dates) == len(rtls_codes)):
        raise ValueError("All input lists must have the same length")

    case_statements_for_meks = [
            f"        WHEN [EquipmentKey] = {mek} THEN '{date} 00:00:00.000'"
            for mek, date in zip(meks, dates)
            ]
    case_block_meks = "\n   ".join(case_statements_for_meks)

    case_statements_for_rtls = [
            f"        WHEN [EquipmentKey] = {mek} THEN '{rtls}'"
            for mek, rtls in zip(meks, rtls_codes)
            ]
    case_block_rtls = "\n".join(case_statements_for_rtls)

    mek_list = ", ".join(f"'{mek}'" for mek in meks)

    sql_command = f"""
    UPDATE [{database}].[dbo].[Equipment]
    SET 
        CycleSetBy = 'Equipment',
        CycleDate = CASE\n   {case_block_meks}
        END,
    [RTLScode] = CASE\n{case_block_rtls}
    END
    WHERE 
       [EquipmentKey] IN ({mek_list});
    """.strip()

    return sql_command



def copy_template():
    template_filename = "TEMPLATE.xlsx"
    if not os.path.exists(template_filename):
        print("Error: TEMPLATE.xlsx not found in the current directory.")
        return

    # Find all files matching the pattern "X_はやい.xlsx"
    existing_files = [f for f in os.listdir() if f.endswith("_はやい.xlsx")]

    # Determine the next available number
    numbers = []
    for file in existing_files:
        try:
            number = int(file.split("_")[0])  # Extract the number before "_はやい.xlsx"
            numbers.append(number)
        except ValueError:
            pass

    next_number = max(numbers, default=0) + 1

    # Create the new file name
    new_filename = f"{next_number}_はやい.xlsx"

    # Copy TEMPLATE.xlsx to the new file
    shutil.copy(template_filename, new_filename)

    print(f"Copied TEMPLATE.xlsx to {new_filename}")


def read_ascii_art(file_path='hayai_art.txt'):
    """
    Read ASCII art from a package data file and add a welcome message.
    
    Args:
        file_path (str): Path to the ASCII art text file
    
    Returns:
        str: ASCII art content with welcome message
    """
    try:
        # Use pkg_resources to locate the file within the package
        ascii_art_path = pkg_resources.resource_filename('ht', f'data/{file_path}')
        
        with open(ascii_art_path, 'r', encoding='utf-8') as file:
            ascii_art = file.read()
        
        # Add welcome message beneath the ASCII art
        return f"{ascii_art}\nWelcome to bd_hayai"
    except (FileNotFoundError, IOError):
        return "Welcome to Hayai Script\nWelcome to bd_hayai"

def print_usage():
    """
    Print usage instructions when 'hayai' is typed without arguments.
    """
    print("\nUsage: hayai  [options] [arguments]\n")
    print("Options:")
    print("  step1 <csv_file>           Process first step with CSV file")
    print("  step2 <csv_file1> <csv_file2>  Process second step with two CSV files")
    print("  cpysrc                     Copy source template")
    print("  tocsv                      Convert Excel to CSV")
    print("\nAdditional flags:")
    print("  -c, --copy                 Copy SQL command to clipboard")
    print("  -l, --log                  Display DataFrame content")

def main():
    # ASCII art printed only once at the start
    print(read_ascii_art())
    
    # Parse initial command-line arguments if provided
    parser = argparse.ArgumentParser(description="Process CSV files, generate SQL, and handle templates.")
    parser.add_argument("options", nargs="?", choices=["step1", "step2", "cpysrc", "tocsv"], help="Step to execute: 'step1', 'step2', 'cpysrc', or 'tocsv'")
    parser.add_argument("csv_file1", nargs="?", help="Path to the first input CSV file (not needed for cpysrc)")
    parser.add_argument("csv_file2", nargs="?", help="Path to the second input CSV file (for step2)")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy the SQL command to the clipboard")
    parser.add_argument("-l", "--log", action="store_true", help="Display the DataFrame content")
    args = parser.parse_args()

    # If invoked with CLI arguments, execute the corresponding command
    if args.options:
        execute_command(args)
        # Prompt for further actions
        interactive_loop(parser)
    else:
        # No arguments provided, start the interactive loop
        print_usage()
        interactive_loop(parser)


def setup_readline():
    """
    Configures readline to enable intelligent file path tab-completion.
    """
    def complete_file_path(text, state):
        """
        Provides tab-completion for file paths, avoiding redundant prefixes.
        """
        # Split the user input into directory and file prefix
        directory, file_prefix = os.path.split(text)
        if not directory:
            directory = "."  # Default to the current directory

        try:
            # List files in the directory
            files = os.listdir(directory)
        except FileNotFoundError:
            files = []

        # Filter files that match the prefix
        matching_files = [f for f in files if f.startswith(file_prefix)]

        # Append the directory path to the matching files for full completion
        completions = [os.path.join(directory, f) if directory != "." else f for f in matching_files]

        # Return the appropriate match for the current state
        if state < len(completions):
            return completions[state]
        return None

    # Set the completer function for readline
    readline.set_completer(complete_file_path)
    readline.parse_and_bind("tab: complete")  # Enable tab-completion

def interactive_loop(parser):
    """
    Handles the interactive loop for repeated user commands.
    """
    setup_readline()  # Enable tab-completion

    while True:
        # Prompt user for input
        user_input = input("\nEnter the [options] [args] [flags] or type 'exit' to quit: ").strip()

        # Exit condition
        if user_input.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break

        # Parse the user's input
        try:
            args = parser.parse_args(user_input.split())
            execute_command(args)
        except SystemExit:
            # Invalid input handling
            print("Invalid command. Please try again.")

def execute_command(args):
    """
    Executes the command based on parsed arguments.
    """
    try:
        if args.options == "step1":
            if not args.csv_file1:
                print("Error: Step 1 requires a CSV file.")
                return
            df = process_csv_step1(args.csv_file1)
            control_numbers = df['CN'].tolist()
            sql_command = get_meks_from_ssms(control_numbers)

            if args.log:
                print("\nDisplaying DataFrame (Step 1):\n")
                print(df)

            print(sql_command)
            if args.copy:
                pyperclip.copy(sql_command)
                print("\nSQL command copied to clipboard!")

        elif args.options == "step2":
            if not (args.csv_file1 and args.csv_file2):
                print("Error: Step 2 requires two CSV files.")
                return

            df_hayai = process_csv_step2(args.csv_file1, args.csv_file2)

            if args.log:
                print("\nDisplaying DataFrame (Step 2):\n")
                print(df_hayai)

            master_entity_keys = df_hayai['MEK'].tolist()
            cycle_start_dates = df_hayai.iloc[:, 1].tolist()
            rtls_tag_codes = df_hayai.iloc[:, 2].tolist()

            sql_command = generate_sql_for_ssms(master_entity_keys, cycle_start_dates, rtls_tag_codes)
            print(sql_command)

            if args.copy:
                pyperclip.copy(sql_command)
                print("\nSQL command copied to clipboard!")

        elif args.options == "cpysrc":
            copy_template()

        elif args.options == "tocsv":
            curr_dir = os.getcwd()
            tocsv(curr_dir)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
