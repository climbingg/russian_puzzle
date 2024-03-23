"""俄羅斯拼圖程式自動解"""

import time
import copy
from collections import namedtuple
import pygame


solutions = []

pygame.init()
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

Puzzle = namedtuple("Puzzle", ["shape", "is_used", "RGB"])
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

all_puzzle = PuzzleInfo(  # 很重要，其實裡面所有的puzzle的shape參數都是必須要是以上這樣，get_all_type的item是0
    Puzzle(
        (
            ("red", "empty", "red"),
            ("red", "red", "red"),
            ("red", "empty", "red"),
        ),
        [False],
        (255, 0, 0),
    ),
    Puzzle(
        (
            ("greenyellow", "greenyellow"),
            ("greenyellow", "greenyellow"),
            ("greenyellow", "greenyellow"),
        ),
        [False],
        (219, 255, 47),
    ),
    Puzzle(
        (
            ("empty", "empty", "violet"),
            ("violet", "violet", "violet"),
            ("empty", "violet", "empty"),
        ),
        [False],
        (238, 130, 238),
    ),
    Puzzle(
        (
            ("empty", "empty", "lime", "empty"),
            ("lime", "lime", "lime", "lime"),
        ),
        [False],
        (0, 255, 0),
    ),
    Puzzle(
        (
            ("empty", "empty", "pink"),
            ("empty", "empty", "pink"),
            ("pink", "pink", "pink"),
        ),
        [False],
        (255, 192, 203),
    ),
    Puzzle(
        (
            ("blue", "blue"),
            ("blue", "empty"),
            ("blue", "blue"),
        ),
        [False],
        (0, 0, 255),
    ),
    Puzzle(
        (
            ("darkorange", "darkorange", "darkorange", "empty"),
            ("empty", "empty", "darkorange", "darkorange"),
        ),
        [False],
        (255, 140, 0),
    ),
    Puzzle(
        (
            ("empty", "empty", "empty", "green"),
            ("green", "green", "green", "green"),
        ),
        [False],
        (0, 128, 0),
    ),
    Puzzle(
        (
            ("empty", "empty", "yellow"),
            ("yellow", "yellow", "yellow"),
            ("yellow", "empty", "empty"),
        ),
        [False],
        (255, 255, 0),
    ),
    Puzzle((("gold", "gold"), ("gold", "gold")), [False], (255, 215, 0)),
    Puzzle(
        (("empty", "purple"), ("purple", "purple"), ("empty", "purple")),
        [False],
        (128, 0, 128),
    ),
    Puzzle(
        (("cyan", "cyan", "empty"), ("empty", "cyan", "cyan")),
        [False],
        (0, 255, 255),
    ),
    Puzzle(
        (
            ("deepskyblue", "deepskyblue"),
            ("deepskyblue", "empty"),
            ("deepskyblue", "empty"),
        ),
        [False],
        (0, 191, 255),
    ),
)


def get_all_type(
    t: tuple[tuple[str, ...], ...],
) -> tuple[tuple[tuple[str, ...], ...], ...]:
    """原本的一種加旋轉七種，把重複的去掉"""
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
    return tuple(sorted(tuple(ret)))


def get_one_of_pt(
    t: tuple[tuple[str, ...], ...], item: int
) -> tuple[tuple[str, ...], ...]:
    return get_all_type(t)[item]


def update_screen(board: list[list[str]]) -> None:
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


def check_put_puzzle(
    board: list[list[str]], pt: tuple[tuple[str, ...], ...], x: int, y: int
) -> bool:
    """檢查是否放得進去"""
    width = len(pt[0])
    heigth = len(pt)
    # 取得高度寬度
    if heigth + y - 1 > 7:
        return False
    if width + x - 1 > 7:
        return False
    # 檢查是否超出邊界
    for y_item, t in enumerate(pt, y):
        for x_item, b in enumerate(t, x):
            if board[y_item][x_item] != "empty" and b != "empty":
                return False  # 重疊就return False
    return True


def put_puzzle(
    board: list[list[str]], pt: tuple[tuple[str, ...], ...], x: int, y: int
) -> None:
    """放一個拼圖"""
    for y_item, t in enumerate(pt, y):
        for x_item, b in enumerate(t, x):
            if b == "empty":
                continue
            board[y_item][x_item] = b


def add_score_board(
    score_board_info: list[list[None | list]],
    pt: tuple[tuple[str, ...], ...],
    index: int,
    x: int,
    y: int,
    pt_type_num: int,
    score_board: list[list[int | str]],
) -> None:
    """把score_board給+1 (如果有覆蓋到的話)"""
    for y_index in range(y + len(pt) - 1, y - 1, -1):
        for x_index, value in enumerate(pt[y_index - y], x):
            if value == "empty":
                continue
            # 確保該位置的元素為整數類型
            current_value = score_board[y_index][x_index]  # 為了過mypy
            if isinstance(current_value, int):
                score_board[y_index][x_index] = current_value + 1
            score_board_info[y_index][x_index].append((index, pt_type_num, x, y))


def dfs(
    board: list[list[str]],
    road: tuple[tuple[int, int, int], ...],
) -> None:
    """優先深度搜索，找出所有答案"""
    if len(road) == 13:
        solutions.append(tuple(map(lambda x: x[1:], sorted(road))))
        print("find one solution")
        return
    board_copy = copy.deepcopy(board)
    score_board_info = list(map(list, ((None,) * 8,) * 8))
    for y in range(8):
        for x in range(8):
            if board[y][x] == "empty":
                score_board_info[y][x] = []
    score_board: list[list[int]] = list(map(list, ((0,) * 8,) * 8))
    for row_item, row in enumerate(board):
        for value_item, value in enumerate(row):
            if value != "empty":
                score_board[row_item][value_item] = -1
    all_spellings: list[tuple[int, int, int, int]] = []
    for index in range(13):
        if all_puzzle[index].is_used[0]:
            continue
        if index == 2:
            pts = (get_one_of_pt(all_puzzle[2].shape, 0),)
        else:
            pts = get_all_type(all_puzzle[index].shape)
        for pt_type_num, pt in enumerate(pts):
            for y in range(8):
                for x in range(8):
                    if not check_put_puzzle(board, pt, x, y):
                        continue
                    add_score_board(
                        score_board_info,
                        pt,
                        index,
                        x,
                        y,
                        pt_type_num,
                        score_board,
                    )
    sorted_score: list[tuple[int, int, int]] = []
    for y, row in enumerate(score_board):
        for x, element in enumerate(row):
            if element != -1:
                sorted_score.append((element, x, y))
    if len(list(filter(lambda x: x[0] == 0, sorted_score))) > 0:
        return
    x, y = min(sorted_score, key=lambda x: x[0])[1:]
    for one_of_smally_x_y in score_board_info[y][x]:
        all_spellings.append(one_of_smally_x_y)
    jsq = 0
    for item, type_num, x, y in all_spellings:
        pt = get_one_of_pt(all_puzzle[item].shape, type_num)
        put_puzzle(board, pt, x, y)
        all_puzzle[item].is_used[0] = True
        update_screen(board)
        road += ((item, type_num, x, y),)
        dfs(board, road)
        road = road[:-1]
        all_puzzle[item].is_used[0] = False
        if len(road) in [0, 1]:
            print(len(road), f"{jsq + 1}/{len(all_spellings)}")
            jsq += 1
        for row_item, li in enumerate(board_copy):
            for column_item, val in enumerate(li):
                board[row_item][column_item] = val
        update_screen(board)


def main() -> None:
    """主程式"""
    board = list(map(list, (("empty",) * 8,) * 8))
    dfs(board, ())
    for solution_num, solution in enumerate(solutions, 1):
        print(f"第{solution_num}個解答是{solution}")


main()
