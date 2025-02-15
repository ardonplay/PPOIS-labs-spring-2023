import lxml.etree as elementor

from lr4.garden.model import Model, create_dir
from lr4.garden.plants import Plant, what_the_plant, what_the_seed, Seed


class Garden:

    def __init__(self, x, y):
        create_dir(x, y)
        self.x = x
        self.y = y
        self.model = Model(self)
        self.time = 0

    def warp(self, index: int):
        for i in range(len(self.model.matrix)):
            for j in range(len(self.model.matrix[0])):
                if self.model.matrix[i][j] is not None:
                    self.model.matrix[i][j].time += index
        self.model.weather.time -= 1
        self.time += index


def load() -> Garden:
    tree = elementor.parse(r'.gardenrc/Entities/plants.xml')
    root = tree.getroot()

    garden = Garden

    for child in root:
        match child.tag:
            case "square":
                position = []
                for pos in child:
                    position.append(int(pos.text))
                garden = Garden(position[0], position[1])
            case "weather":
                for weather in child:
                    match weather.tag:
                        case "time":
                            garden.model.weather.time = int(weather.text)
                        case "type":
                            garden.model.weather.type = weather.text
            case "time":
                garden.time = int(child.text)
            case "plants":
                plant = Plant
                for plants in child:
                    for configs in plants:
                        match configs.tag:
                            case "name":
                                plant = what_the_plant(configs.text)
                            case "length":
                                plant.length = int(configs.text)
                            case "time":
                                plant.time = int(configs.text)
                            case "health":
                                plant.health = int(configs.text)
                            case "position":
                                position = []
                                for pos in configs:
                                    position.append(pos.text)
                                garden.model.add_entity(plant, int(position[0]), int(position[1]))
            case "seeds":
                seed = Seed
                for seeds in child:
                    for configs in seeds:
                        match configs.tag:
                            case "name":
                                seed = what_the_seed(configs.text)
                            case "time":
                                seed.time = int(configs.text)
                            case "health":
                                seed.health = int(configs.text)
                            case "position":
                                position = []
                                for pos in configs:
                                    position.append(pos.text)
                                garden.model.add_entity(seed, int(position[0]), int(position[1]))

    return garden
