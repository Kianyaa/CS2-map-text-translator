import pandas as pd
import re
import os
import json
import requests
from bs4 import BeautifulSoup
from googletrans import Translator


def get_workshop_title(url, translator=None):
    """Fetch the title of a workshop from Steam Community."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title_div = soup.find('div', class_='workshopItemTitle')
        if title_div:
            return title_div.text.strip()
        else:
            return "Warning: Title not found your workshop ID mighty be incorrect."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def setup_directories():
    """Ensure the 'data' and 'data/export' directories exist."""
    cwd = os.getcwd()
    data_dir = os.path.join(cwd, 'data')
    export_dir = os.path.join(data_dir, 'export')

    print()
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print("Not found 'data' folder, created new 'data' directory...")
    
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        print("Not found 'export' folder inside 'data' directory, created new 'data\export' directory...")

    print("\n[Completed directory setup.]\n")
    
    return data_dir, export_dir

def check_directory(data_dir):
    # Define the path for the 'export' folder
    export_dir = os.path.join(data_dir, 'export')
    
    while not os.path.isdir(export_dir):  # Check if 'export' directory exists
        print("The 'export' directory is missing. Please create the 'export' directory.")
        input("Press Enter once you've created the 'export' directory...")
    
    # Loop to check for files with the correct format in the 'export' directory
    while True:
        files_in_data_dir = os.listdir(data_dir)
        
        # Check if there is any file matching the correct format: numeric_id_text.json
        valid_files = [file for file in files_in_data_dir if re.match(r'^\d+_text\.json$', file)]
        
        if valid_files:
            print("Valid JSON files found:\n")
            for file in valid_files:
                print(file)  
            break
        else:
            print("No valid JSON file found. Please place a file matching the '[workshop ID]_text.json' format example: '1234567890_text.json' in the 'data' directory.")
            input("Press Enter once you've added the correct file...")


def translate_text(io_list, translator):
    """Translate Chinese text in the 'io' list and place the translation in the 'replace' field."""
    for io in io_list:
        if 'overrideparam' in io and io['overrideparam']:
            try:
                # Translate the 'overrideparam' text
                translated_text = translator.translate(io['overrideparam'], src='zh-cn', dest='en').text
                # Place the translated text in the 'replace' field
                if 'replace' not in io:
                    io['replace'] = {}  # Ensure 'replace' exists in case it's missing
                io['replace']['overrideparam'] = translated_text
            except Exception as e:
                print(f"Error translating text: {e}")
                # In case of an error, keep the original text in the 'replace' field
                if 'replace' not in io:
                    io['replace'] = {}
                io['replace']['overrideparam'] = io['overrideparam']
    return io_list



def process_workshop_data(data_dir, export_dir, translator):
    """Process and translate all workshop files."""
    files = os.listdir(data_dir)
    workshop_data = {}
    print()

    for file in files:
        match = re.match(r"(\d+)_text\.json", file)
        if match:
            workshop_id = match.group(1)
            url = f'https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}'
            title = get_workshop_title(url, translator)

            # Check if the title is found or not
            if title == "Warning: Title not found your workshop ID mighty be incorrect.":
                print(f"Warning: Title not found for Workshop ID: {workshop_id}")
                print(f"Please check if the Workshop ID is correct: {url}")
                print(f"Cancel all translate file...\n")
                break

            workshop_data[workshop_id] = title

            print(f"Workshop ID: {workshop_id} - {title} translating...")

            try:
                # Load JSON data
                file_path = os.path.join(data_dir, f'{workshop_id}_text.json')
                df = pd.read_json(file_path)
                data = df.get('modify', [])

                modified_data = []
                for item in data:
                    match_data = item.get('match', {})
                    io_list = match_data.get('io', [])

                    translated_io_list = []
                    for io in io_list:
                        if 'overrideparam' in io:
                            translated_text = translator.translate(io['overrideparam'], src='zh-cn', dest='en').text
                            translated_io_list.append({
                                "overrideparam": io['overrideparam']
                            })

                            replace_data = {
                                "overrideparam": translated_text
                            }
                    
                    modified_data.append({
                        "match": {
                            "io": translated_io_list
                        },
                        "replace": {
                            "io": replace_data
                        }
                    })
            except ValueError as e:
                    # Check if the error message matches your expected error
                    if "Unexpected character" in str(e):
                        print("Json format file is not correct, Please check the JSON map lump text data file.\n")
                    else:
                        # If it's another ValueError, print the error message
                        print(f"Error loading JSON file, check json data format is valid: {e}\n")
            except Exception as e:
                # Catch other unexpected errors
                print(f"An unexpected error occurred: {e}")

            # Save the translated JSON file
            output_path = os.path.join(export_dir, f'{workshop_id}_text.json')
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({'modify': modified_data}, f, ensure_ascii=False, indent=2)

            print(f'Translated JSON file exported to {output_path}\n')

    # Save workshop ID and titles to a JSON file
    with open(os.path.join(export_dir, 'workshopid_titles.json'), 'w', encoding='utf-8') as json_file:
        json.dump(workshop_data, json_file, ensure_ascii=False, indent=4)

    print("Completed all map translations!")
    print("Workshop data saved to 'export/workshopid_titles.json'\n")

def main():
    # Initialize Translator
    translator = Translator()

    # Directory setup
    data_dir, export_dir = setup_directories()

    # User input for proceeding
    print("Please place the 'map lump text data' file in the 'data' folder and type [YES / Y] key to proceed...")
    print("Example: data\\3070332866_text.json\n")
    while True:
        user_input = input("Type [YES/Y]: ")
        if user_input.lower() in ['yes', 'y']:
            break
        else:
            print("Please type [YES / Y] key to proceed...\n")

    # Check if directory is empty
    check_directory(data_dir)

    # Process workshop files and translate text
    process_workshop_data(data_dir, export_dir, translator)
    

if __name__ == "__main__":
    main()
