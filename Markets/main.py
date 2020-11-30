import tkinter as tk
from tkinter import Tcl
from tkinter import Canvas, Frame, Menu, Menubutton, Scrollbar, scrolledtext, Label, Button, StringVar
from tkinter.ttk import Treeview
from app_settings import HEIGHT, WIDTH, BGCOLOR
from get_info import get_indices, get_commodities, get_metals, get_gold_silver, get_news, get_bonds, get_countries, COUNTRIES
import webbrowser
import time
import json
import os.path



class AppGetInfo():
    def __init__(self, root=None):
        self.root = root
        self.root.title("Investing Help")
        self.root.minsize(WIDTH, HEIGHT)
        # self.root.maxsize(WIDTH, HEIGHT+800)
        self.__Frames = (Home, Indices, Commodities, Metals, News, GoldSilver, Bonds)
        self.create_widgets()
    
    def create_widgets(self):
        # Menu
        self.menu = Menu(self.root)
        self.menu.add_command(label="Home", command=lambda: self.show_frame("Home"))
        self.menu.add_command(label="Gold/Silver", command=lambda: self.show_frame("GoldSilver"))
        self.menu.add_command(label="Major Indices", command=lambda: self.show_frame("Indices"))
        self.menu.add_command(label="Metals", command=lambda: self.show_frame("Metals"))
        self.menu.add_command(label="Commodities", command=lambda: self.show_frame("Commodities"))
        self.menu.add_command(label="Bonds", command=lambda: self.show_frame('Bonds'))
        self.menu.add_command(label="News", command=lambda: self.show_frame("News"))
        self.root.config(m=self.menu)
        # Container where frames are going to be placed (root for other frames)
        self.container = Frame(self.root)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # For organizing frames
        # Creates the dictionary of frames (frame_class_name:frame_object)
        self.frames = {}
        for F in self.__Frames:
            frame_name = F.__name__
            frame = F(root=self.container, controller=self)
            self.frames[frame_name] = frame
            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("Home")

    def show_frame(self, frame_name):
        ''' Show the frame for the given frame name'''
        frame = self.frames[frame_name] # chooses the frame to prepare
        frame.set_up() # Creates the table/frame with the main data
        frame.tkraise() # Brings the frame to the front

class FrameWidget(Frame):
    def __init__(self, root, controller, get_data):
        ''' Shows all the major indeces and a link to other indices less important 
        get_data is the method that scrapes the web and returns the perfect dataframe'''
        Frame.__init__(self, root)
        self.root = root
        self.controller = controller
        self.get_data = get_data
        self.data_flag = False # to check whether the table already exists to avoid duplicates 
        self.sub_data_flag = False # same as the other but in use for frames(tabs) that have sub frames
        self.sub_frames = {} # incase there is the need for the objects to create subframes other than the table.

    def create_table(self, columns = ("last", "high", "low", "change", "pct_change")):
        self.treeScroll = Scrollbar(self) 
        tv = Treeview(self)
        tv['columns'] = columns
        tv.heading('#0', text='Index', anchor='w')
        tv.column('#0', anchor='w')

        for col in columns:
            if col == 'pct_change':
                text = '% Change' 
            else:
                head = col
                text = col.title()

            tv.heading(col, text=text)
            tv.column(col, anchor="center", width=100)
        
        self.treeview = tv
        self.treeScroll.configure(command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side="right", fill="y")
        self.treeview.pack(side="top", fill="both", expand=True )

    def get_columns(self, table):
        '''''' 
        values = {'Name':None, 'Yield':'yield', 'Prev.':'prev', 'High':'high', 'Low':'low', 
                  'Chg.':'change', 'Chg. %':'pct_change', 'Time':'time', 'Last':'last'}
        temp = table.columns        
        columns = []

        for col in temp:
            # if name is defined don't need it because it is the index
            if values[col] is None:
                continue
            columns.append(values[col])
        return columns

    def set_up(self):
        ''' This is called every time the button that activates the tab is pressed.
            If the button is presses for the first time than it creates the table and sets 
            data_flag to true which basically means that the table already exists so 
            does not need to make another and always calls check_data. '''

        # try to get data to set the treeview table
        self.data = self.get_data()
        if self.data is None:
            return
        else:
            columns = self.get_columns(self.data)

        if not self.data_flag:
            self.data_flag = True
            self.create_table(columns=columns)
        
        self.insert_into_treeview()

    def insert_into_treeview(self):
        ''' Adds the data scrapped from the website to the treeview ''' 
        self.index = self.data.index
        self.treeview.delete(*self.treeview.get_children())
        for idx in range(len(self.index)):
            self.treeview.insert('', 'end', text=self.index[idx], values=tuple(self.data.iloc[idx].values))

    def sub_frame(self, frame_name):
        frame = Frame(self, bd=1) 
        self.sub_frames[frame_name] = frame
        return frame
        
class Home(FrameWidget):
    def __init__(self, root, controller):
        ''' Shows most know commodities including metals/energy/grains/meats/softs '''
        super().__init__(root, controller, get_indices)

class Indices(FrameWidget):
    def __init__(self, root, controller):
        ''' Shows most know commodities including metals/energy/grains/meats/softs '''
        super().__init__(root, controller, get_indices)
    
class Commodities(FrameWidget):
    def __init__(self, root, controller):
        ''' Shows most know commodities including metals/energy/grains/meats/softs '''
        super().__init__(root, controller, get_commodities)
        
class Metals(FrameWidget):
    def __init__(self, root, controller):
        ''' Shows most know commodities including metals/energy/grains/meats/softs '''
        super().__init__(root, controller, get_metals)

class GoldSilver(FrameWidget):
    def __init__(self, root, controller):
        ''' Shows most know commodities including metals/energy/grains/meats/softs '''
        super().__init__(root, controller, get_gold_silver)
        
    
    def set_up(self):
        ''' Same as the method in the super(), but this frame has some extra feature G/S ratio. '''
        super().set_up()
        self.GS_ratio()

    def GS_ratio(self):
        ''' Create the gold/silver the ratio in a subframe ''' 
        self.gold = self.data.loc["Gold"]["Last"]
        self.silver = self.data.loc["Silver"]["Last"]
        self.ratio = self.gold / self.silver

        if not self.sub_data_flag:
            self.sub_data_flag = True
            frame = self.sub_frame("gs_ratio")
            self.text = Label(frame, text="Ratio", font=("Arial", 22))
            self.value = Label(frame, text=self.ratio, font=("Arial", 22))
        
            self.text.pack()
            self.value.pack()
            self.sub_frames["gs_ratio"].pack(side="left", fill="y", expand=False)
        else:
            self.value.configure(text=self.ratio)


    def update(self):
        pass
        
class Bonds(FrameWidget):
    def __init__(self, root, controller):
        ''' Shows the bonds' data available for the country selected '''
        super().__init__(root, controller, get_bonds)
    
    def set_up(self):
        ''' This class calls set up diffentry because it needs the info about the countries before setting the table, 
        so that the dropdown/combobox menu is ready '''

        # try to get data to set the treeview table
        self.countries = self.load_countries()

        # set the options
        self.user_input()

        # get the columns for the table
        dummy_data = get_bonds()
        columns = self.get_columns(dummy_data)

        if not self.data_flag:
            self.data_flag = True
            self.create_table(columns=columns)
        
    
    def load_countries(self):
        try:
            if not os.path.isfile(COUNTRIES):
                return get_countries() # gets the list of countries and saves them

            with open(COUNTRIES, 'r') as fp:
                countries = json.load(fp)
                return countries
        except Exception as e:
            print(e)
        

    def get_value(self):
        country = self.combo.get()
        self.data = self.get_data(country)
        self.insert_into_treeview()

    def user_input(self):
        frame = self.sub_frame('input')
        self.label = tk.ttk.Label(frame, text="Country") 
        self.label.grid(row=0, column=0, sticky='W')
        self.combo = tk.ttk.Combobox(frame, values=self.countries)
        self.combo.grid(row=0, column=1, sticky='E')
        self.combo.current(0) # set to the beginning of the list 
        self.btn = tk.ttk.Button(frame, text='Get', command =self.get_value)
        self.btn.grid(row=0, column=2)

        for frame in self.sub_frames.keys():
            self.sub_frames[frame].pack(fill='both', expand=False)
    
class News(Frame):
    def __init__(self, root, controller):
        ''' Shows most know commodities including metals/energy/grains/meats/softs '''
        Frame.__init__(self, root)
        self.root = root
        self.controller = controller
        self.frames = []
        self.new_frames = True # frames need to be created - True, False otherwise
    
    def set_up(self):
        self.frame = Frame(self)
        if self.new_frames:
            self.new_frames = False
            self.canvas_setup()
        else:
            self.update()

    def canvas_setup(self):
        # Set up of the canvas and under frame
        self.canvas = Canvas(self.frame) # container for scrolling

        # Set up of Scrollbars linked to the main frame
        self.vbar = Scrollbar(self.frame, orient=tk.VERTICAL)
        self.vbar.configure(command=self.canvas.yview) # connectiing the vbar to the canvas
        self.hbar = Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.hbar.configure(command=self.canvas.xview) # connectiing the hbar to the canvas

        # Creates the canvas_frame where the subframes are going to be attached (news)
        self.canvas_frame = Frame(self.canvas) # container with the other frame(news)
        
        # Bind the canvas_frame so that the canvas knows it's size all the time
        # For example when adding/removing other widgets to it
        self.canvas_frame.bind(
            "<Configure>", 
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")
            )
        )
        
        # Tell the canvas to create the scrollable_frame the canvas_frame
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")

        # Configure the canvas / connect it to the bars 
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        
        # Create sub frames
        self.create_sub_frames() # add the data (other frames containing the news)

        # Pack everything
        self.vbar.pack(side="right", fill="y") # vertical scroll bar
        self.hbar.pack(side="bottom", fill="x") # horizontal scroll bar
        self.canvas.pack(side="left", fill="both", expand=True) # canvas
        self.frame.pack(fill="both", expand=True) # container for canvas
    
    def scroll_func(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def create_sub_frames(self):
        data = get_news()
        for idx in range(len(data)):
            frame = Frame(self.canvas_frame, relief=tk.GROOVE, bd=1, width=WIDTH)
            title, link, hour = data.iloc[idx]
            title_lb = Label(frame, text=title, font=("Arial", 15))
            hour_lb = Label(frame, text=hour, font=("Arial", 10))
            title_lb.pack(side="left")
            hour_lb.pack(side="right")
            title_lb.bind("<Button-1>", self.make_lambda(link))
            self.frames.append(frame)
            frame.pack(fill="x")

    def update(self):
        data = get_news()
        for idx, frame in enumerate(self.frames):
            title, link, hour = data.iloc[idx]
            labels = frame.winfo_children()
            labels[0].configure(text=title)
            labels[0].bind("<Button-1>", self.make_lambda(link))
            labels[1].configure(text=hour)

    def make_lambda(self, url):
        ''' creates a differnt scope so that the variable doesnt get caught by lambda '''
        return lambda e: self.callback(url=url)
    
    def callback(self, url):
        webbrowser.open_new_tab(url)
    

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGetInfo(root)
    root.mainloop()