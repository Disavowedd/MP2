import subprocess
import os
import sys

def instruction():

    print("JETOOLSZ v1.0")
    print("Use the Commands -h or -s, to see valid commands or start the process respectively.")
    
def help():
    print("This is a tool that uses RegFileExport, RLA, and RegRipper 3.0")
    print("It focuses on extracting, cleaning, and parsing a NTUSER.DAT file from the Registry")
    print("Commands:")
    print("-h: Display this text")
    print("-s: Prompts you to input target and source destinations.")


def run_commands():
    # Prompt the user for input
    ntuser_dat = input("Enter the path to the NTUSER.DAT file: ")
    ntuser_txt = input("Enter the output path for the NTUSER.TXT file: ")
    
    # Extract directory from ntuser_txt and set up "cleaned" subfolder
    output_dir = os.path.dirname(ntuser_txt)
    cleaned_reg_file = os.path.join(output_dir, "cleaned")
    
    # Create the "cleaned" directory if it doesn't exist
    os.makedirs(cleaned_reg_file, exist_ok=True)
    
    csv_output = input("Enter the output path for the NTUSER.CSV file: ")

    try:
        # Step 1: Export registry file
        subprocess.run(["RegFileExport", ntuser_dat, ntuser_txt], check=True)
        print("Step 1: Registry file exported successfully.")
        
        # Step 2: Clean registry file
        subprocess.run(["rla", "-f", ntuser_dat, "--out", cleaned_reg_file], check=True)
        print(f"Step 2: Registry file cleaned successfully. Output directory: {cleaned_reg_file}")
        
        # Step 3: Parse registry file and save output to CSV
        cleaned_ntuser_dat = os.path.join(cleaned_reg_file, "__NTUSER.dat")
        with open(csv_output, "a") as output_file:
            subprocess.run(["rip", "-r", cleaned_ntuser_dat, "-a"], stdout=output_file, check=True)
        print("Step 3: Parsed registry file saved to CSV successfully.")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")





if __name__ == "__main__":
     if len(sys.argv) > 1:
        if sys.argv[1] == "-s":
            run_commands()
        elif sys.argv[1] == "-h":
            help()
        else:
            print("Invalid argument. Use -h for help.")
     else:
        instruction()