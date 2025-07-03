from sys import argv


def read_lines(input_file):
    """Read lines from input file and return a list of stripped lines."""
    with open(input_file, 'r') as f_in:
        return [line.strip() for line in f_in if line.strip()]


def process_commands(database, lines):
    """Process commands from a list of lines."""
    for command in lines:
        command_parts = command.split(maxsplit=2)
        command_type = command_parts[0]

        if command_type == "CREATE_TABLE":
            parse_create(database, command_parts)
        elif command_type == "INSERT":
            parse_insert(database, command_parts)
        elif command_type == "SELECT":
            parse_select(database, command_parts)
        elif command_type == "UPDATE":
            parse_update(database, command_parts)
        elif command_type == "DELETE":
            parse_delete(database, command_parts)
        elif command_type == "COUNT":
            parse_count(database, command_parts)
        elif command_type == "JOIN":
            parse_join(database, command_parts)
        else:
            print(f"Unknown command: {command}")


def parse_create(database, command_parts):
    """Parses and executes a CREATE_TABLE command."""
    table_name = command_parts[1]
    columns = command_parts[2].split(',')
    create_table(database, table_name, columns)


def create_table(database, table_name, columns):
    """Creates a new table in the database and prints the result."""
    print("###################### CREATE #########################")
    try:
        if table_name in database:
            raise KeyError
        database[table_name] = {"columns": columns, "data": []}
        print(f"Table '{table_name}' created with columns: {columns}")
    except KeyError:
        print(f"Table '{table_name}' already exists.")
    print("#######################################################\n")


def parse_insert(database, command_parts):
    """Parses and executes an INSERT command."""
    table_name = command_parts[1]
    data = command_parts[2].split(',')
    insert(database, table_name, data)


def insert(database, table_name, data):
    """Inserts a new row into the specified table in the database."""
    print("###################### INSERT #########################")
    try:
        if table_name not in database:
            raise KeyError
        elif len(data) != len(database[table_name]["columns"]):
            raise ValueError

        database[table_name]["data"].append(data)
        print(f"Inserted into '{table_name}': {tuple(data)}\n")
        print_table(table_name, database[table_name]["columns"],
                    database[table_name]["data"])

    except KeyError:
        print(f"Table '{table_name}' not found.")
        print(f"Inserted into '{table_name}': {tuple(data)}")
    except ValueError:
        print(f"Number of columns and values do not match.\n"
              f"Inserted into '{table_name}': {tuple(data)}")
    print("#######################################################\n")


def parse_select(database, command_parts):
    """Parses and executes a SELECT command."""
    table_name = command_parts[1]
    columns_part, conditions_part = command_parts[2].split(" WHERE ")
    columns = columns_part.split(',') if columns_part != '*' else ['*']
    conditions_part = conditions_part.strip().strip("{}")
    conditions = {
        condition.split(":")[0].strip().strip('"'):
            condition.split(":")[1].strip().strip('"')
        for condition in conditions_part.split(",")
    }
    select(database, table_name, columns, conditions)


def select(database, table_name, columns, conditions):
    """Selects rows from the specified table in the database."""
    print("###################### SELECT #########################")
    try:
        if table_name not in database:
            raise KeyError
        table = database[table_name]

        if columns == ['*']:
            columns = table["columns"]  # '*' means selecting all columns.
        else:
            for column in columns:
                if column not in table["columns"]:
                    raise ValueError(f"Column {column} does not exist")

        columns_indices = {key: i for i, key in enumerate(table["columns"])}

        # Filter rows based on the given conditions.
        filtered_data = [
            row for row in table["data"]
            if all(row[columns_indices[key]] == value for key, value in
                   conditions.items() if key in table["columns"])
        ]

        # Extract the requested columns from the filtered rows.
        selected_data = [tuple(row[columns_indices[col]] for col in columns)
                         for row in filtered_data]

        print(f"Condition: {conditions}")
        if selected_data:
            print("Select result from '" + table_name + "': " + str(
                selected_data))
        else:
            print(f"Select result from '" + table_name + "': None")

    except KeyError:
        print(f"Table {table_name} not found.")
        print(f"Condition: {conditions}")
        print(f"Select result from '" + table_name + "': None")
    except ValueError as e:
        print(e)
        print(f"Condition: {conditions}")
        print(f"Select result from '" + table_name + "': None")
    print("#######################################################\n")


def parse_update(database, command_parts):
    """Parses and executes an UPDATE command."""
    table_name = command_parts[1]
    updates_part, conditions_part = command_parts[2].split(" WHERE ")
    updates_part = updates_part.strip().strip("{}")
    conditions_part = conditions_part.strip().strip("{}")
    updates = {
        an_update.split(":")[0].strip().strip('"'):
            an_update.split(":")[1].strip().strip('"')
        for an_update in updates_part.split(",")
    }
    conditions = {
        condition.split(":")[0].strip().strip('"'):
            condition.split(":")[1].strip().strip('"')
        for condition in conditions_part.split(",")
    }
    update(database, table_name, updates, conditions)


def update(database, table_name, updates, conditions):
    """Updates rows in the specified table in the database."""
    print("###################### UPDATE #########################")
    try:
        if table_name not in database:
            raise KeyError(f"Table {table_name} not found.")

        table = database[table_name]

        for column in updates.keys():
            if column not in table["columns"]:
                raise ValueError(f"Column {column} does not exist.")

        for condition_key in conditions.keys():
            if condition_key not in table["columns"]:
                raise ValueError(f"Column {condition_key} does not exist.")

        # Map column names to their respective indices for easier access
        columns_indices = {key: i for i, key in enumerate(table["columns"])}
        rows_updated = 0

        # Iterate through each row and apply updates if conditions are met
        for row in table["data"]:
            if all(row[columns_indices[condition_key]] == condition_value
                   for condition_key, condition_value in conditions.items()
                   if condition_key in columns_indices):
                for update_key, update_value in updates.items():
                    row[columns_indices[update_key]] = update_value
                rows_updated += 1

        print(f"Updated '{table_name}' with {updates} where {conditions}")
        print(f"{rows_updated} rows updated.\n")
        print_table(table_name, table["columns"], table["data"])

    except KeyError as e:
        print(f"Updated '{table_name}' with {updates} where {conditions}")
        print(e)
        print("0 rows updated.")
    except ValueError as e:
        print(f"Updated '{table_name}' with {updates} where {conditions}")
        print(e)
        print("0 rows updated.\n")
        print_table(table_name, table["columns"], table["data"])
    print("#######################################################\n")


def parse_delete(database, command_parts):
    """Parses and executes a DELETE command."""
    table_name = command_parts[1]

    if len(command_parts) == 2:
        conditions = {}
    else:
        where_clause = command_parts[2].strip()
        where_conditions = where_clause[6:].strip()
        conditions = {
            condition.split(":")[0].strip().strip('"'):
                condition.split(":")[1].strip().strip('"')
            for condition in where_conditions.strip("{}").split(",")
        }

    delete(database, table_name, conditions)


def delete(database, table_name, conditions):
    """Deletes rows from the specified table in the database."""
    print("###################### DELETE #########################")
    try:
        if table_name not in database:
            raise KeyError(f"Table {table_name} not found.")

        table = database[table_name]
        columns = table["columns"]

        for condition_key in conditions.keys():
            if condition_key not in columns:
                raise ValueError(f"Column {condition_key} does not exist.")

        if conditions == {}:
            rows_deleted = len(table["data"])
            table["data"].clear()
            print(
                f"Deleted all rows from '{table_name}'\n"
                f"{rows_deleted} rows deleted.")
        else:
            columns_indices = {key: i for i, key in enumerate(columns)}
            initial_row_count = len(table["data"])
            table["data"] = [
                row for row in table["data"]
                if not all(row[columns_indices[key]] == value for key, value in
                           conditions.items() if key in columns_indices)
            ]
            rows_deleted = initial_row_count - len(table["data"])
            print(
                f"Deleted rows from '{table_name}' where {conditions}\n"
                f"{rows_deleted} rows deleted.\n")
            print_table(table_name, columns, table["data"])

    except KeyError as e:
        print(f"Deleted from '{table_name}' where {conditions}")
        print(e)
        print("0 rows deleted.")
    except ValueError as e:
        print(f"Deleted from '{table_name}' where {conditions}")
        print(e)
        print("0 rows deleted.\n")
        print_table(table_name, columns, table["data"])
    print("#######################################################\n")


def parse_count(database, command_parts):
    """Parses and executes a COUNT command."""
    table_name = command_parts[1]

    where_clause = command_parts[2].strip()
    if where_clause.startswith("WHERE "):
        where_conditions = where_clause[6:].strip()
        if where_conditions == "*":
            conditions = {}
        else:
            conditions = {
                condition.split(":")[0].strip().strip('"'):
                    condition.split(":")[1].strip().strip('"')
                for condition in where_conditions.strip("{}").split(",")
            }
        count(database, table_name, conditions)


def count(database, table_name, conditions):
    """Counts the number of entries in the specified table in the database."""
    print("###################### COUNT #########################")
    try:
        if table_name not in database:
            raise KeyError(f"Table {table_name} not found")

        table = database[table_name]

        for condition_key in conditions.keys():
            if condition_key not in table["columns"]:
                raise ValueError(f"Column {condition_key} does not exist")

        if not conditions:
            row_count = len(table["data"])
        else:
            columns_indices = {key: i for i, key in
                               enumerate(table["columns"])}
            row_count = sum(
                1 for row in table["data"]
                if all(row[columns_indices[key]] == value for key, value in
                       conditions.items())
            )

        print(f"Count: {row_count}")
        print(f"Total number of entries in '{table_name}' is {row_count}")

    except KeyError as e:
        print(e)
        print(f"Total number of entries in '{table_name}' is 0")
    except ValueError as e:
        print(e)
        print(f"Total number of entries in '{table_name}' is 0")
    print("#######################################################\n")


def parse_join(database, command_parts):
    """Parses and executes a JOIN command."""
    table1_name, table2_name = command_parts[1].split(',')
    on_column = command_parts[2].strip()
    column = on_column[3:].strip()
    join(database, table1_name, table2_name, column)


def join(database, table1_name, table2_name, column):
    """Joins two tables in the database based on a common column."""
    print("####################### JOIN ##########################")
    try:
        table1 = database.get(table1_name)
        table2 = database.get(table2_name)

        if not table1 and not table2:
            raise KeyError(
                f"Table {table1_name} and {table2_name} do not exist")
        elif not table1:
            raise KeyError(f"Table {table1_name} does not exist")
        elif not table2:
            raise KeyError(f"Table {table2_name} does not exist")

        if column not in table1["columns"] or column not in table2["columns"]:
            raise ValueError(f"Column {column} does not exist")

        # Get the column names from both tables
        table1_columns = table1["columns"]

        # Exclude the join column from table2 to avoid duplication.
        # When I didn't do it this way, my columns were lost in the printout on
        # the school's computer. I did this as a solution.
        table2_columns = [col for col in table2["columns"] if
                          col != column]
        new_columns = table1_columns + table2_columns

        # Perform the join by matching rows based on the join column.
        joined_data = [
            {**dict(zip(table1_columns, row1)),
             **{key: row2[table2["columns"].index(key)] for key in
                table2_columns}}
            for row1 in table1["data"]
            for row2 in table2["data"]
            if dict(zip(table1_columns, row1))[column] == row2[
                table2["columns"].index(column)]
        ]

        # Convert the joined data into a list of lists for easier formatting.
        joined_data_list = [
            [row[col] for col in new_columns] for row in joined_data
        ]

        print(f"Join tables {table1_name} and {table2_name}")
        print(f"Join result ({len(joined_data_list)} rows):\n")
        print_table("Joined Table", new_columns, joined_data_list)

    except KeyError as e:
        print(f"Join tables {table1_name} and {table2_name}")
        print(e)
    except ValueError as e:
        print(f"Join tables {table1_name} and {table2_name}")
        print(e)
    print("#######################################################\n")


def print_table(table_name, columns, data):
    """Prints a table with the specified name, columns, and data."""

    # Determine the width of each column
    column_widths = [
        max(len(str(col)), *(len(str(row[i])) for row in data))
        for i, col in enumerate(columns)
    ]

    horizontal_line = "+-" + "-+-".join(
        "-" * width for width in column_widths) + "-+"

    header = "| " + " | ".join(f"{columns[i]:<{column_widths[i]}}" for i in
                               range(len(columns))) + " |"

    rows = [
        "| " + " | ".join(f"{str(row[i]):<{column_widths[i]}}" for i in
                          range(len(columns))) + " |"
        for row in data
    ]

    print(f"Table: {table_name}")
    print(horizontal_line)
    print(header)
    print(horizontal_line)
    for row in rows:
        print(row)
    print(horizontal_line)


def main():
    """Main function to process commands from a file."""
    database = {}
    input_file = argv[1]
    lines = read_lines(input_file)
    process_commands(database, lines)


if __name__ == "__main__":
    main()
