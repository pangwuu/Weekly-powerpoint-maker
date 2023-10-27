import os

running_order_mapping = {
    "V1": "Verse 1",
    "V2": "Verse 2",
    "V3" : "Verse 3",
    "V4": "Verse 4",
    "B": "Bridge",
    "B1": "Bridge 1",
    "B2": "Bridge 2",
    "C": "Chorus",
    "T": "Tag",
    "O": "Outro"
    # Add more mappings as needed
}

def rearrange_lyrics(lyrics, running_order):
    sections = lyrics.split('\n\n')
    rearranged_lyrics = []

    for section in running_order.split(','):
        if '*' in section:  # Check if section has repetition syntax
            section_name, repeat_count = section.split('*')
            section_name = running_order_mapping[section_name.strip()]
            repeat_count = int(repeat_count.strip())
        else:
            section_name = running_order_mapping[section.strip()]
            repeat_count = 1
        print(section_name)
        for s in sections:
            if s.startswith(f"[{section_name.lower().capitalize().strip()}"):
                rearranged_lyrics.extend([s] * repeat_count)
                break

    return '\n\n'.join(rearranged_lyrics)

current_directory = os.path.dirname(os.path.abspath(__file__))

# Get the list of text files in the current directory (excluding "custom_running_order" files)
text_files = [file for file in os.listdir(current_directory) if file.endswith(".txt") and not file.startswith("custom_running_order")]

if not text_files:
    print("No eligible text files found in the current directory.")
else:
    print("Available text files:")
    for idx, file in enumerate(text_files, start=1):
        print(f"{idx}. {file}")

    selection_idx = int(input("Select the index of the text file to apply custom running order: ")) - 1

    if 0 <= selection_idx < len(text_files):
        selected_file = text_files[selection_idx]

        # Read the original lyrics from the selected text file
        with open(f"{current_directory}/{selected_file}" , "r") as file:
            original_lyrics = file.read()

        # Get custom running order from the user
        running_order_input = input("Enter the custom running order (sections separated by commas): ")

        # Rearrange the lyrics based on the running order
        new_lyrics = rearrange_lyrics(original_lyrics, running_order_input)

        # Write the rearranged lyrics to a new text file
        output_filename = f"{current_directory}/custom_running_order_{selected_file}"
        with open(output_filename, "w") as file:
            file.write(new_lyrics)

        print(f"Custom running order lyrics saved to '{output_filename}'.")
    else:
        print("Invalid selection.")
