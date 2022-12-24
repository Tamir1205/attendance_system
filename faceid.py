#Импорт библиотек
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

#ФУНКЦИИ

#Функция для нахождение путей
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#Contact us
def contact():
    mess._show(title='Contact us', message="Please contact us on : 'Admin@sdu.edu.kz' ")


#Функция для пути модули
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Модуль не найден', message='Проверьте путь модули')
        window.destroy()


#Функция для пароля
def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel\psd.txt")
    if exists1:
        tf = open("TrainingImageLabel\psd.txt", "r")
        key = tf.read()
    else:
        new_pas = tsd.askstring('', show='*')
        if new_pas == None:
            mess._show(title='', message='Пароль')
        else:
            tf = open("TrainingImageLabel\psd.txt", "w")
            tf.write(new_pas)
            mess._show(title='', message='')
            return
    password = tsd.askstring('Password', 'Введите пароль', show='*')
    if (password == key):
        TrainImages()
    elif (password == None):
        pass
    else:
        mess._show(title='Wrong Password', message='Неверный пароль')

#Регистрация студента и сканирование лица использу модуль haarcascadefile
def TakeImages():
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = (serial // 2)
        csvFile1.close()
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()
    Id = (txt.get())
    name = (txt2.get())
    if ((name.isalpha()) or (' ' in name)):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # увеличение номера образца
                sampleNum = sampleNum + 1
                # сохранение захваченного лица в папке набора данных TrainingImage
                cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                            gray[y:y + h, x:x + w])
                # отображать кадр
                cv2.imshow('Taking Images', img)
            # кадр 100 миллисекунд
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # перерыв, если номер выборки больше 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Taken for ID : " + Id
        row = [serial, '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message1.configure(text=res)
    else:
        if (name.isalpha() == False):
            res = "Enter Correct name"
            message.configure(text=res)

#Анализируем фотографии студента для определение студента с помощью модуля haarcascadefile
def TrainImages():
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        mess._show(title='No Registrations', message='Пожалуйста, сначала зарегистрируйте кого-нибудь!')
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Профиль успешно сохранен"
    message1.configure(text=res)


#Получаем проанализрованные фотографии и объекты
def getImagesAndLabels(path):
    # получить путь ко всем файлам в папке
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # создать пустой список лиц
    faces = []
    # создать пустой список идентификаторов
    Ids = []
    # теперь перебираем все пути к изображениям и загружаем идентификаторы и изображения
    for imagePath in imagePaths:
        # загрузка изображения и преобразование его в оттенки серого
        pilImage = Image.open(imagePath).convert('L')
        # Теперь мы конвертируем изображение PIL в массив numpy.
        imageNp = np.array(pilImage, 'uint8')
        # получение идентификатора с изображения
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # извлечь лицо из образца обучающего изображения
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

#Отслеживание изображений и проверка данных регистрации, аттенданс
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")
    for k in tv.get_children():
        tv.delete(k)
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        mess._show(title='Data Missing', message='Нажмите «Save Profile», чтобы сбросить данные.!')
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        mess._show(title='Details Missing', message='Сведения о студентах отсутствуют, проверьте!')
        cam.release()
        cv2.destroyAllWindows()
        window.destroy()
    #Основной цикл для проверки аттенденса
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                ID = ID[1:-1]
                bb = str(aa)
                bb = bb[2:-2]
                attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    exists = os.path.isfile("Attendance\Attendance_" + date + ".csv")
    if exists:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(attendance)
        csvFile1.close()
    else:
        with open("Attendance\Attendance_" + date + ".csv", 'a+') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
            writer.writerow(attendance)
        csvFile1.close()
    with open("Attendance\Attendance_" + date + ".csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for lines in reader1:
            i = i + 1
            if (i > 1):
                if (i % 2 != 0):
                    iidd = str(lines[0]) + '   '
                    tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
    csvFile1.close()
    cam.release()
    cv2.destroyAllWindows()

#ИСПОЛЬЗУЕМЫЕ МАТЕРИАЛЫ
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }



######################### GUI FRONT-END #####################################
window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#262523')

frame1 = tk.Frame(window, bg="#99C3C8")  #задний фон для аттенданс лист
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#99C3C8")  #задний фон для регистрации
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Final Project: Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

head2 = tk.Label(frame2, text="                              Registrations                             ", fg="white",bg="#DB5B0B" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                                Attendance                                ", fg="white",bg="#DB5B0B" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Student ID",width=22  ,height=1  ,fg="white"  ,bg="#99C3C8" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=42 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Student Name",width=22  ,fg="white"  ,bg="#99C3C8" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=42 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Write your ID and name \n2)Take your photo and save profile" ,bg="#99C3C8" ,fg="white"  ,width=39 ,height=2, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#99C3C8" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance List",width=20  ,fg="white"  ,bg="#99C3C8"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetails\StudentDetails.csv")
if exists:
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0


#MENU BAR
menubar = tk.Menu(window,relief='ridge')
filemenu = tk.Menu(menubar,tearoff=0)
filemenu.add_command(label='Contact Us', command = contact)
filemenu.add_command(label='Exit',command = window.destroy)
menubar.add_cascade(label='Help',font=('times', 29, ' bold '),menu=filemenu)

#ATTENDANCE TABLE
tv= ttk.Treeview(frame1,height =13,columns = ('name','date','time'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('date',width=133)
tv.column('time',width=133)
tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)
tv.heading('#0',text ='ID')
tv.heading('name',text ='NAME')
tv.heading('date',text ='DATE')
tv.heading('time',text ='TIME')

#SCROLLBAR
scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

#BUTTONS
takeImg = tk.Button(frame2, text="Take Images", command=TakeImages  ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)
trainImg = tk.Button(frame2, text="Save Profile", command=psw ,fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trainImg.place(x=30, y=380)
trackImg = tk.Button(frame1, text="Take Attendance", command=TrackImages  ,fg="white"  ,bg="blue"  ,width=35  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
trackImg.place(x=30,y=50)
quitWindow = tk.Button(frame1, text="FINISH", command=window.destroy  ,fg="white"  ,bg="red"  ,width=35 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=30, y=450)

#END

window.configure(menu=menubar)
window.mainloop()


























##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################