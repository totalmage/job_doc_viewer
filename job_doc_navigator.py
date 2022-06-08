"""
Program that opens and adds simple csv entries using tkinter to present the information
in a more user friendly format.

Easterling Carpenter

Work Table:
5/31/21 from 8:00PM CST to 12:00AM CST
    - Created the following functions: 
        - read_csv
        - make_window
        - generate_doc_section
        - add_doc
        - update_csv
        - main
    - Performed several manual tests to ensure the input would be correctly taken and stored

6/1/21 from 9:00PM CST to 11:00PM CST
    - Edited function read_csv to contain an exception to handle missing csv files
    - Added documentation to functions
    - Created Test function:
        - test_read_csv
        Unable to think of a way to test the global level functions and not sure how to 
        import to test the local functions.
    - Performed tests using test function

"""
from cProfile import label
from fileinput import filename
from logging import root
from pydoc import doc
from tkinter import BOTTOM, END, Entry, Tk, RIGHT, BOTH, RAISED, messagebox
import tkinter
from tkinter.ttk import Frame, Button, Style, Label
import datetime
import os

def read_csv():
    """Try to read in the data points into a dictionary from file jobs_doc.csv
    if it does not exist, it will skip reading the file and print a message to 
    the console and a the file will be generated as soon as update_csv() is called

    Parameters: None

    Return: dictionary with the info in the csv

    Additional notes: Tried to use a tkinter messagebox in the exception to notify user
    but there is strange bug that causes my messagebox to block text entry into the 
    entry field later on.
    """

    jobs_dict = {}
    filename = 'jobs_doc.csv'
    try:
        with open(filename, "rt") as jobfile:

            for line in jobfile:
                clean_line = line.strip()

                comma_index = clean_line.find(',')
                date_key = clean_line[:comma_index]
                descrip_value = clean_line[comma_index+1:]
                jobs_dict[date_key] = descrip_value
        print(f'File: {filename} successfully loaded into Documentation Viewer')
    except FileNotFoundError:
        # tkinter.messagebox.showinfo(title=f'File: {filename} not found', message='Will create file in directory: {os.getcwd()} once jobs are added.')
        print(f'File: {filename} not found... will create file in directory: {os.getcwd()} once jobs are added.')
    return jobs_dict

def make_window():
    """Utilize other methods in job_doc_navigator to 
    create a window with all necessary parts

    Parameters: None

    Return: none
    """
    root = Tk()
    root.geometry('1000x400')
    root.title('Job Documentation Log')
    job_dict = read_csv()

    def generate_doc_section(my_frame):
        COL_NAMES = ('Date Created', 'Description')

        for i, col_name in enumerate(COL_NAMES, start=1):
            Label(my_frame, text=col_name).grid(row=3, column=i, padx=40)
     
        for i, col in enumerate(job_dict, start=1):
            Label(my_frame, text=col).grid(row=4+i, column=1, padx=40)
            Label(my_frame, text=job_dict[col]).grid(row=4+i, column=2, padx=40)


    def add_doc(my_frame):
        text_box = Entry(my_frame, width=150)
        text_box.pack(pady= 10)

        def update_csv(doc):
            user_input = doc
            current_date_time = str(datetime.datetime.now())
            job_dict[current_date_time] = user_input
            to_append = current_date_time +',' +user_input +'\n'

            with open('jobs_doc.csv', 'a') as newsave:
                newsave.write(to_append)

                tkinter.messagebox.showinfo(message='Documentation Saved')
            text_box.delete(0, END)
            generate_doc_section(disp_jobs)   

        save_button = Button(my_frame, text='Save', command= lambda text = text_box.get() : update_csv(text))
        save_button.pack(pady= 10)

    disp_jobs = Frame(root)
    disp_jobs.pack()
    generate_doc_section(disp_jobs)

    disp_textfield = Frame(root)
    disp_textfield.pack(side = BOTTOM)
    doc_sect = Label(text='Document New Jobs Below')
    doc_sect.pack(side=BOTTOM)
    add_doc(disp_textfield)

    root.mainloop()

def main():
    make_window()

if __name__ == '__main__':
    main()