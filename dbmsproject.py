import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# --------------------------------- Database Connection Class ------------------
class Database:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query, data=None):
        self.cursor.execute(query, data)
        self.connection.commit()

    def fetch_all(self, query, data=None):
        self.cursor.execute(query, data)
        return self.cursor.fetchall()

#-----------------------------------Hotel Class Start here------------------------
class hotel:
    def __init__(self, db,customer_info):
        self.db=db  
        self.customer_manager=customer_info
  #----------------   
    def list_hotels(self):    
        query = "SELECT * FROM hotel"
        hotels = self.db.fetch_all(query)
        return hotels  # Returning list of hotels
    
    def list_hotel(self, hotel_id): 
        query = "SELECT * FROM hotel WHERE hotel_id = %s"
        hotels = self.db.fetch_all(query, (hotel_id,))
        return hotels[0] if hotels else None  # Returning the hotel details
  
    def hotel_booking(self, hotel_id, fname, lname, country, email, days_):
        # Booking hotel after validating
        hotel_details = self.list_hotel(hotel_id)
        if hotel_details:
            self.customer_manager.customer_booking(hotel_id, fname, lname, country, email, days_)
            print("Booking successful!")
            messagebox.showinfo("Success", "Your booking was successful!")
        else:
            messagebox.showerror("Error", "Hotel not found. Please try again.")
         
#------------------------------Hotel Class End here------------------------------
#-----------------------------Customer Booking Class Start here------------------
class customer:
    def __init__ (self,db):
        self.db=db  
    def customer_booking(self,hotel_id,fname,lname,country, email,days_):
      try:
          query = "INSERT INTO customer_booking_info (hotel_id,fname,lname,country, email,days_) VALUES (%s,%s, %s, %s, %s,%s)"
          self.db.execute_query(query, (hotel_id,fname,lname,country,email,days_))
          print("Thank You! Your Booking is successful!")   
      except mysql.connector.Error as err:
         print(f"Error: {err}")
#-----------------------------Customer Booking Class End here--------------------
#----------------------------------Property Class START HERE---------------
class RealStateProperty:
    def __init__(self, db):
        self.db = db

    def add_property(self, property_type, location, price):
      try:  
        query = "INSERT INTO properties (type, location, price) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (property_type, location, price))
        messagebox.showinfo("Success", "Property Added Successfully")
      except mysql.connector.Error as err:
          print(f"Error:{err}") 
    def update_properties(self,property_id,availability):
        try:
            query = "UPDATE properties SET status = %s WHERE id = %s"
            self.db.execute_query(query, (availability, property_id))
            messagebox.showinfo("Success", "Property availability updated successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def list_properties(self):
        query = "SELECT * FROM properties"
        return self.db.fetch_all(query)
   
#----------------------------------Property Class END HERE---------------    
# ------------------ Application GUI ------------------
class Application:
    def __init__(self, root, db,hotel_manager,property_manager):
        self.root = root
        self.root.title("Unique Group")
        self.root.geometry("800x600")
        self.db = db
        self.hotel_manager=hotel_manager
        self.property_manager=property_manager
        self.root.config(bg='lightblue') 
        # Main menu screen
        self.create_main_menu()

    def create_main_menu(self):
        # Clear the current frame
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Unique Group (PLC)", font=("Arial", 20), bg="lightblue", width=40).pack(pady=20)
        tk.Button(self.root, text="User Registration", font=("Arial", 14), command=self.register_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.login_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="HOSPITAL", font=("Arial", 14), command=self.show_coming_soon_message, width=20).pack(pady=10)
        tk.Button(self.root, text="PROPERTY LIST", font=("Arial", 14), command=self.view_properties, width=20).pack(pady=10)
        tk.Button(self.root, text="HOTEL", font=("Arial", 14), command=self.view_hotels, width=20).pack(pady=10)
        tk.Button(self.root, text="MAN POWER", font=("Arial", 14), command=self.view_all_jobs, width=20).pack(pady=10)
        tk.Button(self.root, text="Exit", font=("Arial", 14), command=self.root.quit,bg="red", width=20).pack(pady=10)
#-----------------------------------------------
    def register_screen(self):
        # User Registration Screen
        self.clear_screen()
        tk.Label(self.root, text="User Registration", font=("Arial", 20)).pack(pady=20)

        name_label = tk.Label(self.root, text="Name:", font=("Arial", 14))
        name_label.pack()
        name_entry = tk.Entry(self.root, font=("Arial", 14))
        name_entry.pack()

        email_label = tk.Label(self.root, text="Email:", font=("Arial", 14))
        email_label.pack()
        email_entry = tk.Entry(self.root, font=("Arial", 14))
        email_entry.pack()

        password_label = tk.Label(self.root, text="Password:", font=("Arial", 14))
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        password_entry.pack()

        def register_user():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            if name and email and password:
                try:
                    query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
                    self.db.execute_query(query, (name, email, password, "Customer"))
                    messagebox.showinfo("Success", "User registered successfully!")
                    self.create_main_menu()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Database error: {err}")
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(self.root, text="Register", font=("Arial", 14), command=register_user).pack(pady=20)
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack()

    def login_screen(self):
        # User Login Screen
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 20)).pack(pady=20)

        email_label = tk.Label(self.root, text="Email:", font=("Arial", 14))
        email_label.pack()
        email_entry = tk.Entry(self.root, font=("Arial", 14))
        email_entry.pack()

        password_label = tk.Label(self.root, text="Password:", font=("Arial", 14))
        password_label.pack()
        password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        password_entry.pack()

        def login_user():
            email = email_entry.get()
            password = password_entry.get()
            if email and password:
                query = "SELECT * FROM users WHERE email = %s AND password = %s"
                user = self.db.fetch_all(query, (email, password))
                if user:
                    role = user[0][4]
                    if role == "Admin":
                        self.admin_dashboard()
                    else:
                        self.user_dashboard()
                else:
                    messagebox.showerror("Error", "Invalid login credentials!")
            else:
                messagebox.showerror("Error", "All fields are required!")

        tk.Button(self.root, text="Login", font=("Arial", 14), command=login_user).pack(pady=20)
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack()

    def admin_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="Add Property", font=("Arial", 14), command=self.add_property).pack(pady=10)
        tk.Button(self.root, text="Update Property Availability", font=("Arial", 14), command=self.update_property).pack(pady=10)
        tk.Button(self.root, text="View Bookings", font=("Arial", 14), command=self.view_all_bookings).pack(pady=10)
        tk.Button(self.root, text="Post Job Circular", font=("Arial", 14), command=self.add_job_circular).pack(pady=10)
        tk.Button(self.root, text="Logout", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)
#-------------------------- 
    def show_coming_soon_message(self):
         self.clear_screen()
         tk.Label(self.root, text="HOSPITAL LIST", font=("Arial", 20),bg="#ADD8E6").pack(pady=20)
         tk.Button(self.root, text="GULSHAN CLINIC", font=("Arial", 14), command=lambda: messagebox.showinfo("Coming Soon", "More feature will be coming soon."), width=20).pack(pady=10)
         tk.Button(self.root, text="BACK", font=("Arial", 14), command=self.create_main_menu,bg="blue", width=20).pack(pady=10)

    def view_all_bookings(self):
        self.clear_screen()
# Fetch all bookings from the database
        query = "SELECT * FROM customer_booking_info"
        bookings = self.db.fetch_all(query)

        tk.Label(self.root, text="All Customer Bookings", font=("Arial", 20)).pack(pady=20)

        # Table headers
        headers = ["Booking ID", "Hotel ID", "First Name", "Last Name", "Country", "Email", "Days"]
        header_frame = tk.Frame(self.root, bg="lightblue")
        header_frame.pack(pady=5)
        for i, header in enumerate(headers):
            tk.Label(header_frame, text=header, font=("Arial", 12, "bold"),bg="green", width=15, anchor="w").grid(row=0, column=i)

        # Populate the bookings in the table
        if bookings:
            for row_num, booking in enumerate(bookings):
                for col_num, value in enumerate(booking):
                    tk.Label(header_frame, text=value, font=("Arial", 12), width=15, anchor="w").grid(row=row_num + 1, column=col_num)
        else:
            tk.Label(self.root, text="No bookings found.", font=("Arial", 14)).pack(pady=10)

        # Back button
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.admin_dashboard).pack(pady=20)
    
    def add_property(self):
        self.clear_screen()    
        tk.Label(self.root, text="Add Property Details", font=("Arial", 20)).pack(pady=20)
        self.property_type_label=tk.Label(self.root, text="Enter Property Type", font=("Arial", 14))
        self.property_type_label.pack()
        self.property_type_Entry = tk.Entry(self.root, font=("Arial", 14))
        self.property_type_Entry.pack(pady=5)
        self.property_location_label=tk.Label(self.root, text="Location", font=("Arial", 14))
        self.property_location_label.pack()
        self.property_location_Entry = tk.Entry(self.root, font=("Arial", 14))
        self.property_location_Entry.pack(pady=5)
        self.property_price_label=tk.Label(self.root, text="Price", font=("Arial", 14))
        self.property_price_label.pack()
        self.property_price_Entry = tk.Entry(self.root, font=("Arial", 14))
        self.property_price_Entry.pack(pady=5)
        tk.Button(self.root, text="ADD", font=("Arial", 14), command= self.submit_property).pack(pady=20)
        tk.Button(self.root, text="BACK", font=("Arial", 14), command=self.admin_dashboard).pack(pady=20)
    def submit_property(self):
        property_type=self.property_type_Entry.get()
        location=self.property_location_Entry.get()
        price=self.property_price_Entry.get()

        if property_type and location and price:
            try:
                price=float(price)
                self.property_manager.add_property(property_type, location, price)
                self.admin_dashboard()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid Price.")    
        else:
            messagebox.showerror("Error", "Please fill all the details.")
    def add_job_circular(self):
        self.clear_screen()
        tk.Label(self.root, text="Add Job Circular", font=("Arial", 20)).pack(pady=20)
        self.job_title_label=tk.Label(self.root, text="Enter Job Title", font=("Arial",14))
        self.job_title_label.pack()
        self.job_title_Entry=tk.Entry(self.root, font=("Arial", 14))
        self.job_title_Entry.pack(pady=5)
        self.job_detail_label=tk.Label(self.root, text="Description", font=("Arial",20))
        self.job_detail_label.pack()
        self.job_detail_Entry=tk.Entry(self.root, font=("Arial", 14))
        self.job_detail_Entry.pack(pady=5)
        tk.Button(self.root, text="ADD", font=("Arial", 14), command= self.submit_job).pack(pady=20)
        tk.Button(self.root, text="BACK", font=("Arial", 14), command=self.admin_dashboard).pack(pady=20)
    def submit_job(self):
        job_title=self.job_title_Entry.get()
        job_detail=self.job_detail_Entry.get()
        if job_title and job_detail:
            query = "INSERT INTO manpower_jobs (title, description) VALUES (%s, %s)"
            self.db.execute_query(query, (job_title, job_detail))
            messagebox.showinfo("Success", "Job Added Successfully.")
            self.admin_dashboard()
        else:
            messagebox.showerror("Error", "Please fill all the details.")


    def update_property(self):
        self.clear_screen()
        tk.Label(self.root, text="Update Property Details", font=("Arial", 20)).pack(pady=20)
        self.property_update_label=tk.Label(self.root, text="Enter Property ID", font=("Arial", 14))
        self.property_update_label.pack()
        self.property_update_Entry = tk.Entry(self.root, font=("Arial", 14))
        self.property_update_Entry.pack(pady=5)

        # Availability Options
        tk.Label(self.root, text="Select Availability:", font=("Arial", 14)).pack()
        self.availability_combobox = ttk.Combobox(
        self.root, values=["Available", "Not Available"], font=("Arial", 14), state="readonly"
         )
        self.availability_combobox.pack(pady=5)
        self.availability_combobox.set("Available")  # Default selection

    # Buttons
        tk.Button(self.root, text="Update", font=("Arial", 14), command=self.update_details).pack(pady=20)
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.admin_dashboard).pack(pady=10)

    def update_details(self):
        property_id = self.property_update_Entry.get()
        availability = self.availability_combobox.get()

        if property_id and availability:
          try:
            property_id = int(property_id)  # Ensure it's a valid number
            self.property_manager.update_properties(property_id, availability)
            self.admin_dashboard()  # Return to the admin dashboard
          except ValueError:
            messagebox.showerror("Error", "Please enter a valid property ID.")
        else:
         messagebox.showerror("Error", "All fields are required!")

    def view_properties(self):
        self.clear_screen()
# Fetch all bookings from the database
        properties = self.property_manager.list_properties()
        query = "SELECT * FROM customer_booking_info"
        bookings = self.db.fetch_all(query)

        tk.Label(self.root, text="Property List", font=("Arial", 20)).pack(pady=20)

        # Table headers
        headers = ["Property ID", "Type", "Location", "Price", "Status"]
        header_frame = tk.Frame(self.root, bg="lightblue")
        header_frame.pack(pady=5)
        for i, header in enumerate(headers):
            tk.Label(header_frame, text=header, font=("Arial", 12, "bold"),bg="green", width=15, anchor="w").grid(row=0, column=i)

        # Populate the bookings in the table
        if properties:
            for row_num, booking in enumerate(properties):
                for col_num, value in enumerate(booking):
                    tk.Label(header_frame, text=value, font=("Arial", 12), width=15, anchor="w").grid(row=row_num + 1, column=col_num)
        else:
            tk.Label(self.root, text="No Properties Found.", font=("Arial", 14)).pack(pady=10)

        # Back button
        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack(pady=20)
#---------------------------------DISPLAY JOB LIST-----------------------   
    def view_all_jobs(self):
      self.clear_screen()
      query = "SELECT * FROM manpower_jobs"
      manpower = self.db.fetch_all(query)

      tk.Label(self.root, text="JOB DETAILS", font=("Arial", 20)).pack(pady=20)

    # Table headers
      headers = ["JOB ID", "TITLE", "DESCRIPTION", "POSTED DATE"]
      header_frame = tk.Frame(self.root, bg="lightblue")
      header_frame.pack(pady=5)
      for i, header in enumerate(headers):
          tk.Label(header_frame, text=header, font=("Arial", 12, "bold"), bg="green", width="20", anchor="w").grid(row=0, column=i)

    # Scrollable frame for job details
      frame_canvas = tk.Frame(self.root)
      frame_canvas.pack(fill="both", expand=True, padx=10, pady=10)
      canvas = tk.Canvas(frame_canvas)
      scrollbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
      scrollable_frame = tk.Frame(canvas)

      scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
      )

      canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
      canvas.configure(yscrollcommand=scrollbar.set)

      canvas.pack(side="left", fill="both", expand=True)
      scrollbar.pack(side="right", fill="y")

    # Populate the jobs in the scrollable frame
      if manpower:
        for row_num, job in enumerate(manpower):
            tk.Label(scrollable_frame, text=job[0], font=("Arial", 12), width=15, anchor="w").grid(row=row_num, column=0)
            tk.Label(scrollable_frame, text=job[1], font=("Arial", 12), width=15, anchor="w").grid(row=row_num, column=1)
            # Use a Text widget for multi-line description
            text_widget = tk.Text(scrollable_frame, font=("Arial", 12), wrap="word", height=3, width=30)
            text_widget.insert("1.0", job[2])
            text_widget.configure(state="disabled")
            text_widget.grid(row=row_num, column=2)
            tk.Label(scrollable_frame, text=job[3], font=("Arial", 12), width=15, anchor="w").grid(row=row_num, column=3)
      else:
        tk.Label(self.root, text="No jobs found.", font=("Arial", 14)).pack(pady=10)

    # Back button
      tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack(pady=20)


#------------------------------------DISPLAY JOB LIST END-----------------------  

    def user_dashboard(self):
        self.clear_screen()
        tk.Label(self.root, text="USER DASHBOARD", font=("Arial", 20)).pack(pady=20)
        tk.Button(self.root, text="View Hotels", font=("Arial", 14), command=self.view_hotels).pack(pady=10)
        tk.Button(self.root, text="Book Hotel", font=("Arial", 14), command=self.view_hotels).pack(pady=10)
        tk.Button(self.root, text="View Properties", font=("Arial", 14), command=self.view_properties).pack(pady=10)
        tk.Button(self.root, text="Logout", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)
#---------------------------------------------------------------------------------
    def view_hotels(self):
        hotels = self.hotel_manager.list_hotels()
        self.clear_screen()

        tk.Label(self.root, text="Available Hotels", font=("Arial", 20)).pack(pady=20)
        hotel_frame = tk.Frame(self.root, bg="lightblue")
        hotel_frame.pack(pady=10)

        for hotel in hotels:
            hotel_name = hotel[1]
            hotel_button = tk.Button(hotel_frame, text=hotel_name, font=("Arial", 14), width=30, command=lambda hotel_id=hotel[0]: self.view_hotel_details(hotel_id))
            hotel_button.pack(pady=5)

        tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)

    def view_hotel_details(self, hotel_id):
        hotel_details = self.hotel_manager.list_hotel(hotel_id)
        if hotel_details:
            self.clear_screen()
            hotel_name = hotel_details[1]
            location = hotel_details[3]
            per_day_cost = hotel_details[4]
            status = hotel_details[5]

            tk.Label(self.root, text=f"Details of {hotel_name}", font=("Arial", 20)).pack(pady=20)
            tk.Label(self.root, text=f"Location: {location}", font=("Arial", 14)).pack(pady=10)
            tk.Label(self.root, text=f"Per Day Cost: {per_day_cost}", font=("Arial", 14)).pack(pady=10)
            tk.Label(self.root, text=f"Status: {status}", font=("Arial", 14)).pack(pady=10)
            tk.Button(self.root, text="BOOK NOW", font=("Arial", 14), command=lambda: self.booking_details(hotel_id)).pack(pady=10)
            tk.Button(self.root, text="Back", font=("Arial", 14), command=self.create_main_menu).pack(pady=10)
            
        else:
            messagebox.showerror("Error", "Hotel not found. Please try again.")
    
    def booking_details(self,hotel_id):
            self.hotel_manager.list_hotel(hotel_id)
            self.clear_screen()
            tk.Label(self.root, text="Enter your details to book", font=("Arial", 14)).pack(pady=10)    
            self.first_name_label=tk.Label(self.root, text="Your First Name", font=("Arial", 14))
            self.first_name_label.pack()  
            self.first_name_entry = tk.Entry(self.root, font=("Arial", 14))
            self.first_name_entry.pack(pady=5)          
            self.first_name_label=tk.Label(self.root, text="Your Last Name", font=("Arial", 14))
            self.first_name_label.pack()
            self.last_name_entry = tk.Entry(self.root, font=("Arial", 14))
            self.last_name_entry.pack(pady=5)            
            self.first_name_label=tk.Label(self.root, text="Country", font=("Arial", 14))
            self.first_name_label.pack()
            self.country_entry = tk.Entry(self.root, font=("Arial", 14))
            self.country_entry.pack(pady=5)         
            self.first_name_label=tk.Label(self.root, text="Email", font=("Arial", 14))
            self.first_name_label.pack()
            self.email_entry = tk.Entry(self.root,font=("Arial", 14))
            self.email_entry.pack(pady=5)
           
            self.first_name_label=tk.Label(self.root, text="How many Days", font=("Arial", 14))
            self.first_name_label.pack()
            self.days_entry = tk.Entry(self.root,font=("Arial", 14))
            self.days_entry.pack(pady=5)

            tk.Button(self.root, text="Book Now", font=("Arial", 14), command=lambda: self.book_hotel(hotel_id)).pack(pady=20)
            tk.Button(self.root, text="Back", font=("Arial", 14), command=lambda: self.view_hotels()).pack(pady=20)
        
#---------------------------------BOOKING HOTEL METHOD---------------------------      
    def book_hotel(self, hotel_id):
        # Retrieve user inputs
        fname = self.first_name_entry.get()
        lname = self.last_name_entry.get()
        country = self.country_entry.get()
        email = self.email_entry.get()
        days_ = self.days_entry.get()

        if fname and lname and country and email and days_:
            try:
                days_ = int(days_)
                self.hotel_manager.hotel_booking(hotel_id, fname, lname, country, email, days_)
                self.create_main_menu()  # Go back to main menu after booking
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number of days.")
        else:
            messagebox.showerror("Error", "Please fill all the details.")


    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ---------------------------------- Hotel Method End here ------------------        
#---------------------------------------------------------------------------------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------------------------- Main Application ---------------------------
if __name__ == "__main__":
    # Connect to the database
    db = Database(host="localhost", user="root", password="", database="realestatedb")
    customer_manager=customer(db)
    hotel_manager=hotel(db,customer_manager)
    property_manager=RealStateProperty(db)
    # Create main application window
    root = tk.Tk()
    app = Application(root, db,hotel_manager,property_manager)
    root.mainloop()
