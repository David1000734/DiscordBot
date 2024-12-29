'''
Module used to hold a global variable that will be present
throughout the entire project.
'''


def init():
    '''
    Initilization of global variables. ONLY the main should call this.
    '''
    # Also check to see if existing data already exist or not

    # List of servers the bot is currently in and it's relavent data for each
    global server_list
    server_list = {}
