import sqlite3

conn=sqlite3.connect('Flatfinders.db')
conn.execute('''
    create table room(
             property_contact
             

             );
''')

conn.close()

class db_manager:
    def __init__(self):
        self.db="Flatfinders.db"

    def get_conn(self):
        conn=sqlite3.connect(self.db)
        return conn 
    
    def signup(self, name,Mobile,email, password, gender, role):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO user (Name, Mobile, Email, Password, Gender, Role) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name,Mobile,email, password, gender, role))
        conn.commit()
        conn.close()
    def read_data(self):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user')
        rows = cursor.fetchall()  
        conn.close()
        return rows
    def update_attribute(self, mobile, attribute, value):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        
        query = f"UPDATE user SET {attribute} = ? WHERE mobile = ?"
        cursor.execute(query, (value, mobile))
        
        conn.commit()
        conn.close()


manager=db_manager()

# manager.insert_data('Aman',15162,"aman@gmail.com",'jqwhfdjh@12','M','Owner')
#print(manager.read_data())
#
# manager.update_attribute(15162, 'name', 'Aman Sharma')



