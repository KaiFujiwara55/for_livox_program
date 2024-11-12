import pyautogui
import glob
import time
import os

source_file_img = "img\\source_file.png"
target_file_img = "img\\target_file.png"
start_img = "img\\start.png"
finish_status_img = "img\\finish_status.png"
cofidence_value = 0.9

def get_sorce_files(source_files_path):
    source_files = glob.glob(source_files_path)
    source_files = [os.getcwd() + "\\" + sorce_file for sorce_file in source_files]
    return source_files

def get_point_img(img, right=0):
    if pyautogui.locateCenterOnScreen(img, confidence=cofidence_value) == None:
        raise Exception("Not found " + img)
    
    point = pyautogui.locateCenterOnScreen(img, confidence=cofidence_value)

    # 右に100pxずらす
    point = (point[0]+right, point[1])

    return point

def click_point(point):
    pyautogui.click(point)
    time.sleep(1)

def remove_text():
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('delete')
    time.sleep(0.1)

def input_text(text):
    pyautogui.typewrite(text)

def wait_img(img, until=30):
    count = 0
    is_img = None
    while is_img is None:
        time.sleep(3)
        try:
            is_img = pyautogui.locateOnScreen(img, confidence=cofidence_value)
        except Exception as e:
            is_img = None

        count += 1
        if count > until:
            raise Exception("Not found " + img)


if __name__ == "__main__":
    # ページ遷移用に5秒待つ
    time.sleep(3)

    source_files = get_sorce_files(source_files_path="source_files\\*.lvx")
    for source_file in source_files:
        print(source_file)

        click_point(get_point_img(source_file_img, right=100))
        remove_text()
        input_text(source_file)

        click_point(get_point_img(target_file_img, right=100))
        remove_text()
        input_text(source_file.replace("sorce_files", "converted_files").replace(".lvx", ".csv"))

        click_point(get_point_img(start_img))

        wait_img(finish_status_img, until=60)

        time.sleep(3)