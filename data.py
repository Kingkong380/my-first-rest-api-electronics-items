# item={
#     "b1195ab912c54be69959bb15fcbebff5":{
#                                         "name":"Smartphone",
#                                         "price": 599.99
#                                         },
#     "e1a85e4dc8fe42eba6a8bc0b86ebb080":{
#                                         "name":"LED TV",
#                                         "price": 799.99
#                                         },
#     "638371fc38d84b3f82ff7f5b561f5d86":{
#                                         "name":"Wireless Headphone",
#                                         "price": 299.99
#                                         },
#     "d8a8342ca64840b2ba3b3667fa4071ae":{
#                                         "name":"Smart Watch",
#                                         "price": 349.99
#                                         },
# }

import pyodbc

class Products:
    def __init__(self):
        self.cnxn=pyodbc.connect(r'Driver=SQL Server;Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=yes;')
        self.cur=self.cnxn.cursor()

    def get_items(self):
        result=[]
        query="SELECT * FROM Products"
        self.cur.execute(query)
        for row in self.cur.fetchall():
            items={}
            items['ProductID']= row[0]
            items['Name']= row[1]
            items['Brand']= row[2]
            items['Category']= row[3]
            items['Price']= row[4]
            items['Quantity']= row[5]
            result.append(items)
        return result
    
    def get_item(self,id):
        query=f"SELECT * FROM Products WHERE ProductID={id}"
        self.cur.execute(query)
        for row in self.cur.fetchall():
            items={}
            items['ProductID']= row[0]
            items['Name']= row[1]
            items['Brand']= row[2]
            items['Category']= row[3]
            items['Price']= row[4]
            items['Quantity']= row[5]
        return [items]

    def post_item(self,body):
        query=f"INSERT INTO Products (Name,Brand,Category,Price,Quantity) VALUES ('{body['Name']}','{body['Brand']}','{body['Category']}',{body['Price']},{body['Quantity']})"
        self.cur.execute(query)
        self.cnxn.commit()

    def put_item(self,id,body):
        query=f"UPDATE Products set Name='{body['Name']}',Brand='{body['Brand']}',Category='{body['Category']}',Price={body['Price']},Quantity={body['Quantity']} WHERE ProductID={id}"
        self.cur.execute(query)
        if self.cur.rowcount==0:
            return False
        else:
            self.cnxn.commit()
            return True
    def delete_item(self,ProductID):
        query=f"DELETE FROM Products WHERE ProductID={ProductID}"
        self.cur.execute(query)
        if self.cur.rowcount==0:
            return False
        else:
            self.cnxn.commit()
            return True
# db=Products()
# db.post_item()