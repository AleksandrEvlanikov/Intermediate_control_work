import os
import json
from datetime import datetime

file_base = "base.json"
last_id = 0
all_data = []

if not os.path.exists(file_base):
    with open(file_base, "w", encoding="utf-8") as _:
        pass


def edit_note():
    note_id = int(input("Введите ID заметки для редактирования: "))
    if os.path.isfile(file_base):
        with open(file_base, "r", encoding="utf-8") as f:
            try:
                notes = json.load(f)
            except json.JSONDecodeError:
                notes = []
        found = False
        for i, note in enumerate(notes):
            if note["id"] == note_id:
                new_note = input("Введите новую заметку: ")
                notes[i]["note"] = new_note
                found = True
                break
        if found:
            with open(file_base, "w", encoding="utf-8") as f:
                json.dump(notes, f, indent=4)
            print("Заметка успешно отредактирована!")
        else:
            print("Заметка с указанным ID не найдена.")
    else:
        print("Список заметок пуст.")


def show_all():
    if all_data:
        for note in all_data:
            print(f"ID: {note['id']}\nЗаметка: {note['note']}\n")
    else:
        print("Empty data")


def read_records():
    global last_id, all_data

    if os.path.isfile(file_base):
        with open(file_base, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
        if all_data:
            last_id = all_data[-1]["id"]
        return all_data
    return []


def delete_note():
    with open(file_base, "r") as f:
        try:
            notes = json.load(f)
        except json.JSONDecodeError:
            notes = []

    if notes:
        index = int(input('Введите индекс элемента, который вы хотите удалить: '))
        if 0 <= index < len(notes):
            del notes[index]
            with open(file_base, "w") as f:
                json.dump(notes, f, indent=4)
        else:
            print('Неверный индекс. Введите индекс из списка.')
    else:
        print('Список пуст.')

def select_by_date():
    date_str = input("Введите дату(ДД.ММ.ГГ) ")
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
        selected_notes = [note for note in all_data if note["date"]==str(date)]
        if selected_notes:
            for note in selected_notes:
                print(f"ID: {note['id']}\nЗаметка:  {note['note']}\nДата:  {note['date']}\n")
        else:
            print("Нет заметок для этой даты.")
    except ValueError:
        print("Неверный формат даты.")


def add_new_contact():
    global last_id
    string = input("Введите заметку: ")
    date_str = input("Введите дату (ДД.ММ.ГГГГ): ")
    try:
        date = datetime.strptime(date_str, "%d.%m.%Y").date()
        last_id += 1
        new_note = {"id": last_id, "note": string, "date": str(date)}
        all_data.append(new_note)
        with open(file_base, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4)
        print("Заметка успешно добавлена!")
    except ValueError:
        print("Неверный формат даты.")



def main_menu():
    play = True
    while play:
        read_records()
        answer = input("The note :\n"
                       "1. Show all records\n"  # Показать все записи
                       "2. Add a record\n"      # Добавить запись
                       "3. Change\n"            # Изменить
                       "4. Delete\n"            # Удалить
                       "5. select by date\n"    # Выбор по дате
                       "6. Exit\n")             # Выход
        match answer:
            case "1":
                show_all()
            case "2":
                add_new_contact()
            case "3":
                edit_note()
            case "4":
                delete_note()
            case "5":
                select_by_date()
            case "6":
                play = False
            case _:
                print("Try again!\n")


if not os.path.isfile(file_base):
    with open(file_base, "w", encoding="utf-8") as _:
        pass

main_menu()
