import tkinter
import customtkinter
from CTkMessagebox import CTkMessagebox
import os
import random
import time

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('green')
BG_COLOR = 'ghost white'

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('PickMEal')
        self.geometry('720x480')
        self.config(background=BG_COLOR)
        self.resizable(False, False)
        self.iconbitmap('images\program_icon.ico')
        
        #create the main label
        self.greeting = customtkinter.CTkLabel(self, text='Welcome to PickMEal', 
                                               anchor='center', 
                                               font=('Facit', 65),
                                               text_color='SpringGreen2',
                                               bg_color=BG_COLOR)
        self.greeting.pack(pady=(50, 0))

        #create a label with a brief description
        self.description = customtkinter.CTkLabel(self, 
                                                   text='Your custom meal picker!',
                                                   font=('Facit', 20),
                                                   bg_color=BG_COLOR)
        self.description.pack()
        self.home_screen()



    def home_screen(self):
        #destroy d screen if it exists
        try:
            self.frame.destroy()
            self.instructions.destroy()
            self.new_meals.destroy()
        except:
            pass

        try:
            self.meal_choice.destroy()
            self.bon_apetit.destroy()
        except:
            pass

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
        get_meal_btn = customtkinter.CTkButton(self.home_frame, 
                                                text="Get a random meal", 
                                                command=self.get_random_meal, 
                                                font=('Facit', 18),
                                                height=40,
                                                width=175
                                                )
        get_meal_btn.grid(column=0, row=1, padx=10)  

        add_new_btn = customtkinter.CTkButton(self.home_frame, 
                                              text='Add new meals', 
                                              command=self.log_meals,
                                              font=('Facit', 18),
                                              height=40,
                                              width=175
                                              )                    
        add_new_btn.grid(column=1, row=1, padx=10)
    
    def get_random_meal(self):
        
        #Destroy previous buttons and instructions
        self.instructions.destroy()
        self.home_frame.destroy()
        self.rerolls_left = 1
        def print_meal():
            try:
                self.meal_choice.destroy()
                self.frame.destroy()
                self.bon_apetit.destroy()
            except:
                pass
            with open('saved_meals.txt', 'r') as file:
                all_meals = file.readlines()
                if len(all_meals) > 0:
                    self.meal_choice = customtkinter.CTkLabel(self,
                                                text=f"Today you'll be making {random.choice(all_meals)}",
                                                width=600,
                                                height=100,
                                                font=('Facit', 22),
                                                bg_color=BG_COLOR,
                                                wraplength=500)
                    self.meal_choice.pack(pady=(75,10))                  
                    
                    self.bon_apetit = customtkinter.CTkLabel(self,
                                                        text='Bon Apetit!',
                                                        font=('Facit', 22),
                                                        bg_color=BG_COLOR,
                                                        wraplength=500)
                    self.bon_apetit.pack()   

                    #create a frame for the two buttons
                    self.frame = customtkinter.CTkFrame(self, fg_color=BG_COLOR)
                    self.frame.pack()

                    #create a button that allows the user to reroll the meal
                    self.reroll = customtkinter.CTkButton(self.frame, text=f'Reroll once', font=('Facit', 18), command=print_meal)
                    self.reroll.grid(column=1, row=1, padx=10)


                    if self.rerolls_left == 0:
                        self.reroll.configure(state='disabled')


                    #create a button that allows the user to go back to the home page
                        
                    self.back_button = customtkinter.CTkButton(self.frame, text='Back', font=('Facit', 18), command=self.home_screen)
                    self.back_button.grid(column=2, row=1, padx=10) 
                    
                    self.rerolls_left -= 1

                #if there are no saved meals the user is directed to the log_meals screen
                else:
                    CTkMessagebox(self, 
                            width=300,
                            height=150,
                            title='Error', 
                            message="You haven't added any meals yet. You can add some here.", 
                            )
                    self.log_meals()     

        print_meal()  








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
        self.instructions.pack(pady=(50,0))

        #create an entry for new input
        self.new_meals = customtkinter.CTkEntry(self, width=500)
        self.new_meals.pack(pady=(0, 20))

        #create a frame for the two buttons
        self.frame = customtkinter.CTkFrame(self, fg_color=BG_COLOR)
        self.frame.pack()

        #create a button to store the entry input
        self.save_btn = customtkinter.CTkButton(self.frame, text='Save', font=('Facit', 16), command=self.save_meals)
        self.save_btn.grid(column=0, row=1, padx=10)

        #create a button to delete an existing meal from the saved_meals.txt
        self.del_btn = customtkinter.CTkButton(self.frame, text='Edit', font=('Facit', 16), command=self.del_meals)
        self.del_btn.grid(column=1, row=1, padx=10)

        #create a button that allows the user to go back to the home page
          
        self.back_button = customtkinter.CTkButton(self.frame, text='Back', font=('Facit', 16), command=self.home_screen)
        self.back_button.grid(column=2, row=1, padx=10)

    def save_meals(self):
        #get user input 
        user_input = self.new_meals.get()
        if len(user_input) > 0:

            #read the file storing all meals
            with open('saved_meals.txt', 'r+') as file:
                all_meals = file.read().splitlines()
                for meal in user_input.split(','): 

                    #if the meal isn't already saved - save it
                    if meal not in all_meals:
                        file.write(f'{meal.strip()}\n')

            #clear the entry
            self.new_meals.delete(0, len(user_input))

        #in case the user tries to save an empty entry
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
