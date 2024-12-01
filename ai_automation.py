import os
import logging
from time import sleep
from dotenv import load_dotenv, dotenv_values
import google.generativeai as genai
from openai import OpenAI
from toODT import md_to_odt


def load_env_file():
    '''
    Load the ini configuration file.
    '''
    if load_dotenv():
        return dotenv_values()['API_KEY']
    
    return ''


def reorganize_text(text, model='gemini-1.5-flash', max_tokens=500, temperature=0.5):
    '''
    Reorganizes the given text using a specified AI generative model (OpenAI or Gemini).

    This function sends the input text along with a predefined prompt to the chosen model's API,
    which processes the text and returns a reorganized version.

    Args:
        text (str): The text content to be reorganized.
        model (str, optional): The generative model to use. Defaults to `'gemini-1.5-flash'`.
                              - If `'gpt'` is in the model name, the OpenAI API is used.
                              - Otherwise, the Gemini API is used.
        max_tokens (int, optional): The maximum number of tokens for the model to generate. Defaults to `500`.
        temperature (float, optional): The temperature for the model's text generation. Defaults to `0.5`.

    Returns:
        str: The reorganized text returned by the AI model.
        None: If an error occurs during processing or the response is invalid.

    Notes:
        - Reads a predefined prompt from a `prompt.txt` file, appending the input text for processing.
        - Uses the `load_env_file()` function to retrieve the API key for both OpenAI and Gemini APIs.
        - Logs errors in case of API failures or exceptions.

    Raises:
        Exception: Captures and logs exceptions raised by the OpenAI or Gemini API during text processing.
    '''
    # Read the prompt and add the text
    with open('prompt.txt', 'r') as file:
        prompt = file.read().strip() + f'\n\n{text}'

    if 'gpt' in model:
        try:
            client = OpenAI(
                # This is the default and can be omitted
                api_key=load_env_file(),
            )

            completion = client.chat.completions.create(
                model='gpt-4o-mini',#'gpt-3.5-turbo',
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            return completion
        
        except Exception as e:
            print(f'Error processing text with OpenAI API: {e}')
            logging.error(e)
            return None
    else:
        try:
            # Replace with your actual API key
            genai.configure(api_key=load_env_file())

            # Initialize the model (gemini-1.5-flash in this case)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Generate content using the model
            response = model.generate_content(prompt)

            # organized_text = response['choices'][0]['message']['content'].strip()
            return response.text
        
        except Exception as e:
            print(f'Error processing text with Gemini API: {e}')
            logging.error(e)
            return None


def process_all_text_files(input_folder, output_folder):
    '''
    Processes all `.txt` files in a specified input folder and its subdirectories, 
    applying text organization and saving the results in a mirrored directory structure in the output folder.

    Workflow:
        - Traverses all subdirectories within the input folder.
        - For each `.txt` file:
            - Reads the file content.
            - Reorganizes the text using the `reorganize_text` function.
            - Saves the processed text to the output folder, maintaining the same relative directory structure.
        - Combines processed files in each subdirectory into a single file with multiple formats (.txt, .md, .odt).

    Args:
        input_folder (str): The root folder containing `.txt` files to process.
        output_folder (str): The root folder where processed files will be saved.

    Notes:
        - Ensures output directory structure mirrors the input directory structure.
        - Skips processing if the output file already exists.
        - Logs processed and skipped files.
        - Combines processed files in each directory using `combine_text_files_in_folder`.
        - Incorporates a delay (30 seconds) between processing each directory.

    Raises:
        Exception: If there are errors during the file combination step, they are logged but not re-raised.

    '''
    def read_text_file(file_path):
        '''
        Reads and returns the content of a text file.

        Args:
            file_path (str): The path to the text file to be read.

        Returns:
            str: The content of the file as a string.
        '''
        with open(file_path, 'r') as file:
            text = file.read()
        return text   

    def save_text_to_file(text, file_path):
        '''
        Saves a given text string to a specified file.

        Args:
            text (str): The text content to be written to the file.
            file_path (str): The path where the file should be saved.

        Notes:
            Ensures the target directory exists before saving the file.
        '''
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            file.write(text)

    def combine_text_files_in_folder(folder_path, output_folder):
        '''
        Combines the content of all text files in a specified folder into a single file, 
        with the output saved in multiple formats.

        Args:
            folder_path (str): The path to the folder containing .txt files to combine.
            output_folder (str): The path to the folder where the combined file will be saved.

        Notes:
            - Combines text files in the folder, sorted by their filenames.
            - Creates the output file in three formats: .txt, .md, and .odt.
            - Uses an external `md_to_odt` function to convert Markdown (.md) to ODT.
            - Logs the operation and prints the location of the combined file.

        '''
        # Get all .txt files in the folder, sorted by filename
        text_files = sorted([file for file in os.listdir(folder_path) if file.endswith('.txt')])
        
        # Initialize a string to hold the combined text
        combined_text = ''
        
        # Read and concatenate the contents of each .txt file
        for file in text_files:
            file_path = os.path.join(folder_path, file)
            with open(file_path, 'r') as f:
                combined_text += f.read() + '\n'  # Add newline between file contents

        # Define the output path for the combined file, named after the folder
        folder_name = os.path.basename(folder_path)
        combined_output_path = os.path.join(output_folder, f'{folder_name}.txt')
        combined_output_path_md = os.path.join(output_folder, f'{folder_name}.md')
        combined_output_path_odt = os.path.join(output_folder, f'{folder_name}.odt')

        # Ensure the output directory exists, then save the combined text
        os.makedirs(os.path.dirname(combined_output_path), exist_ok=True)
        with open(combined_output_path, 'w') as combined_file:
            combined_file.write(combined_text.strip())  # Strip trailing newline
        
        with open(combined_output_path_md, 'w') as combined_file:
            combined_file.write(combined_text.strip())  # Strip trailing newline
        
        md_to_odt(combined_output_path_md, combined_output_path_odt)

        print(f'Combined and saved: {combined_output_path}')
        logging.info(f'Combined and saved: {combined_output_path}')

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.txt'):
                # Define input file path
                input_file_path = os.path.join(root, file)
                
                # Define output file path with same subfolder structure in the output folder
                relative_path = os.path.relpath(input_file_path, input_folder)
                output_file_path = os.path.join(output_folder, relative_path)
                print(input_file_path)
                logging.info(input_file_path)

                # Read, process, and save the reorganized text
                text = read_text_file(input_file_path)
                if not os.path.exists(output_file_path):
                    organized_text = reorganize_text(text)
                else:
                    continue

                if organized_text != None:
                    save_text_to_file(organized_text, output_file_path)
                else:
                    logging.error(f'{output_file_path} not processed')
                    continue

                print(f'Processed and saved: {output_file_path}')
                logging.info(f'Processed and saved: {output_file_path}')
        else:
            try:
                # print(os.path.join(output_folder,os.path.basename(os.path.dirname(output_file_path))+'.txt'))
                if not os.path.exists(os.path.join(output_folder,os.path.basename(os.path.dirname(output_file_path))+'.txt')):
                    combine_text_files_in_folder(os.path.dirname(output_file_path), output_folder)
            except Exception as e:
                print(f'Error: {e}')
                logging.error(e)

        sleep(30)
