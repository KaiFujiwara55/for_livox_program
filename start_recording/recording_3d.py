import pyautogui
import datetime
import time
from playsound import playsound

record_start_img = "img\\record.png"
save_button_img = "img\\save.png"
file_name_img = "img\\file_name.png"
start_sound = "sound\\start.mp3"
cofidence_value = 0.9


def get_point_img(img, right=0):
    try:
        point = pyautogui.locateCenterOnScreen(img, confidence=cofidence_value)
    except:
        raise Exception("Not found " + img)

    # 右に100pxずらす
    point = (point[0]+right, point[1])

    return point

def click_point(point):
    pyautogui.click(point)

def wait_finish_recording():
    while True:
        try:
            record_button_point = get_point_img(save_button_img)
            break
        except:
            time.sleep(1)

def save_file(file_name):
    click_point(get_point_img(file_name_img, 100))
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("backspace")
    time.sleep(0.5)
    pyautogui.typewrite(file_name)
    time.sleep(0.5)
    click_point(get_point_img(save_button_img))

if __name__ == "__main__":
    output_path = "outputpath"

    # ページ遷移用に5秒待つ
    time.sleep(1)
    playsound(start_sound)

    record_button_point = get_point_img(record_start_img)

    click_point(record_button_point)
    dt = datetime.datetime.timestamp(datetime.datetime.now())

    with open(f"time_list\\record_time_{dt}.txt", "w") as f:
        f.write(output_path, str(dt))

    wait_finish_recording()
    save_file(output_path)
