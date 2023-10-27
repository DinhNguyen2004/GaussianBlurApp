import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import cv2
import os

from PIL import Image, ImageTk, ImageFilter

root = tk.Tk()
root.geometry("740x500")
root.title("Gaussian Blur App")
root.configure(background="black")
root.iconbitmap("images/icon_ima_proc.ico")
root.resizable(width=False, height=False)

# Image background and responsive size windows
class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)
        self.image = Image.open("/images/bg_ima_proc.png")
        self.img_copy = self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image=self.background_image)

e = Example(root)
e.pack(fill=BOTH, expand=YES)

'''
# Tree view
folders = ['/Users/ngocd/PycharmProjects/GaussianBlurAppv2/']

tree = ttk.Treeview()
tree.place(relx= 0.05, rely=0.23, width=270, height=150)

for folder in folders:
    tree.insert('', 'end', folder, text=folder)
    for name in os.listdir(folder):
        tree.insert(folder, 'end', name, text=name)


def solve(event):
    global new_image_select, file_path
    for sel in tree.selection():
        item=tree.item(sel)
        file_path = item['text']
        ima_select = Image.open(file_path).convert('RGB')
        resized_image_select = ima_select.resize((215, 195))
        new_image_select = ImageTk.PhotoImage(resized_image_select)
        ima_select_label.config(image=new_image_select)

        print(item['text'])
        ima_select = Image.open(file_path)
        resized_image_select = ima_select.resize((215, 195))
        new_image_select = ImageTk.PhotoImage(resized_image_select)
        ima_select_label.config(image=new_image_select)
        print(file_path)


tree.bind('<<TreeviewSelect>>',solve) '''
# Treeview

c_drive_directory = "C:/"

current_directory = "C:/"  # Khởi tạo thư mục hiện tại



''''
def populate_treeview(tree, path):
    tree.delete(*tree.get_children())
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        is_directory = os.path.isdir(item_path)
        item_type = "Directory" if is_directory else "File"
        tree.insert('', 'end', text=item, values=(item_type, item_path))
'''
def populate_treeview(tree, path):
    tree.delete(*tree.get_children())
    for item in os.listdir():
        item_path = os.path.join(path, item)
        is_directory = os.path.isdir(item_path)
        item_type = "Directory" if is_directory else "File"
        item_name = os.path.basename(item_path)  # Get the last portion of the path (filename or directory name)
        tree.insert('', 'end', text=item_name, values=(item_type, item_path))


'''def on_treeview_select(event):
    global new_image_select, file_path, ima_select
    selected_item = treeview.focus()
    item_info = treeview.item(selected_item)
    file_path = item_info['values'][1] if len(item_info['values']) > 1 else None
    if file_path:
        if os.path.isdir(file_path):
            populate_treeview(treeview, file_path)
        else:
            print(f"Selected: {file_path}")
'''
def on_treeview_select(event):
    global new_image_select, file_path, ima_select, current_directory, alo_error
    selected_item = treeview.focus()
    item_info = treeview.item(selected_item)
    file_path = item_info['values'][1] if len(item_info['values']) > 1 else None
    if file_path:
        if os.path.isdir(file_path):
            current_directory = file_path  # Cập nhật thư mục hiện tại khi chọn một thư mục
            populate_treeview(treeview, file_path)
        else:
            print(f"Selected: {file_path}")

    for sel in treeview.selection():
        item = treeview.item(sel)
        file_path = item['text']

        #identify path image
        path_img = [".png",".ico",".jpg",".gif"]
        for x in path_img:
            if x not in file_path:
                alo_error = True
            else:
                alo_error = False
                break

        print("result error format image: ", alo_error)
    if alo_error is True:
        messagebox.showerror("Error","Error format image!")
        del alo_error
    else:
        ima_select = Image.open(file_path).convert('RGB')

        resized_image_select = ima_select.resize((215, 195))
        new_image_select = ImageTk.PhotoImage(resized_image_select)
        ima_select_label.config(image=new_image_select)
        '''print(item['text'])
        ima_select = Image.open(file_path)
        resized_image_select = ima_select.resize((215, 195))
        new_image_select = ImageTk.PhotoImage(resized_image_select)
        ima_select_label.config(image=new_image_select)
        print(file_path)'''

def refresh_treeview():
    populate_treeview(treeview, c_drive_directory)
def on_horizontal_scroll(*args):
    treeview.xview(*args)
def on_vertical_scroll(*args):
    treeview.yview(*args)
def undo_directory():
    global current_directory
    parent_directory = os.path.dirname(current_directory)
    if os.path.exists(parent_directory):
        current_directory = parent_directory
        populate_treeview(treeview, current_directory)


treeview = ttk.Treeview(root, columns=("Type", "Path"), show="headings")
treeview.heading("Type", text="Type", anchor="w")
treeview.heading("Path", text="Path", anchor="w")
treeview.column("Type", width=60)
treeview.column("Path", width=400)


# Tạo Scrollbar và đặt nó ở dưới Treeview
xscrollbar = ttk.Scrollbar(root, orient="horizontal", command=on_horizontal_scroll)
xscrollbar.place(relx=0.042, rely=0.533, width=270)  # Đặt Scrollbar ở phía dưới Treeview

yscrollbar = ttk.Scrollbar(root, orient="vertical", command=on_vertical_scroll)
yscrollbar.place(relx=0.4047, rely=0.2357, height=150)  # Đặt Scrollbar ở bên phải Treeview

treeview.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
treeview.bind("<Double-1>", on_treeview_select)


populate_treeview(treeview, "C:/")
treeview.place(relx= 0.042, rely=0.234, width=270, height=150)

refresh_button = tk.Button(root, text="Refresh", command=refresh_treeview)
refresh_button.place(relx= 0.337, rely=0.2357)

#Undo
undo_button = tk.Button(root, text="Undo", width=6, command=undo_directory)
undo_button.place(relx= 0.27, rely=0.2357)
# Rest all

def rest_all():
    global file_path
    radius_sl.set(0)
    kernal_sl.set(1)
    file_path = ''
    ima_select_label.config(image='')
    messagebox.showinfo("Notification","Please! Choose new image")
    refresh_treeview()
        #slider
# Error not image



def popupmsg():
    popup = tk.Tk()
    popup.geometry("150x120")
    popup.iconbitmap("icon_ima_proc.ico")

    def leavemini():
        popup.destroy()
        messagebox.showinfo("Notification", "Please! Chosse image from your disk on TreeView")

    # popup.wm_title("!!!")
    label = tk.Label(popup, text="Have a good today!")
    label.pack(side="top", fill="x", pady=20)
    B1 = tk.Button(popup, text="Okay", command=leavemini)
    B1.pack()
    popup.mainloop()


def get_current_value_radius():
    global  new_image_select, ima_select, radius_v

    try:
        file_path
    except:
        messagebox.showerror("Error Image", "Error!, Image not displayed")
        radius_sl.set(0)
    else:
        if file_path == '':
            radius_sl.set(0)
        else:
            radius_v = int(radius_sl.get())
            ima_select = Image.open(file_path).convert("RGB")
            blurred_image = ima_select.filter(ImageFilter.GaussianBlur(radius=radius_v))
            resized_image_select = blurred_image.resize((215, 195))
            new_image_select = ImageTk.PhotoImage(image=resized_image_select)
            ima_select_label.config(image=new_image_select)


def get_current_value_kernal():
    global  new_image_select, ima_select, kernal_v

    # Condition get value:
    try:
        file_path
    except:
        messagebox.showerror("Error Image", "Error!, Image not displayed")
        kernal_sl.set(1)
    #Condition get value:
    else:
        if file_path == '':
            kernal_sl.set(1)
        else:
            kernal_v = int(kernal_sl.get())
            ima_select = cv2.imread(file_path)
            image_blur = cv2.GaussianBlur(ima_select, (kernal_v, kernal_v), 0)  # Apply Gaussian blur in Cv2
            resized_image_select = cv2.resize(image_blur, (215, 195))
                # Convert image from OpenCV to Pillow's object
            img_pil = Image.fromarray(cv2.cvtColor(resized_image_select, cv2.COLOR_BGR2RGB))
                    # Format compatible with tkinter
            img_tk = ImageTk.PhotoImage(image=img_pil)
            ima_select_label.config(image=img_tk)
            ima_select_label.image = img_tk

'''
past = 1
def fix(n):
    global past
    n = int(n)
    if not n % 2:
        kernal_sl.set(n+1 if n > past else n-1)
        past = kernal_sl.get()

    kernal_v = int(past)
    ima_select = cv2.imread(file_path)
    image_blur = cv2.GaussianBlur(ima_select, (kernal_v, kernal_v), 0)  # Apply Gaussian blur in Cv2
    resized_image_select = cv2.resize(image_blur, (215, 195))
    # Convert image from OpenCV to Pillow's object
    img_pil = Image.fromarray(cv2.cvtColor(resized_image_select, cv2.COLOR_BGR2RGB))
    # Format compatible with tkinter
    img_tk = ImageTk.PhotoImage(image=img_pil)
    ima_select_label.config(image=img_tk)
    ima_select_label.image = img_tk
'''

def export_file():
    global radius_v, kernal_v

    if ima_select_label.cget("image") == '':
        messagebox.showerror("Error Image", "Error!, Image not displayed")
    else:
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        if filename:
            # Method Cv2
            try:
                kernal_v
            except NameError:
                print("kernal_v is not defined")
            else:
                ima_select = cv2.imread(file_path)
                image_blur = cv2.GaussianBlur(ima_select, (kernal_v, kernal_v), 0)  # Apply Gaussian blur in Cv2
                image_blur = Image.fromarray(cv2.cvtColor(image_blur, cv2.COLOR_BGR2RGB))
                image_blur.save(filename)
                print(f"Blurred image saved as {filename.name}")

            # Method PIL
            try:
                radius_v
            except NameError:
                print("radius_v is not defined")
            else:
                ima_select = Image.open(file_path).convert("RGB")
                blurred_image = ima_select.filter(ImageFilter.GaussianBlur(radius=radius_v))
                blurred_image.save(filename)
                print(f"Blurred image saved as {filename.name}")


# Frame other
frame_other = tk.Frame(root, bg="#BBBBBB")
frame_other.place(relx=0.68, rely=0.23)

# Create Label
app_label = tk.Label(root, text='APPLICATION GAUSSIAN BLUR', font=("Inder", 11))
app_label.place(relx=0.35, rely=0.06)

method2_label = tk.Label(root, text='Method: PIL\nRadius', font=("Inder", 9))
method2_label.place(relx=0.07, rely=0.62)

method1_label = tk.Label(root, text='Method: Cv2\nKernal', font=("Inder", 9))
method1_label.place(relx=0.28, rely=0.62)

team_label = tk.Label(frame_other, text='FLAMES TEAM', bg="#92B9E3", fg="#FFFFFF")
team_label.grid(row=0)

# Label hiden
hid_lab = tk.Label(root, text='', width=2)
hid_lab.place(relx=0.403, rely=0.525)

# Sliders
radius_sl = tk.Scale(root, from_=0, to=20, command=lambda value: get_current_value_radius())
radius_sl.place(relx=0.09,rely=0.72)

custom_values = [0, 1, 3, 5, 7, 9]
kernal_sl = tk.Scale(root, from_=1, to=19,resolution=2, command=lambda value: get_current_value_kernal())
kernal_sl.place(relx=0.3,rely=0.72)

# Image team
ima_team = Image.open("images/anime_girl.jpg")
resized_image = ima_team.resize((195, 145))
new_image = ImageTk.PhotoImage(resized_image)

ima_team_label = tk.Label(frame_other, image=new_image)
ima_team_label.grid(row=1)

# Button rest_all
rest_all_btn = tk.Button(root,text='Rest All',bg="#92B9E3", fg="#FFFFFF", command=rest_all)
rest_all_btn.place(relx=0.444, rely=0.7, width=90)


# Button Export file
export_f_btn = tk.Button(root,text='Export File',bg="#92B9E3", fg="#FFFFFF", command=export_file)
export_f_btn.place(relx=0.444, rely=0.8, width=90)

# Processing Button After
ima_select_label = tk.Label(root)
ima_select_label.place(relx=0.667, rely=0.58, width=215,height=195)

### Author: Nguyen Ngoc Dinh

popupmsg()

root.mainloop()


# popup

'''
1. Lỗi file ảnh 
2. Lỗi khi chưa có ảnh k đc trượt
3. Lỗi khi chưa có ảnh k được exportfile
4. 
'''

# Error
'''
1. Rest thư viên 2 lần chỉnh thành 1 mất hết
'''
