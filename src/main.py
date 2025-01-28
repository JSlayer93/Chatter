from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QPushButton, QLabel, QVBoxLayout, QWidget, QScrollArea
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSettings, Qt
import sys
from server import log_in, create_user, find_user, find_rooms, find_room, send_message, add_user_chat, remove_user_chat, create_room

# Function to save a setting in QSettings
def save_setting(key, value):
  settings = QSettings("test")
  settings.setValue(key, value)

# Function to load a setting from QSettings
def load_setting(key, default_value):
  settings = QSettings("test")
  return settings.value(key, default_value)

# Function to remove a setting from QSettings
def remove_setting(key):
  settings = QSettings("test")
  settings.remove(key)

# Define the main application window
class Main_window(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi("mainui.ui", self)
    self.check_if_auth()
    self.sign_out.clicked.connect(self.log_out)
    self.refresh_button.clicked.connect(self.refresh)
    self.create_room_button.clicked.connect(self.go_create_room)
    self.load_groups()

  def load_groups(self):
    rooms = find_rooms()
    if rooms != False:
      for i in rooms:
        room = QPushButton(f'{i["name"]} {len(i["users"])}/{i["maxUsers"]}')
        room.setProperty("id", i["_id"])
        room.clicked.connect(lambda _, id=i["_id"]: self.get_in_room(id))  # Connect with lambda
        self.vbox.addWidget(room)
        
  def refresh(self):
    while self.vbox.count():
      item = self.vbox.takeAt(0)
      widget = item.widget()
      if widget:
          widget.deleteLater()
          
    self.load_groups()
  
  def get_in_room(self, room_id):
    answer = add_user_chat(room_id, load_setting("user", ""))
    roomIsAvelable = find_room(room_id)
    if answer != False and roomIsAvelable != None:
      save_setting("room", room_id)
      room = Room_window()
      stacked_widget.addWidget(room)
      stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
  
  def check_if_auth(self):
    if load_setting("user", "") == "":
      # If no user is saved, show the authentication window
      auth = Auth_Window()
      stacked_widget.addWidget(auth)  
      stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
    else:
      # If a user is saved, verify if they exist in the database
      user = find_user(load_setting("user", ""))
      if user is None:
        remove_setting("user")
        auth = Auth_Window()
        stacked_widget.addWidget(auth)
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
  
  def log_out(self):
    remove_setting("user")
    auth = Auth_Window()
    stacked_widget.addWidget(auth)
    stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
    main = Main_window()
    stacked_widget.removeWidget(main)

  def go_create_room(self):
    create_room = create_room_window()
    stacked_widget.addWidget(create_room)
    stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
  
class create_room_window(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi("createroomui.ui", self)
    self.go_back_button.clicked.connect(self.go_back)
    self.create_room_button.clicked.connect(self.create_room)
  
  def create_room(self):
    if self.name_input.text() == "" : pass
    else: room_id = create_room(load_setting("user", ""), self.name_input.text(), self.password_input.text(), self.spinBox.value())
    
    save_setting("room", room_id)
    room = Room_window()
    stacked_widget.addWidget(room)
    stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
    
  def go_back(self):
    main = Main_window()
    stacked_widget.addWidget(main)
    stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
    create_room = create_room_window()
    stacked_widget.removeWidget(create_room)  # Remove auth window after successful login
  
class Room_window(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi("roomui.ui", self)
    self.get_messages()
    self.message_line.returnPressed.connect(self.send_message)
    self.leave_room_button.clicked.connect(self.leave_room)
      
  def get_messages(self):
    room = find_room(load_setting("room", ""))
    messages = room["messages"]
    width = int(self.message_line.width()/2)
    
    for i in messages:
      if str(load_setting("user", "")) == str(i["sender"]):
        myMessage = QLabel(i["message"])
        myMessage.setMinimumWidth(width)
        myMessage.setAlignment(Qt.AlignRight)
        self.vbox.addWidget(myMessage)
      else:
        message = QLabel(f'{i["name"]}: {i["message"]}')
        message.setMinimumWidth(width)
        self.vbox.addWidget(message)
  
  def send_message(self):
    text = self.message_line.text().strip()
    user = find_user("6787ecb685366a41551f6efb")
    width = int(self.message_line.width()/2)
    
    if self.message_line.text() == "":
      pass
    elif len(self.message_line.text()) > 20:
      send_message(text, load_setting("user", ""), user["name"], load_setting("room", ""))
        
      myMessage = QLabel(self.message_line.text())
      self.message_line.setText("")
      myMessage.setMinimumWidth(width)
      myMessage.setAlignment(Qt.AlignRight)
      self.vbox.addWidget(myMessage)
    else:
      send_message(text, load_setting("user", ""), user["name"], load_setting("room", ""))
      
      myMessage = QLabel(self.message_line.text())
      self.message_line.setText("")
      myMessage.setMinimumWidth(width)
      myMessage.setAlignment(Qt.AlignRight)
      self.vbox.addWidget(myMessage)
  
  def leave_room(self):
    main = Main_window()
    stacked_widget.addWidget(main)
    stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
    
  def hideEvent(self, event):
    room = Room_window()
    stacked_widget.removeWidget(room) 
    remove_user_chat(load_setting("room", ""), load_setting("user", ""))
    remove_setting("room")

# Define the authentication window
class Auth_Window(QMainWindow):
  def __init__(self):
    super().__init__()
    loadUi("authui.ui", self)
    self.setFixedSize(174, 250)
    self.sign_in_button.clicked.connect(self.auth)
    self.sign_up_button.clicked.connect(self.register)

  # Handle user authentication
  def auth(self):
    if self.name_input.text() == "" or self.password_input.text() == "":
      pass  # Do nothing if inputs are empty
    else:
      user = log_in(self.name_input.text(), self.password_input.text())
      if user is not False:
        save_setting("user", str(user))
        main = Main_window()
        stacked_widget.addWidget(main)
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
        auth = Auth_Window()
        stacked_widget.removeWidget(auth)  # Remove auth window after successful login
      else:
        self.wrong_label.setText("Wrong")  # Show error message for incorrect login
  
  # Handle user registration
  def register(self):
    if self.name_input.text() == "" or self.password_input.text() == "":
      pass  # Do nothing if inputs are empty
    else:
      user = create_user(self.name_input.text(), self.password_input.text())
      if user is not False:
        save_setting("user", str(user))
        stacked_widget.setCurrentIndex(stacked_widget.currentIndex() + 1)
        auth = Auth_Window()
        stacked_widget.removeWidget(auth)  # Remove auth window after successful registration
      else:
        self.wrong_label.setText("Wrong")  # Show error message for failed registration

# Define the main function to run the application
def main():
  global stacked_widget 
  app = QApplication(sys.argv)
  stacked_widget = QStackedWidget()  
  main = Main_window()
  stacked_widget.addWidget(main)
  stacked_widget.setFixedHeight(500)
  stacked_widget.setFixedWidth(700)
  stacked_widget.show()
  sys.exit(app.exec_())

# Run the main function only when the script is executed directly
if __name__ == "__main__":
  main()