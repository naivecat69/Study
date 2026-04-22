#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

using namespace std;

// compile: clang++ -O2 -std=c++17 parsing.cpp -o parsing (Mac air M4)

static constexpr int    MAX_ERR      = 3;
static constexpr size_t PATTERN_SIZE = 8;   // DEADBEEFDEADBEEF
static constexpr size_t LEN_OFFSET   = 10;  // 8바이트 패턴 + 2바이트 Sync 뒤
static constexpr size_t LEN_SIZE     = 2;
const uint8_t PATTERN[PATTERN_SIZE] {
    0xDE, 0xAD, 0xBE, 0xEF,
    0xDE, 0xAD, 0xBE, 0xEF
};

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "사용법: " << argv[0] << " <파일경로>\n";
        return 1;
    }

    ifstream f(argv[1], ios::binary | ios::ate);
    if (!f) { cerr << "input.bin 못 엶\n"; return 1; }
    streamsize size = f.tellg();
    f.seekg(0, ios::beg);
    vector<uint8_t> buf(size);
    f.read(reinterpret_cast<char*>(buf.data()), size);
    f.close();

    ofstream out("result.bin", ios::binary);
    if (!out) { cerr << "result.bin 못 엶\n"; return 1; }

    auto t0 = chrono::high_resolution_clock::now();

    size_t frame_count = 0;
    for (size_t i = 0; i + PATTERN_SIZE <= buf.size(); ++i) {
        int hamming = 0;
        for (size_t j = 0; j < PATTERN_SIZE; ++j)
            hamming += __builtin_popcount(PATTERN[j] ^ buf[i + j]);
        if (hamming > MAX_ERR) continue;

        if (i + LEN_OFFSET + LEN_SIZE > buf.size()) {
            cerr << "위치 " << i << ": length 필드 범위 초과, skip\n";
            continue;
        }

        uint16_t length = (uint16_t(buf[i + LEN_OFFSET])     << 8)
                        |  uint16_t(buf[i + LEN_OFFSET + 1]);

        if (i + length > buf.size()) {
            cerr << "위치 " << i << ": 길이 " << length
                 << "B 가 버퍼 초과, skip\n";
            continue;
        }

        out.write(reinterpret_cast<const char*>(buf.data() + i), length);
        cout << "프레임 " << frame_count++ << " @ " << i
             << ", 비트오류 " << hamming
             << ", 길이 " << length << "B\n";
    }

    auto t1 = chrono::high_resolution_clock::now();
    auto us = chrono::duration_cast<chrono::microseconds>(t1 - t0).count();
    cerr << "[C++] elapsed: " << us << " us (" << us/1000.0 << " ms)\n";
    cerr << "총 " << frame_count << " 프레임 result.bin 저장\n";
    return 0;
}
