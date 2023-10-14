#include <iostream>
#include <vector>
#include <set>
#include <ctime>
#include <cstdlib>
#include <map>
#include <fstream>
#include <string>
#include <sstream>


std::vector<std::vector<int>> read_field(std::string path){
    std::string str;
    std::ifstream file(path);
    if (file.fail())
        return {};
    getline(file,str);
    std::vector<std::vector<int>> result;
    int i,j;
    int first = 2;
    while (first<str.size()){
        std::vector<int> vec;
        std::string tmp;
        for (i=0;str[i+first]!=']';i++){
            tmp += str[i+first];
        }
        first += i+4;
    
        int first2 = 0;
        while (first2<tmp.size()){
            std::string tmp2="";
            for (j=0;tmp[j+first2]!=',';j++){
                if (j>tmp.size())break;
                tmp2 += tmp[j+first2];
            }
            first2 += j+1;
            vec.push_back(stoi(tmp2));
        }
        result.push_back(vec);
    }
    file.close();
    return result;
}

std::vector<std::vector<int>> field_masons = read_field("./Field_Data/Field_Masons.txt"),
                              field_walls = read_field("./Field_Data/Field_Walls.txt"),
                              field_structures = read_field("./Field_Data/Field_Masons.txt"),
                              build_vec = read_field("./Plan/Build.txt"),
                              move_vec = read_field("./Plan/Move.txt"),
                              break_vec = read_field("./Plan/Break.txt");

/*
std::vector<std::vector<int>> field_masons = {
    {0, 0, 0, 0, 0, 1, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 2, 0, 0, 0},
    {0, 0, 0, 0,-1,-2, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 3, 0, 0, 0, 0, 0, 4}
};

std::vector<std::vector<int>> field_walls = {
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0},
    {0, 0, 0, 2, 0, 0, 0, 0}
};

std::vector<std::vector<int>> field_structures = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0},
    {0, 0, 1, 0, 0, 0, 0, 0}
};
std::vector<std::vector<int>> move_vec = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
};
std::vector<std::vector<int>> build_vec = {
    {0, 0, 0, 0, 1, 0, 1, 0},
    {0, 0, 0, 0, 0, 1, 0, 0},
    {0, 0, 0, 0, 1, 0, 0, 0},
    {0, 0, 0, 1, 0, 1, 0, 0},
    {0, 1, 0, 0, 0, 0, 0, 0},
    {1, 0, 0, 0, 0, 0, 1, 0},
    {0, 1, 0, 0, 0, 0, 0, 1},
    {0, 0, 0, 0, 0, 0, 1, 0}
};
std::vector<std::vector<int>> break_vec = {
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0},
    {0, 0, 0, 0, 0, 0, 0, 0}
};
*/

const int h = field_masons.size();
const int w = field_masons[0].size();
int n = 0;
int min_turn = 100;
int min_turn_sum = 600;

int t = 0;
int t_sum = 0;
int cnt = 0;
std::set<std::pair<int, int>> masons_point_before;

std::vector<std::pair<int, int>> direction_dict = {
    {-1, -1}, {-1, 0}, {-1, 1}, {0, 1},
    {1, 1}, {1, 0}, {1, -1}, {0, -1},
    {-1, 0}, {0, 1}, {1, 0}, {0, -1},
};

std::map<int, int> move_break_dict = {{1, 12}, {3, 13}, {5, 14}, {7, 15}};
std::map<int, int> build_break_dict = {{8, 12}, {9, 13}, {10, 14}, {11, 15}};

std::vector<std::vector<int>> log_li(n, std::vector<int>());
std::vector<std::vector<int>> min_log_li;

bool move_able(std::pair<int, int> point, int d) {
    int i = point.first + direction_dict[d].first;
    int j = point.second + direction_dict[d].second;
    if (!(0 <= i && i < h)) {
        return false;
    }
    if (!(0 <= j && j < w)) {
        return false;
    }
    if (field_masons[i][j] < 0) {
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

int move_able_random(std::pair<int, int> point) {
    std::vector<int> move_able_li;
    for (int d = 0; d < 8; ++d) {
        if (move_able(point, d)) {
            move_able_li.push_back(d);
        }
    }
    move_able_li.push_back(16);
    int random_index = rand() % move_able_li.size();
    return move_able_li[random_index];
}
int main() {
    srand(time(0));

    std::vector<std::pair<int, int>> masons_point_A(6);
    std::set<std::pair<int, int>> move_set_A,build_set_A,break_set_A;

    for (int i=0;i<h;i++){
        for (int j=0;j<w;j++){
            if (field_masons[i][j]>0){
                n++;
                masons_point_A[field_masons[i][j]-1] = {i,j};
            }
            if (move_vec[i][j] == 1){
                move_set_A.insert({i,j});
            }
            if (build_vec[i][j] == 1){
                build_set_A.insert({i,j});
            }
            if (build_vec[i][j] == 1){
                build_set_A.insert({i,j});
            }
        }
    }
    masons_point_before = {masons_point_A.begin(), masons_point_A.end()};

    while (cnt < 30000) {
        cnt++;
        std::vector<std::pair<int, int>> masons_point= masons_point_A;
        masons_point_before = std::set<std::pair<int, int>>(masons_point.begin(), masons_point.end());
        std::set<std::pair<int, int>> move_set = move_set_A;
        std::set<std::pair<int, int>> build_set = build_set_A;
        std::set<std::pair<int, int>> break_set =break_set_A;
        t = 0;
        t_sum = 0;
        log_li = std::vector<std::vector<int>>(n, std::vector<int>());
        std::vector<int> masons_que(6, 0);
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
                int i,j;
                if (move_d != 16){
                    i = masons_point[mason].first + direction_dict[move_d].first;
                    j = masons_point[mason].second + direction_dict[move_d].second;
                    masons_point_before.erase({masons_point[mason].first, masons_point[mason].second});
                    masons_point[mason] = {i, j};
                    masons_point_before.insert({i, j});

                    if (field_walls[i][j] == 2) {
                        masons_que[mason]++;
                        log_li[mason].push_back(move_break_dict[move_d]);
                        if (build_set.find({i, j}) != build_set.end()) {
                            build_set.erase({i, j});
                        }
                    }
                    log_li[mason].push_back(move_d);
                }
                if (move_set.count(masons_point[mason])) {
                    move_set.erase(masons_point[mason]);
                }

                for (int wall_d = 8; wall_d < 12; ++wall_d) {
                    i = masons_point[mason].first + direction_dict[wall_d].first;
                    j = masons_point[mason].second + direction_dict[wall_d].second;

                    if (build_set.find({i, j}) != build_set.end()
                        && field_structures[i][j] != 2
                        && field_masons[i][j] >= 0) {
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
            //t++;
            for (auto li:log_li){
                if (t<li.size()){
                    t = li.size();
                    t_sum += li.size();
                }
            }
        }
        if (t < min_turn && t_sum < min_turn_sum) {
            min_turn = t;
            min_turn_sum = t_sum;
            min_log_li = log_li;
            /* std::cout << min_turn << ' ' << min_turn_sum << std::endl; */
        }
    }

    /* std::cout << "min_turn : " << min_turn << std::endl; */

	std::cout << "["; 
    for (int mason = 0; mason < n; ++mason){
		std::cout << "["; 
        for (int i = 0; i < min_log_li[mason].size(); ++i) {
			if (i == min_log_li[mason].size() - 1){
				std::cout << min_log_li[mason][i] << "";
			}else{
				std::cout << min_log_li[mason][i] << ", ";
			}
        }
		if (mason == n - 1){
			std::cout << "]"; 
		}else{
			std::cout << "],"; 
		}
	}
	std::cout << "]";

    /* time_t end = time(0); */
    // std::cout << "took: " << end - start << " seconds" << std::endl;

    return 0;
}
