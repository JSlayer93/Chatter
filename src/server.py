# Importing necessary libraries
from pymongo import MongoClient  # For interacting with MongoDB
from bson import ObjectId  # For working with MongoDB ObjectIDs
import hashlib  # For hashing passwords
import string  # For generating random strings
import secrets  # For generating secure random strings
from dotenv import load_dotenv, dotenv_values  # For loading environment variables
import os  # For accessing environment variables

# Load environment variables from .env file
load_dotenv()

# Connecting to MongoDB cluster (replace with your connection string)
client = MongoClient(os.getenv("DATABASE"))

# Creating a database named "MyDatabase"
db = client["MyDatabase"]

# Creating a collection named "Users" to store user data
users = db["Users"]

# Creating a collection named "Rooms" to store chat room data
rooms = db["Rooms"]

# Function to generate a random 24-character ID
def create_id():
  alphabet = string.ascii_letters + string.digits  # All letters and digits
  key = ''.join(secrets.choice(alphabet) for _ in range(24))  # Randomly select 24 characters
  return key

# Function to hash a password using SHA-256
def hash_password(password):
  hash_object = hashlib.sha256(password.encode('utf-8'))  # Create a SHA-256 hash object
  hashed_password = hash_object.hexdigest()  # Get the hexadecimal digest of the hash
  return hashed_password

# Function to check if a password matches a hashed password
def check_password(password, hashed_password):
  hashed_input = hash_password(password)  # Hash the input password
  return hashed_input == hashed_password  # Compare the hashes

# Function to find a user by their ID
def find_user(id):
  try:
    return users.find_one({"_id": ObjectId(id)})  # Find user by ObjectId
  except:
    return None  # Return None if there's an error (e.g., invalid ID format)

# Function to create a new user
def create_user(name, password):
  if users.find_one({"name": name}) is None:  # Check if the user already exists
    users.insert_one({"name": name, "password": hash_password(password)})  # Insert new user
    user = users.find_one({"name": name})  # Find the newly created user
    return user["_id"]  # Return the user's ID
  return False  # Return False if the user already exists

# Example: Create a user with name "test" and password "test"
create_user("test", "test")

# Function to log in a user
def log_in(name, password):
  user = users.find_one({"name": name})  # Find the user by name
  if user and check_password(password, user.get("password")):  # Check if the password matches
    return user["_id"]  # Return the user's ID if login is successful
  return False  # Return False if login fails

# Function to remove a user by name
def remove_user(name):
  users.delete_one({"name": name})  # Delete the user from the collection

# Chat operations

# Function to find all chat rooms
def find_rooms():
  try:
    return list(rooms.find({}))  # Return a list of all rooms
  except Exception as e:
    return False  # Return False if there's an error

# Function to create a new chat room
def create_room(user, name, password="", maxUsers=8):
  try:
    if maxUsers > 8:  # Ensure the maximum number of users is not exceeded
      return False
    room = rooms.insert_one({
      "name": name,
      "users": [user],  # Add the creator to the users list
      "messages": [],  # Initialize an empty messages list
      "password": password,  # Set the room password (if any)
      "maxUsers": maxUsers  # Set the maximum number of users
    })
    return room.inserted_id
  except:
    return False  # Return False if there's an error

# Function to add a user to a chat room
def add_user_chat(id, user):
  try:
    chat = find_room(id)  # Find the room by ID
    if len(chat["users"]) >= chat["maxUsers"]:  # Check if the room is full
      return False
    rooms.update_one({"_id": ObjectId(id)}, {"$push": {"users": user}})  # Add the user to the room
  except Exception as e:
    return False  # Return False if there's an error

# Function to remove a user from a chat room
def remove_user_chat(id, user):
  try:
    rooms.update_one({"_id": ObjectId(id)}, {"$pull": {"users": user}})  # Remove the user from the room
    room = find_room(id)
    if len(room["users"]) == 0: delete_room(id)
  except Exception as e:
    return False  # Return False if there's an error

# Function to find a room by its ID
def find_room(id):
  try:
    room = rooms.find_one({"_id": ObjectId(id)})  # Find the room by ObjectId
    return room
  except:
    return None  # Return None if there's an error
  
def delete_room(id):
  try:
    room = rooms.delete_one({"_id": ObjectId(id)})  # Find the room by ObjectId
    return room
  except:
    return None  # Return None if there's an error

# Function to send a message in a chat room
def send_message(message, sender, name, id):
  try:
    rooms.update_one({"_id": ObjectId(id)}, {
      "$push": {
        "messages": {
          "_id": create_id(),  # Generate a unique message ID
          "sender": sender,  # The sender's ID
          "name": name,  # The sender's name
          "message": message  # The message content
        }
      }
    })
  except Exception as e:
    return False  # Return False if there's an error
  
# print(find_room("6799090f6cd911e074130055"))
  
# create_room("6787ecb685366a41551f6sfb", "test")