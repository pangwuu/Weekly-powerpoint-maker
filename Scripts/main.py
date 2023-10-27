import bible_passage, Custom_Running_Order, new_file_creator, song_finder

def main():
    # Create new powerpoint based on mode
    new_file_creator.create_new_powerpoint()
    # Search for the three songs - open powerpoints or create new ones if needed
    song_finder.find_and_open_songs()
    # Get bible passage
    bible_passage.bible_passage()

if __name__ == "__main__":
    main()