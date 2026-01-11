class DocumentSpecificScrambler:
    def __init__(self, start_seed=1):
        """
        문서에 'initialized to 1'이라고 되어 있으므로 초기값 1 설정
        """
        # 다항식이 x^5 + x^2 + 1 이므로 최소 5비트 이상 필요.
        # 그림에는 x^9까지 있지만, 핵심 동작은 5차 다항식 피드백임.
        self.state = start_seed

    def next_scramble_symbol(self):
        # 1. 문서에 나온 대로 하위 3비트(x^2, x^1, x^0)를 추출해서 N을 만듦
        #    N = 4*x2 + 2*x1 + 1*x0
        #    이것은 state의 하위 3비트를 그냥 읽으면 됨 (Mask 0b111 = 7)
        N = self.state & 0b111  # (0 ~ 7 사이의 값)

        # 2. 다항식 x^5 + x^2 + 1 에 따른 피드백 계산 (Fibonacci LFSR 기준)
        #    x^5 (5번째 전) 와 x^2 (2번째 전)를 XOR
        #    비트 인덱스로 치면: (state >> 4) 와 (state >> 1) 위치일 확률 높음 (0-based index 시)
        #    혹은 일반적인 x^5 + x^2 + 1 탭: 5번 비트와 2번 비트 사용

        # bit_5 = (self.state >> 4) & 1  <-- 보통 x^5 항 (MSB쪽)
        # bit_2 = (self.state >> 1) & 1  <-- x^2 항

        # [주의] 문서 그림의 화살표 방향을 보면 XOR 결과가 왼쪽(입력)으로 들어감.
        # 일반적인 LFSR 구현:
        # feedback = bit_at_position_5 ^ bit_at_position_2

        bit_5 = (self.state >> 4) & 1
        bit_2 = (self.state >> 1) & 1

        feedback = bit_5 ^ bit_2

        # 3. 레지스터 시프트 (왼쪽으로 밀고 LSB에 피드백 or 오른쪽으로 밀고 MSB에 피드백)
        # 그림상: x9, x8 ... x0 순서이고 화살표가 왼쪽으로 들어가는 거면 Left Shift.
        # 하지만 통신 국룰은 보통 Right Shift 후 MSB 삽입 혹은 Left Shift 후 LSB 삽입임.
        # 여기서는 그림의 x^0 가 LSB라고 가정하고 Left Shift로 구현함.

        self.state = ((self.state << 1) & 0x3FF) | feedback
        # 0x3FF는 10비트 마스크 (그림에 x^9까지 있어서 10비트 유지해봄)

        return N


# --- 실행 검증 ---
scrambler = DocumentSpecificScrambler()

print("--- 생성된 스크램블링 심볼 (N) ---")
for i in range(10):
    val = scrambler.next_scramble_symbol()
    print(f"Index {i}: {val} (Binary: {bin(val)})")