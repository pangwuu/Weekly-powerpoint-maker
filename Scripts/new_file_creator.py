import shutil
from datetime import datetime, timedelta
import os

def create_new_powerpoint():
    # Get the current date
    current_date = datetime.today()

    # Calculate the next Sunday's date
    days_until_sunday = (6 - current_date.weekday()) % 7
    next_sunday = current_date + timedelta(days=days_until_sunday)

    # Format the date as dd_mm_yy
    formatted_date = next_sunday.strftime("%d_%m_%y")
    source_file = "/Users/johnnywu/Desktop/Weekly powerpoint maker/Slides/Template dark.pptx"

    target_file = f"/Users/johnnywu/Desktop/Weekly powerpoint maker/Slides/{formatted_date}.pptx"

    if os.path.exists(target_file):
        overwrite = input(f"The file {target_file} already exists. Do you want to overwrite it? (y/n): ").strip().lower()
        if overwrite != "y":
            print("File not copied.")
            return

    try:
        # Copy the file with the desired naming format
        shutil.copy(source_file, target_file)
        print(f"File copied successfully to {target_file}")
    except Exception as e:
        print(f"Error copying the file: {str(e)}")
