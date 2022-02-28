import os
import pickle
import re


class SaveManager:
    def __init__(self, saves_dir):
        self.saves_dir = saves_dir
        self.save_names = self.get_save_files()

    def save_game(self, game, file_name):
        save_bin = open(file_name, 'wb')
        pickle.dump(game, save_bin)
        save_bin.close()

    def load_game(self, file_name):
        try:
            save_file = open(f'{self.saves_dir}{file_name}', 'rb')
            game_load = pickle.load(save_file)
            save_file.close()
        except FileNotFoundError:
            game_load = None
        return game_load

    def delete_game(self, file_name, file_path):
        self.save_names.remove(file_name)
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_save_files(self):
        saves = []
        for save_file in os.listdir('save_files'):
            if re.search(r".bin$", save_file) is not None:
                saves.append(save_file[:-4])
        return saves
