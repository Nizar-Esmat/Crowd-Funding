import re
import json as js
from datetime import datetime

def savaToFile(data, fileName):
    try:
        with open(fileName, 'w') as file:
            js.dump(data, file, indent=4)
        print(f"Data successfully saved to {fileName}.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")

def loadFromFile(fileName):
    try:
        with open(fileName, 'r') as file:
            data = js.load(file)
        return data
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")
        return []

def CreateAccount():
    name_pattern = r"^[A-Za-z]+$"
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    number_pattern = r"^01\d{9}$"
    password_pattern = r'^(?=.*[A-Z])(?=.*[a-z]).{8,}$'

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    valid_fname = re.match(name_pattern, first_name)
    valid_lname = re.match(name_pattern, last_name)
    if not valid_fname or not valid_lname:
        return "Error: Invalid name. Names should contain only letters."

    email = input("Enter your email: ")
    valid_email = re.match(email_pattern, email)
    if not valid_email:
        return "Error: Invalid email format."

    password = input("Enter your password: ")
    valid_password = re.match(password_pattern, password)
    if not valid_password:
        return "Error: Password must contain at least one uppercase letter, one lowercase letter, and be at least 8 characters long."

    confirm_password = input("Enter the password confirmation: ")
    if password != confirm_password:
        return "Error: Passwords do not match."

    mobile = input("Enter your mobile number: ")
    valid_number = re.match(number_pattern, mobile)
    if not valid_number:
        return "Error: Invalid mobile number. It should start with '01' and be 11 digits long."

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "mobile": mobile
    }

    return user

def login(users):
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    for user in users:
        if user["email"] == email and user["password"] == password:
            print("Login successful!")
            return user

    print("User not found or incorrect credentials.")
    return None

def createProject(user):
    title = input("Enter your project title: ")
    details = input("Enter project details: ")
    target = float(input("Enter the target (EGP): "))

    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None

    if start_date > end_date:
        print("Error: Start date must be before end date.")
        return None

    project = {
        "title": title,
        "details": details,
        "target": target,
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "owner": user["email"]
    }
    print("Project created successfully!")
    return project

def view_project(projects):
    if len(projects) == 0:
        print("No projects found.")
        return
    else:
        for project in projects:
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Target: {project['target']} EGP")
            print(f"Start Date: {project['start_date']}")
            print(f"End Date: {project['end_date']}")
            print(f"Owner: {project['owner']}")
            print("-" * 20)

def editProject(projects, user):
    title = input("Enter the title of the project you want to edit: ")
    for project in projects:
        if project["title"] == title and project["owner"] == user["email"]:
            print("Editing project:", title)
            newDetails = input("Enter new details: ")
            newTarget = float(input("Enter new target (EGP): "))
            if len(newDetails) == 0:
                project["details"] = project["details"]
            else:
                project["details"] = newDetails
            if newTarget == 0:
                project["target"] = project["target"]
            else:
                project["target"] = newTarget
            print("Project updated successfully!")
            return
    print("Project not found or you do not have permission to edit it.")

def Delete(projects, user):
    title = input("Enter the title of the project you want to delete: ")
    for project in projects:
        if project["title"] == title and project["owner"] == user["email"]:
            projects.remove(project)
            print("Project deleted successfully!")
            return
    print("Project not found or you do not have permission to delete it.")

def search_by_date(projects):
    date = input("Enter the date to search for projects (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    found_projects = []
    for project in projects:
        project_start_date = datetime.strptime(project["start_date"], "%Y-%m-%d")
        project_end_date = datetime.strptime(project["end_date"], "%Y-%m-%d")
        if project_start_date <= date <= project_end_date:
            found_projects.append(project)

    if found_projects:
        print(f"Projects found for {date.strftime('%Y-%m-%d')}:")
        view_project(found_projects)
    else:
        print("No projects found for the given date.")

def main():
    users = loadFromFile("users.json")
    projects = loadFromFile("projects.json")

    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            user = CreateAccount()
            if isinstance(user, dict):  # Check if user is successfully created
                users.append(user)
                savaToFile(users, "users.json")
                print("User registered successfully!")
        elif choice == "2":
            user = login(users)
            if user:
                while True:
                    print("\n1. Create Project\n2. View Projects\n3. Edit Project\n4. Delete Project\n5. Search Projects by Date\n6. Logout")
                    option = input("Choose an option: ")
                    if option == "1":
                        project = createProject(user)
                        if project:
                            projects.append(project)
                            savaToFile(projects, "projects.json")
                    elif option == "2":
                        view_project(projects)
                    elif option == "3":
                        editProject(projects, user)
                        savaToFile(projects, "projects.json")
                    elif option == "4":
                        Delete(projects, user)
                        savaToFile(projects, "projects.json")
                    elif option == "5":
                        search_by_date(projects)
                    elif option == "6":
                        break
                    else:
                        print("Invalid option.")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()