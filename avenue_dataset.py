import os
from PIL import Image
import json


class AvenueDataset:
    def __init__(self):
        self.base_path = 'avenue/testing/frames'
        self.now_video = '01'
        self.label_data = None
        with open('avenue.json', 'r', encoding='utf-8') as f:
            self.label_data = json.load(f)
            f.close()

    def get_video_data(self, video_id=None):
        if video_id is not None:
            self.now_video = video_id
        video_base_path = self.base_path + '/' + self.now_video
        frames_list = os.listdir(video_base_path)
        img_list = []
        for frame in frames_list:
            path = video_base_path + '/' + frame
            img = Image.open(path)
            img_list.append(img)


        label_list = [0] * self.label_data[self.now_video]['length']
        for anomalie in self.label_data[self.now_video]['anomalies']:
            for _, anomalie_list in anomalie.items():
                for anomalie_frame_list in anomalie_list:
                    start_frame = anomalie_frame_list[0] - 1
                    end_frame = anomalie_frame_list[1]
                    for i in range(start_frame, end_frame):
                        label_list[i] = 1
        if video_id is None:
            self.update_video()
        return img_list, label_list

    def update_video(self):
        video_id = int(self.now_video)
        video_id += 1
        self.now_video = '{:02d}'.format(video_id)


if __name__ == '__main__':
    a = AvenueDataset()

    for i in range(21):
        a.get_video_data()
