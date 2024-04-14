import pyodbc

class DataOfUser:
    def __init__(self):
        self.cnxn=pyodbc.connect(r'Driver=SQL Server;Server=localhost\SQLEXPRESS;Database=master;Trusted_connection=yes;')
        self.cur=self.cnxn.cursor()

    def get_user(self):
        result=[]
        query=f"SELECT * FROM Users"
        self.cur.execute(query)
        for row in self.cur.fetchall():
             user={}
             user['id']=row[0]
             user['username']=row[1]
             result.append(user)
        return result

    def create_user(self,username,password):
        query=f"INSERT INTO Users(username,password) VALUES('{username}','{password}')"
        try:
            self.cur.execute(query)
            self.cnxn.commit()
            return True
        except pyodbc.IntegrityError:
             return False
        
    def delete_user(self,id):
            query=f"DELETE FROM Users where id={id}"
            self.cur.execute(query)
            if self.cur.rowcount==0:
                return False
            else:
                self.cnxn.commit()
                return True

    def Verify_user(self,username,password):
         query=f"SELECT * FROM Users WHERE username='{username}' and password='{password}'"
         self.cur.execute(query)
         result=self.cur.fetchone()
         if result is not None:
              return result[0]
         return False
