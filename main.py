




if __name__ == "__main__":
    from main_communication import MainCommunicator
    from mysql_database import MysqlDatabase
    MysqlDatabase.checks_database()
    MainCommunicator.run()
    MainCommunicator.end_of_program()