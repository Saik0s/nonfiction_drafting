import logging
# Removed the unnecessary imports from utils

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_prompt_from_file(prompt_file):
    try:
        with open(prompt_file, 'r', encoding='utf-8') as infile:
            return infile.read()
    except Exception as e:
        logger.error(f"Error reading prompt from file {prompt_file}: {e}")
        return None

def save_file(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(content)
        logger.info(f"File saved: {filepath}")
    except Exception as e:
        logger.error(f"Error saving file {filepath}: {e}")

def open_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
            return infile.read()
    except Exception as e:
        logger.error(f"Error opening file {filepath}: {e}")
        return None
