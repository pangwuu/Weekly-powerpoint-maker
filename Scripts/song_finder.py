import os, subprocess, lyricsgenius, shutil, re
import ccli
import pyperclip

# Path to the root directory containing "Songs" and "Complete Slides" directories
root_directory = "/Users/johnnywu/Desktop/Weekly powerpoint maker"

# This ain't meant to be seen
genius_token = "mfoyE4xeYy6XHR-TpI4icg-P4rH67lcKU47tXE-zWbb2XoOinj8KGAvkacUr0-Bt"

# Path to the "Songs" directory
songs_directory = os.path.join(root_directory, "songs")

# List all the song files in the "Songs" directory and sort them alphabetically. Do not open the template file
song_files = sorted([f for f in os.listdir(songs_directory) if (f.endswith(".pptx") and f != "Template - PLEASE COPY.pptx")])

# Since the lyrics from genius have some weird stuff we're using some regex patterns to get rid of them. 
# We also make the beginning of every section on a new line
def format_lyrics(lyrics_text):

    formatted_lyrics = ""
    lines = lyrics_text.split('\n')
    
    for line in lines:
        if line.strip():  # Skip empty lines
# Change this code so it detects ANY "[" rather than needing to start the line with it. If the [ appears
# but IS NOT at the beginning of the line, break up the line such that the [ is on the next next line.
            if line.startswith("["):
                formatted_lyrics += '\n'  # Start a new line before sections like [Chorus], [Verse], etc.
            formatted_lyrics += line + '\n'

    pattern = r'\d+.*Contributors.*\['
    match_contributors = re.search(pattern, formatted_lyrics)

    if match_contributors:
        modified_text = formatted_lyrics[:match_contributors.start()] + formatted_lyrics[match_contributors.end() - 1:]
    else:
        modified_text = formatted_lyrics

    pattern = r'You might also like\['
    match = re.search(pattern, modified_text)

    if match:
        modified_text = modified_text[:match.start()] + "\n" + modified_text[match.end() - 1:]

    modified_text = formatted_lyrics
    formatted_section = ""
    lines = modified_text.split('\n')
    
    for line in lines:
        if line.strip():  # Skip empty lines
            if line.startswith("["):
                formatted_section += '\n'  # Start a new line before sections like [Verse], [Chorus], etc.
            formatted_section += line + '\n'
    
    if formatted_section.strip().endswith(("1", "2", "3", "4", "5", "6", "7", "8", "9")):
        formatted_section = formatted_section[:-2]

    return formatted_section

# Fetch lyrics using the Genius API
def fetch_lyrics(song_name, artist):

    # Increase timeout if it isn't working
    genius = lyricsgenius.Genius(genius_token, timeout=10) 
    artist = artist.title()
    
    if artist != "":
        confirm_song_name = input(f"To confirm, you're looking for {song_name.replace('.pptx', '')} by {artist}: (Y to continue) ")
    else:
        confirm_song_name = input(f"To confirm, you're looking for {song_name.replace('.pptx', '')}: (Y to continue) ")
    
    # Searches the api for the song
    if confirm_song_name.lower().strip() == "y":
        song = genius.search_song(song_name.replace(".pptx", ""), artist, get_full_info=False)
        if song:
            # Obtains the lyrics
            lyrics = song.lyrics
            print("ORIGINAL")
            print(lyrics)
            print("ORIGINAL END\n\n")

            formatted_lyrics = f"{song.title} Lyrics\n\n{lyrics}"

            # Strip "embed" at the end
            if formatted_lyrics.endswith("Embed"):
                new_formatted_lyrics = format_lyrics(formatted_lyrics[:-len("Embed")].strip())
            else:
                new_formatted_lyrics = format_lyrics(formatted_lyrics.strip())
            
            # Ask for confirmation if this is indeed the song you're looking for by getting the first 200 characters
            print(new_formatted_lyrics[:200])
            keep_going = input("\nDoes the above sample look like what you're looking for? (Y to continue, any other key to exit)\n")
            
            if keep_going.lower().strip() != "y":
                return ""
            
            # Confirm the output directory and create it if it does not exist
            output_directory = f"{root_directory}/Lyrics text files/"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
            
            # Write into the file
            with open(f"{root_directory}/lyrics text files/{song_name.replace('.pptx', '')}_Lyrics.txt", "w") as file:
                file.write(new_formatted_lyrics)
                
            print("Lyrics saved to a text file.")

            # Copy the template powerpoint, and create a new one that has the song name.
            copy_powerpoint = input("Would you like to copy the template PowerPoint? (Y for yes)\n")
            if copy_powerpoint:
                template_path = os.path.join(songs_directory, "Template - PLEASE COPY.pptx")
                new_song_path = os.path.join(songs_directory, f"{song_name}.pptx")
                shutil.copy(template_path, new_song_path)
                print("PowerPoint file copied and renamed.")
                
                # Open the newly created PowerPoint file
                subprocess.run(["open", new_song_path])  # This is for macOS. Adjust for other platforms.
            
                # Open the text file
                text_file_path = f"{root_directory}/lyrics text files/{song_name.replace('.pptx', '')}_Lyrics.txt"
                subprocess.run(["open", text_file_path])  # This is for macOS. Adjust for other platforms.

            return new_formatted_lyrics
        else:
            return "Lyrics not available for this song."
    else:
        return "Lyrics not available for this song."


def find_and_open_songs():

    # Prompt the user for action (lyrics or PowerPoint)

    # Enter the songs. Save to an array
    # If the song exists, open the powerpoint file
    # If it does not exist, search for it using function == 1

    while True:
        search_song_name = input("Enter the song name you are trying to find: (n to exit): ")

        if search_song_name.lower().strip() == "n":
            break

        matching_indices = [idx for idx, song_file in enumerate(song_files) if search_song_name.lower() in song_file.lower()]
        
        print()
        if not matching_indices:
            print(f"No matching PowerPoint files found for '{search_song_name}'.")
            create = input("Would you like to create one? (Y for yes)\n").lower().strip()
            if create == 'y':
                artist = input("Enter the artist: ")
                search_song_name = search_song_name.title()
                lyrics = fetch_lyrics(search_song_name, artist)

                if lyrics == "":
                    continue
                # Get ccli data
                ccli_info = ccli.find_ccli_info(search_song_name)
                if found_song_name is not None:
                    print(f"CCLI Number for '{found_song_name}': {ccli_info}\nFound and copied to clipboard")
                else:
                    print(f"Song containing '{search_song_name}' not found in the CSV file.")
            

        else:
            print("Matching PowerPoint files:")
            for idx, song_file in enumerate(song_files):
                if search_song_name.lower() in song_file.lower():
                    print(f"{idx}. {song_file}")


            selected_indices = input("Enter the index of the PowerPoint file to open or 'A' to open all matching files (A/N): ").strip().lower()

            if selected_indices == 'a':
                selected_indices = matching_indices + 1
            else:
                try:
                    index = int(selected_indices) - 1
                    if 0 <= index < len(song_files):
                        selected_indices = [index]
                    else:
                        print("Invalid index. No PowerPoint files opened.")
                        selected_indices = []
                except ValueError:
                    print("Invalid input. No PowerPoint files opened.")
                    selected_indices = []

            for idx in selected_indices:
                if 0 <= idx < len(song_files):
                    song_name = song_files[idx + 1]
                    song_path = os.path.join(songs_directory, song_name)
                    subprocess.run(["open", song_path])  # This is for macOS. Adjust for other platforms.
                    print(f"Opened PowerPoint: {song_name}")
                    # Get ccli data
                    found_song_name, ccli_number = ccli.find_ccli_info(song_name)
                    if found_song_name is not None:
                        print(f"CCLI Number for '{found_song_name}': {ccli_number}")
                    else:
                        print(f"Song containing '{search_song_name}' not found in the CSV file.")

find_and_open_songs()