import json
class User:
    def __init__(self,username,email,date):
        self.username = username
        self.email=email
        self.date = date

    def add_user(self, password, username, role='user'):
    # Load existing user data from file
        with open('users.json', 'r') as infile:
            data = json.load(infile)

        # Check if email already exists
        for user in data:
            if user['email'] == self.email:
                return 'Email already exists. Please use a different email.'

        # Create new user 
        new_user = {"email": self.email, "password": password, "username": username, "date": self.date,"role": role}
        data.append(new_user)

        #  updated data back to file
        with open('users.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

        return None  

    #logOut
    def exit_user(user_email):
        # Load existing user data from file
        with open('users.json', 'r') as infile:
            data = json.load(infile)

        # Filter out user with matching email
        new_data = [user for user in data if user['email'] != user_email]

        # Update data back to file
        with open('users.json', 'w') as outfile:
            json.dump(new_data, outfile, indent=4)


   



        



        


