i = 0
while True:
    names = ["Azzam","Dolaif", "Ali"]
    user_input = input("Enter a name to check: ")

    if user_input in names:
        print("Name is in database")

    else:
        print(f"Name: {user_input} isn't in database.")
        break
    i+=1