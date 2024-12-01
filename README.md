# Automated Prompt Processing

This project automates the task of combining a base prompt from a `prompt.txt` file with the contents of `.txt` files from a folder and processes them using an AI API. The application preserves the folder's structure while unifying files within the same folder into three formats (`.txt`, `.odt`, and `.md`). It also uses a securely stored API key for authentication.

## Features

- **Prompt Automation**: Combines a base prompt from `prompt.txt` with the contents of `.txt` files in a folder.
- **Folder Structure Preservation**: Retains the original folder hierarchy.
- **Unified Outputs**: Merges `.txt` files from the same folder into a single file in three formats:
  - Plain text (`.txt`)
  - OpenDocument Text (`.odt`)
  - Markdown (`.md`)
- **API Integration**: Processes combined prompts using an AI API with secure authentication through a `.env` file.

## Requirements

Before running this project, ensure the following are installed:

1. **Python** (>= 3.8)
2. A valid API key for the Gemini or OpenAI service (stored in a `.env` file).
3. **Pandoc** for converting text to `.odt` and `.md`.

## Getting Started

1. **Clone the Repository**
```bash
git clone https://github.com/Eclipse91/Automated-Prompt-Processing.git
```

2. **Navigate to the Project Directory**
```bash
cd Automated-Prompt-Processing
```

3. **Install Pandoc**
Install Pandoc, which is required for file format conversions:
- **Linux**:  
  ```bash
  sudo apt install pandoc
  ```
- **macOS**:  
  ```bash
  brew install pandoc
  ```
- **Windows**:  
  Download the installer from the [official Pandoc page](https://pandoc.org/installing.html) or install via Chocolatey:
  ```bash
  choco install pandoc
  ```

4. **Install the required dependencies** (creating a virtual environment is strongly recommended):
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up the `.env` File**
Create a `.env` file in the root directory with the following content:
```
API_KEY=your_api_key_here
```

6. **Prepare the `prompt.txt` File**
Create a `prompt.txt` file containing the base prompt to be appended to all files. For example:
```
Please process the following content intelligently:
```

7. **Add a folder with the files to elaborate**
Add a folder to the root directory containing the files to be processed.

8. **Run the Application**
Run the main script:
```bash
python3 main.py
```

## Configuration

### Obtaining a Gemini API Key
1. Visit the [Gemini API Signup Page](https://www.gemini.com/settings/api).
2. Log in or create a new account.
3. Navigate to **Settings > API Settings**.
4. Click **Create a New API Key**:
   - Select appropriate permissions (e.g., read-only, trading).
   - Assign the API key to a specific scope or sub-account, if required.
5. Confirm the request via Gemini’s two-factor authentication (2FA).
6. Copy and securely store the generated API key.

## File Descriptions

### `main.py`
- Entry point of the application.
- Iterates through the `input_folder` directory.
- Calls `ai_automation.py` for prompt processing and `toODT.py` for file format conversions.

### `ai_automation.py`
- Reads the API key from `.env`.
- Combines `prompt.txt` with the contents of `.txt` files in each folder.
- Sends the combined text to the AI API and processes the response.

### `toODT.py`
- Converts `.md` files into `.odt` formats using Pandoc.
- Ensures compatibility with tools like LibreOffice and Microsoft Word.

### `.env`
- Securely stores the API key for accessing the AI API.

### `prompt.txt`
- Contains the base prompt text to be appended to all the text in the files.

## Example Workflow

1. Input Folder Structure:
   ```
   ├── input_folder/
   │  ├── folder1/
   │  │   ├── file1.txt
   │  │   └── file2.txt
   │  ├── folder2/
   │  │   └── file3.txt
   ```
2. Base Prompt (`prompt.txt`):
   ```
   Please process the following content intelligently:
   ```
3. Output Folder Structure (after running `main.py`):
   ```
   ├──output_folder/
   │  ├── folder1/
   │  │   ├── file1.txt
   │  │   └── file2.txt
   │  ├── folder2/
   │  │   └── file3.txt
   |  ├── folder1.odt
   │  ├── folder1.md
   │  ├── folder1.txt
   │  ├── folder2.odt
   │  ├── folder2.md
   │  ├── folder2.txt
   ```

## Notes
- Input files must be in `.txt` format.
- Customize the `prompt.txt` file before running the script to suit your processing requirements.
- Ensure the `.env` file contains a valid API key.

## License
This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE) file for more details.