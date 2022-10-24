from typing import Dict, Iterable, Optional


def get_drop_table_query(table_name: str) -> str:
    """Generate a DROP TABLE query given a table name.

    Args:
        table_name: table name.
    """
    return f"DROP TABLE IF EXISTS {table_name};"


def get_create_table_query(table_name: str, table_args: Iterable[str]) -> str:
    """Generate a CREATE TABLE query given a table name and a list of arguments.

    Args:
        table_name: table name.
        table_args: An iterable of strings including column names, data types and any
            other modfiers.
    """
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(table_args)});"


def get_simple_insert_query(table_name: str, columns: Iterable[str]) -> str:
    """Insert row into the given table.

    Args:
       table_name: table name.
       columns: Columns into which to insert row data.
    """
    return (
        f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES "
        f"({', '.join(['%s'] * len(columns))}) "
    )


def get_simple_select_query(
    table_name: str,
    columns: Iterable[str],
    where_columns: Dict[str, str],
    limit: Optional[int] = None,
) -> str:
    """Generate a simple select query.

    Args:
        columns: columns to select.
        table_name: table name to select columns from.
        where_columns: add a mandatory where clause. The keys and values in the
            dictionary will build an equality (i.e. WHERE key = value).
        limit: Optionally, add a query limit.

    """
    where_columns_str = (
        [f"{key} = {value}" for key, value in where_columns.items()]
        if where_columns
        else None
    )
    return (
        f"SELECT {', '.join(columns)} FROM {table_name} "
        f"WHERE {' AND '.join(where_columns_str)} "
        + (f"LIMIT {limit} " if limit else "")
    )
