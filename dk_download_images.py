import os
import urllib.request
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Function to download files (for both test and train)
def download_file(url, folderpath):
    try:
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
            
        filepath = os.path.join(folderpath, os.path.basename(url))
        if not os.path.exists(filepath):  # Check if file already exists
            urllib.request.urlretrieve(url, filepath)
        return "success", url
    except Exception as e:
        print(url, traceback.format_exc())
        return "error", url

# Function to download train images based on labels
def downloadTrainFile(line):
    try:
        tokens = line.split(',')
        url = tokens[0].strip()
        label = tokens[1].strip()
        folderpath = os.path.join("train", label)
        return download_file(url, folderpath)
    except Exception as e:
        print(f"Error processing line: {line}, {traceback.format_exc()}")
        return "error", line

# Function to handle parallel downloading using ThreadPoolExecutor with progress tracking
def download_in_parallel(urls, download_function):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_function, url) for url in urls]
        for _ in tqdm(as_completed(futures), total=len(futures)):
            pass

# Main download logic
if __name__ == "__main__":
    # Read the CSV and prepare for download
    with open('train.csv') as csvTrain:
        lines = csvTrain.readlines()

    # Remove header and clean lines
    clean_lines = [line.strip() for line in set(lines[1:])]

    print(f"Total unique files to download: {len(clean_lines)}")
    print('Downloading...')

    # Download train files in parallel with progress tracking
    download_in_parallel(clean_lines, downloadTrainFile)


