import time

from psycopg2 import sql


def upsert_json(json_data, table_name, unique_columns):
    # If unique_columns is a string, convert it into a list
    if isinstance(unique_columns, str):
        unique_columns = [unique_columns]

    value_list = []
    query_list = []

    for record in json_data:
        columns = record.keys()
        values = [record[column] for column in columns]

        # Building the INSERT INTO part of the query
        insert_query = sql.SQL(
            "INSERT INTO {table} ({fields}) VALUES ({values})"
        ).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
            values=sql.SQL(", ").join(sql.Placeholder() * len(values)),
        )

        # Building the ON CONFLICT part of the query for composite key
        conflict_target = sql.SQL(", ").join(map(sql.Identifier, unique_columns))
        update_query = sql.SQL("ON CONFLICT ({unique}) DO UPDATE SET ").format(
            unique=conflict_target
        )
        update_query += sql.SQL(", ").join(
            [
                sql.Identifier(key) + sql.SQL(" = EXCLUDED.") + sql.Identifier(key)
                for key in columns
                if key not in unique_columns
            ]
        )

        query_list.append(insert_query + update_query)

        # values * 2 because each placeholder needs a value in both INSERT and UPDATE parts
        value_list.append(values)

    return (query_list, value_list)


def insert_json(json_data, table_name):
    value_list = []
    query_list = []

    for record in json_data:
        columns = record.keys()
        values = [record[column] for column in columns]

        # Building the INSERT INTO part of the query
        insert_query = sql.SQL(
            "INSERT INTO {table} ({fields}) VALUES ({values})"
        ).format(
            table=sql.Identifier(table_name),
            fields=sql.SQL(", ").join(map(sql.Identifier, columns)),
            values=sql.SQL(", ").join(sql.Placeholder() * len(values)),
        )

        query_list.append(insert_query)

        value_list.append(values)

    return (query_list, value_list)


def commit_sql(cursor, sql_call, sleep_time=0.05):
    try:
        for query, value in zip(sql_call[0], sql_call[1]):
            cursor.execute(query, value)
            time.sleep(sleep_time)  # Sleep for specified time
        return True  # Indicate success
    except Exception as e:
        print(f"Error executing query: {e}")
        return False  # Indicate failure
