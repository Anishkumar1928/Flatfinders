import psycopg2
from time import time
import os


class RentalAppDB:
    def __init__(self):
        # PostgreSQL connection string
        self.connection_string = os.getenv("POSTGRESQL_DATABASE_URL")
        self.connection = psycopg2.connect(self.connection_string)
   
    # User CRUD Operations
    def create_user(self, name, mobile, email, password, gender, role):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "user" (name, mobile, email, password, gender, role)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (name, mobile, email, password, gender, role))
                self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error creating user: {e}")
            self.connection.rollback()

    def read_user(self, userid):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM "user" WHERE "user_id" = %s;', (userid,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error reading user: {e}")
            self.connection.rollback()
            return None
        
    def read_user_mobile(self, mobile):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM "user" WHERE "mobile" = %s;', (mobile,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error reading user: {e}")
            self.connection.rollback()
            return None
        
    def read_user_email(self, email):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT * FROM "user" WHERE "email" = %s;', (email,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error reading user: {e}")
            self.connection.rollback()
            return None

    def update_user(self, user_id, changes):
        try:
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
        except psycopg2.Error as e:
            print(f"Error updating user: {e}")
            self.connection.rollback()

    def update_user_email(self, email, changes):
        try:
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
                    query += " WHERE email = %s;"
                    params.append(email)
                    cursor.execute(query, params)
                    self.connection.commit()
                else:
                    print("No fields to update.")
        except psycopg2.Error as e:
            print(f"Error updating user: {e}")
            self.connection.rollback()



    def delete_user(self, mobile):
        try:
            user = self.read_user(mobile)
            if user:
                with self.connection.cursor() as cursor:
                    cursor.execute('DELETE FROM "user" WHERE "mobile" = %s;', (mobile,))
                    self.connection.commit()
                return f'{user[1]} deleted'
            else:
                return 'User not found'
        except psycopg2.Error as e:
            print(f"Error deleting user: {e}")
            self.connection.rollback()
            return 'Error deleting user'

    # Property CRUD Operations
    def create_property(self, user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO property (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING property_id;
                """, (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen))
                
                # Fetch the inserted property_id
                property_id = cursor.fetchone()[0]
                self.connection.commit()
                return property_id
        except psycopg2.Error as e:
            print(f"Error creating property: {e}")
            self.connection.rollback()
            return None


    def read_property(self, property_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM property WHERE property_id = %s;", (property_id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error reading property: {e}")
            self.connection.rollback()
            return None
        
    def read_property_pincode(self, pincode):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(" select * from property where pin_code = %s;", (pincode,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error reading property: {e}")
            self.connection.rollback()
            return None
        
    def read_property_by_id(self, userid):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(" select * from property where user_id = %s;", (userid,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error reading property: {e}")
            self.connection.rollback()
            return None

    def update_property(self, property_id, user_id=None, property_type=None, rent=None, address=None, pin_code=None, dimensions=None, accommodation=None, is_occupancy=None, is_parking=None, is_kitchen=None):
        try:
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
        except psycopg2.Error as e:
            print(f"Error updating property: {e}")
            self.connection.rollback()

    def delete_property(self, property_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM property WHERE property_id = %s;", (property_id,))
                self.connection.commit()
                return "property deleted"
        except psycopg2.Error as e:
            print(f"Error deleting property: {e}")
            self.connection.rollback()
            return f"Error deleting property: {e}"

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
            print(f"Error inserting profile picture for user {user_id}: {e}")
            self.connection.rollback()

    def read_user_profile_pic(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM photo WHERE user_id = %s AND photo_type = 'Profile_pic';", (user_id,))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error reading profile picture for user {user_id}: {e}")
            self.connection.rollback()
            return None

    def update_user_profile_pic(self, user_id, photo_id_link):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE photo SET photo_id_link = %s
                    WHERE user_id = %s AND photo_type = 'Profile_pic';
                """, (photo_id_link, user_id))
                self.connection.commit()
                print("Profile updated successfully")
        except psycopg2.Error as e:
            print(f"Error updating profile picture for user {user_id}: {e}")
            self.connection.rollback()

    def delete_user_profile_pic(self, user_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM photo WHERE user_id = %s AND photo_type = 'Profile_pic';", (user_id,))
                self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error deleting profile picture for user {user_id}: {e}")
            self.connection.rollback()

    # Property Picture CRUD Operations
    def create_property_picture(self, property_id, photo_id_link):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO photo (photo_type, photo_id_link, property_id)
                    VALUES ('Property_pic', %s, %s);
                """, (photo_id_link, property_id))
                self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error inserting property picture for property {property_id}: {e}")
            self.connection.rollback()

    def read_property_picture(self, property_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT * FROM photo WHERE property_id = %s AND photo_type = 'Property_pic';", (property_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error reading property picture for property {property_id}: {e}")
            self.connection.rollback()
            return None

    def update_property_picture(self, property_id, photo_id_link):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE photo SET photo_id_link = %s
                    WHERE property_id = %s AND photo_type = 'Property_pic';
                """, (photo_id_link, property_id))
                self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error updating property picture for property {property_id}: {e}")
            self.connection.rollback()

    def delete_property_picture(self, property_id):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM photo WHERE property_id = %s AND photo_type = 'Property_pic';", (property_id,))
                self.connection.commit()
        except psycopg2.Error as e:
            print(f"Error deleting property picture for property {property_id}: {e}")
            self.connection.rollback()

    def close(self):
        self.connection.close()




