import math

import pygame
import random
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()


class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    # GREEN = 123, 104, 238
    # RED = 106, 90, 205
    COLOR_LIGHT_SEA_GREEN = 0, 169, 165
    COLOR_GUNMETAL = 9, 35, 39
    COLOR_LIGHT_SKY_BLUE = 144, 194, 231
    COLOR_RED_CRYSTALS = 239, 45, 86
    COLOR_DOGWOOD_ROSE = 220, 19, 108
    COLOR_AZURE = 49, 133, 252
    LIGHT_BLUE = 173, 216, 230
    CORNFLOWER_BLUE = 100, 149, 237
    MEDIUM_SLATE_BLUE = 123, 104, 238
    ROYAL_BLUE = 65, 105, 225
    BLUE_VIOLET = 138, 43, 226
    DARK_SLATE_BLUE = 72, 61, 139
    BACKGROUND_COLOR = 30, 30, 30
    SLATE_BLUE = 106, 90, 205
    MEDIUM_PURPLE = 147, 112, 219
    LAVENDER = 230, 230, 250
    GHOST_WHITE = 248, 248, 255
    MIDNIGHT_BLUE = 25, 25, 112
    DARK_BLUE = 0, 0, 139
    RED = "#DE541E"
    GREEN = '#16F4D0'
    # padding on left and right

    FONT = pygame.font.SysFont("comicsans", 20)
    LARGE_FONT = pygame.font.SysFont("comicsans", 30)
    GRADIENTS = [
        (65, 105, 225),
        (100, 149, 237),
        (135, 206, 250),
        # (176, 196, 222)
    ]
    TITLE_Y = 5
    CONTROLS1_Y = 65
    CONTROLS2_Y = 115
    N_SLIDER_Y = 155
    N_SLIDER_TEXT_Y = 180

    def __init__(self, width, height, lst):
        """
        :param lst: the list to be sorted
        """

        self.width = width
        self.height = height
        self.SIDE_PAD = self.width / 10
        self.TOP_PAD = 220
        # used by pygame to draw everything on
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.lst = []
        self.min_val = 0
        self.max_val = 0
        self.block_width = 0
        self.block_height = 0
        self.start_x = 0
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = self.block_width = (self.width - self.SIDE_PAD) / len(lst)
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    # fill the entire screen with the color
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'ASCENDING' if ascending else 'DESCENDING'}",
                                        1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, draw_info.TITLE_Y))

    controls1 = draw_info.FONT.render("R - RESET | SPACE - START SORTING | A - ASCENDING | D - DESCENDING",
                                      1, draw_info.WHITE)
    draw_info.window.blit(controls1, (draw_info.width / 2 - controls1.get_width() / 2, draw_info.CONTROLS1_Y))

    controls2 = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | H - Heap Sort | M - Merge Sort |"
                                      "Q - Quick Sort",
                                      1, draw_info.WHITE)
    draw_info.window.blit(controls2, (draw_info.width / 2 - controls2.get_width() / 2, draw_info.CONTROLS2_Y))
    draw_list(draw_info)


def draw_list(draw_info, color_positions=None, clear_bg=False):
    if color_positions is None:
        color_positions = {}
    lst = draw_info.lst

    # clear the portion of the screen where the list is being drawn
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, value in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (value - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIENTS[i % len(draw_info.GRADIENTS)]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        value = random.randint(min_val, max_val)
        lst.append(value)

    return lst


def set_sliders(draw_information):
    _N_TEXTBOX_WIDTH = 100
    _FPS_LABEL_WIDTH = 500
    _FPS_TEXTBOX_WIDTH = 200
    _N_TEXTBOX_HEIGHT = 40
    _N_SLIDER_INIT = 50
    _FPR_SLIDER_INIT = 60
    n_slider = Slider(draw_information.window, 10, draw_information.N_SLIDER_Y, 500, 20, min=10, max=1000, step=50,
                      curved=False, colour=draw_information.COLOR_LIGHT_SEA_GREEN,
                      handleColour=draw_information.COLOR_GUNMETAL, handleRadius=14, )
    n_slider.setValue(_N_SLIDER_INIT)
    n_output = TextBox(draw_information.window, 10, draw_information.N_SLIDER_TEXT_Y, _N_TEXTBOX_WIDTH,
                       _N_TEXTBOX_HEIGHT,
                       fontSize=20, font=draw_information.FONT, colour=draw_information.COLOR_AZURE,
                       borderColour=draw_information.MIDNIGHT_BLUE,
                       textColour=draw_information.BLACK,
                       borderThickness=1)
    n_output.disable()  # act as label instead o textbox

    fps_start_x = draw_information.window.get_width() - _FPS_LABEL_WIDTH - 10

    fps_slider = Slider(draw_information.window, fps_start_x,
                        draw_information.N_SLIDER_Y, 500, 20, min=10, max=360, step=5,
                        curved=False, colour=draw_information.COLOR_LIGHT_SEA_GREEN,
                        handleColour=draw_information.COLOR_GUNMETAL, handleRadius=14, )
    fps_output = TextBox(draw_information.window, fps_start_x,
                         draw_information.N_SLIDER_TEXT_Y, _N_TEXTBOX_WIDTH + 10,
                         _N_TEXTBOX_HEIGHT,
                         fontSize=20, font=draw_information.FONT, colour=draw_information.COLOR_AZURE,
                         borderColour=draw_information.MIDNIGHT_BLUE,
                         textColour=draw_information.BLACK,
                         borderThickness=1)
    fps_slider.setValue(_FPR_SLIDER_INIT)
    n_output.disable()  # act as label instead o textbox

    return [n_slider, n_output, fps_slider, fps_output]


def main_sort():
    n = 50
    min_val = 10
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_information = DrawInformation(1300, 800, lst)
    sorting = False
    ascending = True
    _FPS = 30
    # determines how quickly the loop can run
    clock = pygame.time.Clock()
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "BUBBLE SORT"
    sorting_algorithm_generator = None
    # pygame event loop - need a loop constantly running in the background whenever using pygame
    n_slider, n_output, fps_slider, fps_output = set_sliders(draw_information)

    run = True
    while run:
        # FPS = 60, max # of times the loop can run per second
        clock.tick(_FPS)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            # draw the window
            draw(draw_information, sorting_algorithm_name, ascending)

        events = pygame.event.get()
        # will return list of all events that have occurred since the last loop
        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_information.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting is False:
                sorting = True
                # calling generator function first returns a generator object
                sorting_algorithm_generator = sorting_algorithm(draw_information, ascending)
                lst = generate_starting_list(n, min_val, max_val)
                draw_information.set_list(lst)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algorithm_name = "Heap Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm = merge_sort
                sorting_algorithm_name = "Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algorithm_name = "Quick Sort"

        n_output.setText(f'N = {n_slider.getValue()}')
        fps_output.setText(f'FPS = {fps_slider.getValue()}')
        n = n_slider.getValue()
        _FPS = fps_slider.getValue()
        pygame_widgets.update(events)
        pygame.display.update()
    pygame.quit()


def quick_sort(draw_info, ascending=True):
    def quick_sort_helper(lst, low, high):
        if low >= high:
            return
        hoare_partition_generator = hoare_partition(lst, low, high)
        while True:
            try:
                next(hoare_partition_generator)
                yield True
            except StopIteration as e:
                hoare_partition_index = e.value
                break

        gen1 = quick_sort_helper(lst, low, hoare_partition_index - 1)
        while True:
            try:
                next(gen1)
                yield True
            except StopIteration:
                break
        gen2 = quick_sort_helper(lst, hoare_partition_index + 1, high)
        while True:
            try:
                next(gen2)
                yield True
            except StopIteration:
                break

    def hoare_partition(lst, start, end):
        partition_index = start
        low = start + 1
        high = end
        while True:
            if ascending:
                while low <= high and lst[low] <= lst[partition_index]:
                    low += 1
                while low <= high and lst[high] >= lst[partition_index]:
                    high -= 1
            else:
                while low <= high and lst[low] >= lst[partition_index]:
                    low += 1
                while low <= high and lst[high] <= lst[partition_index]:
                    high -= 1

            if low <= high:
                lst[low], lst[high] = lst[high], lst[low]
                draw_list(draw_info, {low: draw_info.GREEN, high: draw_info.RED}, clear_bg=True)
                yield True
            else:
                break

        lst[partition_index], lst[high] = lst[high], lst[partition_index]
        draw_list(draw_info, {start: draw_info.GREEN, high: draw_info.RED}, clear_bg=True)
        yield True
        return high

    gen = quick_sort_helper(draw_info.lst, 0, len(draw_info.lst) - 1)
    while True:
        try:
            next(gen)
            yield True
        except StopIteration:
            break


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - i - 1):
            n1 = lst[j]
            n2 = lst[j + 1]
            if (n1 > n2 and ascending) or (n1 < n2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, clear_bg=True)
                yield True
    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = ascending and i > 0 and lst[i - 1] > current
            descending_sort = not ascending and i > 0 and lst[i - 1] < current
            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.GREEN, i + 1: draw_info.RED}, clear_bg=True)
            yield True

    return lst


def heap_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def left_child(i):
        return 2 * i + 1

    def right_child(i):
        return 2 * i + 2

    # sink down to rightful place
    def max_heapify(elements, size, index):
        while True:
            left = left_child(index)
            right = right_child(index)
            largest = index
            if left < size and ((ascending and elements[left] > elements[index]) or (
                    not ascending and elements[left] < elements[index])):
                largest = left

            if right < size and ((ascending and elements[right] > elements[largest]) or (
                    not ascending and elements[right] < elements[largest])):
                largest = right

            if largest != index:
                elements[largest], elements[index] = elements[index], elements[largest]
                draw_list(draw_info, {largest: draw_info.GREEN, index: draw_info.RED}, clear_bg=True)
                yield True
                index = largest
            else:
                break

    def build_max_heap(elements):
        size = len(elements)
        for j in range(size // 2 - 1, -1, -1):
            max_heapify_generator_inner = max_heapify(elements, size, j)
            while True:
                try:
                    next(max_heapify_generator_inner)
                    yield True
                except StopIteration:
                    break
            yield True

    build_max_heap_generator = build_max_heap(lst)
    while True:
        try:
            next(build_max_heap_generator)
            yield True
        except StopIteration:
            break

    for i in range(len(lst) - 1, -1, -1):
        lst[0], lst[i] = lst[i], lst[0]
        draw_list(draw_info, {0: draw_info.GREEN, i: draw_info.RED}, clear_bg=True)
        max_heapify_generator = max_heapify(lst, i, 0)
        while True:
            try:
                next(max_heapify_generator)
                yield True
            except StopIteration:
                break

    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_helper(x, start, end):
        if len(x) < 2:
            return x
        result = []
        mid = int(len(x) / 2)
        left_gen = merge_sort_helper(x[:mid], start, start + mid)

        while True:
            try:
                next(left_gen)
                yield True
            except StopIteration as e:
                y = e.value
                break

        right_gen = merge_sort_helper(x[mid:], start + mid, end)

        while True:
            try:
                next(right_gen)
                yield True
            except StopIteration as e:
                z = e.value
                break

        i = 0
        j = 0
        while i < len(y) and j < len(z):
            if ascending:
                if y[i] > z[j]:
                    result.append(z[j])
                    j += 1
                else:
                    result.append(y[i])
                    i += 1
            else:
                if y[i] < z[j]:
                    result.append(z[j])
                    j += 1
                else:
                    result.append(y[i])
                    i += 1

            draw_info.lst[start: end] = result + y[i:] + z[j:]
            draw_list(draw_info, {start + j: draw_info.GREEN, start + i: draw_info.RED}, clear_bg=True)
            yield True
        result += y[i:]
        result += z[j:]
        return result

    merge_sort_helper_generator = merge_sort_helper(lst, 0, len(lst))
    while True:
        try:
            next(merge_sort_helper_generator)
            yield True
        except StopIteration:
            break


if __name__ == "__main__":
    main_sort()
