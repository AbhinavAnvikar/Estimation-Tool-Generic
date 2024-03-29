import psycopg2

class Users:

    global conn_string
    conn_string = "host='localhost' dbname='Estimation_Schema' user='NC_DB_USER' password='12345678'"

    @staticmethod
    def checkUsernameExists(u_name,conn):
        # Method to verify if username exists
        cursor = conn.cursor()
        result = '-1'
        print(u_name)
        cursor.execute("select * from check_username('{}')".format(u_name))
        result = cursor.fetchone()[0]
        return result

    @staticmethod
    def registerUser(u_name,password,re_pass,u_mail):

        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print("Connected Successfully")
        err_text =''
        success = ''
        if Users.checkUsernameExists(u_name,conn):
            err_text = 'Already exists'
        else:
            cursor.execute("select * from new_user_validation(%s,%s,%s,%s)",(u_name,password,re_pass,u_mail))
            res = cursor.fetchone()
            err_text = res[0]
            success = res[1]
            if success =='false' and str(err_text).__contains__('Re-enter'):
                print("Please ensure the re-enterred password match with password")
            else:
                print("user_registered_successfully : "+u_name)
        conn.commit()
        conn.close()

        return err_text
       # except:
        #    print("Unable to connect DB")

    @staticmethod
    def checkLogin(u_name,password):
        #Method to verify the login credentials in order to login
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("select * from check_login_credential(%s,%s)", (u_name, password))
        res = cursor.fetchone()
        err_text = res[0]
        success = res[1]
        print(err_text)
        return err_text

    @staticmethod
    def passwordValidation(password):
        # method to verify the input password is as per the required format
        conn = psycopg2.connect(conn_string)
        success = True
        cursor = conn.cursor()
        cursor.execute("select * from password_validation('{0}')".format(password))
        res = cursor.fetchall()
        for i in range(3):
            if res[i][1] == 0:
                success = False
        conn.commit()
        conn.close()
        #print(res)
        return res, success

if __name__=="__main__":
    print(Users.passwordValidation('Abhinav1990'));
    #conn = psycopg2.connect(conn_string)
    #print(Users.checkUsernameExists('Anvikar',conn))