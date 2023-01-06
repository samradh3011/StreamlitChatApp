from streamlit_server_state import server_state, server_state_lock
import streamlit as st

if "messages" not in server_state:
    server_state["messages"] = []

if "NORMAL_PASSWORD_STR" not in server_state:
    server_state["NORMAL_PASSWORD_STR"] = "123"
    
if "ADMIN_PASSWORD_STR" not in server_state:
    server_state["ADMIN_PASSWORD_STR"] = "991152"

if "LAST_IMAGE" not in server_state:
    server_state["LAST_IMAGE"] = None

def adminView():
    st.write(f"Current Password: {server_state['NORMAL_PASSWORD_STR']}")
    new_password = st.sidebar.text_input("New Password")
    confirm_password = st.sidebar.text_input("Confirm Password")
    change_btn = st.sidebar.button("Change")

    if change_btn:
        if new_password == confirm_password:
            server_state["NORMAL_PASSWORD_STR"] = new_password
            st.success("Password Changed")
        else:
            st.error("Passwords Don't Match")

def displayMessages():
    st.markdown("---")
    st.header("Messages")
    col1, col2 = st.columns(2)
    message_str = ""

    if len(server_state["messages"]) > 0:
        for message in reversed(server_state["messages"]):
            message_str += f"{message['MESSAGE']} by {message['NAME']}\n"
        
        col1.text_area("Chats", message_str, height=200)

    if server_state["LAST_IMAGE"] is not None:
        col2.image(server_state["LAST_IMAGE"]["IMAGE"], f"by - {server_state['LAST_IMAGE']['NAME']}")
    
def normalView():
    name = st.sidebar.text_input("Name")
    clear_chats = st.sidebar.button("Clear Chats")

    col1, col2 = st.columns(2)
    message = col1.text_area("Message",height=240)
    send_btn = col1.button("Send")

    camera_input = col2.camera_input("Take Pick")
    send_image_btn = col2.button("Send Image")

    if send_btn:
        if message != "":
            with server_state_lock["messages"]:
                server_state["messages"] = server_state["messages"] + [{"NAME": name, "MESSAGE": message}]

    
    if send_image_btn:
        if camera_input is not None:
            with server_state_lock["LAST_IMAGE"]:
                server_state["LAST_IMAGE"] = {"NAME": name, "IMAGE":camera_input}

    
    if clear_chats:
        with server_state_lock["messages"]:
            server_state["messages"] = []
        with server_state_lock["LAST_IMAGE"]:
            server_state["LAST_IMAGE"] = None
    
    displayMessages()


#
password_input = st.sidebar.text_input("Password")

if password_input == server_state["NORMAL_PASSWORD_STR"]:
    normalView()
elif password_input == server_state["ADMIN_PASSWORD_STR"]:
    adminView()