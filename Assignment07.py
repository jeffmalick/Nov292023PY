# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
# jmalick, 11/24/2023, changes to support assignment 7
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.


class Person():
    """
    Class representing a person with first and last names.
    Attributes:
        first_name (str): The person's first name.
        last_name (str): The person's last name.
    ChangeLog: (Who, When, What)
    jmalick,11.26.2023,Created Class
    """

    def __init__(self, first_name: str, last_name: str):
        """
        Initializes a person object with the specified first and last names.
        Args:
            first_name (str): The person's first name.
            last_name (str): The person's last name.
        """
        self._first_name = first_name
        self._last_name = last_name

    @property
    def first_name(self) -> str:
        """
        Gets the person's first name.
        Returns: str: The person's first name.
        """
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        """
        Sets the person's first name.
        Args: first_name (str): The person's first name.
        """
        if value.isalpha():
            self._first_name = value
        else:
            raise ValueError('first name can only contaion letters.')

    @property
    def last_name(self) -> str:
        """
        Gets the person's last name.
        Returns: str: The person's last name.
        """
        return self._last_name

    @last_name.setter
    def last_name(self, value: str):
        """
        Sets the person's last name.
        Args: last_name (str)
        """
        if value.isalpha():
            self._last_name = value
        else:
            raise ValueError('last name can only contaion letters.')

    def __str__(self):
        """
        Override __str__() method with first name, last name
        :return: str
        """
        return f"{self._first_name},{self._last_name}"

class Student(Person):
    """
    Class representing a student, inheriting from the Person class.
    Attributes:
        first_name (str): student's first name. (Inherited from Person)
        last_name (str): student's last name. (Inherited from Person)
        course_name (str): course student is registering for.
    ChangeLog: (Who, When, What)
    jmalick,11.26.2023,Created Class
    """
    _course_name: str  # holds Student object course name.
    def __init__(self, first_name: str, last_name: str, course_name: str):
        """
        Initializes the Student object with first name, last name, and course name.
        Args:
            first_name (str): The student's first name.
            last_name (str): The student's last name.
            course_name (str): The course name.
        """
        super().__init__(first_name, last_name)
        self._course_name = course_name

    @property
    def course_name(self) -> str:
        """
        Gets the person's first name.
        Returns: str: The person's first name.
        """
        return self._course_name

    @course_name.setter
    def course_name(self, value: str):
        """
        Sets course name.
        Args: course_name (str):
        """
        if value:
            self._course_name = value
        else:
            raise ValueError('Course can not be blank')

    def __str__(self):
        """
        Override __str__() method with first name, last name, course
        :return: str
        """
        return f"{self._first_name},{self._last_name},{self._course_name}"

# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    jmalick, 11.28.2023, changed to process file as list of objects
    """
    @staticmethod
    def read_data_from_file(file_name: str) -> list[Student]:
    #def read_data_from_file(file_name: str, student_data: list):
        """ This function reads data from a json file and loads it into a list of dictionary rows
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jmalick, 11.28.2023, reads data into Student object
        :param file_name: string data with name of file to read from
        :return: list of Student objects
        """
        dict_table: list[dict[str, str, str]] = []

        try:
            file = open(file_name, "r")
            dict_table = json.load(file)
            file.close()
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if file.closed == False:
                file.close()
        student_data: list[Students] = []
        for row in dict_table:
            student_data.append(Student(row['FirstName'], row['LastName'],row['CourseName']))
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """ This function writes data to a json file with data from a list of dictionary rows
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jmalick, 11.28.2023, Change to use Student object
        :param file_name: string data with name of file to write to
        :param student_data: list of objects to be writen to the file
        :return: None
        """

        try:
            file = open(file_name, "w")
            dict_table: list[dict] = []
            for row in student_data:  # list of Student objects to list of dictionaries
                dict_table.append({'FirstName': row.first_name,
                                   'LastName': row.last_name,
                                   'CourseName': row.course_name})

            json.dump(dict_table, file)
            file.close()
            IO.output_student_and_course_names(student_data=student_data)
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message,error=e)
        finally:
            if file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    ChangeLog: (Who, When, What)
    RRoot,1.1.2030,Created Class
    RRoot,1.2.2030,Added menu output and input functions
    RRoot,1.3.2030,Added a function to display the data
    RRoot,1.4.2030,Added a function to display custom error messages
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the a custom error messages to the user

        ChangeLog: (Who, When, What)
        RRoot,1.3.2030,Created function

        :param message: string with message data to display
        :param error: Exception object with technical message to display

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """ This function displays the menu of choices to the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function


        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """ This function gets a menu choice from the user

        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function

        :return: string with the users choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """ This function displays the student and course names to the user
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jmalick, 11.28.2023, changed to support Student object
        :param student_data: list Student objects to be displayed
        :return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student._first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list[Student]) -> list[Student]:
        """ This function gets the student's first name and last name, with a course name from the user
        ChangeLog: (Who, When, What)
        RRoot,1.1.2030,Created function
        jmalick, 12.28.2023, Changed to use Student object
        :param student_data: list of dictionary rows to be filled with input data
        :return: list
        """

        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            student = Student(student_first_name, student_last_name, course_name)
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Start of main body

# When the program starts, read the file data into a list of objects (table)
# Extract the data from the file
students: list[Student] = FileProcessor.read_data_from_file(file_name=FILE_NAME)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
