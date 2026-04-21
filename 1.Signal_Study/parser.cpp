#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

static constexpr int MAX_ERR = 1;
const uint8_t PATTERN[] {0xDE,0xAD,0xBE,0xEF};

int main() {

    ifstream f("input.bin", ios::binary | ios::ate);  // ate: 끝에서 시작
    if (!f) { cerr << "파일 못 엶\n"; return 1; }

    streamsize size = f.tellg();
    f.seekg(0, ios::beg);

    vector<uint8_t> buf(size);
    f.read(reinterpret_cast<char*>(buf.data()), size);

    for (size_t i = 0; i + 4 <= buf.size(); ++i) {
        int hamming = 0;
        for (size_t j = 0; j < 4; ++j)
            hamming += __builtin_popcount(PATTERN[j] ^ buf[i + j]);
        if (hamming <= MAX_ERR)
            std::cout << "위치 " << i << ", 비트오류 " << hamming << '\n';
    }


    return 0;
}
