def quitCommand():
    quit_check = input("Are you sure you want to quit? (Y/N)").lower()
    return quit_check == 'yes' or quit_check == 'y'


if __name__ == '__main__':
    quit_val = False
    user_info = {'user_id'}
    print("Welcome to World Construct!")
    while not quit_val:
        input_value = input()