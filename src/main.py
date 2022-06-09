from sys import argv
from typing import Generator


class Interpreter:
    def __init__(self, file_data) -> None:
        self.file_data = file_data
        self.valid_types = ["SHORT", "INT", "LONG", "TEXT", "DATE"]  # TODO: Więcej typów być musi bo projekt udusi
        self.data = None

    '''
        This function generates a dictionary of strings based on input from the file provided to the class instance.
        It does so by splitting the text by "!", which signals new table, then puts everything else in proper index.
    '''

    def format_data(self) -> dict[str]:
        data_dict = {}
        cur_index = None

        for line in self.file_data:
            if line.isspace() or len(line) == 0:
                continue

            if "!" in line:
                new_line = line.replace("!", "").strip().split(" ")
                new_line = "_".join(new_line)

                cur_index = new_line
                data_dict[cur_index] = []
            else:
                data_dict[cur_index].append(line)

        self.data = data_dict
        return data_dict

    '''
        The validate_types function simply checks if the types are valid or not.
    '''

    def validate_types(self, data=None) -> None:
        if not data:
            data = self.data

        for table, attrib_list in data.items():
            for attrib in attrib_list:
                if attrib.split(" ")[1] not in self.valid_types:
                    raise SyntaxError(f'{attrib_list[0]} is not a valid type.')

    '''
       I have no idea how to describe this one. It just creates a string which is a valid SQL query and fills it in with
       the data from the very first function. 
    '''

    def to_sql(self, data=None) -> Generator[str]:
        if not data:
            data = self.data

        for table, attrib_list in data.items():
            sql_string = f'CREATE TABLE `{table}` (\n'

            for attrib in attrib_list:
                sql_string += attrib + ",\n"

            pos = sql_string.rfind(',')

            sql_string = sql_string[:pos] + "" + sql_string[pos + 1:]

            sql_string += ");"

            yield sql_string


def main() -> None:
    file_name = argv[1]

    with open(file_name) as f:
        file_data = [line.strip() for line in f.readlines()]

    interpreter = Interpreter(file_data)

    formatted_data = interpreter.format_data()
    interpreter.validate_types(formatted_data)

    print("\n\n".join(list(interpreter.to_sql(formatted_data))))


if __name__ == '__main__':
    main()
