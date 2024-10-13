import os
import pandas as pd
import argparse
import pyperclip
import shutil


def process_csv_step1(file_path):
    df = pd.read_csv(file_path)
    df['CN'] = df['CN'].apply(lambda x: str(x).zfill(8))
    return df.iloc[:, [4, 5, 6]]

def process_csv_step2(file1, file2):
    df_from_enduser = process_csv_step1(file1)

    df_from_ssms = pd.read_csv(file2, header=None)
    df_from_ssms.drop([2, 3, 4], axis=1, inplace=True)
    df_from_ssms.rename(columns={0: 'MEK', 1: 'CN_'}, inplace=True)
    df_from_ssms['CN_'] = df_from_ssms['CN_'].apply(lambda x: str(x).zfill(8))

    df_hayai = pd.concat([df_from_enduser, df_from_ssms], axis=1)
    df_hayai['MEK'] = df_hayai['MEK'].fillna(0).astype(int)

    return df_hayai

def get_meks_from_ssms(control_numbers):
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
        [URMCCEX3].[dbo].[Equipment]
    WHERE 
        [ControlNo] IN (\n{', '.join([f"'{cn}'" for cn in control_numbers])} 
        )
    ORDER BY 
        CASE\n    {case_block}  
    END;
    """.strip()
    return sql_command

def generate_sql_for_ssms(meks, dates, rtls_codes):
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
    UPDATE [URMCCEX3].[dbo].[Equipment]
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

def main():
    parser = argparse.ArgumentParser(description="Process CSV files, generate SQL, and handle templates.")
    parser.add_argument("step", choices=["step1", "step2", "cpysrc"], help="Step to execute: 'step1', 'step2', or 'cpysrc'")
    parser.add_argument("csv_file1", nargs="?", help="Path to the first input CSV file (not needed for cpysrc)")
    parser.add_argument("csv_file2", nargs="?", help="Path to the second input CSV file (for step2)")
    parser.add_argument("-c", "--copy", action="store_true", help="Copy the SQL command to the clipboard")
    parser.add_argument("-l", "--log", action="store_true", help="Display the DataFrame content")

    pyperclip.set_clipboard('xsel')
    args = parser.parse_args()

    if args.step == "step1":
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

    elif args.step == "step2":
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

    elif args.step == "cpysrc":
        copy_template()

if __name__ == "__main__":
    main()