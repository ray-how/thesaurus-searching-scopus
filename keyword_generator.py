import logging
import sys
import pyperclip


from data_struct import Data_struct




def run():
    logging.basicConfig(level=logging.INFO)

    clipboard_text = pyperclip.paste()

    clipboard_text = clipboard_text.replace("\r", "")
    clipboard_text = clipboard_text.replace("\t ", "\t")  # This action is needed for tables copied from Microsoft Word

    with open("_clipboard_data.txt", "w") as f:
        f.write(clipboard_text)

    current_data = Data_struct()

    with open("_clipboard_data.txt", "r") as f:
        current_data.process_first_line(f.readline())

        counter = 0
        for each_line_after_first_line in f:
            current_data.read_keywords(each_line_after_first_line, counter)
            counter += 1

    current_data.reorganize()
    current_data.write_all_keywords()

    print("Copied to clipboard:")
    print(current_data.get_text())
    pyperclip.copy(current_data.get_text())


if __name__ == "__main__":
    sys.exit(run())
