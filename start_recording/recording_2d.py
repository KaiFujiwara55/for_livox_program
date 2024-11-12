# 2次元lidarを用いて，スキャンデータを取得，csvファイルに出力

import csv
import time
import numpy as np
import matplotlib.pyplot as plt
from hokuyolx import HokuyoLX

# スキャンデータをcsvに変換する
def scan2csv(timestamp, scan_data, csv_path):
    # scan_dataは二次元配列[[測定角度(rad), 距離(mm)]]
    dist_list = list(np.ravel(scan_data))
    
    with open(csv_path, encoding="utf-8", mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp]+dist_list)

# process管理用のtxtファイルを開く
def open_txt(txt_path):
    with open(txt_path, "r") as f:
        content = f.read().split(",")
    
    is_scan = bool(int(content[0]))
    output_path = content[1].replace("\n", "")
    
    return is_scan, output_path

# 測定を行う
def scan():
    status_path = "start_recording\\now_process.txt"

    laser = HokuyoLX()
    while True:
        # 3次元LiDAR側のステータスを確認
        is_scan, csv_path = open_txt(status_path)

        if is_scan:
            try:
                # lidarでスキャン
                timestamp, scan_data = laser.get_dist()
                # スキャンデータをcsvに変換
                scan2csv(timestamp, scan_data, csv_path)
            except Exception as e:
                break
        
        if is_scan == False:
            time.sleep(1)
    
    laser.close()

if __name__ == "__main__":
    scan()
