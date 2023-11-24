import shutil
from datetime import datetime, timedelta
import os
import subprocess
import utilities


def calculate_nth_sunday(current_date, n):
    days_until_sunday = (6 - current_date.weekday()) % 7  # Days until the next Sunday
    days_until_nth_sunday = days_until_sunday + (n - 1) * 7  # Days until the nth Sunday
    next_nth_sunday = current_date + timedelta(days=days_until_nth_sunday)
    return next_nth_sunday


def create_new_powerpoint():
    # Get the current date
    current_date = datetime.today()

    # Calculate the next Sunday's date

    current_date = datetime.today()

    # Calculate and display the first 5 Sundays
    for n in range(1, 6):
        next_nth_sunday = calculate_nth_sunday(current_date, n)
        print(f"{n}. {next_nth_sunday.strftime('%Y-%m-%d')}")

    # Allow the user to select a Sunday
    user_input = input("Enter the number (1-5) to select a Sunday: ")

    try:
        selected_sunday = int(user_input)
        if 1 <= selected_sunday <= 5:
            selected_date = calculate_nth_sunday(current_date, selected_sunday)
            print(f"You selected: {selected_date.strftime('%Y-%m-%d')}")
        else:
            print("Invalid input. Please enter a number from 1 to 5.")
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 5.")

    # Format the date as dd_mm_yy
    formatted_date = selected_date.strftime("%d_%m_%y")
    slides_folder = os.path.dirname(__file__)
    source_file = f"{slides_folder}/../Slides/Template dark.pptx"

    target_file = f"{slides_folder}/../Slides/{formatted_date}.pptx"

    if os.path.exists(target_file):
        overwrite = input(f"The file {target_file} already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != "y":
            print("File not copied.")
            return
    try:
        # Copy the file with the desired naming format
        shutil.copy(source_file, target_file)
        print(f"File copied successfully to {target_file}")
        utilities.open_file(target_file)
    except Exception as e:
        print(f"Error copying the file: {str(e)}")