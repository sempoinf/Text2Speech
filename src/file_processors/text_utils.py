import re
import os

from selenium import webdriver
from selenium.webdriver.safari.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import docx2txt
from PyPDF2 import PdfReader

class TextChunker:
    def __init__(self, max_length=181):
        self.max_length = max_length

    def clean_text(self, text):
        # Remove extra spaces between words
        text = re.sub(r'\s+', ' ', text)
        
        # Remove spaces before punctuation marks like: "text .", "text ,"
        text = re.sub(r'\s([?.!,":;])', r'\1', text)
        
        # Remove extra spaces around punctuation
        text = re.sub(r'\s([?.!,":;])', r'\1', text)
        
        # Trim spaces at the start and end of the text
        return text.strip()

    def split_text(self, text):
        # Clean the text first
        text = self.clean_text(text)
        
        # Split the cleaned text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []  # This will store the resulting text chunks
        current_chunk = sentences[0]  # Start with the first sentence

        for sentence in sentences[1:]:
            # Try to add the next sentence to the current chunk
            if len(current_chunk) + len(sentence) + 1 <= self.max_length:
                current_chunk += " " + sentence  # If it fits, add to the current chunk
            else:
                # If it doesn't fit, save the current chunk and start a new one
                chunks.append(current_chunk)
                current_chunk = sentence  # New chunk starts with the current sentence

        # Add the last chunk to the list
        chunks.append(current_chunk)

        # Merge chunks if needed (if their total length is less than the max_length)
        merged_chunks = []
        current_chunk = chunks[0]  # Start with the first chunk

        for chunk in chunks[1:]:
            if len(current_chunk) + len(chunk) + 1 <= self.max_length:
                # If the current chunk and the next one fit together, merge them
                current_chunk += " " + chunk
            else:
                # Otherwise, push the current chunk and start a new one
                merged_chunks.append(current_chunk)
                current_chunk = chunk

        # Add the final chunk
        merged_chunks.append(current_chunk)

        return merged_chunks
    
    def from_file(self, file_path, split=False):
        # Detect file type and process accordingly
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        elif file_extension == '.docx':
            text = self._extract_text_from_docx(file_path)
        elif file_extension == '.pdf':
            text = self._extract_text_from_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        if split:
            return self.split_text(text)
        else:
            return text
    
    def _extract_text_from_docx(self, file_path):
        if not file_path.lower().endswith('.docx'):
            raise ValueError("File is not a DOCX file.")
        
        try:
            text = docx2txt.process(file_path)
            return text
        except Exception as e:
            print(f"Error processing DOCX file: {e}")
            return None
    
    def _extract_text_from_pdf(self, file_path):
        # Extract text from PDF file
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages])
        return text

    def from_url(self, url, split=False):
        # Set up Safari options
        safari_options = Options()
        safari_options.headless = True  # Set headless to True if you want to run without a GUI

        # Create a Safari driver
        driver = webdriver.Safari(options=safari_options)

        # Navigate to the URL
        driver.get(url)
        
        # Explicit wait to ensure the page is fully loaded (wait for an element that loads after all content)
        try:
            # Wait until an element with the class "text-content" is present on the page (change this selector if needed)
            WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.CLASS_NAME, "text-content"))  # Replace with the correct element on the page
            )
        except Exception as e:
            print(f"Error while waiting for page load: {e}")
            driver.quit()
            return
        
        # Get the page HTML after it has loaded all elements
        soup = BeautifulSoup(driver.page_source, "html.parser")
        text = soup.get_text(separator=" ")  # Extract clean text
        text = " ".join(text.split())  # Remove extra spaces
        
        driver.quit()  # Close the browser

        # Split the text if 'split' is True, otherwise return the entire text
        if split:
            return self.split_text(text)
        else:
            return text
        
    def save_chunks_to_file(self, text, file_path, split=False):
        chunks = self.split_text(text) if split else text
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(chunk + "\n" for chunk in chunks)
        return file_path

if __name__ == "__main__":
    chunker = TextChunker()

    # Check text splitter form str
    # text = "Небо было пасмурным, а тёмные облака подавляли величественную атмосферу Дворца. Великолепный дворцовый зал был окутан тёмными облаками, как будто это была огромная клетка, крепко удерживающая людей."
    # print(len(text))
    # formated_txt = chunker.split_text(text)
    # print(formated_txt[0])
    # print(len(formated_txt)) # out 2, cause 198 symbs

    # 198 in originaly, but after splitted -> 197, bacause space between takes deleted
    # leng = 0
    # for i, seg in enumerate(formated_txt, start=1):
    #     print(f"Segment {i} - {len(seg)} length")
    #     leng += len(seg)
    # print(leng)


    # Check text get from file
    # in_dir = r'data/input/test_text.txt'
    # in_dir = r'tables.txt'
    # test_txt = chunker.from_file(in_dir, split=False)
    # print(test_txt)
    # print(len(test_txt))
    # test_txt = chunker.from_file(r'../Pets/test_text.txt', split=True)
    # print(test_txt)
    # print(len(test_txt))
    # for i, seg in enumerate(test_txt, start=1):
    #     print(f"Segment {i} - {len(seg)} length")


    # Check text get site
    # site_url = r'https://ranobelib.me/ru/28369--the-rebirth-of-the-malicious-empress-of-military-lineage/read/v1/c2'
    # test_txt = chunker.from_url(url=site_url, split=False)
    # print(test_txt[:1000])
    # print(len(test_txt))

    # test_txt = chunker.from_url(url=site_url, split=True)
    # print(test_txt[:1000])
    # print(len(test_txt))
    # counter = 0
    # for i, seg in enumerate(test_txt, start=1):
    #     print(f"Segment {i} - {len(seg)} length")
    #     if len(seg) > 181:
    #         print(seg)
    #         counter = counter+1
    #     # if i == 123:
    #     # print(seg)
    # print(counter)

    # Check .docx worker
    # test_txt = chunker.from_file(file_path=r'/Users/yaao20u291/Pets/test.docx', split=True)
    # print(test_txt)

    # Check .pdf worker
    # test_txt = chunker.from_file(file_path=r'/Users/yaao20u291/Pets/test_text.pdf', split=True)
    # print(test_txt)
