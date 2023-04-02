# from attr import s 
import streamlit as st  
# import streamlit.components.v1 as components
# import streamlit_authenticator as stauth
import utils.authenticate as stauth
import utils.util as sqlcon
import pandas as pd
import hashlib  


def main(connection):
    
    c= connection

    usernames , names , passwords = sqlcon.call_users()
    hashed_passwords = stauth.Hasher(passwords).generate()


    credentials = {"usernames":{}}


    for un, name, pw in zip(usernames, names, hashed_passwords):
        user_dict = {"name":name,"password":pw}
        credentials["usernames"].update({un:user_dict})
        

    _authenticator = stauth.Authenticate(credentials,'in_responseCookie', 
                                        'auth',cookie_expiry_days=0)
    
    st.title("In-Response System")


    def render_admin_page():
    
        st.title('Admin Page')
        st.write('Welcome *%s*' % (name))
        st.write('Welcome ')
        adminMenu = st.selectbox("Admin Menu", ["Home", "Opened Tickets", "Closed Tickets","Users Profiles","Add User"])
        if adminMenu == "Home":
            st.subheader("Dashboard")
        elif adminMenu == "Opened Tickets":
            st.subheader("Browse Open Tickets")
        elif adminMenu == "Closed Tickets":
            st.subheader("Browse Closed Tickets")
        elif adminMenu == "Users Profiles":
            st.subheader("Profiles:")

            query = 'SELECT id, username , name, email FROM users;'
            
            cursor = c.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            # Displaying data using Streamlit table
            df = pd.DataFrame(results,columns=('ID','Username','Name','Email'))
            # CSS to inject contained in a string
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)

            # Display a static table
            st.table(df)
        elif adminMenu == "Add User":  
            st.subheader("Add New User")

            # Create input fields for the user's name, email, and password
            new_username = st.text_input("Username")
            new_name = st.text_input("Name")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            
 

            # Add a button to submit the new user
            if st.button("Add User"):
                hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
                sqlQ = "INSERT INTO `users`(`username`, `password`, `name`, `email`) VALUES (%s,%s,%s,%s)" 
                values = (new_username, hashed_password, new_name, new_email)
                cursor = None
               
                cursor = c.cursor()
                cursor.execute(sqlQ, values)
                c.commit()
                # Show a success message
                st.success(f"Added user: {new_name} ({new_email}) with username: {new_username}")
 

    def render_regular_page():
        st.write('Welcome *%s*' % (name))
        userMenu = st.selectbox("Menu", ["Home", "Opened Tickets", "Closed Tickets"])
        if userMenu == "Home":
            st.subheader("Dashboard")
        elif userMenu == "Opened Tickets":
            st.subheader("Browse Open Tickets")
        elif userMenu == "Closed Tickets":
            st.subheader("Browse Closed Tickets")
  
    
    name, authentication_status, username = _authenticator.login('Login','main')

    adminusername='admin'
    
    if authentication_status:
            if username == adminusername:
                render_admin_page()
                _authenticator.logout("logout","main")
                
            elif username != adminusername:
                render_regular_page()
                _authenticator.logout("logout","main")

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')


if __name__ == '__main__':
    c= sqlcon.create_db_connection()
    main(c)
    