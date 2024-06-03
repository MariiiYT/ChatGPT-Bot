from tkinter import *
import customtkinter
import openai
import os
import pickle

# Submit to ChatGPT
def speak():
	if chat_entry.get():
		# Define file name
		filename = "api_key"

		try:
			if os.path.isfile(filename):
				# Open the file
				input_file = open(filename, 'rb')

				# Load the data from the file into a variable
				stuff = pickle.load(input_file)

				# Query
				# Define the API key
				openai.api_key = stuff

				# Create instance
				openai.Model.list()

				# Define query
				response = openai.Completion.create(
					model = "gpt-3.5-turbo-instruct",
					prompt = chat_entry.get(),
					temperature = 0,
					max_tokens=60,
					top_p = 1.0,
					frequency_penalty=0.0,
					presence_penalty=0.0
					)

				my_text.insert(END, (response["choices"][0]["text"]).strip())
				my_text.insert(END, "\n\n")
			else:
				 # Create the file
				  input_file = open(filename, 'wb')
				  # Close it
				  input_file.close()
				  # Error message
				  my_text.insert(END, "\n\nKey required")

		except Exception as e:
			my_text.insert(END, f"\n\n There was an error\n\n{e}")
	else:
		my_text.insert(END, "\n\nHey, you forgot to type something")

# Clear screen
def clear():
	# Clear the main textbox
	my_text.delete(1.0, END)

	# Clear the query widget
	chat_entry.delete(0, END)

root = customtkinter.CTk()
root.title("ChatGPT Bot")
root.geometry('600x600')

# Set color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# Create frame
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

# Add text widget
my_text = Text(text_frame,
	bg="#343638",
	width=65,
	bd=1,
	fg="#d6d6d6",
	relief="flat",
	wrap=WORD,
	selectbackground='#1f538d')

my_text.grid(row=0,column=0)

# Do API stuff
def key():
	# Define file name
	filename = "api_key"

	try:
		if os.path.isfile(filename):
			# Open the file
			input_file = open(filename, 'rb')

			# Load the data from the file into a variable
			stuff = pickle.load(input_file)

			# Output stuff to our entry box
			api_entry.insert(END, stuff)
		else:
			 # Create the file
			  input_file = open(filename, 'wb')
			  # Close it
			  input_file.close()

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

# Save the key
def save_key():
	# Define the filename
	filename = "api_key"
	try:
		# Open the file
		output_file = open(filename, 'wb')

		# Throw data in the file
		pickle.dump(api_entry.get(), output_file)

		# Delete the entry box
		api_entry.delete(0, END)

		# Hide the API frame
		api_frame.pack_forget()
		# Resize the app
		root.geometry('600x600')

	except Exception as e:
		my_text.insert(END, f"\n\n There was an error\n\n{e}")

# Create scrollbar
text_scroll = customtkinter.CTkScrollbar(text_frame,
	command=my_text.yview)
text_scroll.grid(row=0,column=1, sticky="ns")

# Add the scrollbar
my_text.configure(yscrollcommand=text_scroll.set)

# Entry widget
chat_entry = customtkinter.CTkEntry(root,
	placeholder_text="Type something to ChatGPT...",
	width=535,
	height=50,
	border_width=2)
chat_entry.pack(pady=10)

# Create button frame
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

# Submit Button
submit_button = customtkinter.CTkButton(button_frame,
	text="Send",
	command=speak)
submit_button.grid(row=0, column=0, padx=25)

# Clear Button
clear_button = customtkinter.CTkButton(button_frame,
	text="Clear the screen",
	command=clear)
clear_button.grid(row=0, column=1, padx=25)

# API Button
api_button = customtkinter.CTkButton(button_frame,
	text="Send a key",
	command=key)
api_button.grid(row=0, column=2, padx=25)

# Add API frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=10)

# Add API entry widget
api_entry = customtkinter.CTkEntry(api_frame,
	placeholder_text="Enter API key here",
	width=350, height=50, border_width=1)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# API button
api_save_button = customtkinter.CTkButton(api_frame,
	text="Save Key",
	command=save_key)
api_save_button.grid(row=0, column=1, padx=10)

root.mainloop()
