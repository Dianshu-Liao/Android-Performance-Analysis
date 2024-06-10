import os




class Util:


    @staticmethod
    def list_files(directory):
        file_paths = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        return file_paths

    @staticmethod
    def line_numbers_of_txt_file(file_path):
        f = open(file_path, 'r')
        lines = f.readlines()
        f.close()
        return len(lines)


    @staticmethod
    def find_files(directory, endswith):
        csv_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(endswith):
                    csv_files.append(os.path.join(root, file))
        return csv_files