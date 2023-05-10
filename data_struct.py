import logging


class Data_struct:
    def __init__(self):
        self._in_data = dict()
        self._organized_data = list()
        self._output_string = ""

    def process_first_line(self, line):
        sp_line = self.split_a_line(line.upper())
        self._in_data["HEAD"] = sp_line

    def read_keywords(self, line, line_count):
        sp_line = self.split_a_line(line)
        self.append_line_to_property(sp_line, line_count)

    @staticmethod
    def split_a_line(line):
        line = line.replace("\n", "")
        sp_line = line.split("\t")
        return sp_line

    def append_line_to_property(self, splited_line, property_key):

        self._in_data[property_key] = []

        for word_comb in splited_line:

            # empty keywords will not be deleted now. Otherwise the line contents will be distorted
            if word_comb == "":
                self._in_data[property_key].append("")
                continue

            # connect the combined keywords with "AND". e.g. "powder bed" -> "(powder AND bed)"
            word_list = word_comb.split()
            if len(word_list) > 1:
                new_words = "( " + word_list[0]
                inside_of_quotation_marks = False
                for i in range(len(word_list) - 1):

                    # Do not add "AND" operator inside of a pair of quotation marks
                    if word_list[i].startswith("\""):
                        inside_of_quotation_marks = True
                    if word_list[i].endswith("\""):
                        inside_of_quotation_marks = False

                    # Do not add "AND" operator after "NOT" operator.
                    if word_list[i].upper() != "NOT" and not inside_of_quotation_marks:
                        new_words = new_words + " AND"
                    new_words = new_words + " " + word_list[i + 1]
                new_words = new_words + " )"
            else:
                new_words = word_list[0]

            self._in_data[property_key].append(new_words)

    def get_table_dimensions_and_check(self):
        length = len(self._in_data["HEAD"])
        for each_key in self._in_data.keys():
            if length != len(self._in_data[each_key]):
                raise ValueError(
                    f"The input table has only {len(self._in_data[each_key])} rows in column {int(each_key) + 2}. The row number in the first column is {length}")

        return length, len(self._in_data)


    def reorganize(self):
        amount_table_row, amount_table_column = self.get_table_dimensions_and_check()

        for nr_row in range(amount_table_row):
            self._organized_data.append([])
            for each_key in self._in_data.keys():
                self._organized_data[nr_row].append(self._in_data[each_key][nr_row])

        # check if the complete row is a blank row and remove it
        new_organized_data = []
        for list_with_similar_keywords in self._organized_data:
            if any(element != "" for element in list_with_similar_keywords):
                new_organized_data.append(list_with_similar_keywords)
            else:
                logging.info("An empty row has been removed.")

        # check if the search scope is defined
        for list_with_similar_keywords in new_organized_data:
            if list_with_similar_keywords[0] == "":
                list_with_similar_keywords[0] = "TITLE-ABS-KEY"
                logging.info("Default search scope 'TITLE-ABS-KEY' has been added.")

        # clear all empty strings
        for i in range(len(new_organized_data)):
            new_organized_data[i] = [y for y in new_organized_data[i] if y != ""]

        self._organized_data = new_organized_data

        del self._in_data

    def add_text(self, text):
        self._output_string = self._output_string + text

    def write_all_keywords(self):
        length = len(self._organized_data)
        for i in range(length):
            self.add_text(self._organized_data[i][0] + " ")
            self.add_text("( ")
            self.write_a_group_of_similar_keywords(self._organized_data[i])
            self.add_text(") ")
            if i != length - 1:
                self.add_text("AND ")

    def write_a_group_of_similar_keywords(self, list_with_similar_keywords):
        length = len(list_with_similar_keywords)
        for i in range(length-1):

            self.add_text(list_with_similar_keywords[i+1] + " ")
            if i != length - 2:
                self.add_text("OR ")

    def get_text(self):

        return self._output_string

