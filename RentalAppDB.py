import sqlite3

class RentalAppDB:
    def __init__(self, db_name='rental_app.db'):
        self.db = db_name
        self.create_tables()

    def create_tables(self):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            # Create User Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    mobile INTEGER UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    gender TEXT CHECK (gender IN ('M', 'F', 'T')) NOT NULL,
                    role TEXT CHECK (role IN ('Owner', 'Renter')) NOT NULL
                );
            """)

            # Create Property Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS property (
                    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    property_type TEXT CHECK (property_type IN ('Flat', 'Room')) NOT NULL,
                    rent REAL NOT NULL,
                    address TEXT NOT NULL,
                    Pin_Code INTEGER NOT NULL,
                    dimensions REAL NOT NULL,
                    accommodation TEXT CHECK (accommodation IN 
                        ('OnlyGirls', 'OnlyBoys', 'OnlyFamily', 'FamilyAndGirls', 'Both')) NOT NULL,
                    is_occupancy BOOLEAN NOT NULL,
                    is_parking BOOLEAN NOT NULL,
                    is_kitchen BOOLEAN NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE
                );
            """)

            # Create Photo Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS photo (
                    photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    photo_type TEXT CHECK (photo_type IN ('Profile_pic', 'Property_pic')) NOT NULL,
                    photo_id_link TEXT NOT NULL,
                    user_id INTEGER,
                    property_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (property_id) REFERENCES property (property_id) ON DELETE CASCADE,
                    CHECK (user_id IS NOT NULL OR property_id IS NOT NULL)
                );
            """)

    # User CRUD Operations
    def create_user(self, name, mobile, email, password, gender, role):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user (name, mobile, email, password, gender, role)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (name, mobile, email, password, gender, role))

    def read_user(self,mobile):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user WHERE mobile = ?;", (mobile,))
            return cursor.fetchone()
        
    def update_user(self, user_id, changes):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            query = "UPDATE user SET "
            params = []
            
            # Prepare the fields to update based on the provided changes
            fields_to_update = []
            for field, value in changes.items():
                if value is not None:  # Only include fields that are not None
                    fields_to_update.append(f"{field} = ?")
                    params.append(value)

            # Check if there are fields to update
            if fields_to_update:
                query += ", ".join(fields_to_update)
                query += " WHERE user_id = ?;"
                params.append(user_id)
                cursor.execute(query, params)
            else:
                print("No fields to update.")


    def delete_user(self, user_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user WHERE user_id = ?;", (user_id,))

    # Property CRUD Operations
    def create_property(self, user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO property (user_id, property_type, rent, address, Pin_Code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen))

    def read_property(self, property_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM property WHERE property_id = ?;", (property_id,))
            return cursor.fetchone()

    def update_property(self, property_id, user_id=None, property_type=None, rent=None, address=None, pin_code=None, dimensions=None, accommodation=None, is_occupancy=None, is_parking=None, is_kitchen=None):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            query = "UPDATE property SET "
            params = []
            if user_id:
                query += "user_id = ?, "
                params.append(user_id)
            if property_type:
                query += "property_type = ?, "
                params.append(property_type)
            if rent:
                query += "rent = ?, "
                params.append(rent)
            if address:
                query += "address = ?, "
                params.append(address)
            if pin_code:
                query += "Pin_Code = ?, "
                params.append(pin_code)
            if dimensions:
                query += "dimensions = ?, "
                params.append(dimensions)
            if accommodation:
                query += "accommodation = ?, "
                params.append(accommodation)
            if is_occupancy is not None:
                query += "is_occupancy = ?, "
                params.append(is_occupancy)
            if is_parking is not None:
                query += "is_parking = ?, "
                params.append(is_parking)
            if is_kitchen is not None:
                query += "is_kitchen = ?, "
                params.append(is_kitchen)

            query = query.rstrip(', ') + " WHERE property_id = ?;"
            params.append(property_id)
            cursor.execute(query, params)

    def delete_property(self, property_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM property WHERE property_id = ?;", (property_id,))

    # User Profile Picture CRUD Operations
    def create_user_profile_pic(self, user_id, photo_id_link):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO photo (photo_type, photo_id_link, user_id)
                VALUES ('Profile_pic', ?, ?);
            """, (photo_id_link, user_id))

    def read_user_profile_pic(self, user_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM photo WHERE user_id = ? AND photo_type = 'Profile_pic';", (user_id,))
            return cursor.fetchone()

    def update_user_profile_pic(self, user_id, photo_id_link):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE photo SET photo_id_link = ?
                WHERE user_id = ? AND photo_type = 'Profile_pic';
            """, (photo_id_link, user_id))

    def delete_user_profile_pic(self, user_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM photo WHERE user_id = ? AND photo_type = 'Profile_pic';", (user_id,))

    # Property Picture CRUD Operations
    def create_property_picture(self, property_id, photo_id_link):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO photo (photo_type, photo_id_link, property_id)
                VALUES ('Property_pic', ?, ?);
            """, (photo_id_link, property_id))

    def read_property_picture(self, property_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM photo WHERE property_id = ? AND photo_type = 'Property_pic';", (property_id,))
            return cursor.fetchone()

    def update_property_picture(self, property_id, photo_id_link):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE photo SET photo_id_link = ?
                WHERE property_id = ? AND photo_type = 'Property_pic';
            """, (photo_id_link, property_id))

    def delete_property_picture(self, property_id):
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM photo WHERE property_id = ? AND photo_type = 'Property_pic';", (property_id,))

# Example Usage
if __name__ == "__main__":
    db = RentalAppDB()

    # Create a new user and add a profile picture
    db.create_user('John Doe', 1234567890, 'john@example.com', 'password123', 'M', 'Owner')
    db.create_user_profile_pic(1, 'profile_pic_url.jpg')

    # Read the user's profile picture
    profile_pic = db.read_user_profile_pic(1)
    print("User Profile Picture:", profile_pic)

    # Update the user's profile picture
    db.update_user_profile_pic(1, 'new_profile_pic_url.jpg')

    # Create and manipulate properties as needed using the CRUD functions
