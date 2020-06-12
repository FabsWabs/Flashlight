import os
import pickle
from src.core.tile import *
from src.core.utils import resource_path


class Level:
    """Contains all the information about existing levels.
    
    Functions:
    render          -- render all elements in a level
    get_objects     -- get all the objects in the current level
    is_valid        -- check if level contains one start and one goal
    save            -- save the level with pickle
    load_map        -- load a level from pickle file
    get_all_levels  -- get a list of all existing levels
    """
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

    def add_object(self, obj, pos):
        self.boxes_list[pos] = obj

    def delete_object(self, arg):
        if arg == 'Start':
            for obj in list(self.boxes_list.values()):
                if type(obj) is Start:
                    del self.boxes_list[obj.get_pos()]
        elif arg == 'End':
            for obj in list(self.boxes_list.values()):
                if type(obj) is End:
                    del self.boxes_list[obj.get_pos()]
        else:
            del self.boxes_list[arg]

    def get_object(self, arg):
        if arg == 'Start':
            for obj in self.boxes_list.values():
                if type(obj) is Start:
                    return obj
        elif arg == 'End':
            for obj in self.boxes_list.values():
                if type(obj) is End:
                    return obj
        else:
            if arg in self.boxes_list:
                return self.boxes_list[arg]
            else:
                return None

    def get_start_tuple(self):
        for obj in self.boxes_list.values():
            if type(obj) is Start:
                return obj.get_pos()
        
    def get_end_tuple(self):
        for obj in self.boxes_list.values():
            if type(obj) is End:
                return obj.get_pos()

    def get_objects(self):
        return self.boxes_list
    
    def print_objects(self):
        for obj in self.boxes_list.items():
            print(f'Key: {obj[0]}, Tile: {type(obj[1])}, Connection: {obj[1].get_connection()}')
        print()

    def is_valid(self):
        start, end = False, False
        for obj in self.boxes_list.values():
            if type(obj) is Start:
                start = True
            elif type(obj) is End:
                end = True
        return start and end

    def is_free(self, pos):
        if (not pos in self.boxes_list.keys()):
            return True
        else:
            return False

    def save(self, name):
        for obj in self.boxes_list.values():
            obj.del_surf()
        folder = resource_path(os.path.join("assets/levels", name))
        if not os.path.exists(folder):
            os.mkdir(folder)
            file = os.path.join(folder, name + '.pkl')
            with open(file, 'wb') as output:
                pickle.dump([self.get_objects()], output, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            print('level already exists!')

    def load_map(self, name):
        folder = resource_path(os.path.join("assets/levels", name))
        if os.path.exists(folder):
            file = os.path.join(folder, name + '.pkl')
            with open(file, 'rb') as input:
                data = pickle.load(input)
                self.boxes_list, = data
                for obj in self.boxes_list.values():
                    obj.add_surf()
        else:
            print('level does not exist')

    def get_all_levels(self):
        list_names = []
        folder = resource_path("assets/levels")
        list_names = [element for element in os.listdir(folder) if os.path.isdir(os.path.join(folder, element))]
        return list_names

    def delete_level(self, name):
        import shutil
        folder = resource_path(os.path.join("assets/levels", name))
        shutil.rmtree(folder)
        pass