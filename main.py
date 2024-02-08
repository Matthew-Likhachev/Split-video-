import cv2
import os
from tkinter import *
TOTAL_FRAME_NUM = 0
def chng_img(img_path, save_path,thresh_):
    im_gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    im_bw = cv2.threshold(im_gray, thresh_, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(save_path, im_bw)

def separ_v(video_path, save_path,video_name, isNewFolder):
    capture = cv2.VideoCapture(video_path)
    frameNr = 0
    global  TOTAL_FRAME_NUM
    while (True):

        success, frame = capture.read()

        if success:
            #если разбиение по папкам - имена в каждой папке начинаются с 0
            if isNewFolder:
                temp_path = f'{save_path}\\{video_name} fr_{frameNr}.jpg'
                frameNr += 1
                #fChng_thresh(temp_path, f"D:\MyFiles\programming\python\cut video\\video\\res\\res_{frameNr}.jpg")
            else:
                temp_path = f'{save_path}\\fr_{TOTAL_FRAME_NUM}.jpg'
                TOTAL_FRAME_NUM += 1
            cv2.imwrite(temp_path, frame)
        else:
            break


    capture.release()

def createFolder(path):
    if os.path.exists(path):
        print(f"Folder already Exists. Path: {path}")
    else:
        os.mkdir(path)

#folders_list - список для сохранения в папки  с иерархией как у видео папок
def find_video(video_path, save_path, layers, isNewFolder, folders_list):
    content = os.listdir(video_path)
    #кол-во слоев, учитывая иходную дирикторию
    if(layers>0):
        for file in content:
            tempPath = video_path+'\\'+file

            #нашли видео
            if (file.endswith(".avi")):
                tempsavepath = save_path
                if isNewFolder:
                    #создаем папки по списку
                    for folder_name in folders_list:
                        #имя папки без расширения
                        createFolder(tempsavepath+"\\"+folder_name)
                        tempsavepath = tempsavepath+"\\"+folder_name
                #Делим видео на кадры
                separ_v(tempPath, tempsavepath,file.replace("."," "), isNewFolder)


            #нашли папку
            if os.path.isdir(tempPath):
                # берем имя папки
                folders_list.append(tempPath.split("\\")[-1])
                find_video(tempPath,save_path,layers-1, isNewFolder, folders_list)
            #Удаление из имени папки из списка
            if len(folders_list)!=0 and os.path.isdir(tempPath):
                folders_list.pop(-1)



def find_chng_img(total_path,layers, isNewFolder, thresh):
    content = os.listdir(total_path)
    # кол-во слоев, учитывая иходную дирикторию
    if (layers > 0):
        for file in content:
            tempPath = total_path + '\\' + file

            # нашли картинку
            if (file.endswith(".jpg")):
                chng_img(tempPath,tempPath,thresh)

            # нашли папку
            if os.path.isdir(tempPath):
                find_chng_img(tempPath, layers - 1, isNewFolder, thresh)


# video_path = r'D:\MyFiles\programming\python\cut video\video'
# save_path = r"D:\MyFiles\programming\python\cut video\res"
# layers = 3
# isNewFolder =False
# thresh = 20

def cng_isNewFolder():
    if var_Ch.get() == True:
        isNewFolder=True
    else:
        isNewFolder=False

def clicked():
    video_path = video_path_E.get()
    save_path = save_path_E.get()
    layers = int(layers_E.get())
    thresh = int(thresh_E.get())
    print(isNewFolder)
    find_video(video_path,save_path,layers, isNewFolder,[])
    if(isNewFolder):
        find_chng_img(save_path,layers,isNewFolder,thresh)
    else:
        find_chng_img(save_path, layers, isNewFolder, thresh)


window = Tk()
window.geometry("800x800")
#current working directory
cwd1 = StringVar()
cwd1.set(os.getcwd())

video_path_L = Label(window, text="Путь к видео/папке", width=20)
video_path_L.grid(column=1,row = 10)
video_path_E = Entry(window, textvariable=str(cwd1), width=50)
video_path_E.grid(column=1,row = 20)

cwd2 = StringVar()
cwd2.set(os.getcwd())
save_path_L = Label(window, text="Сохранить в", width=20)
save_path_L.grid(column=1,row = 40)
save_path_E = Entry(window, textvariable=str(cwd2), width=50)
save_path_E.grid(column=1,row = 50)

ivnl = StringVar()
ivnl.set(str("1"))
layers_L = Label(window, text="Сколько подпапок просматривать для поиска?", width=30)
layers_L.grid(column=1,row = 60)
layers_E = Entry(window, textvariable=str(ivnl), width=50)
layers_E.grid(column=1,row = 70)

ivnth = StringVar()
ivnth.set(str("20"))
thresh_L = Label(window, text="Значение Threshhold", width=20)
thresh_L.grid(column=1,row = 80)
thresh_E = Entry(window, textvariable=str(ivnth), width=50)
thresh_E.grid(column=1,row = 90)

var_Ch = BooleanVar()
var_Ch.set(True)
isNewFolder = bool(var_Ch.get())
folder_Ch = Checkbutton(window, text="Создавать подпапки",
                 variable=var_Ch,
                 onvalue=True, offvalue=False,
                 command= cng_isNewFolder)
folder_Ch.grid(column=1,row = 100)

btn = Button(window, text="Погнали!", command=clicked, width=10)
btn.grid(column=10,row = 20)

window.mainloop()







