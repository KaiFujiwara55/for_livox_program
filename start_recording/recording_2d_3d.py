import pyautogui
import datetime
import time
from playsound import playsound

record_start_img = "img\\record.png"
save_button_img = "img\\save.png"
file_name_img = "img\\file_name.png"
start_sound = "sound\\start.mp3"
status_path = "start_recording\\now_process.txt"
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
    output_folder = "output_folder"
    file_name = "file_name"

    # 「取得中」に2次元LiDAR用ステータスを変更
    with open(status_path, "w") as f:
        f.write("1,"+output_folder+"\\2d\\"+file_name+".csv")

    # ページ遷移用に5秒待つ
    time.sleep(5)
    playsound(start_sound)

    # レコード開始ボタンをクリック
    record_button_point = get_point_img(record_start_img)
    click_point(record_button_point)

    # レコード開始時刻をunix時間で記録
    dt = datetime.datetime.timestamp(datetime.datetime.now())
    dt_txt_path = f"time_list\\{file_name}.txt"
    with open(dt_txt_path, mode="w") as f:
        f.write(str(dt))

    # レコード終了してファイル保存画面が出たら終了
    wait_finish_recording()

    # レコード終了時間をunix時間で記録
    dt = datetime.datetime.timestamp(datetime.datetime.now())
    with open(dt_txt_path, mode="a") as f:
        f.write("\n"+str(dt))

    # 3Dデータを保存
    save_file(output_folder+"\\3d\\"+file_name+".lvx")

    # 「取得終了」に2次元LiDAR用ステータスを変更
    with open(status_path, "w") as f:
        f.write("0,path")

