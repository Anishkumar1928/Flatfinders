import psycopg2

def copy_tables():
    # Connect to the old database
    old_conn = psycopg2.connect("postgresql://flatfinders_owner:lc0okti2nVdW@ep-jolly-rain-a1vbvt19.ap-southeast-1.aws.neon.tech/flatfinders?sslmode=require")
    old_cursor = old_conn.cursor()

    # Connect to the new database
    new_conn = psycopg2.connect("postgresql://neondb_owner:pCQ17GRgseEA@ep-floral-queen-a1ho5e16.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
    new_cursor = new_conn.cursor()

    # Get the list of all tables from the old database
    old_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = old_cursor.fetchall()

    # For each table, copy the schema and data
    for table in tables:
        table_name = table[0]

        # Copy the schema (create table)
        old_cursor.execute(f"SELECT pg_get_tabledef('{table_name}');")
        create_table_query = old_cursor.fetchone()[0]
        new_cursor.execute(create_table_query)

        # Copy the data
        old_cursor.execute(f"SELECT * FROM {table_name};")
        rows = old_cursor.fetchall()
        columns = [desc[0] for desc in old_cursor.description]
        insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
        psycopg2.extras.execute_values(new_cursor, insert_query, rows)

    # Commit and close connections
    new_conn.commit()
    old_conn.close()
    new_conn.close()

copy_tables()
