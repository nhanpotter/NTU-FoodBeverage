import pygame
import pickle
import datetime
import time
import sys, math
from shortest_distance import shortest_path
from sort_and_search import *

###define constants, colors, ...
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GREY = (200, 200, 200)
BROWN = (255, 248, 220)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
WIDTH = WIDTH_INIT = 1200
HEIGHT = HEIGHT_INIT = 800
BLIT_X = 0
BLIT_Y = 0
STEP = 40
RATIO = 1.3
###load image and music
window_surface = pygame.display.set_mode((WIDTH_INIT, HEIGHT_INIT))
original_image = pygame.image.load("NTUmap.png")
image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
tick_image = pygame.image.load("tick.png")

###initialize pygame and create window
clock = pygame.time.Clock()
pygame.init()


###class of objects
# Foodcourt (including stall)
class FoodCourt:

    # initialise
    def __init__(self, name, address, number):
        self.name = name  # arguments to set all the instance variables
        self.address = address
        self.number = number
        self.stall_list = []

    def addStall(self, stall_name, category, aircon_availability, address, wkday_op_time, wkday_cl_time, wkend_op_time,
                 wkend_cl_time):
        s = Stall(stall_name, category, aircon_availability, address, wkday_op_time, wkday_cl_time, wkend_op_time,
                  wkend_cl_time)
        self.stall_list.append(s)  # stalls added into FoodCourt obj  (Stall obj belongs to FoodCourt obj)

    def addFood(self, stall_name, food_name, price, rating):
        found = False  # to ensure that stall name is added in the correct format (Can prevent typos etc)
        for s_name in self.stall_list:
            if (s_name.name == stall_name):
                found = True
                break
        if found == False:
            print("ERROR : Stall not found, unable to add", food_name, "in", stall_name)
            return

        try:  # to ensure that price and rating of the food are added in the correct format (ie. price cannot be negative, ratings cannot be more than 5)
            if price > 0 and (rating > 0 and rating <= 5):
                for stall in self.stall_list:
                    if stall.name == stall_name:
                        stall.addFood(food_name, price,
                                      rating)  # Procedural abstraction: Only need to call this function (addFood) to add the food, the FoodCourt class does not need to know how the Stall class implements the addFood function
            else:
                raise ValueError
        except ValueError:

            print("ERROR : Couldn't add", food_name, "to", stall_name, "with price", price)

    def searchFoodByName(self, food_name):
        __searchResultList = []
        for stall in self.stall_list:
            list1 = stall.searchFoodByName(food_name)  # this result is returned from the function in Stall object
            for food in list1:
                result_dict = {"Food Court Name": self.name,
                               "Stall Name": stall.name,
                               # for each of the result from the Stall object, a dict will be created
                               "Food Name": food.name,
                               "Price": food.price,
                               "Rating": food.rating,
                               "Aircon Availability": stall.aircon_availability,
                               "Weekday Opening Hours": stall.wkday_op_time + "-" + stall.wkday_cl_time,
                               "Weekend Opening Hours": stall.wkend_op_time + "-" + stall.wkend_cl_time,
                               "Open/Close": stall.getStallStatus()}
                __searchResultList.append(result_dict)
        return __searchResultList

    def searchByPrice(self, min, max):
        __searchResultList = []
        for stall in self.stall_list:
            list1 = stall.searchByPrice(min, max)  # this result is returned from the function in Stall object
            for food in list1:
                result_dict = {"Food Court Name": self.name,
                               "Stall Name": stall.name,
                               "Food Name": food.name,
                               "Price": food.price,
                               "Rating": food.rating,
                               "Aircon Availability": stall.aircon_availability,
                               "Weekday Opening Hours": stall.wkday_op_time + "-" + stall.wkday_cl_time,
                               "Weekend Opening Hours": stall.wkend_op_time + "-" + stall.wkend_cl_time,
                               "Open/Close": stall.getStallStatus()}
                __searchResultList.append(result_dict)
        return __searchResultList

    def searchByCategory(self, user_food_category):
        __searchResultList = []
        for stall in self.stall_list:
            food_belongs_to_cat = stall.checkIfBelongToCategory(
                user_food_category)  # this result is returned from the function in Stall object
            if food_belongs_to_cat == True:
                result_dict = {"Food Court Name": self.name,
                               "Stall Name": stall.name,
                               "Category": stall.category,
                               "Address": stall.address,
                               "Contact Number": self.number,
                               "Aircon Availability": stall.aircon_availability,
                               "Weekday Opening Hours": stall.wkday_op_time + "-" + stall.wkday_cl_time,
                               "Weekend Opening Hours": stall.wkend_op_time + "-" + stall.wkend_cl_time,
                               "Open/Close": stall.getStallStatus()}
                __searchResultList.append(result_dict)
        return __searchResultList

    def getStalls(self):
        __searchResultList = []
        for stall in self.stall_list:
            result_dict = {"Food Court Name": self.name,
                           "Stall Name": stall.name,
                           "Category": stall.category,
                           "Address": stall.address,
                           "Contact Number": self.number,
                           "Aircon Availability": stall.aircon_availability,
                           "Weekday Opening Hours": stall.wkday_op_time + "-" + stall.wkday_cl_time,
                           "Weekend Opening Hours": stall.wkend_op_time + "-" + stall.wkend_cl_time,
                           "Open/Close": stall.getStallStatus()}
            __searchResultList.append(result_dict)
        return __searchResultList

    def searchByAirconAvailability(self, user_aircon):
        __searchResultList = []
        for stall in self.stall_list:  # goes thru all the stalls in the stall list and returns a dict of stalls with aircon or no aircon (based on input from user_aircon)
            if stall.aircon_availability.lower() == user_aircon:
                result_dict = {"Food Court Name": self.name,
                               "Stall Name": stall.name,
                               "Aircon Availability": stall.aircon_availability,
                               "Weekday Opening Hours": stall.wkday_op_time + "-" + stall.wkday_cl_time,
                               "Weekend Opening Hours": stall.wkend_op_time + "-" + stall.wkend_cl_time,
                               "Open/Close": stall.getStallStatus()}
                __searchResultList.append(result_dict)
        return __searchResultList

    def getStallByName(self, sname):
        __searchResultList = []
        for stall in self.stall_list:
            if sname.lower() in stall.name.lower():
                __searchResultList.append(stall)
        return __searchResultList


# Stall (including Food)
class Stall:

    # intialise
    def __init__(self, name, category, aircon_availability, address, wkday_op_time, wkday_cl_time, wkend_op_time,
                 wkend_cl_time):
        self.name = name
        self.category = category
        self.address = address
        self.aircon_availability = aircon_availability
        self.wkday_op_time = wkday_op_time
        self.wkday_cl_time = wkday_cl_time
        self.wkend_op_time = wkend_op_time
        self.wkend_cl_time = wkend_cl_time
        self.food_list = []

    def addFood(self, name, price, rating):
        f = Food(name, price, rating)  # from Food object bc Food obj belongs to Stall obj
        self.food_list.append(f)

    def checkIfBelongToCategory(self, user_input_category):
        splitted_category = self.category.split(",")  # split the categories in 1 food
        splitted_user_category = user_input_category.split(
            ",")  # split the categories that the user inputted (user has to input in x,y format when searchng by categories)
        no_of_matches = len(splitted_user_category)
        for user_cat in splitted_user_category:
            for category in splitted_category:
                if category.strip().lower() == user_cat.strip().lower():
                    no_of_matches -= 1
                    break

        if no_of_matches == 0:
            return True
        else:
            return False

    def time_in_range(self, start, end, x):
        # """Return true if x is in the range [start, end]"""
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end

    def getStallStatus(self):
        # Compare the time here and return open or close
        splitted_wkday_op_time = self.wkday_op_time.split(":")
        splitted_wkday_cl_time = self.wkday_cl_time.split(":")
        wkday_op_hour_int = int(splitted_wkday_op_time[0])
        wkday_op_min_int = int(splitted_wkday_op_time[1])
        wkday_cl_hour_int = int(splitted_wkday_cl_time[0])
        wkday_cl_min_int = int(splitted_wkday_cl_time[1])

        splitted_wkend_op_time = self.wkend_op_time.split(":")
        splitted_wkend_cl_time = self.wkend_cl_time.split(":")
        wkend_op_hour_int = int(splitted_wkend_op_time[0])
        wkend_op_min_int = int(splitted_wkend_op_time[1])
        wkend_cl_hour_int = int(splitted_wkend_cl_time[0])
        wkend_cl_min_int = int(splitted_wkend_cl_time[1])

        current_hour = datetime.datetime.now().hour
        current_min = datetime.datetime.now().minute
        current_wkday = datetime.datetime.today().weekday()

        if current_wkday in range(0, 5):
            start = datetime.time(wkday_op_hour_int, wkday_op_min_int, 0)
            end = datetime.time(wkday_cl_hour_int, wkday_cl_min_int, 0)
            stall_opening = self.time_in_range(start, end, datetime.time(current_hour, current_min, 0))
            if stall_opening == True:
                return ("OPEN")
            else:
                return ("CLOSED")

        elif current_wkday in range(5, 7):
            start = datetime.time(wkend_op_hour_int, wkend_op_min_int, 0)
            end = datetime.time(wkend_cl_hour_int, wkend_cl_min_int, 0)
            stall_opening = self.time_in_range(start, end, datetime.time(current_hour, current_min, 0))
            if stall_opening == True:
                return ("OPEN")
            else:
                return ("CLOSED")

    # def between(self, a, b, c): #check if b is in between a and c
    #     return ((a <= b) and (b < c)) or ((c < a) and (a <= b)) or ((b < c) and (c < a))

    def searchFoodByName(self, food_name):
        __resultList = []
        for food in self.food_list:
            if len(food_name) > 0:
                if food_name.lower() in food.name.lower():  # the keyword 'in' is to check whether a word contains in another word under food names
                    __resultList.append(food)
            else:  # if nth is inputted (eg. user inputs space bar), len of food_name is 0, so all the food belonging to this stall will be appended into the list
                __resultList.append(food)
        return __resultList

    def searchByPrice(self, min,
                      max):  # user enter min and max price and will return a list of food within the searched range
        __resultlist = []
        self.food_list = sorted(self.food_list, key=lambda x: x.price)
        for food in self.food_list:
            if food.price >= min and food.price <= max:
                __resultlist.append(food)
        return __resultlist

    def getFood(self, user_input):
        __searchResultList = []
        for food in self.food_list:
            if user_input.lower() in food.name.lower():
                __searchResultList.append(food)
        return __searchResultList


# Food
class Food:
    # intialise
    def __init__(self, name, price, rating):  # add the details of the foods into the Food object
        self.name = name
        self.price = price
        self.rating = rating


# Vertex
class Vertex:
    def __init__(self, name, coordinates):
        self.name = name
        self.coordinates = coordinates
        self.distance = sys.maxsize
        self.predecessor = None
        self.visited = False
        self.adjacent = {}

    def __lt__(self, other):
        self_priority = self.distance
        other_priority = other.distance
        return self_priority < other_priority


# Graph (contain Vertex)
class Graph:
    def __init__(self):
        self.vertex_set = []

    def add_vertex(self, name, coordinates):
        v = Vertex(name, coordinates)
        self.vertex_set.append(v)

    def add_adjacent(self, vertex1, vertex2):
        for node1 in self.vertex_set:
            if node1.name == vertex1:
                for node2 in self.vertex_set:
                    if node2.name == vertex2:
                        weight_x = node1.coordinates[0] - node2.coordinates[0]
                        weight_y = node1.coordinates[1] - node2.coordinates[1]
                        weight = math.sqrt(weight_x ** 2 + weight_y ** 2)
                        node1.adjacent[node2.name] = weight
                        node2.adjacent[node1.name] = weight

    def get_adjacent(self):
        list = []
        for vert in self.vertex_set:
            list.append(vert.adjacent)
        return list

    def set_start(self, posX, posY):
        nearest_distance = sys.maxsize
        for index, node in enumerate(self.vertex_set):
            if math.sqrt((node.coordinates[0] - posX) ** 2 + (node.coordinates[1] - posY) ** 2) < nearest_distance:
                nearest_distance = math.sqrt((node.coordinates[0] - posX) ** 2 + (node.coordinates[1] - posY) ** 2)
                nearest_index = index
        self.vertex_set[nearest_index].distance = nearest_distance  # modify later
        return nearest_index

    def get_index(self, name):
        for index, node in enumerate(self.vertex_set):
            if node.name == name:
                return index


# class for UI
class Textbox:
    def __init__(self, x, y, w, h, text, color, font_size=20):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = text
        self.color = color
        text_srf = self.font.render(self.text, True, self.color)
        text_rect = text_srf.get_rect()
        text_rect.center = self.rect.center
        window_surface.blit(text_srf, text_rect)

    def draw_align(self, y_new, h_new, text_new):
        align_rect = pygame.Rect(self.x, y_new, self.w, h_new)
        text_align = self.font.render(text_new, True, self.color)
        text_align_rect = text_align.get_rect()
        text_align_rect.center = align_rect.center
        window_surface.blit(text_align, text_align_rect)


class Button:
    def __init__(self, x, y, w, h, text, color, font_size=20):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.big_font = pygame.font.Font('freesansbold.ttf', font_size + 5)
        self.text = text
        pygame.draw.rect(window_surface, color, self.rect)
        pygame.draw.rect(window_surface, BLACK, self.rect, 1)
        text_srf = self.font.render(self.text, True, BLACK)
        text_rect = text_srf.get_rect()
        text_rect.center = self.rect.center
        window_surface.blit(text_srf, text_rect)

    def move_and_click(self, mouseX, mouseY, color_click, counter, reverse):
        global screen_running
        mouseX_unclicked, mouseY_unclicked = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouseX_unclicked, mouseY_unclicked):
            pygame.draw.rect(window_surface, color_click, self.rect)
            pygame.draw.rect(window_surface, BLACK, self.rect, 1)
            text_srf = self.big_font.render(self.text, True, BLACK)
            text_rect = text_srf.get_rect()
            text_rect.center = self.rect.center
            window_surface.blit(text_srf, text_rect)
        if self.rect.collidepoint(mouseX, mouseY):
            screen_running = False
            if reverse == False:
                counter += 1
            if reverse == True:
                counter -= 1
            time.sleep(0.2)
        return counter

    def move_and_take(self, mouseX, mouseY, color_click, counter, last):
        global screen_running
        map_index = None
        mouseX_unclicked, mouseY_unclicked = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouseX_unclicked, mouseY_unclicked):
            pygame.draw.rect(window_surface, color_click, self.rect)
            pygame.draw.rect(window_surface, BLACK, self.rect, 1)
            text_srf = self.big_font.render(self.text, True, BLACK)
            text_rect = text_srf.get_rect()
            text_rect.center = self.rect.center
            window_surface.blit(text_srf, text_rect)
        if self.rect.collidepoint(mouseX, mouseY):
            screen_running = False
            counter += 1
            if last == False:
                map_index = -12 + self.y / 50
            else:
                map_index = -100 + self.y
            time.sleep(0.2)
        return counter, map_index

    def click_only(self, color_click, counter, reverse):
        mouseX_unclicked, mouseY_unclicked = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouseX_unclicked, mouseY_unclicked):
            pygame.draw.rect(window_surface, color_click, self.rect)
            pygame.draw.rect(window_surface, BLACK, self.rect, 1)
            text_srf = self.big_font.render(self.text, True, BLACK)
            text_rect = text_srf.get_rect()
            text_rect.center = self.rect.center
            window_surface.blit(text_srf, text_rect)
        mouse_pressed = pygame.mouse.get_pressed()
        mouseX = mouseY = 0
        if mouse_pressed[0]:
            mouseX, mouseY = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouseX, mouseY):
            if reverse == False:
                counter += 1
            if reverse == True:
                counter -= 1
            time.sleep(0.1)
        mouseX = mouseY = 0
        return counter

    def move_and_update(self, mouseX, mouseY, color_click):
        map_index = None
        mouseX_unclicked, mouseY_unclicked = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouseX_unclicked, mouseY_unclicked):
            pygame.draw.rect(window_surface, color_click, self.rect)
            pygame.draw.rect(window_surface, BLACK, self.rect, 1)
            text_srf = self.big_font.render(self.text, True, BLACK)
            text_rect = text_srf.get_rect()
            text_rect.center = self.rect.center
            window_surface.blit(text_srf, text_rect)
        if self.rect.collidepoint(mouseX, mouseY):
            map_index = -2 + self.y / 50
        return map_index


class Inputbox:
    def __init__(self, x, y, w, h, text, font_size=20):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = text
        self.active = False  # also use for Yes or No
        self.string = ""
        self.color = GREY

    def input_text(self, event):
        text_srf = self.font.render(self.text, True, BLACK)
        text_rect = text_srf.get_rect()
        text_rect.midright = self.rect.midleft
        window_surface.blit(text_srf, text_rect)
        unuse_key = [pygame.K_RETURN, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_BACKSPACE]
        # for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = WHITE if self.active else GREY
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if not event.key in unuse_key:
                if event.key == pygame.K_BACKSPACE and len(self.string) > 0:
                    self.string = self.string[:-1]
                if not event.key in unuse_key:
                    self.string += event.unicode
        pygame.draw.rect(window_surface, self.color, self.rect)
        pygame.draw.rect(window_surface, BLACK, self.rect, 1)
        text_input_srf = self.font.render(self.string, True, BLACK)
        text_input_rect = text_input_srf.get_rect()
        text_input_rect.midleft = self.rect.midleft
        window_surface.blit(text_input_srf, text_input_rect)

    def tick_box(self, event):
        text_srf = self.font.render(self.text, True, BLACK)
        text_rect = text_srf.get_rect()
        text_rect.midright = self.rect.midleft
        window_surface.blit(text_srf, text_rect)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            # Change the current color of the input box.
        if not self.active:
            pygame.draw.rect(window_surface, self.color, self.rect)
        if self.active:
            pygame.draw.rect(window_surface, self.color, self.rect)
            tick = pygame.transform.scale(tick_image, (self.w, self.h))
            window_surface.blit(tick, (self.x, self.y))
        pygame.draw.rect(window_surface, BLACK, self.rect, 1)


###function
def zoom_in():
    global WIDTH, HEIGHT, BLIT_X, BLIT_Y
    OLD_WIDTH, OLD_HEIGHT = WIDTH, HEIGHT
    WIDTH *= RATIO
    WIDTH = round(WIDTH)
    HEIGHT *= RATIO
    HEIGHT = round(HEIGHT)
    BLIT_X -= (WIDTH - OLD_WIDTH) / 2
    BLIT_Y -= (HEIGHT - OLD_HEIGHT) / 2


def zoom_out():
    global WIDTH, HEIGHT, BLIT_X, BLIT_Y
    OLD_WIDTH, OLD_HEIGHT = WIDTH, HEIGHT
    WIDTH /= RATIO
    WIDTH = round(WIDTH)
    HEIGHT /= RATIO
    HEIGHT = round(HEIGHT)
    BLIT_X -= (WIDTH - OLD_WIDTH) / 2
    BLIT_Y -= (HEIGHT - OLD_HEIGHT) / 2


def zoom_initial():
    global WIDTH, HEIGHT, BLIT_X, BLIT_Y
    if BLIT_X > 0:
        BLIT_X = 0
    elif BLIT_X < WIDTH_INIT - WIDTH:
        BLIT_X = WIDTH_INIT - WIDTH
    if BLIT_Y > 0:
        BLIT_Y = 0
    elif BLIT_Y < HEIGHT_INIT - HEIGHT:
        BLIT_Y = HEIGHT_INIT - HEIGHT


def mouse_to_pos(BLIT_X, BLIT_Y, WIDTH, HEIGHT, mouseX, mouseY):
    x = round((mouseX - BLIT_X) * WIDTH_INIT / WIDTH)
    y = round((mouseY - BLIT_Y) * HEIGHT_INIT / HEIGHT)
    return x, y


def main():
    global OLD_WIDTH, OLD_HEIGHT, WIDTH, HEIGHT, BLIT_X, BLIT_Y, FPS, screen_running, screen_counter
    screen_counter = 1
    subscreen1_counter = subscreen2_counter = subscreen3_counter = subscreen4_counter = 0
    mapscreen1_counter = mapscreen2_counter = 0
    map2_name = 0

    zoom_i = 0
    #######
    while True:
        file_data = open("main_data.txt", "rb")
        foodcourt_list = pickle.load(file_data)
        node_data = open("node_data.txt", "rb")
        g = pickle.load(node_data)
        if screen_counter == 1:
            mouseX = mouseY = posX = posY = 0
            screen_running = True
            while screen_running:
                pressed = pygame.key.get_pressed()
                mouse_pressed = pygame.mouse.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    ### using map
                if pressed[pygame.K_LEFTBRACKET] and 0 <= zoom_i < 5:
                    zoom_in()
                    zoom_i += 1
                elif pressed[pygame.K_RIGHTBRACKET] and 0 < zoom_i <= 5:
                    zoom_out()
                    zoom_i -= 1
                if pressed[pygame.K_RIGHT]:
                    BLIT_X -= STEP
                elif pressed[pygame.K_DOWN]:
                    BLIT_Y -= STEP
                elif pressed[pygame.K_LEFT]:
                    BLIT_X += STEP
                elif pressed[pygame.K_UP]:
                    BLIT_Y += STEP
                zoom_initial()  # if the screen get out of the window
                #
                image = pygame.transform.scale(original_image, (WIDTH, HEIGHT))
                window_surface.fill(WHITE)
                window_surface.blit(image, (BLIT_X, BLIT_Y))  ####change this to blit it
                # draw on image
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    if not (mouseX > WIDTH_INIT - 230 and mouseY < 100):
                        mouseX_check = mouseX
                        mouseY_check = mouseY
                        posX, posY = mouse_to_pos(BLIT_X, BLIT_Y, WIDTH, HEIGHT, mouseX_check, mouseY_check)
                if posX != 0 and posY != 0:
                    position_box = Textbox(WIDTH_INIT - 210, 10, 170, 20, "Position: " + str(posX) + ", " + str(posY),
                                           BLACK)
                    submit_button = Button(WIDTH_INIT - 210, 40, 140, 35, "SUBMIT?", GREY, 30)
                    screen_counter = submit_button.move_and_click(mouseX, mouseY, GREEN, screen_counter, False)
                # FPS
                clock.tick(FPS)
                pygame.display.flip()

        if screen_counter == 2 and subscreen1_counter == 0 and subscreen2_counter == 0 and subscreen3_counter == 0:
            mouseX = mouseY = 0
            screen_running = True
            food_inputbox = Inputbox(250, 250, 300, 50, "Food name: ", 30)
            min_price = Inputbox(350, 350, 75, 50, "Min price($): ", 30)
            max_price = Inputbox(350, 500, 75, 50, "Max price($): ", 30)
            aircon_tick_box = Inputbox(950, 350, 75, 50, "Aircon Availability ", 30)
            # min_price = Inputbox()
            while screen_running:
                # draw on surface
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                window_surface.fill(WHITE)
                pygame.draw.line(window_surface, BLACK, [0, 200], [WIDTH_INIT, 200], 5)
                pygame.draw.line(window_surface, BLACK, [0, 600], [WIDTH_INIT, 600], 5)
                food_court_button = Button(400, 75, 400, 75, "Food court lists", GREY, 30)
                subscreen1_counter = food_court_button.move_and_click(mouseX, mouseY, GREEN, subscreen1_counter, False)
                update_button = Button(200, 675, 400, 75, "Update information", GREY, 30)
                subscreen3_counter = update_button.move_and_click(mouseX, mouseY, GREEN, subscreen3_counter, False)
                add_button = Button(650, 675, 400, 75, "Add new food", GREY, 30)
                subscreen4_counter = add_button.move_and_click(mouseX, mouseY, GREEN, subscreen4_counter, False)
                search_button = Button(900, 480, 200, 75, "Search", GREY, 30)
                subscreen2_counter = search_button.move_and_click(mouseX, mouseY, YELLOW, subscreen2_counter, False)
                # back button
                back_button = Button(0, HEIGHT_INIT - 75, 100, 75, "BACK", RED, 30)
                screen_counter = back_button.move_and_click(mouseX, mouseY, RED, screen_counter, True)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    # draw input box
                    food_inputbox.input_text(event)
                    min_price.input_text(event)
                    max_price.input_text(event)
                    aircon_tick_box.tick_box(event)
                    pygame.display.flip()

                clock.tick(FPS)

        if subscreen1_counter == 1:
            mouseX = mouseY = 0
            screen_running = True
            page_counter = 1
            aircon1_tick_box = Inputbox(300, 625, 75, 75, "Aircon: ", 25)
            category_inputbox = Inputbox(300, 710, 290, 75, "Category: ", 25)
            distance_tick_box = Inputbox(950, 700, 75, 75, "Sort by distance: ", 25)
            while screen_running:
                # initialize new used class
                used_graph1 = Graph()
                used_graph1.vertex_set = [i for i in g.vertex_set]
                results1 = get_all_stalls(foodcourt_list)
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                if aircon1_tick_box.active:
                    results1 = search_by_aircon_availability(results1)
                if len(category_inputbox.string) > 0:
                    category_search_list = search_by_category(category_inputbox.string, foodcourt_list)
                    results1 = intersection(results1, category_search_list)

                for i in results1:
                    i["Distance"] = round(shortest_path(used_graph1, posX, posY, i["Food Court Name"], True))
                if distance_tick_box.active:
                    results1 = mergesort(results1, "Distance", False)

                page_limit = int(len(results1) / 10)
                page_remain = len(results1) % 10
                window_surface.fill(WHITE)

                # back button
                back_button1 = Button(0, HEIGHT_INIT - 75, 150, 75, "BACK", RED, 30)
                subscreen1_counter = back_button1.move_and_click(mouseX, mouseY, RED, subscreen1_counter, True)

                text1 = Textbox(0, 20, 200, 50, "Food court", BLACK, 14)
                text2 = Textbox(200, 20, 200, 50, "Stall", BLACK, 14)
                text3 = Textbox(400, 20, 200, 50, "Category", BLACK, 15)
                text4 = Textbox(600, 20, 350, 50, "Address", BLACK, 13)
                text5 = Textbox(950, 20, 75, 50, "Aircon", BLACK, 16)
                text6 = Textbox(1025, 20, 100, 50, "Distance", BLACK, 17)
                text7 = Textbox(1125, 20, 75, 50, "Status", BLACK, 17)
                pygame.draw.line(window_surface, BLACK, [0, 80], [WIDTH_INIT, 80], 5)

                if page_limit == 0:
                    pass
                elif page_limit == 1 and page_remain == 0:
                    pass
                elif page_counter == 1:
                    scroll_right_button = Button(950, 625, 100, 50, 'Next', GREY)
                    page_counter = scroll_right_button.click_only(GREEN, page_counter, False)
                elif (page_remain == 0 and page_counter == page_limit) or (page_counter == page_limit + 1):
                    scroll_left_button = Button(800, 625, 100, 50, 'Previous', GREY)
                    page_counter = scroll_left_button.click_only(RED, page_counter, True)
                else:
                    scroll_right_button = Button(950, 625, 100, 50, 'Next', GREY)
                    page_counter = scroll_right_button.click_only(GREEN, page_counter, False)
                    scroll_left_button = Button(800, 625, 100, 50, 'Previous', GREY)
                    page_counter = scroll_left_button.click_only(RED, page_counter, True)
                # draw table
                if page_limit != 0 and page_counter != page_limit + 1:
                    for i in range((page_counter - 1) * 10, page_counter * 10):
                        text1.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results1[i]["Food Court Name"])
                        text2.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results1[i]["Stall Name"])
                        text3.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results1[i]["Category"])
                        text4.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, str(results1[i]["Address"]))
                        text5.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50,
                                         str(results1[i]["Aircon Availability"]))
                        text6.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, str(results1[i]["Distance"]))
                        text7.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results1[i]["Open/Close"])
                        pygame.draw.line(window_surface, BLACK, [0, 200 + (i - 1 - (page_counter - 1) * 10) * 50],
                                         [WIDTH_INIT, 200 + (i - 1 - (page_counter - 1) * 10) * 50], 1)
                if page_remain != 0:
                    if page_counter == page_limit + 1:
                        for i in range(page_remain):
                            text1.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results1[i + page_limit * 10]["Food Court Name"])
                            text2.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results1[i + page_limit * 10]["Stall Name"])
                            text3.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results1[i + page_limit * 10]["Category"])
                            text4.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             str(results1[i + page_limit * 10]["Address"]))
                            text5.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             str(results1[i + page_limit * 10]["Aircon Availability"]))
                            text6.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             str(results1[i + page_limit * 10]["Distance"]))
                            text7.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results1[i + page_limit * 10]["Open/Close"])
                            pygame.draw.line(window_surface, BLACK, [0, 100 + (i + 1) * 500 / page_remain],
                                             [WIDTH_INIT, 100 + (i + 1) * 500 / page_remain], 1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    aircon1_tick_box.tick_box(event)
                    category_inputbox.input_text(event)
                    distance_tick_box.tick_box(event)
                    pygame.display.flip()
                clock.tick(FPS)

        if subscreen2_counter == 1:
            # variable or used object
            mouseX = mouseY = 0
            screen_running = True
            error = 0
            map_index = 0
            used_graph2 = Graph()
            used_graph2.vertex_set = [i for i in g.vertex_set]
            # get results list
            if len(max_price.string) == 0:
                max_price.string = str(sys.maxsize)
            if len(min_price.string) == 0:
                min_price.string = "0"
            results_list = []
            try:
                price_search_list = search_by_price(float(min_price.string), float(max_price.string), foodcourt_list)
                food_search_list = search_by_food(food_inputbox.string, foodcourt_list)
                results_list = intersection(food_search_list, price_search_list)
                for i in results_list:
                    i["Distance"] = round(shortest_path(used_graph2, posX, posY, i["Food Court Name"], True))
            except ValueError:
                error = 1

            if aircon_tick_box.active:
                results_list = search_by_aircon_availability(results_list)
            page_counter = 1
            page_limit = int(len(results_list) / 10)
            page_remain = len(results_list) % 10
            # tick box
            price_tick_box = Inputbox(500, 625, 75, 75, "Sort by price: ", 25)
            rating_tick_box = Inputbox(500, 710, 75, 75, "Sort by rating: ", 25)
            distance_tick_box = Inputbox(900, 710, 75, 75, "Sort by distance: ", 25)
            while screen_running:
                # get mouse pos
                mouseX = mouseY = 0
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()

                results = results_list
                if price_tick_box.active:
                    results = mergesort(results, "Price", False)
                if rating_tick_box.active:
                    results = mergesort(results, "Rating", True)
                if distance_tick_box.active:
                    results = mergesort(results, "Distance", False)
                window_surface.fill(WHITE)
                # back_button
                back_button2 = Button(0, HEIGHT_INIT - 75, 150, 75, "BACK", RED, 30)
                subscreen2_counter = back_button2.move_and_click(mouseX, mouseY, RED, subscreen2_counter, True)
                # draw table
                text1 = Textbox(0, 20, 250, 50, "Food court", BLACK, 16)
                text2 = Textbox(250, 20, 250, 50, "Stall", BLACK, 16)
                text3 = Textbox(500, 20, 300, 50, "Food name", BLACK, 16)
                text4 = Textbox(800, 20, 100, 50, "Distance", BLACK)
                text5 = Textbox(900, 20, 100, 50, "Price", BLACK)
                text6 = Textbox(1000, 20, 100, 50, "Rating", BLACK)
                text7 = Textbox(1100, 20, 100, 50, "Status", BLACK)
                pygame.draw.line(window_surface, BLACK, [0, 80], [WIDTH_INIT, 80], 5)
                if error == 1:
                    error_text = Textbox(0, -100, WIDTH_INIT, HEIGHT_INIT, "Wrong input!", RED, 40)
                if len(results) == 0:
                    no_result_text = Textbox(0, 0, WIDTH_INIT, HEIGHT_INIT, "No result was found!", RED, 40)
                elif page_limit == 0:
                    pass
                elif page_limit == 1 and page_remain == 0:
                    pass
                elif page_counter == 1:
                    scroll_right_button = Button(950, 625, 75, 75, 'Next', GREY)
                    page_counter = scroll_right_button.click_only(GREEN, page_counter, False)
                elif (page_remain == 0 and page_counter == page_limit) or (page_counter == page_limit + 1):
                    scroll_left_button = Button(800, 625, 75, 75, 'Previous', GREY)
                    page_counter = scroll_left_button.click_only(RED, page_counter, True)
                else:
                    scroll_right_button = Button(950, 625, 75, 75, 'Next', GREY)
                    page_counter = scroll_right_button.click_only(GREEN, page_counter, False)
                    scroll_left_button = Button(800, 625, 75, 75, 'Previous', GREY)
                    page_counter = scroll_left_button.click_only(RED, page_counter, True)
                # draw table
                if page_limit != 0 and page_counter != page_limit + 1:
                    for i in range((page_counter - 1) * 10, page_counter * 10):
                        # map_button
                        vars()["map_button" + str(i - (page_counter - 1) * 10)] = Button(800, 100 + (
                                    i - (page_counter - 1) * 10) * 50, 100, 50, "", GREY)
                        mapscreen2_counter, map_index = vars()[
                            "map_button" + str(i - (page_counter - 1) * 10)].move_and_take(mouseX, mouseY, WHITE,
                                                                                           mapscreen2_counter, False)
                        try:
                            map2_name = results[int(map_index + page_counter * 10)]["Food Court Name"]
                        except TypeError:
                            pass
                        # if map2_name != 0:
                        #     print(map2_name)
                        text1.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results[i]["Food Court Name"])
                        text2.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results[i]["Stall Name"])
                        text3.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results[i]["Food Name"])
                        text4.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, str(results[i]["Distance"]))
                        text5.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, str(results[i]["Price"]))
                        text6.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, str(results[i]["Rating"]))
                        text7.draw_align(100 + (i - (page_counter - 1) * 10) * 50, 50, results[i]["Open/Close"])
                        pygame.draw.line(window_surface, BLACK, [0, 200 + (i - 1 - (page_counter - 1) * 10) * 50],
                                         [WIDTH_INIT, 200 + (i - 1 - (page_counter - 1) * 10) * 50], 1)

                if page_remain != 0:
                    if page_counter == page_limit + 1:
                        for i in range(page_remain):
                            # map_button
                            map_button = Button(800, 100 + i * 500 / page_remain, 100, 500 / page_remain, "", GREY)
                            mapscreen2_counter, map_index = map_button.move_and_take(mouseX, mouseY, WHITE,
                                                                                     mapscreen2_counter, True)
                            try:
                                map2_name = results[int(map_index * page_remain / 500 + page_limit * 10)][
                                    "Food Court Name"]
                            except TypeError:
                                pass
                            text1.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results[i + page_limit * 10]["Food Court Name"])
                            text2.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results[i + page_limit * 10]["Stall Name"])
                            text3.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results[i + page_limit * 10]["Food Name"])
                            text4.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             str(results[i + page_limit * 10]["Distance"]))
                            text5.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             str(results[i + page_limit * 10]["Price"]))
                            text6.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             str(results[i + page_limit * 10]["Rating"]))
                            text7.draw_align(100 + i * 500 / page_remain, 500 / page_remain,
                                             results[i + page_limit * 10]["Open/Close"])
                            pygame.draw.line(window_surface, BLACK, [0, 100 + (i + 1) * 500 / page_remain],
                                             [WIDTH_INIT, 100 + (i + 1) * 500 / page_remain], 1)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    price_tick_box.tick_box(event)
                    rating_tick_box.tick_box(event)
                    distance_tick_box.tick_box(event)
                    if price_tick_box.active:
                        if rating_tick_box.active:
                            price_tick_box.active = False
                        if distance_tick_box.active:
                            price_tick_box.active = False
                    if rating_tick_box.active:
                        if price_tick_box.active:
                            rating_tick_box.active = False
                        if distance_tick_box.active:
                            rating_tick_box.active = False
                    if distance_tick_box.active:
                        if price_tick_box.active:
                            distance_tick_box.active = False
                        if rating_tick_box.active:
                            distance_tick_box.active = False
                    pygame.display.flip()
                clock.tick(FPS)

        if subscreen3_counter == 1:
            mouseX = mouseY = 0
            screen_running = True
            used_price = used_rating = 0
            # input box
            fc_update_box = Inputbox(200, 10, 250, 75, "Food Court Name: ", 15)
            stall_update_box = Inputbox(600, 10, 200, 75, "Stall name: ", 15)
            food_update_box = Inputbox(875, 10, 150, 75, "Food: ", 15)
            price_update_box = Inputbox(400, HEIGHT_INIT / 2 + 50, 100, 50, "Price: ")
            rating_update_box = Inputbox(800, HEIGHT_INIT / 2 + 50, 100, 50, "Rating: ")
            fc_only = stall_only = food_only = -1

            while screen_running:
                window_surface.fill(WHITE)
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                # back_button
                back_button3 = Button(0, HEIGHT_INIT - 75, 150, 75, "BACK", RED, 30)
                subscreen3_counter = back_button3.move_and_click(mouseX, mouseY, RED, subscreen3_counter, True)

                pygame.draw.line(window_surface, BLACK, [0, 95], [WIDTH_INIT, 95], 5)
                fc_list = get_fc_name(fc_update_box.string, foodcourt_list)

                for i in range(len(fc_list)):
                    button = Button(0, 100 + 50 * i, 400, 50, "", GREY)
                    fc_index = button.move_and_update(mouseX, mouseY, WHITE)
                    try:
                        fc_only = fc_list[int(fc_index)]
                        fc_update_box.string = fc_only.name
                        print(food_update_box.string)
                    except:
                        pass

                    text = Textbox(0, 100 + 50 * i, 400, 50, fc_list[i].name, BLACK, 14)
                    pygame.draw.line(window_surface, BLACK, [0, 150 + 50 * i], [400, 150 + 50 * i], 1)

                if fc_only != -1:
                    stall_list = fc_only.getStallByName(stall_update_box.string)
                    for i in range(len(stall_list)):
                        button = Button(400, 100 + 50 * i, 400, 50, "", GREY)
                        stall_index = button.move_and_update(mouseX, mouseY, WHITE)
                        try:
                            stall_only = stall_list[int(stall_index)]
                            stall_update_box.string = stall_only.name
                        except:
                            pass
                        text = Textbox(400, 100 + 50 * i, 400, 50, stall_list[i].name, BLACK, 14)
                        pygame.draw.line(window_surface, BLACK, [400, 150 + 50 * i], [800, 150 + 50 * i], 1)

                if stall_only != -1:
                    food_list = stall_only.getFood(food_update_box.string)
                    for i in range(len(food_list)):
                        button = Button(875, 100 + 50 * i, 150, 50, "", GREY)
                        food_index = button.move_and_update(mouseX, mouseY, WHITE)
                        try:
                            food_only = food_list[int(food_index)]
                            food_update_box.string = food_only.name
                        except:
                            pass
                        text = Textbox(875, 100 + 50 * i, 150, 50, food_list[i].name, BLACK, 14)
                        pygame.draw.line(window_surface, BLACK, [875, 150 + 50 * i], [1025, 150 + 50 * i], 1)
                if food_only != -1:
                    text_food = Textbox(1025, 10, 75, 75, "Price", BLACK, 15)
                    text_rating = Textbox(1100, 10, 100, 75, "Rating", BLACK, 15)
                    text1 = Textbox(1025, 100, 75, 50, str(food_only.price), BLACK)
                    text2 = Textbox(1100, 100, 100, 50, str(food_only.rating), BLACK)
                    text_update = Textbox(0, 0, WIDTH_INIT, HEIGHT_INIT, "UPDATE!!!", RED, 30)
                    text_and = Textbox(550, HEIGHT_INIT / 2 + 50, 100, 50, "AND", RED, 30)

                    try:
                        used_price = float(price_update_box.string)
                        used_rating = float(rating_update_box.string)
                        if used_rating <=5:
                            update_button = Button(WIDTH_INIT - 150, HEIGHT_INIT - 75, 150, 75, "UPDATE", YELLOW, 30)
                            subscreen3_counter = update_button.move_and_click(mouseX, mouseY, GREEN, subscreen3_counter,
                                                                              True)
                    except:
                        pass
                if not screen_running and used_rating!=0 and used_price!=0:
                    update(used_price, used_rating, fc_only.name, stall_only.name, food_only.name, foodcourt_list)
                    file_update_data = open("main_data.txt", "wb")
                    pickle.dump(foodcourt_list, file_update_data)
                    file_update_data.close()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    fc_update_box.input_text(event)
                    if fc_only != -1:
                        stall_update_box.input_text(event)
                        if stall_only != -1:
                            food_update_box.input_text(event)
                            if food_only != -1:
                                price_update_box.input_text(event)
                                rating_update_box.input_text(event)
                    pygame.display.flip()
                clock.tick(FPS)

        if subscreen4_counter == 1:
            mouseX = mouseY = 0
            used_food = used_price = used_rating = 0
            screen_running = True
            # input box
            fc_update_box = Inputbox(200, 10, 250, 75, "Food Court Name: ", 15)
            stall_update_box = Inputbox(600, 10, 200, 75, "Stall name: ", 15)
            food_update_box = Inputbox(500, 500, 250, 75, "Food: ", 30)
            price_update_box = Inputbox(500, 600, 150, 75, "Price: ", 30)
            rating_update_box = Inputbox(500, 700, 150, 75, "Rating: ", 30)
            fc_only = stall_only = -1
            while screen_running:
                window_surface.fill(WHITE)
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                # back_button
                back_button4 = Button(0, HEIGHT_INIT - 75, 150, 75, "BACK", RED, 30)
                subscreen4_counter = back_button4.move_and_click(mouseX, mouseY, RED, subscreen4_counter, True)

                pygame.draw.line(window_surface, BLACK, [0, 95], [WIDTH_INIT, 95], 5)
                fc_list = get_fc_name(fc_update_box.string, foodcourt_list)

                for i in range(len(fc_list)):
                    button = Button(0, 100 + 50 * i, 400, 50, "", GREY)
                    fc_index = button.move_and_update(mouseX, mouseY, WHITE)
                    try:
                        fc_only = fc_list[int(fc_index)]
                        fc_update_box.string = fc_only.name
                        print(food_update_box.string)
                    except:
                        pass

                    text = Textbox(0, 100 + 50 * i, 400, 50, fc_list[i].name, BLACK, 14)
                    pygame.draw.line(window_surface, BLACK, [0, 150 + 50 * i], [400, 150 + 50 * i], 1)

                if fc_only != -1:
                    stall_list = fc_only.getStallByName(stall_update_box.string)
                    for i in range(len(stall_list)):
                        button = Button(400, 100 + 50 * i, 400, 50, "", GREY)
                        stall_index = button.move_and_update(mouseX, mouseY, WHITE)
                        try:
                            stall_only = stall_list[int(stall_index)]
                            stall_update_box.string = stall_only.name
                        except:
                            pass
                        text = Textbox(400, 100 + 50 * i, 400, 50, stall_list[i].name, BLACK, 14)
                        pygame.draw.line(window_surface, BLACK, [400, 150 + 50 * i], [800, 150 + 50 * i], 1)
                if stall_only != -1:
                    text_update = Textbox(0, 0, WIDTH_INIT, HEIGHT_INIT - 100, "ADD NEW FOOD!!!", RED, 30)
                    try:
                        used_price = float(price_update_box.string)
                        used_rating = float(rating_update_box.string)
                        used_food = food_update_box.string
                        if used_rating <=5:
                            update_button = Button(WIDTH_INIT - 150, HEIGHT_INIT - 75, 150, 75, "ADD", YELLOW, 30)
                            subscreen4_counter = update_button.move_and_click(mouseX, mouseY, GREEN, subscreen3_counter,
                                                                              True)
                    except:
                        pass

                if not screen_running and used_price!=0 and used_rating!=0 and len(used_food)>0:
                    add(used_price, used_rating, fc_only.name, stall_only.name, used_food, foodcourt_list)
                    file_update_data = open("main_data.txt", "wb")
                    pickle.dump(foodcourt_list, file_update_data)
                    file_update_data.close()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    fc_update_box.input_text(event)
                    if fc_only != -1:
                        stall_update_box.input_text(event)
                        if stall_only != -1:
                            food_update_box.input_text(event)
                            price_update_box.input_text(event)
                            rating_update_box.input_text(event)

                    pygame.display.flip()
                clock.tick(FPS)

        if mapscreen2_counter == 1:
            # variable
            mouseX = mouseY = 0
            screen_running = True
            used_graph3 = Graph()
            used_graph3.vertex_set = [i for i in g.vertex_set]
            draw_path = [i for i in shortest_path(used_graph3, posX, posY, map2_name, False)]
            image = pygame.transform.scale(original_image, (WIDTH_INIT, HEIGHT_INIT))
            while screen_running:
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    mouseX, mouseY = pygame.mouse.get_pos()
                window_surface.fill(WHITE)
                window_surface.blit(image, (0, 0))
                # back button
                back_button_map = Button(0, HEIGHT_INIT - 75, 100, 75, "BACK", RED, 30)
                mapscreen2_counter = back_button_map.move_and_click(mouseX, mouseY, RED, mapscreen2_counter, True)
                # draw initial point
                pygame.draw.circle(window_surface, RED, (posX, posY), 6)
                # draw path
                for i in range(len(draw_path) - 1):
                    pygame.draw.line(window_surface, BLACK, draw_path[i], draw_path[i + 1], 5)
                pygame.draw.line(window_surface, BLACK, draw_path[-1], (posX, posY), 5)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                pygame.display.flip()
                clock.tick(FPS)


################DATA#####################
# this list contains foodcourt object

################DATA####################

###define variables

###main program

main()
