import json
import csv
from typing import List, Dict, Union
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def read_table_csv(filename: str) -> List[Dict]:
    file_path = BASE_DIR / "src" / filename
    with open(file_path, 'r', encoding='utf-8', newline='') as file:
        readed_file = csv.DictReader(file)
        return list(readed_file)


def read_json(filename: str) -> Union[list, dict]:
    file_path = BASE_DIR / "src" / filename
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def create_json(filename: str, data: Union[list, dict]) -> None:
    file_path = BASE_DIR / "src" / filename
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def create_result(output_filename: str) -> None:
    user_list = [{"name": user["name"], "gender": user["gender"], "address": user["address"], "age": user["age"], "books": []} for user in read_json("users.json")]
    book_list = [{"title": book["Title"], "author": book["Author"], "pages": book["Pages"], "genre": book["Genre"]} for book in read_table_csv("books.csv")]
    
    book_index = 0
    while book_index < len(book_list):
        for user in user_list:
            if book_index < len(book_list):
                user["books"].append(book_list[book_index])
                book_index += 1
            else:
                break
    
    create_json(output_filename, user_list)


create_result("result.json")