#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <regex>

using namespace std;

// Function to read a two-dimensional array from a file
vector<vector<int>> readTwoDArrayFromFile(const string& filename) {
    ifstream inputFile(filename);

    if (!inputFile.is_open()) {
        throw runtime_error("Failed to open the file.");
    }

    vector<vector<int>> twoDArray;
    string line;

    while (getline(inputFile, line)) {
        vector<int> row;
        smatch match;
        regex pattern("-?\\d+");

        // Find all integer numbers in the line
        while (regex_search(line, match, pattern)) {
            int number = stoi(match[0]);
            row.push_back(number);
            line = match.suffix();
        }

        twoDArray.push_back(row);
    }

    inputFile.close();
    return twoDArray;
}

int main() {
    try {
        vector<vector<int>> data = readTwoDArrayFromFile("./Field_Data/Field_Masons.txt");

        // Print the two-dimensional array
        cout << "[";
        for (size_t i = 0; i < data.size(); ++i) {
            cout << "[";
            for (size_t j = 0; j < data[i].size(); ++j) {
                cout << data[i][j];
                if (j < data[i].size() - 1) {
                    cout << ", ";
                }
            }
            cout << "]";
            if (i < data.size() - 1) {
                cout << ", ";
            }
        }
        cout << "]" << endl;
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}
