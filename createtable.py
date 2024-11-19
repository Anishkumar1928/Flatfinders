import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    "postgresql://flatfinders_owner:lc0okti2nVdW@ep-jolly-rain-a1vbvt19.ap-southeast-1.aws.neon.tech/flatfinders?sslmode=require"
)
cursor = conn.cursor()

# Create User Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS "user" (
        user_id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        mobile BIGINT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        gender TEXT CHECK (gender IN ('M', 'F', 'T')) NOT NULL,
        role TEXT CHECK (role IN ('Owner', 'Renter')) NOT NULL
    );
""")

# Create Property Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS property (
        property_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        property_type TEXT CHECK (property_type IN ('Flat', 'Room')) NOT NULL,
        rent REAL NOT NULL,
        address TEXT NOT NULL,
        Pin_Code INTEGER NOT NULL,
        dimensions REAL NOT NULL,
        accommodation TEXT CHECK (accommodation IN 
            ('OnlyGirls', 'OnlyBoys', 'OnlyFamily', 'FamilyAndGirls', 'Both')),
        is_occupancy BOOLEAN NOT NULL,
        is_parking BOOLEAN NOT NULL,
        is_kitchen BOOLEAN NOT NULL,
        FOREIGN KEY (user_id) REFERENCES "user" (user_id) ON DELETE CASCADE
    );
""")

# Create Photo Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS photo (
        photo_id SERIAL PRIMARY KEY,
        photo_type TEXT CHECK (photo_type IN ('Profile_pic', 'Property_pic')) NOT NULL,
        photo_id_link TEXT NOT NULL,
        user_id INTEGER,
        property_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES "user" (user_id) ON DELETE CASCADE,
        FOREIGN KEY (property_id) REFERENCES property (property_id) ON DELETE CASCADE,
        CHECK (user_id IS NOT NULL OR property_id IS NOT NULL)
    );
""")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Tables created successfully!")
