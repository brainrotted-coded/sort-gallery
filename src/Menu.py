from src.Exiftool import Exiftool
from src.Multimedia import Multimedia


def display_menu():
    print("MENU:")
    print("1. Rename files.")
    print("2. Change all dates.")
    print("3. Print all elements list.")
    print("4. Install Exiftool.")
    print("0. Exit.")


class Menu:
    def __init__(self, path: str):
        """
        This class allows you to use a menu to make it easier to use all the Multimedia functions.
        :param path: The path where you are going to sort your images and videos
        :type path: str
        """
        self._multimedia: Multimedia = Multimedia(path)
        self._exiftool: Exiftool = Exiftool()

    def menu(self):
        """
        The menu that calls the display_menu() function and makes you to select an option:
            1. Rename files.
            2. Change all dates.
            3. Print files list.
            0. Exit.
        If you select an invalid option, it will ask you again a valid option.
        If you select an invalid option three times, the program will close.
        """
        run_menu: bool = True
        strike: int = 0
        while run_menu:
            display_menu()
            option: str = input("Select an option: ")
            print("")
            if option == "1":
                print("1. Rename files:")
                self._multimedia.rename_files(self._multimedia.path)
            elif option == "2":
                print("2. Change all dates:")
                self._multimedia.change_all_modify_dates(self._multimedia.path)
                self._multimedia.fix_filetype()
                self._multimedia.change_all_dates()
            elif option == "3":
                print("3. Print files list:")
                self._multimedia.print_elements_list()
            elif option == "4":
                print("4. Install Exiftool.")
                self._exiftool.install_exiftool()
            elif option == "0":
                print("0. Leaving...")
                run_menu = False
            else:
                print("Please, enter a valid option.")
                strike += 1
                if strike >= 3:
                    run_menu = False
            print("")
