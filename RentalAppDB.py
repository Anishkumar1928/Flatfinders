import psycopg2


class RentalAppDB:
    def __init__(self):
        # PostgreSQL connection pool initialization
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,  # Min and Max connection pool size
            user="flatfinders_owner",
            password="lc0okti2nVdW",
            host="ep-jolly-rain-a1vbvt19.ap-southeast-1.aws.neon.tech",
            database="flatfinders",
            sslmode="require"
        )

    # Get connection from the pool
    def get_connection(self):
        return self.connection_pool.getconn()

    # Release connection back to the pool
    def release_connection(self, conn):
        self.connection_pool.putconn(conn)

    # User CRUD Operations
    def create_user(self, name, mobile, email, password, gender, role):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO "user" (name, mobile, email, password, gender, role)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, (name, mobile, email, password, gender, role))
                conn.commit()
        finally:
            self.release_connection(conn)

    def read_user(self, mobile):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM "user" WHERE "mobile" = %s;', (mobile,))
                return cursor.fetchone()
        finally:
            self.release_connection(conn)

    def update_user(self, user_id, changes):
        conn = self.get_connection()
        try:
            query = 'UPDATE "user" SET '
            params = []

            fields_to_update = [f"{field} = %s" for field, value in changes.items() if value is not None]
            params.extend([value for field, value in changes.items() if value is not None])

            if fields_to_update:
                query += ", ".join(fields_to_update) + " WHERE user_id = %s;"
                params.append(user_id)
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
            else:
                print("No fields to update.")
        finally:
            self.release_connection(conn)

    def delete_user(self, mobile):
        conn = self.get_connection()
        try:
            if self.read_user(mobile):
                user = self.read_user(mobile)
                with conn.cursor() as cursor:
                    cursor.execute('DELETE FROM "user" WHERE "mobile" = %s;', (mobile,))
                    conn.commit()
                return f'{user[1]} deleted'
            else:
                return 'User not found'
        finally:
            self.release_connection(conn)

    # Property CRUD Operations
    def create_property(self, user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO property (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (user_id, property_type, rent, address, pin_code, dimensions, accommodation, is_occupancy, is_parking, is_kitchen))
                conn.commit()
        finally:
            self.release_connection(conn)

    def read_property(self, property_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM property WHERE property_id = %s;", (property_id,))
                return cursor.fetchone()
        finally:
            self.release_connection(conn)

    def update_property(self, property_id, **kwargs):
        conn = self.get_connection()
        try:
            query = "UPDATE property SET "
            params = []

            for field, value in kwargs.items():
                if value is not None:
                    query += f"{field} = %s, "
                    params.append(value)

            query = query.rstrip(', ') + " WHERE property_id = %s;"
            params.append(property_id)

            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
        finally:
            self.release_connection(conn)

    def delete_property(self, property_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM property WHERE property_id = %s;", (property_id,))
                conn.commit()
        finally:
            self.release_connection(conn)

    # User Profile Picture CRUD Operations
    def create_user_profile_pic(self, user_id, photo_id_link):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO photo (photo_type, photo_id_link, user_id)
                    VALUES ('Profile_pic', %s, %s);
                """, (photo_id_link, user_id))
                conn.commit()
        finally:
            self.release_connection(conn)

    def read_user_profile_pic(self, user_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM photo WHERE user_id = %s AND photo_type = 'Profile_pic';", (user_id,))
                return cursor.fetchone()
        finally:
            self.release_connection(conn)

    def update_user_profile_pic(self, user_id, photo_id_link):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE photo SET photo_id_link = %s
                    WHERE user_id = %s AND photo_type = 'Profile_pic';
                """, (photo_id_link, user_id))
                conn.commit()
        finally:
            self.release_connection(conn)

    def delete_user_profile_pic(self, user_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM photo WHERE user_id = %s AND photo_type = 'Profile_pic';", (user_id,))
                conn.commit()
        finally:
            self.release_connection(conn)

    # Property Picture CRUD Operations
    def create_property_picture(self, property_id, photo_id_link):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO photo (photo_type, photo_id_link, property_id)
                    VALUES ('Property_pic', %s, %s);
                """, (photo_id_link, property_id))
                conn.commit()
        finally:
            self.release_connection(conn)

    def read_property_picture(self, property_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM photo WHERE property_id = %s AND photo_type = 'Property_pic';", (property_id,))
                return cursor.fetchone()
        finally:
            self.release_connection(conn)

    def update_property_picture(self, property_id, photo_id_link):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE photo SET photo_id_link = %s
                    WHERE property_id = %s AND photo_type = 'Property_pic';
                """, (photo_id_link, property_id))
                conn.commit()
        finally:
            self.release_connection(conn)

    def delete_property_picture(self, property_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM photo WHERE property_id = %s AND photo_type = 'Property_pic';", (property_id,))
                conn.commit()
        finally:
            self.release_connection(conn)

# Usage Example
# if __name__ == "__main__":
#     db = RentalAppDB()

#     # Test User CRUD Operations
#     db.create_user("Alice", "9876543210", "alice@example.com", "securepass", "F", "Renter")
#     user = db.read_user("9876543210")
#     print("Created User:", user)

#     db.update_user(user[0], {"email": "alice.new@example.com", "password": "newsecurepass"})
#     updated_user = db.read_user("9876543210")
#     print("Updated User:", updated_user)

#     print(db.delete_user("9876543210"))
