"""show use"""

import time
from collections import namedtuple
import pygame


pygame.init()
WIDTH, HEIGHT = 1000, 1000


Puzzle = namedtuple("Puzzle", ["shape", "RGB"])
PuzzleInfo = namedtuple(
    "PuzzleInfo",
    [
        "red",
        "greenyellow",
        "violet",
        "lime",
        "pink",
        "blue",
        "darkorange",
        "green",
        "yellow",
        "gold",
        "purple",
        "cyan",
        "deepskyblue",
    ],
)

color = [
    "red",
    "greenyellow",
    "violet",
    "lime",
    "pink",
    "blue",
    "darkorange",
    "green",
    "yellow",
    "gold",
    "purple",
    "cyan",
    "deepskyblue",
]

all_puzzle = PuzzleInfo(  # 很重要，其實裡面所有的puzzle的shape參數都是必須要是以上這樣，get_all_type的item是0
    Puzzle(
        (
            ("red", "empty", "red"),
            ("red", "red", "red"),
            ("red", "empty", "red"),
        ),
        (255, 0, 0),
    ),
    Puzzle(
        (
            ("greenyellow", "greenyellow"),
            ("greenyellow", "greenyellow"),
            ("greenyellow", "greenyellow"),
        ),
        (219, 255, 47),
    ),
    Puzzle(
        (
            ("empty", "empty", "violet"),
            ("violet", "violet", "violet"),
            ("empty", "violet", "empty"),
        ),
        (238, 130, 238),
    ),
    Puzzle(
        (
            ("empty", "empty", "lime", "empty"),
            ("lime", "lime", "lime", "lime"),
        ),
        (0, 255, 0),
    ),
    Puzzle(
        (
            ("empty", "empty", "pink"),
            ("empty", "empty", "pink"),
            ("pink", "pink", "pink"),
        ),
        (255, 192, 203),
    ),
    Puzzle(
        (
            ("blue", "blue"),
            ("blue", "empty"),
            ("blue", "blue"),
        ),
        (0, 0, 255),
    ),
    Puzzle(
        (
            ("darkorange", "darkorange", "darkorange", "empty"),
            ("empty", "empty", "darkorange", "darkorange"),
        ),
        (255, 140, 0),
    ),
    Puzzle(
        (
            ("empty", "empty", "empty", "green"),
            ("green", "green", "green", "green"),
        ),
        (0, 128, 0),
    ),
    Puzzle(
        (
            ("empty", "empty", "yellow"),
            ("yellow", "yellow", "yellow"),
            ("yellow", "empty", "empty"),
        ),
        (255, 255, 0),
    ),
    Puzzle((("gold", "gold"), ("gold", "gold")), (255, 215, 0)),
    Puzzle(
        (("empty", "purple"), ("purple", "purple"), ("empty", "purple")),
        ((128, 0, 128)),
    ),
    Puzzle(
        (("cyan", "cyan", "empty"), ("empty", "cyan", "cyan")),
        (0, 255, 255),
    ),
    Puzzle(
        (
            ("deepskyblue", "deepskyblue"),
            ("deepskyblue", "empty"),
            ("deepskyblue", "empty"),
        ),
        (0, 191, 255),
    ),
)


def get_one_of_pt(
    t: tuple[tuple[str, ...], ...], item: int
) -> tuple[tuple[str, ...], ...]:
    """原本的一種加旋轉七種，把重複的去掉，取出指定項數種"""
    width = len(t[0])
    heigth = len(t)
    ret = {t, t[::-1]}
    for _ in range(3):
        temp_t_t: tuple[tuple[str, ...], ...] = ()
        for x in range(width - 1, -1, -1):
            temp_t: tuple[str, ...] = ()
            for y in range(heigth):
                temp_t += (t[y][x],)
            temp_t_t += (temp_t,)
        t = temp_t_t
        ret.add(t)
        ret.add(t[::-1])
        width, heigth = heigth, width
    return tuple(sorted(tuple(ret)))[item]


def update_screen(board: list[list[str]]) -> None:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    for spacing in range(100, 901, 100):
        pygame.draw.line(screen, (0, 0, 0), (100, spacing), (900, spacing), 10)
    for spacing in range(100, 901, 100):
        pygame.draw.line(screen, (0, 0, 0), (spacing, 100), (spacing, 900), 10)
    for y_index, li in enumerate(board):
        for x_index, i in enumerate(li):
            if i != "empty":
                pygame.draw.rect(
                    screen,
                    eval(f"all_puzzle.{i}.RGB"),
                    (
                        100 * (x_index + 1) + 5,
                        100 * (7 - y_index + 1) + 5,
                        95,
                        95,
                    ),
                )
    pygame.display.flip()
    time.sleep(0.4)


def put_puzzle(
    board: list[list[str]], pt: tuple[tuple[str, ...], ...], x: int, y: int
) -> None:
    """放一個拼圖"""
    for y_item, t in enumerate(pt, y):
        for x_item, b in enumerate(t, x):
            if b == "empty":
                continue
            board[y_item][x_item] = b


def user_answer() -> tuple[int, int]:
    """詢問正解編號以及旋轉翻轉編號"""
    num = input("請問要幾號正解(1~69415):")
    while num not in set(map(str, set(range(1, 69416)))):
        num = input("請問要幾號正解(1~69415)只能輸入1~69415!!:")
    item = int(num)
    num = input("請問要1~8種的哪一種正解(旋轉翻轉會有8種):")
    while num not in set(map(str, set(range(1, 9)))):
        num = input("請問要1~8種的哪一種正解(旋轉翻轉會有8種)只能輸入1~8!!:")
    item_item = int(num)
    return item, item_item


def main() -> None:
    """主程式"""
    with open("solutions.txt") as file:
        file = file.read()
        str_solutions = file.split("\n\n")
        solutions = list(map(lambda x: x.split("\n"), str_solutions))
        solutions = list(map(lambda x: list(map(lambda x: tuple(map(int, x.split(" "))), x)), solutions))
    solution_num = user_answer()
    board = list(map(list, (("empty",) * 8,) * 8))
    solution = solutions[solution_num[0] - 1]
    for i, pt_info in enumerate(solution):
        put_puzzle(board, get_one_of_pt(all_puzzle[i].shape, pt_info[0]), pt_info[1], pt_info[2])
    board = get_one_of_pt(tuple(map(tuple, board)), solution_num[1] - 1)
    update_screen(board)
    for i in range(10):
        print(f"剩下{10 - i}秒!!")
        time.sleep(1)
    print("剩下0秒!!")
    print("觀賞結束")
    

main()
