from typing import Tuple, Dict, List


class TuringMachine:
    def __init__(self, sigma: Tuple[str], gamma: Tuple[str], Q: Tuple[str],
                 f: Dict[Tuple[str, str], Tuple[str, str, str]], B: str, q0: str, F: Tuple[str]) -> None:
        self.sigma = sigma
        self.gamma = gamma
        self.Q = Q
        self.f = f
        self.B = B
        self.q0 = q0
        self.F = F

    def run(self, inp: List[str], ptr=0) -> Tuple[List[str], bool]:
        tape = inp.copy()
        pointer = ptr
        q = self.q0

        while True:
            if pointer < 0:
                return self.clear(tape), False
            if pointer == len(tape):
                tape.append(self.B)

            state = (q, tape[pointer])
            if state in self.f:
                p, x, d = self.f[state]
                tape[pointer] = x
                pointer += 1 if d == "R" else -1
                q = p
            else:
                return self.clear(tape), q in self.F

    def clear(self, inp: List[str]) -> List[str]:
        if inp[-1] != self.B:
            return inp
        ind = len(inp) - 1
        for i in range(ind, -1, -1):
            if inp[i] != self.B:
                ind = i + 1
                break
        else:
            return []
        return inp[:ind]
