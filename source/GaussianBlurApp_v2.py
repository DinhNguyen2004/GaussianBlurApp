import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import cv2
import os

from PIL import Image, ImageTk, ImageFilter

# Treeview
def populate_treeview(tree):
    for item in os.listdir():
        item_path = os.path.join(item)
        is_folder = os.path.isdir(item_path)
        item_type = "Folder" if is_folder else "File"
        tree.insert('', 'end', text=item_path, values=(item_type, item_path))

# Bắt sự kiện trong Treeview
def on_treeview_select(event):
    global new_image_select, file_path, ima_select, alo_error
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

# Slider
def on_horizontal_scroll(*args):
    treeview.xview(*args)
def on_vertical_scroll(*args):
    treeview.yview(*args)

# Restall
def rest_all():
    global file_path
    radius_sl.set(0)
    kernal_sl.set(1)
    file_path = ''
    ima_select_label.config(image='')
    messagebox.showinfo("Notification","Please! Choose new image")

# Popup Xin chào
def popupmsg():
    popup = tk.Tk()
    popup.geometry("150x120")
    popup.iconbitmap("icon_ima_proc.ico")

    def leavemini():
        popup.destroy()
        messagebox.showinfo("Notification", "Please! Chosse image from your disk on TreeView")

    label = tk.Label(popup, text="Have a good today!")
    label.pack(side="top", fill="x", pady=20)
    B1 = tk.Button(popup, text="Okay", command=leavemini)
    B1.pack()
    popup.mainloop()

# Lấy giá trị bán kính
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

# Lấy giá trị Kernal
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

# Xuất file
def export_file():
    global radius_v, kernal_v, filename
    if ima_select_label.cget("image") == '':
        messagebox.showerror("Error Image", "Error! Image not displayed")
    else:
        filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if not filename:
            return
        if filename:
            try:       #Method Cv2
                kernal_v
            except NameError:
                print("kernal_v is not defined")
            else:
                ima_select = cv2.imread(file_path)
                image_blur = cv2.GaussianBlur(ima_select, (kernal_v, kernal_v), 0)  # Apply Gaussian blur in Cv2
                image_blur = Image.fromarray(cv2.cvtColor(image_blur, cv2.COLOR_BGR2RGB))
                image_blur.save(filename)
                print(f"Blurred image saved as {filename.name}")
            try:        #Method PIL
                radius_v
            except NameError:
                print("radius_v is not defined")
            else:
                ima_select = Image.open(file_path).convert("RGB")
                blurred_image = ima_select.filter(ImageFilter.GaussianBlur(radius=radius_v))
                blurred_image.save(filename)
                print(f"Blurred image saved as {filename.name}")


# Khởi tạo tkinter
root = tk.Tk()
root.geometry("740x500")
root.title("Gaussian Blur App")
root.iconbitmap("icon_ima_proc.ico")
root.resizable(width=False, height=False)

# Background
background_image = PhotoImage(file="bg_ima_proc.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Treeview
treeview = ttk.Treeview(root, columns=("Type", "Path"), show="headings")
treeview.heading("Type", text="Type", anchor="w")
treeview.heading("Path", text="Path", anchor="w")
treeview.column("Type", width=60)
treeview.column("Path", width=400)

# Tiêu đề treeview
captree = tk.Label(root, text="Current Directory", font=("Helvetica", 11))
captree.place(relx=0.156, rely=0.165)

# Tạo Scrollbar và đặt nó ở dưới Treeview, xử lý
xscrollbar = ttk.Scrollbar(root, orient="horizontal", command=on_horizontal_scroll)
xscrollbar.place(relx=0.042, rely=0.533, width=270)  # Đặt Scrollbar ở phía dưới Treeview

yscrollbar = ttk.Scrollbar(root, orient="vertical", command=on_vertical_scroll)
yscrollbar.place(relx=0.4047, rely=0.2357, height=150)  # Đặt Scrollbar ở bên phải Treeview

treeview.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)

# Thực hiện lệnh trong treeview
treeview.bind("<Double-1>", on_treeview_select)

#Hiển thị Treeview
populate_treeview(treeview)
treeview.place(relx= 0.042, rely=0.234, width=270, height=150)

# Frame nhóm
frame_other = tk.Frame(root, bg="#BBBBBB")
frame_other.place(relx=0.68, rely=0.23)

# Image team
team_label = tk.Label(frame_other, text='FLAMES TEAM', bg="#92B9E3", fg="#FFFFFF")
team_label.grid(row=0)

ima_team = Image.open("anime_girl.jpg")
resized_image = ima_team.resize((195, 145))
new_image = ImageTk.PhotoImage(resized_image)

ima_team_label = tk.Label(frame_other, image=new_image)
ima_team_label.grid(row=1)

# Create Label
app_label = tk.Label(root, text='APPLICATION GAUSSIAN BLUR', font=("Inder", 11))
app_label.place(relx=0.35, rely=0.06)

method2_label = tk.Label(root, text='Method: PIL\nRadius', font=("Inder", 9))
method2_label.place(relx=0.07, rely=0.62)

method1_label = tk.Label(root, text='Method: Cv2\nKernal', font=("Inder", 9))
method1_label.place(relx=0.28, rely=0.62)

# Label hiden trang trí cho treeview
hid_lab = tk.Label(root, text='', width=2)
hid_lab.place(relx=0.403, rely=0.525)

# Lấy giá trị từ slider
radius_sl = tk.Scale(root, from_=0, to=20, command=lambda value: get_current_value_radius())
radius_sl.place(relx=0.09,rely=0.72)

custom_values = [0, 1, 3, 5, 7, 9]
kernal_sl = tk.Scale(root, from_=1, to=19,resolution=2, command=lambda value: get_current_value_kernal())
kernal_sl.place(relx=0.3,rely=0.72)

# Button rest_all
rest_all_btn = tk.Button(root,text='Rest All',bg="#92B9E3", fg="#FFFFFF", command=rest_all)
rest_all_btn.place(relx=0.444, rely=0.7, width=90)

# Button Export file
export_f_btn = tk.Button(root,text='Export File',bg="#92B9E3", fg="#FFFFFF", command=export_file)
export_f_btn.place(relx=0.444, rely=0.8, width=90)

# Last result
ima_select_label = tk.Label(root)
ima_select_label.place(relx=0.667, rely=0.58, width=215,height=195)

popupmsg()

root.mainloop()
