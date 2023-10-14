#include <iostream>
#include <vector>
#include <set>
/* #include <ctime> */
#include <cstdlib>
#include <map>
#include <random>

using namespace std; 

const int h = 8;
const int w = 8;
const int n = 2;
int min_turn = 50;

int t = 0;
int cnt = 0;

vector<pair<int, int>> masons_point = {{0, 5}, {3, 4}};
set<pair<int, int>> masons_point_before(masons_point.begin(), masons_point.end());
vector<int> masons_que(n, 0);

vector<pair<int, int>> direction_dict = {
    {-1, -1}, {-1, 0}, {-1, 1}, {0, 1},
    {1, 1}, {1, 0}, {1, -1}, {0, -1},
};

map<int, int> move_break_dict = {{1, 12}, {3, 13}, {5, 14}, {7, 15}};
map<int, int> build_break_dict = {{8, 12}, {9, 13}, {10, 14}, {11, 15}};

vector<vector<int>> log_li(n, vector<int>());
vector<vector<int>> min_log_li;

vector<vector<int>> field_masons = {
    {0, 0, 0, 0, 0, 1, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 2, 0, 0, 0},
    {0, 0, 0, 0, -1, -2, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
};

vector<vector<int>> field_walls = {
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0}
};

vector<vector<int>> field_structures = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0}
};

bool move_able(pair<int, int> point, int d) {
    int i = point.first + direction_dict[d].first;
    int j = point.second + direction_dict[d].second;
    if (!(0 <= i && i < h)) {
        return false;
    }
    if (!(0 <= j && j < w)) {
        return false;
    }
    if (field_masons[i][j] != 0) {
        return false;
    }
    if (field_walls[i][j] == 2 && d % 2 == 0) {
        return false;
    }
    if (field_structures[i][j] == 1) {
        return false;
    }
    if (masons_point_before.find({i, j}) != masons_point_before.end()) {
        return false;
    }
    return true;
}

int move_able_random(pair<int, int> point) {
    vector<int> move_able_li;
    for (int d = 0; d < 8; ++d) {
        if (move_able(point, d)) {
            move_able_li.push_back(d);
        }
    }
    int random_index = rand() % move_able_li.size();
    return move_able_li[random_index];
}

int main() {
    random_device rd;
    mt19937 generator(rd());
    uniform_int_distribution<int> distribution(1, 100);
    double randomReal = distribution(generator);
    srand((int)randomReal);
    /* time_t start = time(0); */

    while (cnt < 10000) {
        cnt++;
        masons_point = {{0, 5}, {3, 4}};
        masons_point_before = set<pair<int, int>>(masons_point.begin(), masons_point.end());
        set<pair<int, int>> move_set = {{5, 5}, {3, 7}, {6, 1}};
        set<pair<int, int>> build_set = {{1, 3}};
        set<pair<int, int>> break_set = {{7, 3}};
        t = 0;
        log_li = vector<vector<int>>(n, vector<int>());

        while (!move_set.empty() || !build_set.empty() || !break_set.empty()) {
            if (t > min_turn) {
                break;
            }
            for (int mason = 0; mason < n; ++mason) {
                if (masons_que[mason] > 0) {
                    masons_que[mason]--;
                    continue;
                }

                int move_d = move_able_random(masons_point[mason]);
                int i = masons_point[mason].first + direction_dict[move_d].first;
                int j = masons_point[mason].second + direction_dict[move_d].second;
                masons_point_before.erase({masons_point[mason].first, masons_point[mason].second});
                masons_point[mason] = {i, j};
                masons_point_before.insert({i, j});

                if (field_walls[i][j] == 2) {
                    masons_que[mason]++;
                    log_li[mason].push_back(move_break_dict[move_d]);
                    if (break_set.find({i, j}) != build_set.end()) {
                        break_set.erase({i, j});
                    }
                }
                log_li[mason].push_back(move_d);

                if (move_set.count(masons_point[mason])) {
                    move_set.erase(masons_point[mason]);
                }

                for (int wall_d = 8; wall_d < 12; ++wall_d) {
                    i = masons_point[mason].first + direction_dict[wall_d].first;
                    j = masons_point[mason].second + direction_dict[wall_d].second;

                    if (build_set.find({i, j}) != build_set.end()) {
                        masons_que[mason]++;
                        if (field_walls[i][j] == 2) {
                            masons_que[mason]++;
                            log_li[mason].push_back(build_break_dict[wall_d]);
                            if (break_set.find({i, j}) != break_set.end()) {
                                break_set.erase({i, j});
                            }
                        }
                        log_li[mason].push_back(wall_d);
                        build_set.erase({i, j});
                    }

                    if (break_set.find({i, j}) != break_set.end()) {
                        if (field_walls[i][j] == 2) {
                            masons_que[mason]++;
                            log_li[mason].push_back(build_break_dict[wall_d]);
                            break_set.erase({i, j});
                        }
                    }
                }
            }
            t++;
        }
        if (t < min_turn) {
            min_turn = t;
            min_log_li = log_li;
            // cout << min_turn << endl;
        }
    }
    cout << "min_turn : " << min_turn << endl;

    // for (int mason = 0; mason < n; ++mason){
    //     for (int i = 0; i < min_log_li[mason].size(); ++i) {
    //         cout << min_log_li[mason][i] << " ";
    //     }
    // }
    // cout << endl;

    /* time_t end = time(0); */
    // cout << "took: " << end - start << " seconds" << endl;

    return 0;
}
