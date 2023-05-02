import tkinter
import customtkinter
from CTkMessagebox import CTkMessagebox
import os

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('green')
BG_COLOR = 'ghost white'

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('PickMEal')
        self.geometry('720x480')
        self.config(pady=60, background=BG_COLOR)

        #create the main label
        self.greeting = customtkinter.CTkLabel(self, text='Welcome to PickMEal', 
                                               anchor='center', 
                                               font=('Facit', 65),
                                               text_color='SpringGreen2',
                                               bg_color=BG_COLOR)
        self.greeting.pack()

        #create a label with a brief description
        self.description = customtkinter.CTkLabel(self, 
                                                   text='Your custom meal picker!',
                                                   font=('Facit', 20),
                                                   bg_color=BG_COLOR)
        self.description.pack()

        #create a label with instructions   
        self.instructions = customtkinter.CTkLabel(self,
                                                   text='PickMEal allows you to keep a list of all meals you can cook and will return a random one so you no longer have to think about what you want to cook for dinner.',
                                                    width=600,
                                                     height=100,
                                                     font=('Facit', 18),
                                                     bg_color=BG_COLOR,
                                                     wraplength=500)
        self.instructions.pack(pady=(75,10))

        #create a frame for homepage buttons
        self.home_frame = customtkinter.CTkFrame(self, fg_color=BG_COLOR)
        self.home_frame.pack()

        #create 2 buttons to give the user a choice how to proceed
        pick_meal_btn = customtkinter.CTkButton(self.home_frame, 
                                                text="Get a random meal", 
                                                command=self.log_meals, 
                                                font=('Facit', 18),
                                                height=40,
                                                width=175
                                                )
        pick_meal_btn.grid(column=0, row=1, padx=10)  

        add_new_btn = customtkinter.CTkButton(self.home_frame, 
                                              text='Add new meals', 
                                              command=self.log_meals,
                                              font=('Facit', 18),
                                              height=40,
                                              width=175
                                              )                    
        add_new_btn.grid(column=1, row=1, padx=10)
        


    def log_meals(self):
        #Destroy previous buttons and instructions
        self.instructions.destroy()
        self.home_frame.destroy()

        #create new instructions
        self.instructions = customtkinter.CTkLabel(self,
                                                   text='Enter one or multiple meals separated by a comma, or edit your list of existing meals.',
                                                   width=600,
                                                   height=100,
                                                   font=('Facit', 18),
                                                   bg_color=BG_COLOR,
                                                   wraplength=500)
        self.instructions.pack(pady=(70,0))

        #create an entry for new input
        self.new_meals = customtkinter.CTkEntry(self, width=500)
        self.new_meals.pack(pady=(0, 20))

        #create a frame for the two buttons
        self.frame = customtkinter.CTkFrame(self, fg_color=BG_COLOR)
        self.frame.pack()

        #create a button to store the entry input
        self.save_btn = customtkinter.CTkButton(self.frame, text='Save', command=self.save_meals)
        self.save_btn.grid(column=0, row=1, padx=10)

        #create a button to delete an existing meal from the saved_meals.txt
        self.del_btn = customtkinter.CTkButton(self.frame, text='Edit', command=self.del_meals)
        self.del_btn.grid(column=1, row=1, padx=10)

    def save_meals(self):
        user_input = self.new_meals.get()
        if len(user_input) > 0:
            with open('saved_meals.txt', 'a') as file:
                for meal in user_input.split(','): 
                    file.write(f'{meal.strip()}\n')
        else:
            CTkMessagebox(self, 
                          width=300,
                          title='Error', 
                          message="You haven't added any meals.", 
                          icon='warning',
                          )
    
    def del_meals(self):
        try:
            os.startfile('saved_meals.txt')
        except FileNotFoundError:
            CTkMessagebox(self, 
                          width=300,
                          title='Error', 
                          message='You have no saved meals!', 
                          icon='cancel')
            

program = GUI()
program.mainloop()
