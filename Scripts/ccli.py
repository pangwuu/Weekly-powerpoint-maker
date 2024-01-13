import csv, pyperclip
import random
import os


def find_ccli_info(song_name):
    song_name = song_name.replace(".pptx", "")
<<<<<<< Updated upstream
    csv_file = f"{os.path.dirname(__file__)}/../CCLI/CCLI.csv"
=======
    csv_file = "/Weekly powerpoint maker/CCLI/CCLI.csv"
>>>>>>> Stashed changes
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)  # Pass the opened file, not the file path
        next(reader)  # Skip the header row
        for row in reader:
            csv_song_name = row[0].strip()
            ccli_description = row[1].strip()
            ccli_number = row[2].strip()
            if song_name.lower() in csv_song_name.lower():
                pyperclip.copy(f"CCLI: {ccli_description}\n{ccli_number}")
                return f"CCLI: {ccli_description}\n{ccli_number}", True

    ccli_number = random.randint(0, 1000000)
    pyperclip.copy(f"CCLI license number\n{ccli_number}")
    return f"CCLI license number\n{ccli_number}", False

# csv_file = "/Users/johnnywu/Desktop/Weekly powerpoint maker/CCLI/ccli.csv"
# user_input = "hosanna"  # Replace with the song name you're searching for

# found_song_name, ccli_number = find_ccli_info(user_input, csv_file)

# if found_song_name is not None:
#     print(f"CCLI Number for '{found_song_name}': {ccli_number}")
# else:
#     print(f"Song containing '{user_input}' not found in the CSV file.")
