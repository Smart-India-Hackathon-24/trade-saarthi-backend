import csv
import os
from typing import List, Dict
import logging

class CsvOperations:
    @staticmethod
    def read_csv(file_path: str) -> List[str]:
        try:
            if not os.path.exists(file_path):
                # Ensure directory exists
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # Create empty file
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    pass
                return []
                
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                return [row[0].lower().strip() for row in reader if row and row[0].strip()]
        except Exception as e:
            logging.error(f"Error reading CSV file {file_path}: {str(e)}")
            return []

    @staticmethod
    def write_csv(file_path: str, words: List[str]) -> bool:
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for word in words:
                    if word.strip():  # Only write non-empty words
                        writer.writerow([word.lower().strip()])
            return True
        except Exception as e:
            logging.error(f"Error writing to CSV file {file_path}: {str(e)}")
            return False

    @staticmethod
    def add_word(file_path: str, word: str) -> Dict:
        try:
            words = CsvOperations.read_csv(file_path)
            word = word.lower().strip()
            
            if not word:
                return {"status": "error", "message": "Word cannot be empty"}
                
            if word in words:
                return {"status": "error", "message": "Word already exists"}
                
            words.append(word)
            if CsvOperations.write_csv(file_path, words):
                return {"status": "success", "message": "Word added successfully"}
            else:
                return {"status": "error", "message": "Failed to write to file"}
        except Exception as e:
            logging.error(f"Error adding word to {file_path}: {str(e)}")
            return {"status": "error", "message": f"Internal error: {str(e)}"}

    @staticmethod
    def delete_word(file_path: str, word: str) -> Dict:
        try:
            words = CsvOperations.read_csv(file_path)
            word = word.lower().strip()
            
            if not word:
                return {"status": "error", "message": "Word cannot be empty"}
                
            if word not in words:
                return {"status": "error", "message": "Word not found"}
                
            words.remove(word)
            if CsvOperations.write_csv(file_path, words):
                return {"status": "success", "message": "Word deleted successfully"}
            else:
                return {"status": "error", "message": "Failed to write to file"}
        except Exception as e:
            logging.error(f"Error deleting word from {file_path}: {str(e)}")
            return {"status": "error", "message": f"Internal error: {str(e)}"} 