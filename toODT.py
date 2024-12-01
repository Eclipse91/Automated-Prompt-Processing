import logging
import pypandoc

def md_to_odt(input_file, output_file):
    """
    Convert a Markdown file to an OpenDocument Text file (.odt).

    Args:
        input_file (str): Path to the Markdown (.md) file.
        output_file (str): Path for the output OpenDocument (.odt) file.
    """
    try:
        # Convert the file from markdown to odt
        pypandoc.convert_file(input_file, 'odt', outputfile=output_file)
        print(f"Conversion successful: '{input_file}' → '{output_file}'")
        logging.info(f"Conversion successful: '{input_file}' → '{output_file}'")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(e)

# Example usage
# md_to_odt('Untitled 1.md', 'Untitled 1.odt')