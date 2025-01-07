"""
Created on Tue Dec 17 00:27:21 2024

@author: naomichellsea
"""

"""
Assessment 2 - DDA
Naomeal
For this assignment you are tasked with developing an application that makes use of 
data retrieved from an API. Your application should aim to demonstrate a range of programming 
techniques introduced over the course of CodeLab I and CodeLab II, including use of functions 
and where appropriate object oriented programming and GUI.
The final application should be delivered via a functioning interactive GUI built using Tkinter. 
This GUI should allow the user to interact via mouse and/or keyboard input.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import pygame
import io
import os


class Naomeal:
    def __init__(self, root):
        self.root = root
        self.root.title("Naomeal")
        self.root.geometry("850x750")
        self.bg_color = "#ffffff" #background colour for main gui page
        self.card_color = "#f7f7f7"
        self.categoryicons() #background image for different pages
        self.favorites = []  #empty list to store favourite meals
        self.content_frame = tk.Frame(self.root, bg=self.bg_color) #add frame to hold content for smooth transitions
        self.content_frame.pack(fill="both", expand=True)
        self.categorypagebg() 
        self.welcomepage()
        self.welcomepagebg()
        self.card_color = "#ffffff"
        self.meal_label = None
        self.bg_music() #background music

#function to add background music
    def bg_music(self):
        """Initialize and play background music."""
        pygame.mixer.init()
        music_file = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/resto jazz.mp3" 
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.2)  #volume to control the music
        pygame.mixer.music.play(-1)  #play the music in loop

#First page for welcoming the users to my app
    def welcomepage(self):
        """Sets the background image and creates the homepage with a 'Proceed' button."""
        self.welcomepagebg()  #background image for this page
        #clear previous content to go to next page
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        #proceed button clickable to move to next page
        startbutton = tk.Button(self.content_frame, text="Next", command=self.categorypage, 
                                font=("Helvetica", 16), bg="#6b0707", fg="#6b0707", relief="flat")
        startbutton.bind("<Button-1>", lambda e, cmd=self.categorypage: [self.buttonsound(), cmd()])
        startbutton.place(relx=0.21, rely=0.868, anchor="center")

    def welcomepagebg(self):
        """Sets the background image for the current page."""
        image_path = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/home.png"  
        try:
            backimg = Image.open(image_path)
            backimg = backimg.resize((900, 750), Image.LANCZOS)  #resize the image to fit the gui window
            backimg = ImageTk.PhotoImage(backimg)
            #background label to place it in frame
            bglabel = tk.Label(self.content_frame, image=backimg)
            bglabel.place(relwidth=1, relheight=1)  #ensures it covers the whole frame
            #prevents garbage collection
            self.content_frame.bg_image = backimg  #store the image reference
            bglabel.lower() #put the background to the back of other widgets so it overlap
        except FileNotFoundError:
            print(f"No Background Image {image_path}")


#Second page for letting the users choose their desired catergory 
    def categorypage(self):
        """Directly navigates to the next page content."""
        #Clear the current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.categorypagebg() #set the bg image for next page
        self.categoryicons()  #clickable image button for pages.

    def categorypagebg(self):
        """Sets the background image within the content frame."""
        image_path = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/main.png"
        try:
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((900, 750), Image.LANCZOS)  #resizing the image to fit the window
            bg_image = ImageTk.PhotoImage(bg_image)
            #create the background label and place it to content frame
            background_label = tk.Label(self.content_frame, image=bg_image)
            background_label.place(relwidth=1, relheight=1)  #ensures image covers the entire frame
            self.root.bg_image = bg_image  #prevents garbage collection
            background_label.lower()  #put the background to the back of other widgets so it overlap
        except FileNotFoundError:
            print(f"No Background Image {image_path}")

    def categoryicons(self):
        #Creates three clickable image buttons in a zigzag layout.
        icon_paths = [
            "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/1.png",
            "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/2.png",
            "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/3.png",
        ]
        commands = [
            self.randommeal,
            self.dishespagetwo,
            self.ingredientmeal,
        ]
        positions = [(0.13, 0.45), (0.78, 0.62), (0.25, 0.97)]
        for i, (path, command, pos) in enumerate(zip(icon_paths, commands, positions)):
            try:
                icon = Image.open(path).resize((550, 300), Image.LANCZOS)
                icon = ImageTk.PhotoImage(icon)
                button = tk.Label(self.root, image=icon, cursor="hand2", bd=0, relief="flat")
                button.image = icon  #store image references
                button.place(relx=pos[0], rely=pos[1], anchor="center")
                button.bind("<Button-1>", lambda e, cmd=command: [self.buttonsound(), cmd()])
                button.bind("<Enter>", lambda e, btn=button, path=path: self.iconcategoryhover(btn, path, (560, 310)))
                button.bind("<Leave>", lambda e, btn=button, path=path: self.iconcategoryhover(btn, path, (550, 300)))
            except FileNotFoundError:
                print(f"No Icon Image {path}")


#Third page for letting the users explore random meal
    def randommeal(self):
        self.clearswidgets()  #Clear previous widgets
        
        image_path = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/wang.png"  #Set background image
        try:
            bgimg = Image.open(image_path)
            bgimg = bgimg.resize((900, 750), Image.LANCZOS)  #resizing the image
            bgimg = ImageTk.PhotoImage(bgimg)
            bglabel = tk.Label(self.root, image=bgimg)
            bglabel.place(relwidth=1, relheight=1)
            self.root.bgimg = bgimg  #prevents garbage collection
            bglabel.lower()  
        except FileNotFoundError:
            print(f"No Background Image {image_path}")

        #Meal card frame, creates new frame everytime.
        self.mealframe = tk.Frame(self.root, bg=self.card_color, relief="raised", bd=3)
        self.mealframe.place(relx=0.5, rely=0.53, anchor="center", width=700, height=500)

        #random meal "search" button
        searchbtn = tk.Button(self.mealframe, text="Make Me Yummy Meal!", font=("Helvetica", 12), bg="#6b0707", command=self.searchclicked)
        searchbtn.pack(side="left", padx=20, pady=10)

        #add to favourites button
        self.myfav = tk.Button(self.mealframe, text="My Favourite", font=("Helvetica", 12), bg="#6b0707", state="disabled", command=self.myfav)
        self.myfav.pack(side="right", padx=20, pady=10)

    def searchclicked(self):
        #called when user search random meal button is clicked
        mealname, mealdescr, mealimg = self.randommealapi()
        if mealname:
            #update the meal card with the meal details from the API
            self.resultsmeal(mealname, mealdescr, mealimg)
            self.mealname = mealname  #storing the meal name for later
            self.myfav.config(state="normal")  #enable the add to favourties button from disable.
        else:
            messagebox.showerror("Failed to make you a meal ;< ")

    def myfav(self):
        if hasattr(self, "mealname") and self.mealname:  # Check if mealname exists
            if self.mealname not in self.favorites:
                self.favorites.append(self.mealname)
                messagebox.showinfo("Favorites", f"'{self.mealname}' added to favorites! ❤️ ")
            else:
                messagebox.showinfo("Favorites", f"'{self.mealname}' is already in your favorites.")
        else:
            messagebox.showerror("No meal has been selected ;/")
    
    def resultsmeal(self, mealname, mealdescr, mealimg):
        # Create a new meal label every time to avoid issues with destroying/recreating
        if hasattr(self, 'meal_label') and self.meal_label: #creates new meal label everytime to avoid destroying
            self.meal_label.destroy()  #destroy old label to create new one
        
        self.meal_label = tk.Label(self.mealframe, text=f"{mealname}\n\n{mealdescr}",
                                bg=self.card_color, font=("Helvetica", 12), wraplength=480)
        self.meal_label.pack(pady=20)
        try:
            mealpic = Image.open(requests.get(mealimg, stream=True).raw)
            mealpic = mealpic.resize((150, 150), Image.LANCZOS)
            mealpic = ImageTk.PhotoImage(mealpic)
            image_label = tk.Label(self.mealframe, image=mealpic)
            image_label.image = mealpic  #prevents garbage collection
            image_label.pack(side="top", pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

    def randommealapi(self):
        #fetch random meal from API
        try:
            url = "https://www.themealdb.com/api/json/v1/1/random.php"
            response = requests.get(url, timeout=10)  #timeout before error handling
            response.raise_for_status()  #it raise and error for HTTP issues
            data = response.json()
            #extract meak details from API
            meal = data['meals'][0]
            mealname = meal['strMeal']
            mealdescr = meal['strInstructions']
            mealimg = meal['strMealThumb']
            return mealname, mealdescr, mealimg
        except Exception as e:
            print(f"Error fetching meal data: {e}")
            return None, None, None

        
#4th page for user to choose their desired type of dishes.
    def dishespagetwo(self):
        self.clearswidgets()
        image_path = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/samp.png" #bg image for this new frame
        try:
            bgimgtwo = Image.open(image_path)
            bgimgtwo = bgimgtwo.resize((900, 750), Image.LANCZOS)  #LANCZOS instead of ANTIALIAS
            bgimgtwo = ImageTk.PhotoImage(bgimgtwo)
            background_label = tk.Label(self.root, image=bgimgtwo)
            background_label.place(relwidth=1, relheight=1)
            self.root.bgimgtwo = bgimgtwo  #prevents garbage collection
            background_label.lower()
        except FileNotFoundError:
            print(f"No Background Image{image_path}")        
        dishes = ["Beef", "Chicken", "Dessert", "Pasta", "Seafood", "Vegetarian"]
        #this is the category cards in grid layout
        cards = []  #storing card reference for later use
        for i, category in enumerate(dishes):
            card = tk.Frame(self.root, bg=self.card_color, relief="raised", bd=2, highlightthickness=1)
            card.place(relx=(0.2 + (i % 3) * 0.3), rely=(0.2 + (i // 3) * 0.3), width=200, height=200)
            #rounded corners for shadow effect
            card.configure(highlightbackground="#ccc", highlightcolor="#ccc", relief="flat")
            card["borderwidth"] = 2  #visible border for the card
            #load the PNG image
            icon = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/food.png"  #replace with you image file path
            icnimg = Image.open(icon)
            icnimg = icnimg.resize((80, 80), Image.LANCZOS)  #resize the image if needed
            icnpic = ImageTk.PhotoImage(icnimg)
            #creating label to display the image
            iconplace = tk.Label(card, image=icnpic, bg=self.card_color)
            iconplace.image = icnpic  
            iconplace.pack(pady=10)
            label = tk.Label(card, text=category, bg=self.card_color, font=("Helvetica", 14, "bold"))
            label.pack(side="top", pady=10)
            #button with hover animation
            btn = tk.Button(
                card,
                text="Explore",
                bg="#A02334",
                fg="#FFAD60",
                font=("Helvetica", 12),
                command=lambda cat=category: self.dishesclicked(cat)
            )
            btn.pack(side="bottom", pady=10)
            cards.append(card)  #save references for later use
    
    def dishesclicked(self, category):
        #handles the users click options on a dishesclicked.
        meals = self.dishesapi(category)   #fetch filtered meals for the selected category.
        self.clearswidgets()  #Clear the current content
        self.dishesresultspg(meals, category)  #display results in grid frame.
        self.dishesani()  #apply animations for new page
    
    def dishesresultspg(self, meals, category):
        self.clearswidgets()
        image_path = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/bem.png" #bg image for this new frame
        try:
            bgimgtwo = Image.open(image_path)
            bgimgtwo = bgimgtwo.resize((900, 750), Image.LANCZOS)  #LANCZOS instead of ANTIALIAS
            bgimgtwo = ImageTk.PhotoImage(bgimgtwo)
            background_label = tk.Label(self.root, image=bgimgtwo)
            background_label.place(relwidth=1, relheight=1)
            self.root.bgimgtwo = bgimgtwo  #prevents garbage collection
            background_label.lower()
        except FileNotFoundError:
            print(f"No Background Image{image_path}")    
        rows = 3  # 3 rows in the grid
        columns = 3  # 3 columns in the grid
        dishescard = []

        for i, meal in enumerate(meals):
            row = i // columns
            col = i % columns

            #each meal card i put with rounded corners and a shadow effect so it will not look plain
            card = tk.Frame(
                self.root, 
                bg="#ffffff", 
                relief="groove", 
                bd=2, 
                highlightthickness=0
            )
            card.grid(row=row, column=col, padx=(50, 0), pady=(50, 0))
            card.configure(highlightbackground="#e0e0e0", highlightcolor="#e0e0e0")
            card["borderwidth"] = 2

            #for font and alignment
            label = tk.Label(
                card, 
                text=meal['strMeal'], 
                bg="#ffffff", 
                font=("Helvetica", 14, "bold"), 
                fg="#333333", 
                anchor="center", 
                wraplength=200  # i added wrapping text if the text is too long so it will look organize.
            )
            label.pack(side="top", pady=15)
            # Save the card references
            dishescard.append(card)

    def explorebutton(self, meal):
        """Handle when the user clicks to explore a meal."""
        print(f"Exploring meal: {meal['strMeal']}")
        #use the API to get the detailed meal data using the meal
        meal_id = meal.get('idMeal')  #Extract the meal id
        if not meal_id:
            print("Error: Meal ID not found!")
            return

        #get meal details using API meal ids
        mealdetails = self.dishesapi(meal_id)
        if mealdetails:
            print(f"Fetched ! {mealdetails}")
        else:
            #message box for the errors to notify
            root = tk.Tk()
            root.withdraw()  #hiding the root window
            messagebox.showerror("Error", "No Details Found")

    def dishesapi(self, category):
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            meals = response.json().get('meals', [])
            return meals
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            self.show_error_message("Failed to load meals. Please try again later.")
            return []
        
    def dishesani(self, options):
        """Display options in a 5-column grid with slide-in animations."""
        self.clearswidgets()  #to clear the existing widgets in the exising window

        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(fill="both", expand=True)

        #display options in 5 column grid
        for i, option in enumerate(options):
            card = tk.Frame(container, bg=self.card_color, relief="raised", bd=2)
            card.grid(row=i // 5, column=i % 5, padx=3, pady=3, sticky="nsew")

            #content to the card such as meal name
            option_name = option.get("strMeal", "Unknown")
            label = tk.Label(card, text=option_name, bg=self.card_color, font=("Helvetica", 12, "bold"))
            label.pack(pady=2)

            #explore button that are clickable 
            explore_button = tk.Button(card, text="Explore", command=lambda opt=option: self.explorebutton(opt))
            explore_button.pack(pady=2)

            #slide in animation in the card
            self.root.after(100 * i, lambda widget=card: self.transitionsin(widget))

    def transitionsin(self, widget, duration=500):
        """Animates a widget sliding in and ensures it stays in its final position."""
        widget.update_idletasks()  #to update the widget geometry
        x_start = -200  #starting position
        y_start = widget.winfo_y() 
        x_end = widget.winfo_x() 

        steps = 20  #the number of animation steps
        dx = (x_end - x_start) / steps  #distance to move per step

        def slide_step(step):
            """Move the widget one step closer to its final position."""
            nonlocal x_start
            if step <= steps:
                x_start += dx
                widget.place(x=int(x_start), y=y_start)  #adjust widgets gradually
                self.root.after(duration // steps, lambda: slide_step(step + 1))
            else:
                widget.place(x=x_end, y=y_start)  #ensures it stays at the final position because of animation

        #to start the animation
        slide_step(0)


#5th page for user to enter their existing ingredients to make dishes.
    def ingredientmeal(self):
        self.clearswidgets()
        image_path = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/festival.png" #sets another background image for this frame
        try:
            bgimgthree = Image.open(image_path)
            bgimgthree = bgimgthree.resize((900, 750), Image.LANCZOS)  #resize the image if needed
            bgimgthree = ImageTk.PhotoImage(bgimgthree)
            bglabelthree = tk.Label(self.root, image=bgimgthree) 
            bglabelthree.place(relwidth=1, relheight=1)
            self.root.bgimgthree = bgimgthree   #prevents garbage collection
            bglabelthree.lower()
        except FileNotFoundError:
            print(f"No Background Image {image_path}")
        #search bar user can use
        entersearch = tk.Label(self.root, text="Enter Ingredient:", font=("Helvetica", 16), bg=self.bg_color)
        entersearch.place(relx=0.2, rely=0.2, anchor="center")
        ingredentry = tk.Entry(self.root, font=("Helvetica", 14))
        ingredentry.place(relx=0.5, rely=0.2, width=300, anchor="center")
        searchbtn = tk.Button(self.root, text="Search", font=("Helvetica", 12), command=lambda: self.ingredientmealapi(ingredentry.get()))
        searchbtn.bind("<Button-1>", lambda e, cmd=self.categorypage: [self.buttonsound(), cmd()])
        searchbtn.place(relx=0.8, rely=0.2, anchor="center")
        #results frame area
        self.resultsarea = tk.Frame(self.root, bg=self.bg_color)
        self.resultsarea.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)
        #canvas for the results frame
        frame = tk.Canvas(self.resultsarea, bg=self.bg_color)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        #scroll bar for the results frame
        scrollbar = tk.Scrollbar(self.resultsarea, orient=tk.VERTICAL, command=frame.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #configure the canvas with scrollbar
        frame.configure(yscrollcommand=scrollbar.set)
        #bind canvas with scrollbar
        frame.bind("<Configure>", lambda e: frame.configure(scrollregion=frame.bbox("all")))

    def displayresult(self, data):
        """Display results in the results frame."""
        for widget in self.resultsarea.winfo_children(): #clear orevious resukts in frane
            widget.destroy()

        meals = data.get("meals", [])  #check if there is a meal
        if not meals:
            no_results_label = tk.Label(self.resultsarea, text="No results found", font=("Helvetica", 14), bg=self.bg_color)
            no_results_label.pack(pady=10)
        else:
            for idx, item in enumerate(meals): #Display the meal recipe
                recipe_name = item.get("strMeal", "No name")
                recipe_image_url = item.get("strMealThumb", "")
                
                #show the recipe name
                recipe_label = tk.Label(self.resultsarea, text=recipe_name, font=("Helvetica", 14), bg=self.bg_color)
                recipe_label.grid(row=idx, column=0, pady=5, padx=10, sticky="w")

            if recipe_image_url:
                try:
                    img_response = requests.get(recipe_image_url)
                    img_response.raise_for_status()  #to make sure that request is successful
                    img_data = io.BytesIO(img_response.content)  #it converts bytes into a file-like object
                    img = Image.open(img_data)  
                    img = img.resize((100, 100), Image.LANCZOS)  
                    img = ImageTk.PhotoImage(img)
                    img_label = tk.Label(self.resultsarea, image=img, bg=self.bg_color)
                    img_label.image = img  
                    img_label.grid(row=idx, column=1, pady=5, padx=10)
                except requests.exceptions.RequestException as e:
                    print(f"Error image fetch {e}")
                except Exception as e:
                    print(f"Error image loading {e}")

        #example onyl to d isplay each recipe 
        for idx, item in enumerate(data.get("recipes", [])):
            recipe_name = item.get("name", "No name")
            recipe_label = tk.Label(self.resultsarea, text=recipe_name, font=("Helvetica", 14), bg=self.bg_color)
            recipe_label.grid(row=idx, column=0, pady=5, padx=10, sticky="w")

    def ingredientmealapi(self, ingredient):
        api_url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                self.displayresult(data)
            else:
                print(f"Error API fetch {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error API request{e}")
#end of function pages

#general functions
    def clearswidgets(self):
        for widget in self.root.winfo_children(): #clears all the widgets from the screen
            widget.destroy()

    def buttonsound(self):
        """Plays a sound effect when a button is clicked."""
        btnsoundpath = "/Users/naomichellsea/Advance Programming/Assessment 2 - Naomeal/Evidence of Design/click-21156.mp3"  
        try:
            pygame.mixer.init()
            pygame.mixer.Sound(btnsoundpath).play()
        except Exception as e:
            print(f"Error playing sound: {e}")

    def iconcategoryhover(self, button, path, size):
        """Handles hover effect for buttons."""
        try:
            icon = Image.open(path).resize(size, Image.LANCZOS)
            button.image = ImageTk.PhotoImage(icon)
            button.configure(image=button.image)
        except FileNotFoundError:
            print(f"Hover icon not found at {path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Naomeal(root)
    root.mainloop()  #to start the tkinter with all the functions.
