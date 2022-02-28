import os
import pickle


class SaveManager:
    def __init__(self, saves_name_file):
        self.saves_name_file = saves_name_file
        self.save_names = self.get_save_names_from_file()

    def save_game(self, game, file_name):
        save_bin = open(file_name, 'wb')
        pickle.dump(game, save_bin)
        save_bin.close()

    def create_file(self, game, file_name):
        if file_name not in self.save_names:
            self.save_names.append(game.save_file_name)
            file = open(self.saves_name_file, 'a')
            file.write(game.save_file_name + '\n')
            file.close()
            self.save_game(game, file_name)

    def load_game(self, file_name):
        try:
            save_file = open(file_name, 'rb')
            game_load = pickle.load(save_file)
            save_file.close()
        except FileNotFoundError:
            game_load = None
        return game_load

    def delete_game(self, file_name, file_path):
        self.save_names.remove(file_name)
        with open(self.saves_name_file, 'w') as file:
            for name in self.save_names:
                file.write(f'{name}\n')
        file.close()

        if os.path.exists(file_path):
            os.remove(file_path)

    def get_save_names_from_file(self):
        try:
            file = open(self.saves_name_file, 'r')
            save_names = []
            for line in file:
                save_names.append(line.rstrip())
            file.close()
            return save_names
        except FileNotFoundError:
            open(self.saves_name_file, 'x').close()
            return []

