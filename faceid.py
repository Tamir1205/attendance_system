#import library
import os  
import numpy as np  #библиотека для работы с многомерным массивом
import face_recognition #библиотека для распознавания образов, в задачу которого входит автоматическая локализация лица
import cv2  #библиотека компьютерного зрения, которая предназначена для анализа, классификации и обработки изображений.
from datetime import datetime #библиотека для времени


video_capture = cv2.VideoCapture(0) #Подключение камеры

#Загрузка фотогафии студентов и кодирование (анализ) датасета
diana_image = face_recognition.load_image_file("dataset/1.jpg")
diana_encoding = face_recognition.face_encodings(diana_image)[0]

ainur_image = face_recognition.load_image_file("dataset/2.jpg")
ainur_encoding = face_recognition.face_encodings(ainur_image)[0]

amirkhan_image = face_recognition.load_image_file("dataset/3.jpg")
amirkhan_encoding = face_recognition.face_encodings(amirkhan_image)[0]

daniyar_image = face_recognition.load_image_file("dataset/4.jpg")
daniyar_encoding = face_recognition.face_encodings(daniyar_image)[0]

zhanel_image = face_recognition.load_image_file("dataset/5.jpg")
zhanel_encoding = face_recognition.face_encodings(zhanel_image)[0]

#Добавление кодированых лиц в массив
known_face_encoding = [
    diana_encoding,
    ainur_encoding,
    amirkhan_encoding,
    daniyar_encoding,
    zhanel_encoding,  
    ]

#Добавление ФИ студентов в массив
known_faces_names = [
    "Diana Omarbayeva",
    "Ainur Dossan",
    "Amirkhan Kadyrkhan",
    "Daniyar Yelubayev",
    "Zhanel Sadykova",
    ]

students = known_faces_names.copy()

#Новые массивы и логическое значение
face_locations = [] 
face_encodings = []
face_names = []
s = True 

#Настоящее время
now = datetime.now() 

#Открываем файл Attendace.txt и на первую строку пишу attendance system
with open('Attendance.txt','w') as f:
    f.write('ATTENDACE SYSTEM')
    f.write('\n')

#Основной цикл программы
while True:
    _,frame = video_capture.read()  #Чтение камеры
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)  #Размеры рамка
    rgb_small_frame = small_frame[:,:,::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame) #Используя команду находим лицо
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations) #Кодируем лицо в реальном времени
        face_names = []
        for face_encoding in face_encodings: #Сравнение с лицами реального времени с лицами студентов из датасета
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding) #Находим схожесть лиц
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding) 
            best_match_index = np.argmin(face_distance) #Находим лучший схожесть лиц и берем его индекс
            print(face_distance)
            if matches[best_match_index]: #Если совпадает то берем ФИ студента
                name = known_faces_names[best_match_index]
            face_names.append(name) #Добавляем ФИ в список
            if name in known_faces_names: #Если имя студента в списке имен то удаляем из списка и выводим его ФИ в txt файле 
                if name in students:      
                    students.remove(name) #Удаление ФИ из списка
                    now = datetime.now() #Настоящее время
                    f = open('Attendance'+'.txt','a')
                    f.writelines(["Student:",name,"     ","Time:",str(now.hour),":",str(now.minute),":",str(now.second),'\n']) #Пишем ФИ студента в файле и настоящее время до секунды
                    print(name)
                    

    cv2.imshow("attendace system",frame)#Название программы
    if cv2.waitKey(1) & 0xFF == ord('q'):  # При нажатии клавиши "Q" остановить программу
        break

#Закрыть программу
video_capture.release()
cv2.destroyAllWindows()
f.close()










































         
