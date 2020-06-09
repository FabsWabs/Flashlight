import os
import pickle
from src.core.tile import *


class Level:
    def __init__(self, name=None, level=None):
        if name is not None:
            self.load_map(name)
        elif level is not None:
            self.start, self.end, self.boxes_list = level
        else:
            self.boxes_list = {}
            self.start = None
            self.end = None
        
    def render(self, screen):
        for box in self.boxes_list.values():
            box.show(screen)
        if self.start is not None:
            self.start.show(screen)
        if self.end is not None:
            self.end.show(screen)

    def add_box(self, pos):
        self.boxes_list[pos] = Box(pos)

    def add_start(self, pos):
        self.start = Start(pos)

    def add_end(self, pos):
        self.end = End(pos)

    def del_box(self, pos):
        del self.boxes_list[pos]

    def del_start(self):
        del self.start

    def del_end(self):
        del self.end

    def get_start_tuple(self):
        return self.start.get_pos()

    def get_end_tuple(self):
        return self.end.get_pos()

    def get_boxes(self):
        return self.boxes_list

    def get_level(self):
        return [self.start, self.end, self.boxes_list]

    def is_free(self, pos):
        if (not pos in self.boxes_list.keys() and 
            not pos == self.get_start_tuple() and 
            not pos == self.get_end_tuple()):
            return True
        else:
            return False

    def save(self, name):
        for box in self.boxes_list.values():
            box.del_surf()
        self.start.del_surf()
        self.end.del_surf()
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../assets/levels", name)
        if not os.path.exists(folder):
            os.mkdir(folder)
            file = os.path.join(folder, name + '.pkl')
            with open(file, 'wb') as output:
                pickle.dump(self.get_level(), output, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print('level already exists!')

    def load_map(self, name):
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../assets/levels", name)
        if os.path.exists(folder):
            file = os.path.join(folder, name + '.pkl')
            with open(file, 'rb') as input:
                data = pickle.load(input)
                self.start, self.end, self.boxes_list = data
                for box in self.boxes_list.values():
                    box.add_surf()
                self.start.add_surf()
                self.end.add_surf()
        else:
            print('level does not exist')

    def get_all_levels(self):
        list_names = []
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../assets/levels")
        list_names = [element for element in os.listdir(folder) if os.path.isdir(os.path.join(folder, element))]
        return list_names

    def delete_level(self, name):
        import shutil
        folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../assets/levels", name)
        shutil.rmtree(folder)
        pass