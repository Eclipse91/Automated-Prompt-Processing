import os
import logging
from datetime import datetime
import ai_automation


def log_configurator() -> str:
    '''
    Configure and initialize the logger.
    '''
    log_directory = './logs/'
    os.makedirs(log_directory, exist_ok=True)
    current_datetime = datetime.now()
    current_file_name = os.path.splitext(os.path.basename(__file__))[0]
    formatted_datetime = current_datetime.strftime('%Y%m%d_%H%M%S')
    log_file = f'{log_directory}{current_file_name}_{formatted_datetime}.log'

    logging.basicConfig(
        filename=log_file, 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    logging.info('Program started')

    return log_file

def main():
    # Configure and initialize the logger file
    log_file = log_configurator()
    logging.info(f'Logger configured: {log_file}')

    # Folder with subfolders of .txt files
    input_folder_path = ''        
    # Output folder to save the reorganized texts
    output_folder_path = ''
    
    ai_automation.process_all_text_files(input_folder_path, output_folder_path)


if __name__ == '__main__':
    main()
