import pyperclip
from meaningless import WebExtractor
from meaningless.utilities.exceptions import InvalidSearchError


def bible_passage():
    verse_max = 5  # The max number of verses that compose a part
    newlines_max = 5  # The max number of lines that compose a part - 1

    while True:
        verse_reference = input("Enter a Bible verse reference such as '2 Peter 1:5-11' (n to exit)\n")
        
        if verse_reference.lower().strip() == "n":
            return

        try:
            extractor = WebExtractor(translation="NIV", output_as_list=True)
            verse_text = extractor.search(verse_reference)
            break
        except InvalidSearchError:
            go_again = input("No text found. Would you like to try again? (Y for yes, any other key to exit)\n")
            if go_again.lower().strip() == "y":
                continue
            else:
                return

    verse_remaining = len(verse_text)
    verse_count = 0
    part_count = 0
    part = ""
    for i, verse in enumerate(verse_text):
        part = f"{part}{verse}"
        # This ensures each slide has a consistent number of verses
        verse_count = (verse_count + 1) % verse_max
        # This is kept track of to ensure a partial collection at the end is accounted for
        verse_remaining -= 1
        # Each part consists of either a set number of verses OR an approximate set of lines.
        # There might be situations where a really long verse takes up an entire slide's worth of space,
        # or the alternative where lots of verses are placed onto one slide
        if verse_count <= 0 or verse_remaining <= 0 or part.count("\n") >= newlines_max:
            verse_count = 0  # Need to reset the verse count in case it's the other conditions that matched
            part_count += 1
            pyperclip.copy(part)

            print(f"Part {part_count} - Bible verse copied to clipboard:")
            print(part)
            part = ""
            if verse_remaining > 0:
                input("Press Enter to copy the next part...")
