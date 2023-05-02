import tkinter
import customtkinter
from CTkMessagebox import CTkMessagebox
import os

customtkinter.set_appearance_mode('light')
customtkinter.set_default_color_theme('green')

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('PickMEal')
        self.geometry('1280x720')
        self.config(pady=40)
        self.grid_columnconfigure((0), weight=1)

        #create the main label
        self.greeting = customtkinter.CTkLabel(self, text='Welcome to PickMEal', 
                                               anchor='center', font=('Facit', 65),
                                               text_color='SpringGreen2')
        self.greeting.grid(row=0, column=0, columnspan=1, padx=40, pady=5)

        #create a label with a brief description
        self.description = customtkinter.CTkLabel(self, 
                                                   text='Your custom meal picker!',
                                                   font=('Facit', 20))
        self.description.grid(row=1, column=0, columnspan=1)

        #create an entry for new input
        self.new_meals = customtkinter.CTkEntry(self, width=500, placeholder_text='Enter one or multiple meals, separated by a comma')
        self.new_meals.grid(row=2, column=0, columnspan=1, pady=20)

        #create a button to store the entry input
        self.save_btn = customtkinter.CTkButton(self, text='Save', command=self.save_meals)
        self.save_btn.grid(row=3,column=0, padx=20, pady=10)

        #create a button to delete an existing meal from the saved_meals.txt
        self.del_btn = customtkinter.CTkButton(self, text='Delete', command=self.del_meals)
        self.del_btn.grid(row=3, column=1, padx=20, pady=10)
    
    def save_meals(self):
        user_input = self.new_meals.get()
        if len(user_input) > 0:
            with open('saved_meals.txt', 'a') as file:
                file.write(f'{user_input}\n')
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
