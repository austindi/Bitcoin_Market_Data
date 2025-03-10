import os 
from secure_database import * 

if __name__ == '__main__': 
   folder = 'database' 
   if not os.path.isdir( folder ): 
      os.mkdir( folder ) 
   create_user_database()
   username = input( 'Enter a Username: ' ) 
   password = input( 'Enter a Password: ' ) 

   create_user(username, password )
   if verify_user(username, password):
       print("🔓 Access granted!")
   else:
       print("🔒 Access denied!")
