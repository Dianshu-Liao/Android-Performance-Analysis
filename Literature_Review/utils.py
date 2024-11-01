import os
import pandas as pd
import json
import pickle


class Utils:

    @staticmethod
    def load_keywords(file_path='./Keywords.txt', spliter='\n'):
        # 打开文件并读取内容
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        # 默认使用\n分隔字符串并存储到列表中
        keywords = file_content.split(spliter)

        return keywords

    @staticmethod
    def get_all_subfiles(folder_path):
        # 获取指定文件夹下的所有文件，并返回完整路径
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if
                 os.path.isfile(os.path.join(folder_path, f))]
        return files

    @staticmethod
    def merge_all_csvs_under_a_folder(folder_path, saved_path):
        csv_files = Utils.get_all_subfiles(folder_path)
        df = pd.DataFrame()
        for csv_file in csv_files:
            csv_df = pd.read_csv(csv_file)
            df = pd.concat([df, csv_df], ignore_index=True)
        df_no_duplicates = df.drop_duplicates()
        df_no_duplicates.to_csv(saved_path, index=0)

    @staticmethod
    def remove_csv_duplicates(csv_path):
        df = pd.read_csv(csv_path)
        df = df.drop_duplicates()
        df.to_csv(csv_path, index=False)

    @staticmethod
    def dict_to_json(dic, json_path):
        # 将字典存储为JSON文件
        with open(json_path, 'w') as f:
            json.dump(dic, f)

    @staticmethod
    def save_list_to_pkl(list_data, saved_file_path):
        with open(saved_file_path, 'wb') as f:
            pickle.dump(list_data, f)

    @staticmethod
    def read_pkl_to_list(saved_file_path):
        with open(saved_file_path, 'rb') as f:
            list_data = pickle.load(f)
        return list_data


    @staticmethod
    def find_files(directory, endswith):
        csv_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(endswith):
                    csv_files.append(os.path.join(root, file))
        return csv_files

