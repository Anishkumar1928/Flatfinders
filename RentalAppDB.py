import psycopg2


class RentalAppDB:
    def __init__(self):
        # PostgreSQL connection string
        self.connection_string = "postgresql://flatfinders_owner:lc0okti2nVdW@ep-jolly-rain-a1vbvt19.ap-southeast-1.aws.neon.tech/flatfinders?sslmode=require"
        self.connection = psycopg2.connect(self.connection_string)
       

    # User CRUD Operations
    def create_user(self, name, mobile, email, password, gender, role):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO "user" (name, mobile, email, password, gender, role)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (name, mobile, email, password, gender, role))
            self.connection.commit()

    def read_user(self, mobile):
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM "user" WHERE "mobile" = %s;', (mobile,))
            return cursor.fetchone()

    def update_user(self, user_id, changes):
        with self.connection.cursor() as cursor:
            query = 'UPDATE "user" SET '
            params = []

            # Prepare the fields to update based on the provided changes
            fields_to_update = []
            for field, value in changes.items():
                if value is not None:  # Only include fields that are not None
                    fields_to_update.append(f"{field} = %s")
                    params.append(value)

            # Check if there are fields to update
            if fields_to_update:
                query += ", ".join(fields_to_update)
                query += " WHERE user_id = %s;"
                params.append(user_id)
                cursor.execute(query, params)
                self.connection.commit()
            else:
                print("No fields to update.")

    def delete_user(self, mobile):
        if self.read_user(mobile):
            user =self.read_user(mobile)
            with self.connection.cursor() as cursor:
                cursor.execute('DELETE FROM "user" WHERE "mobile" = %s;', (mobile,))
                self.connection.commit()
            return f'{user[1]} deleted'
        else:
            return 'user not found'

    # Property CRUD Operations
    def create_property(self, user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO property (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen))
            self.connection.commit()

    def read_property(self, property_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM property WHERE property_id = %s;", (property_id,))
            return cursor.fetchone()

    def update_property(self, property_id, user_id=None, property_type=None, rent=None, address=None, pin_code=None, dimensions=None, accommodation=None, is_occupancy=None, is_parking=None, is_kitchen=None):
        with self.connection.cursor() as cursor:
            query = "UPDATE property SET "
            params = []
            if user_id:
                query += "user_id = %s, "
                params.append(user_id)
            if property_type:
                query += "property_type = %s, "
                params.append(property_type)
            if rent:
                query += "rent = %s, "
                params.append(rent)
            if address:
                query += "address = %s, "
                params.append(address)
            if pin_code:
                query += "pin_code = %s, "
                params.append(pin_code)
            if dimensions:
                query += "dimensions = %s, "
                params.append(dimensions)
            if accommodation:
                query += "accommodation = %s, "
                params.append(accommodation)
            if is_occupancy is not None:
                query += "is_occupancy = %s, "
                params.append(is_occupancy)
            if is_parking is not None:
                query += "is_parking = %s, "
                params.append(is_parking)
            if is_kitchen is not None:
                query += "is_kitchen = %s, "
                params.append(is_kitchen)

            query = query.rstrip(', ') + " WHERE property_id = %s;"
            params.append(property_id)
            cursor.execute(query, params)
            self.connection.commit()

    def delete_property(self, property_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM property WHERE property_id = %s;", (property_id,))
            self.connection.commit()

    # User Profile Picture CRUD Operations
    def create_user_profile_pic(self, user_id, photo_id_link):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO photo (photo_type, photo_id_link, user_id)
                    VALUES ('Profile_pic', %s, %s);
                """, (photo_id_link, user_id))
                self.connection.commit()
                print(f"Profile picture for user {user_id} added successfully.")
        except psycopg2.Error as e:
            print(f"Error inserting profile picture for user {user_id}: {str(e)}")

    def read_user_profile_pic(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM photo WHERE user_id = %s AND photo_type = 'Profile_pic';", (user_id,))
            return cursor.fetchone()

    def update_user_profile_pic(self, user_id, photo_id_link):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE photo SET photo_id_link = %s
                WHERE user_id = %s AND photo_type = 'Profile_pic';
            """, (photo_id_link, user_id))
            self.connection.commit()

    def delete_user_profile_pic(self, user_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM photo WHERE user_id = %s AND photo_type = 'Profile_pic';", (user_id,))
            self.connection.commit()

    # Property Picture CRUD Operations
    def create_property_picture(self, property_id, photo_id_link):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO photo (photo_type, photo_id_link, property_id)
                VALUES ('Property_pic', %s, %s);
            """, (photo_id_link, property_id))
            self.connection.commit()

    def read_property_picture(self, property_id):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM photo WHERE property_id = %s AND photo_type = 'Property_pic';", (property_id,))
            return cursor.fetchone()

    def update_property_picture(self, property_id, photo_id_link):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                UPDATE photo SET photo_id_link = %s
                WHERE property_id = %s AND photo_type = 'Property_pic';
            """, (photo_id_link, property_id))
            self.connection.commit()

    def delete_property_picture(self, property_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM photo WHERE property_id = %s AND photo_type = 'Property_pic';", (property_id,))
            self.connection.commit()

# if __name__ == "__main__":
#     db = RentalAppDB()

#     # Test User CRUD Operations
#     # print("\n--- Testing User CRUD Operations ---")
#     db.create_user("Alice", "9876543210", "alice@example.com", "securepass", "F", "Renter")
#     user = db.read_user("9876543210")
#     print("Created User:", user)

#     # db.update_user(user[0], {"email": "alice.new@example.com", "password": "newsecurepass"})
#     # updated_user = db.read_user("9876543210")
#     # print("Updated User:", updated_user)

    
#     print(db.delete_user("9876543210"))

    # # Test Property CRUD Operations
    # print("\n--- Testing Property CRUD Operations ---")
    # db.create_property(user[0], "Flat", 1500, "45 Elm St", 987654, "1000", "OnlyFamily", True, False, True)
    # property_info = db.read_property(1)  # Assuming property ID starts at 1
    # print("Created Property:", property_info)

    # db.update_property(property_info[0], rent=1700, address="50 Maple St")
    # updated_property = db.read_property(property_info[0])
    # print("Updated Property:", updated_property)

    # db.delete_property(property_info[0])
    # print("Property Deleted:", db.read_property(property_info[0]))

    # # Test User Profile Picture CRUD Operations
    # print("\n--- Testing User Profile Picture CRUD Operations ---")
    # db.create_user("Bob", "8765432109", "bob@example.com", "mypassword", "M", "Owner")
    # bob = db.read_user("8765432109")
    # db.create_user_profile_pic(bob[0], "bob_profile_pic_url")
    # profile_pic = db.read_user_profile_pic(bob[0])
    # print("Created User Profile Picture:", profile_pic)

    # db.update_user_profile_pic(bob[0], "bob_new_profile_pic_url")
    # updated_profile_pic = db.read_user_profile_pic(bob[0])
    # print("Updated User Profile Picture:", updated_profile_pic)

    # db.delete_user_profile_pic(bob[0])
    # print("Profile Picture Deleted:", db.read_user_profile_pic(bob[0]))

    # Test Property Picture CRUD Operations
    # print("\n--- Testing Property Picture CRUD Operations ---")
    # db.create_property(bob[0], "Room", 2000, "75 Oak St", 54321, "800", "OnlyFamily", False, True, True)
    # property_info = db.read_property(2)  # Assuming next property ID is 2
    # db.create_property_picture(property_info[0], "property_picture_url")
    # property_pic = db.read_property_picture(property_info[0])
    # print("Created Property Picture:", property_pic)

    # db.update_property_picture(property_info[0], "property_new_picture_url")
    # updated_property_pic = db.read_property_picture(property_info[0])
    # print("Updated Property Picture:", updated_property_pic)

    # db.delete_property_picture(property_info[0])
    # print("Property Picture Deleted:", db.read_property_picture(property_info[0]))

    # print(db.delete_user("8765432109"))

