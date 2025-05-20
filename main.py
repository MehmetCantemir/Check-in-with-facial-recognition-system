import tkinter as tk
from tkinter import messagebox
import cv2
import os
import sqlite3
from tkinter import ttk
import face_recognition
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


def face_save(name, surname):
    
    """
    Creates a folder with the given name and surname,
    takes face photos from the camera, and saves them in this folder.

    Parameters:
        name (str): The person's name.
        surname (str): The person's surname.
    """
    
    
     # Creates the folder name for the photos to be saved and the full path of the folder.
    folder_name = f"{name}_{surname}"
    folder_path = os.path.join("dataset", folder_name)
    
    
    # If the folder does not exist, create it.
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        
        
    # Open the camera and start capturing photos.
    # The haarcascade_frontalface_default.xml file is used for face detection.
    cap = cv2.VideoCapture(0)
    yuz_cascPath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(yuz_cascPath)
    
    sayac = 0
    max_photo = 5

    # Reads a frame from the camera
     # If a frame cannot be read (e.g., if the camera is disconnected)
    while True:
        ret, frame = cap.read() 
        if not ret:            
            break
        
        # Convert the frame to grayscale for face detection
        # Detect faces in the frame
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grey, 1.3, 5)

        # For each detected face: Increase the photo counter.
        for (x, y, w, h) in faces:
            sayac += 1
            yuz = frame[y:y+h, x:x+w] # Crops the face region.
            cv2.imwrite(f"{folder_path}/face_{sayac}.jpg", yuz) #Saves the face to a file.
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Show Your Face to the Camera", frame) # Displays the image from the camera (with face rectangles) on the screen.
        if cv2.waitKey(1) & 0xFF == ord('q') or sayac >= max_photo:# If the 'q' key is pressed or the maximum number of photos is reached,
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"{sayac} face photos saved!")
    
    
def save_user_database(name, surname,midterm, final, student_number):
    

    """
    Saves user information (name, surname, midterm, final, student_number, folder_path) to a SQLite database.

    Parameters:
        name (str): The name of the user.
        surname (str): The surname of the user.
        midterm (int): The midterm exam score of the user.
        final (int): The final exam score of the user.
        student_number (int): The student number of the user.
        folder_path (str): The folder path associated with the user.
    """
    
    folder_path = f"{name}_{surname}"
    conn = sqlite3.connect("users.db") # database connection
    cursor = conn.cursor()
    cursor.execute("INSERT INTO kullanicilar (name, surname,midterm,final,student_number,folder_path) VALUES (?, ?, ?,?, ?, ?)",
                   (name, surname, midterm, final, student_number, folder_path)) # insert data into the database
                  
    conn.commit() # commit the changes
    conn.close() # close the connection

def sign_up():

    """
    Creates a new window for user sign-up, including fields for name, surname, midterm, final, and student number,
    and a button to save the data and scan the user's face.
    
    """

    
    def save():
        
        """
        Retrieves user input from the entry fields, calls face_save and save_user_database functions,
        and closes the sign-up window. Displays a warning message if name and surname are not entered.
        """
        # get the name,surname, midterm, final, and student number from the entry fields
        name = entry_name.get()
        surname = entry_surname.get()  
        midterm = entry_midterm.get()
        final = entry_final.get()
        student_number = entry_student_number.get()
        
        if name and surname:
            face_save(name, surname) # save the face images
            save_user_database(name, surname, midterm, final, student_number) # save the user data to the database
            new_window.destroy()
        else:
            messagebox.showwarning("Warning", "please enter your name and surname")

    new_window = tk.Toplevel()
    new_window.title("Sign Up")
    new_window.geometry("300x250")

    tk.Label(new_window, text="Name:").pack()
    entry_name = tk.Entry(new_window)
    entry_name.pack()

    tk.Label(new_window, text="Surname:").pack()
    entry_surname = tk.Entry(new_window)
    entry_surname.pack()
    
    tk.Label(new_window, text="Midterm:").pack()
    entry_midterm = tk.Entry(new_window)
    entry_midterm.pack()
    
    tk.Label(new_window, text="Final:").pack()
    entry_final = tk.Entry(new_window)
    entry_final.pack()
    
    tk.Label(new_window, text="Student Number:").pack()
    entry_student_number = tk.Entry(new_window)
    entry_student_number.pack()
    tk.Button(new_window, text="Scan and Save Face", command=save).pack(pady=10)

def log_in():
    
    
    """
    Opens the camera, captures the user's face, compares it to registered faces in the database,
    and logs the user in if a match is found.
    """

    def user_recognition():
        
        """
        Captures the user's face using the camera, detects faces, and compares the captured face
        with the faces stored in the database. If a match is found, the user is logged in.
        
        """
        # Opens the default camera and specifies the path to the Haar Cascade XML file for face detection.
        cap = cv2.VideoCapture(0) 
        yuz_cascPath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        face_cascade = cv2.CascadeClassifier(yuz_cascPath)
    
        # Reads a frame from the camera
        ret, frame = cap.read()
        
        # If a frame cannot be read (e.g., if the camera is disconnected)
        if not ret:
            messagebox.showerror("Mistake", "The camera did not open.")
            
        # Convert the frame to grayscale for face detection
        gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        yuzler = face_cascade.detectMultiScale(gri, 1.3, 5)

        # If no faces are detected, release the camera and show an error message
        if len(yuzler) == 0:
            cap.release()
            cv2.destroyAllWindows()
            messagebox.showerror("Hata", "Yüz algılanamadı. Lütfen kameraya net bir şekilde bakın.")
            return
        
        # For each detected face: Save the face image and draw a rectangle around it.
        for (x, y, w, h) in yuzler:
            yuz_resmi = frame[y:y+h, x:x+w]
            cv2.imwrite("entered_face.jpg", yuz_resmi)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cap.release()
        cv2.destroyAllWindows()

        # Compare recognized face
        known_face = face_recognition.load_image_file("entered_face.jpg")
        encodings = face_recognition.face_encodings(known_face)

        if len(encodings) == 0:
            messagebox.showerror("mistake", "Face recognition failed. The face was not detected clearly.")
            return

        known_face_encoding = encodings[0]

        # Compare faces in database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar")
        datas = cursor.fetchall()
        conn.close()

        # Iterate through the database and compare the known face with each face in the database
        for data in datas:
            folder_path = data[6]  
            face_image_path = os.path.join("dataset", folder_path , "face_1.jpg")
            if os.path.exists(face_image_path):
                database_face = face_recognition.load_image_file(face_image_path)
                database_face_encoding_list = face_recognition.face_encodings(database_face)

                if len(database_face_encoding_list) == 0:
                    continue 
                
                # Compare the known face with the database face
                database_face_encoding = database_face_encoding_list[0]
                eslesme = face_recognition.compare_faces([database_face_encoding], known_face_encoding)

                if eslesme[0]:
                    messagebox.showinfo("Welcome", f" {data[1]} {data[2]} is here!")
                    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    conn_log = sqlite3.connect("login_logs.db")  
                    cursor_log = conn_log.cursor()
                    cursor_log.execute("INSERT INTO giris_kayitlari (name, surname, login_time) VALUES (?, ?, ?)",
                   (data[1], data[2], login_time))
                    conn_log.commit()
                    conn_log.close()
                    return

        messagebox.showerror("Mistake", "The identified face was not found!")
    user_recognition()
       
def view_users():
    
    """
    Creates a new window to display registered users in a treeview format.
    """
    window_list = tk.Toplevel()
    window_list.title("Registered Users")
    window_list.geometry("400x300")

    tree = ttk.Treeview( window_list, columns=("id", "name", "surname", "midterm","final","student_number","folder_path"), show="headings")
    tree.heading("id", text="id")
    tree.heading("name", text="name")
    tree.heading("surname", text="surname")
    tree.heading("midterm", text="midterm")
    tree.heading("final", text="final")
    tree.heading("student_number", text="student_number")
    tree.heading("folder_path", text="folder_path")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kullanicilar")
    data = cursor.fetchall()
    conn.close()

    for data in data:
        tree.insert("", "end", values=data)

def view_login_logs():
    
    """
    Creates a new window to display login logs from the database in a treeview widget.
    
    """
    
    window_logs = tk.Toplevel()
    window_logs.title("Login Logs")
    window_logs.geometry("400x300")

    tree = ttk.Treeview(window_logs, columns=("id", "name", "surname", "login_time"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("surname", text="Surname")
    tree.heading("login_time", text="Login Time")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = sqlite3.connect("login_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM giris_kayitlari")
    logs = cursor.fetchall()
    conn.close()

    for log in logs:
        tree.insert("", "end", values=log)

def show_weekly_logins():
    
    
    """
    Fetches login data from the last week from the database and displays it in a bar chart.
    """
    
    # Connect to database
    conn = sqlite3.connect("login_logs.db")
    cursor = conn.cursor()

    # Calculate the last 7 days
    now = datetime.now()
    seven_days_ago = now - timedelta(days=7)

    #Get data
    cursor.execute("SELECT name, login_time FROM giris_kayitlari")
    rows = cursor.fetchall()
    conn.close()

    # Filter and count logins
    login_counts = {}

    for name, login_time in rows:
        login_dt = datetime.strptime(login_time, "%Y-%m-%d %H:%M:%S")
        if login_dt >= seven_days_ago:
            login_counts[name] = login_counts.get(name, 0) + 1

    if not login_counts:
        messagebox.showinfo("Info", "There have been no logins in the last week.")
        return

    # Graphic drawing
    names = list(login_counts.keys())
    counts = list(login_counts.values())

    plt.figure(figsize=(8, 5))
    plt.bar(names, counts, color='skyblue')
    plt.xlabel("User Names")
    plt.ylabel("Login Count")
    plt.title("User Login Numbers in the Last Week")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
def open_user_management_window():
    
    """
    Opens a new window for user management, allowing the user to delete or update user information.
    
    """
    
    
    # Users list
    def refresh_user_list():
        user_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, name, surname, student_number FROM kullanicilar")
        for row in cursor.fetchall():
            user_listbox.insert(tk.END, f"{row[0]} - {row[1]} {row[2]} (No: {row[3]})")

    # Delete and update user functions
    def delete_user():
        selected = user_listbox.get(tk.ACTIVE)
        if not selected:
            return
        user_id = selected.split(" - ")[0]
        confirm = messagebox.askyesno("Delete", f"Are you sure you want to delete this user?\nID: {user_id}")
        if confirm:
            cursor.execute("DELETE FROM kullanicilar WHERE id=?", (user_id,))
            conn.commit()
            refresh_user_list()


    # Update user function
    def update_user():
        selected = user_listbox.get(tk.ACTIVE)
        if not selected:
            return
        user_id = selected.split(" - ")[0]

        new_name = entry_name.get()
        new_surname = entry_surname.get()
        new_midterm = entry_midterm.get()
        new_final = entry_final.get()
        new_student_number = entry_student_number.get()

        if all([new_name, new_surname, new_midterm, new_final, new_student_number]):
            cursor.execute("""
                UPDATE kullanicilar
                SET name=?, surname=?, midterm=?, final=?, student_number=?
                WHERE id=?
            """, (new_name, new_surname, new_midterm, new_final, new_student_number, user_id))
            conn.commit()
            refresh_user_list()
        else:
            messagebox.showwarning("Missing Information", "All fields must be filled in.")

    # Database connection
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # New window for user management
    window = tk.Toplevel()
    window.title("Management of Users ")
    window.geometry("600x500")  # → Daha büyük pencere boyutu

    # User list
    user_listbox = tk.Listbox(window, width=60)
    user_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Delete and Update buttons
    tk.Button(window, text="Delete User", command=delete_user).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(window, text="Update User", command=update_user).grid(row=1, column=1, padx=5, pady=5)

    # Input fields for update (except folder_path)
    labels = ["Name", "Surname", "Midterm", "Final", "Student Number"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(window, text=label + ":").grid(row=2+i, column=0, sticky="e")
        entry = tk.Entry(window)
        entry.grid(row=2+i, column=1, padx=5, pady=2)
        entries.append(entry)

    entry_name, entry_surname, entry_midterm, entry_final, entry_student_number = entries

    refresh_user_list()

    
# Main window
pencere = tk.Tk()
pencere.title("Attandance Application")
pencere.geometry("500x500")

tk.Label(pencere, text="Welcome!", font=("Arial", 14)).pack(pady=20)
tk.Button(pencere, text="Attandence ", command=log_in, width=15).pack(pady=5)
tk.Button(pencere, text="Sign Up", command=sign_up, width=15).pack(pady=5)
tk.Button(pencere, text="View Users", command=view_users, width=20).pack(pady=5)
tk.Button(pencere, text="View Login Logs", command=view_login_logs, width=20).pack(pady=5)
tk.Button(pencere, text="Last Week's Entries", command=show_weekly_logins, width=25).pack(pady=5)
tk.Button(pencere, text="Manage Users", command=open_user_management_window).pack(pady=10)


pencere.mainloop()