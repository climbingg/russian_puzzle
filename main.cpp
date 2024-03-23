#include <iostream>
#include <vector>
#include <array>
#include <unordered_set>
#include <fstream>
#include <unordered_map>
#include <algorithm>

std::vector<std::array<std::array<int, 3>, 13>> solutions;

std::unordered_map<std::string, int> pt_str_to_int {
    {"red", 0},
    {"greenyellow", 1},
    {"violet", 2},
    {"lime", 3},
    {"pink", 4},
    {"blue", 5},
    {"darkorange", 6},
    {"green", 7},
    {"yellow", 8},
    {"gold", 9},
    {"purple", 10},
    {"cyan", 11},
    {"deepskyblue", 12},
};

struct Puzzle {
    std::vector<std::vector<std::string>> shape;
    bool is_used;
    Puzzle(const std::vector<std::vector<std::string>>& shape, const bool& is_used) : shape(shape), is_used(is_used) {}
};

struct PuzzleInfo {
    const Puzzle red{
        {
            {"red", "empty", "red"},
            {"red", "red", "red"},
            {"red", "empty", "red"},
        },
        false,
    };
    const Puzzle greenyellow{
        {
            {"greenyellow", "greenyellow", "greenyellow"},
            {"greenyellow", "greenyellow", "greenyellow"},
        },
        false,
    };
    const Puzzle violet{
        {
            {"empty", "empty", "violet"},
            {"violet", "violet", "violet"},
            {"empty", "violet", "empty"},
        },
        false,
    };
    const Puzzle lime{
        {
            {"empty", "empty", "lime", "empty"},
            {"lime", "lime", "lime", "lime"},
        },
        false,
    };
    const Puzzle pink{
        {
            {"empty", "empty", "pink"},
            {"empty", "empty", "pink"},
            {"pink", "pink", "pink"},
        },
        false,
    };
    const Puzzle blue{
        {
            {"blue", "blue"},
            {"blue", "empty"},
            {"blue", "blue"},
        },
        false,
    };
    const Puzzle darkorange{
        {
            {"darkorange", "darkorange", "darkorange", "empty"},
            {"empty", "empty", "darkorange", "darkorange"},
        },
        false,
    };
    const Puzzle green{
        {
            {"empty", "empty", "empty", "green"},
            {"green", "green", "green", "green"},
        },
        false,
    };
    const Puzzle yellow{
        {
            {"empty", "empty", "yellow"},
            {"yellow", "yellow", "yellow"},
            {"yellow", "empty", "empty"},
        },
        false,
    };
    const Puzzle gold{{{"gold", "gold"}, {"gold", "gold"}}, false};
    const Puzzle purple{
        {{"empty", "purple"}, {"purple", "purple"}, {"empty", "purple"}},
        false,
    };
    const Puzzle cyan{
        {{"cyan", "cyan", "empty"}, {"empty", "cyan", "cyan"}},
        false,
    };
    const Puzzle deepskyblue{
        {
            {"deepskyblue", "deepskyblue"},
            {"deepskyblue", "empty"},
            {"deepskyblue", "empty"},
        },
        false,
    };
};

PuzzleInfo all_puzzle;
std::vector<Puzzle> all_puzzle_num = {
    all_puzzle.red,
    all_puzzle.greenyellow,
    all_puzzle.violet,
    all_puzzle.lime,
    all_puzzle.pink,
    all_puzzle.blue,
    all_puzzle.darkorange,
    all_puzzle.green,
    all_puzzle.yellow,
    all_puzzle.gold,
    all_puzzle.purple,
    all_puzzle.cyan,
    all_puzzle.deepskyblue,
};

std::vector<std::vector<std::vector<std::string>>> get_all_type(std::vector<std::vector<std::string>> t) {
    int width = t[0].size();
    int heigth = t.size();
    std::vector<std::vector<std::string>> reverse_t = t;
    std::vector<std::vector<std::vector<std::string>>> res = {t};
    std::reverse(reverse_t.begin(), reverse_t.end());
    std::vector<std::string> temp_t;
    std::vector<std::vector<std::string>> temp_t_t;
    res.push_back(reverse_t);
    for (int _ = 0;_ < 3;_++) {
        temp_t_t = {};
        for (int x = width - 1;x >= 0;x--) {
            temp_t = {};
            for (int y = 0;y < heigth;y++) {
                temp_t.push_back(t[y][x]);
            }
            temp_t_t.push_back(temp_t);
        }
        t = temp_t_t;
        res.push_back(t);
        reverse_t = t;
        std::reverse(reverse_t.begin(), reverse_t.end());
        res.push_back(reverse_t);
        std::swap(width, heigth);
    }
    std::sort(res.begin(), res.end());
    std::vector<std::vector<std::vector<std::string>>> ret = {res[0]};
    for (int type_num_ptr = 1;type_num_ptr < res.size();type_num_ptr++) {
        if (res[type_num_ptr] != res[type_num_ptr - 1]) {
            ret.push_back(res[type_num_ptr]);
        }
    }
    return ret;
}

std::vector<std::vector<std::string>> get_one_of_pt(std::vector<std::vector<std::string>> t, int item) {
    return get_all_type(t)[item];
}

bool check_put_puzzle(std::array<std::array<int, 8>, 8>& board, std::vector<std::vector<std::string>> pt, int x, int y) {
    int width = pt[0].size();
    int heigth = pt.size();
    if (heigth + y - 1 > 7) {
        return false;
    }
    if (width + x - 1 > 7) {
        return false;
    }
    std::vector<std::string> t;
    std::string b;
    for (int y_index = y;y_index < heigth + y;y_index++) {
        t = pt[y_index - y];
        for (int x_index = x;x_index < width + x;x_index++) {
            b = t[x_index - x];
            if (b == "empty") {
                continue;
            }
            if (board[y_index][x_index] == 13) {
                continue;
            }
            return false;
        }
    }
    return true;
}

void put_puzzle(std::array<std::array<int, 8>, 8>& board, std::vector<std::vector<std::string>> pt, int x, int y) {
    std::vector<std::string> t;
    std::string b;
    for (int y_index = y;y_index < pt.size() + y;y_index++) {
        t = pt[y_index - y];
        for (int x_index = x;x_index < pt[0].size() + x;x_index++) {
            b = t[x_index - x];
            if (b == "empty") {
                continue;
            }
            board[y_index][x_index] = pt_str_to_int[b];
        }
    }
}

void add_score_board(
    std::array<std::array<std::vector<std::array<int, 4>>, 8>, 8>& score_board_info,
    std::vector<std::vector<std::string>> pt,
    int index,
    int x,
    int y,
    int pt_type_num,
    std::array<std::array<int, 8>, 8>& score_board
) {
    std::string value;
    for (int y_index = y + pt.size() - 1;y_index >= y;y_index--) {
        for (int x_index = x;x_index < x + pt[0].size();x_index++) {
            value = pt[y_index - y][x_index - x];
            if (value == "empty") {
                continue;
            }
            if (score_board[y_index][x_index] == -1) {
                continue;
            }
            score_board[y_index][x_index]++;
            score_board_info[y_index][x_index].push_back({index, pt_type_num, x, y});
        }
    }
}

bool check_zero_item(std::array<int, 3> arr) {
    return arr[0] == 0;
}

void dfs(std::array<std::array<int, 8>, 8>& board, std::vector<std::array<int, 4>> road) {
    if (road.size() == 13) {
        std::sort(road.begin(), road.end());
        std::array<std::array<int, 3>, 13> solution;
        for (int i = 0;i < 13;i++) {
            solution[i] = {road[i][1], road[i][2], road[i][3]};
        }
        solutions.push_back(solution);
        std::cout << "find one solution" << std::endl;
        return;
    }
    std::array<std::array<int, 8>, 8> board_copy = board;
    std::array<std::array<std::vector<std::array<int, 4>>, 8>, 8> score_board_info;
    std::array<std::array<int, 8>, 8> score_board;
    for (int y = 0;y < 8;y++) {
        for (int x = 0;x < 8;x++) {
            if (board[y][x] == 13) {
                score_board[y][x] = 0;
            }
            else {
                score_board[y][x] = -1;
            }
        }
    }
    std::vector<std::vector<std::vector<std::string>>> pts;
    std::vector<std::vector<std::string>> pt;
    for (int index = 0;index < 13;index++) {
        if (all_puzzle_num[index].is_used) {
            continue;
        }
        if (index == 2) {
            pts = {get_one_of_pt(all_puzzle.violet.shape, 0)};
        }
        else {
            pts = get_all_type(all_puzzle_num[index].shape);
        }
        for (int pt_type_num = 0;pt_type_num < pts.size();pt_type_num++) {
            pt = pts[pt_type_num];
            for (int y = 0;y < 8;y++) {
                for (int x = 0;x < 8;x++) {
                    if (!(check_put_puzzle(board, pt, x, y))) {
                        continue;
                    }
                    add_score_board(score_board_info, pt, index, x, y, pt_type_num, score_board);
                }
            }
        }
    }
    std::vector<std::array<int, 3>> sorted_score;
    for (int y = 0;y < 8;y++) {
        for (int x = 0;x < 8;x++) {
            if (score_board[y][x] == -1) {
                continue;
            }
            sorted_score.push_back({score_board[y][x], x, y});
        }
    }
    std::vector<std::array<int, 3>> check_vec;
    std::copy_if(sorted_score.begin(), sorted_score.end(), std::back_inserter(check_vec), check_zero_item);
    if (check_vec.size() > 0) {
        return;
    }
    std::array<int, 3> smally_x_y = *std::min_element(sorted_score.begin(), sorted_score.end());
    int smally_x = smally_x_y[1];
    int smally_y = smally_x_y[2];
    std::vector<std::array<int, 4>> all_spellings = score_board_info[smally_y][smally_x];
    int type_num;
    int x;
    int y;
    int index;
    int jsq = 0;
    for (int i = 0;i < all_spellings.size();i++) {
        index = all_spellings[i][0];
        type_num = all_spellings[i][1];
        x = all_spellings[i][2];
        y = all_spellings[i][3];
        pt = get_one_of_pt(all_puzzle_num[index].shape, type_num);
        put_puzzle(board, pt, x, y);
        road.push_back({index, type_num, x, y});
        all_puzzle_num[index].is_used = true;
        dfs(board, road);
        road.pop_back();
        all_puzzle_num[index].is_used = false;
        if (road.size() == 0 || road.size() == 1) {
            std::cout << road.size() << " " << jsq + 1 << "/" << all_spellings.size() << std::endl;
            jsq++;
        }
        board = board_copy;
    }
}

int main() {
    std::array<std::array<int, 8>, 8> board;
    for (int y = 0;y < 8;y++) {
        for (int x = 0;x < 8;x++) {
            board[y][x] = 13;
        }
    }
    dfs(board, {});
    std::ofstream outfile("solutions.txt");
    std::cout << "solutions.size(): " << solutions.size() << std::endl;
    std::array<std::array<int, 3>, 13> solution;
    for (int i = 0;i < solutions.size();i++) {
        solution = solutions[i];
        for (int j = 0;j < 13;j++) {
            if (i < solutions.size() - 1 || j < 12) {
                outfile << solution[j][0] << " " << solution[j][1] << " " << solution[j][2] << std::endl;
            }
            else {
                outfile << solution[j][0] << " " << solution[j][1] << " " << solution[j][2];
            }
        }
        if (i < solutions.size() - 1) {
            outfile << std::endl;
        }
    }
    outfile.close();
    return 0;
}
