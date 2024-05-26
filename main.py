import cv2
import mediapipe as mp
import time
import pyautogui
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

# Class click mouse !!!!!!!!!!
class Event:
    def __init__(self):
        self.mouse_down = False
        self.count = 0
        self.target_count = 0

    def spuat(self, distance1):
        if distance1 < 150 and not self.mouse_down:
            pyautogui.mouseDown() 
            
            self.mouse_down = True
        elif distance1 >= 155 and self.mouse_down:
            pyautogui.mouseUp()
            self.count += 1
            self.mouse_down = False

            if self.count == self.target_count:
                
                # Gọi phương thức trừu tượng
                self.mission_complete()  

    # Phương thức này sẽ được ghi đè trong các lớp con    
    def mission_complete(self):
        pass  

# Kế thừa từ lớp cha Event
class complete(Event):
    def mission_complete(self):
        print("Mission complete")
        
# Đa hình     
class Another(Event):
    def mission_complete(self):
        cv2.putText(img, "Mission complete", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        cv2.imshow("Train Spuat", img)
        cv2.waitKey(3000)
        cv2.destroyWindow("Train Spuat")
        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# nhận diện pose
mpPose = mp.solutions.pose
pose = mpPose.Pose( model_complexity=1,min_detection_confidence=0.9, min_tracking_confidence=0.9)

# vẽ các khớp nối ra
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(1)
pTime = 0

# Sử dụng đóng gói để tạo đối tượng
sukien = complete()

# Sử dụng đa hình
sukien = Another()

h, w, c = 0, 0, 0
 
cv2.namedWindow("Real", cv2.WINDOW_NORMAL)

######################################################################################################################
    
root = tk.Tk()

root.title("calculator Count")
root.geometry("350x550") 
root.configure(bg='lightblue')

# Kết nối database
connection = mysql.connector.connect(host='localhost', user='root', password='', port='3306', database='test')
                                     
# c = connection.cursor()
def set_count():
    try:
        sukien.target_count = int(entry_enter.get())
        # NHận dữ liệu được nhập
        MSNC = entry_MSNC.get()
        REP = entry_rep.get()
        COUNT = entry_enter.get()
        
        insert_query = "INSERT INTO `muctieu_datra`(`MSNC`, `REP`,`COUNT`) VALUES (%s,%s,%s)"
        vals = (MSNC,REP,COUNT)
        c.execute(insert_query,vals)
        # connection.commit()
        
        messagebox.showinfo("Update", "Information has been updated")
    except:
        messagebox.showinfo("Error", "Re-enter information")
        
  
# Logo
img = Image.open("bp.png")  
img = img.resize((200, 200), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)
logo_label = tk.Label(root, image=photo, bg='lightblue')
logo_label.pack()


# Nhập lại ID
label_MSNC = tk.Label(root, text="RE-Enter MSNC",bg='lightblue',font=('Arial', 18, 'bold'))
label_MSNC.pack(pady=10,padx= 10)
entry_MSNC = tk.Entry(root)
entry_MSNC.pack()

# Số Rep
label_rep = tk.Label(root, text="Enter Rep",bg='lightblue',font=('Arial', 18, 'bold'))
label_rep.pack(pady=10,padx= 10)
entry_rep = tk.Entry(root)
entry_rep.pack()

# Số lần count
label_enter= tk.Label(root, text="Target squat",bg='lightblue',font=('Arial', 18, 'bold'))
label_enter.pack(pady=10,padx= 10)
entry_enter = tk.Entry(root)
entry_enter.pack()

# Nút nhấn
button = tk.Button(root, text="Set count", command=set_count,bg='orange')
button.pack(pady=10,padx= 10)


#######################################################################################################################

while cap.isOpened():
    root.update()
    success,img=cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = pose.process(imgRGB)
  
    # ghi các điểm kết quả ra
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h , w, c = img.shape
            cx, cy = int(w * lm.x), int(h * lm.y)
            
            if id == 24:
                left_hip = [cx, cy]
            if id == 30:
                right_anke = [cx, cy]
                
     # công thức pytago không gian   
        distance1 = ((left_hip[0] - right_anke[0]) ** 2 + (left_hip[1] - right_anke[1]) ** 2) ** 0.5
        sukien.spuat(distance1)
    
    # Cập nhật FPS       
    cTime=time.time()
    fps = 2/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(0,240,5),3)
    
    # Ghi lại số lần spuat
    cv2.rectangle(img, (10, h - 40), (250, h - 10), (55, 20, 255), -1)
    cv2.putText(img, f"Counted: {sukien.count}", (20, h - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
    
    cv2.imshow("Real", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
