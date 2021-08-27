from typing import List, Tuple

from turing_machine import TuringMachine
from collections import defaultdict
import regex


class TuringMachinesLoader:
    def __init__(self, path: str) -> None:
        self.sets = {}
        self.lists = {}
        self.funcs = defaultdict(dict)
        self.machines = {}
        with open(path, mode='r') as file:
            self.load_str(file.read())

    def load_str(self, code: str) -> None:
        function_regex = regex.compile(r"^(\w+)\((\w+),(\w+)\)=\((\w+),(\w+),(\w+)\)$")
        set_regex = regex.compile(r"^(\w+)=\{(?:(\w+),)*(\w+)?\}$")
        machine_regex = regex.compile(r"^(\w+)=\((\w+),(\w+),(\w+),(\w+),(\w+),(\w+),(\w+)\)$")
        list_regex = regex.compile(r"^(\w+)=\[(?:(\w+),)*(\w+)?\]$")

        for line in code.replace(" ", "").split():
            if line[0] == "#":
                continue
            elif function_regex.match(line):
                match = function_regex.match(line)

                f_name = match.group(1)
                f_params = (match.group(2), match.group(3))
                f_return = (match.group(4), match.group(5), match.group(6))

                if f_params in self.funcs[f_name]:
                    raise Exception(f'Parameter {f_params} duplicated on transition function {f_name}')

                self.funcs[f_name][f_params] = f_return
            elif set_regex.match(line):
                match = set_regex.match(line)

                s_name = match.group(1)
                s_elements = tuple(match.captures(2) + match.captures(3))

                if len(set(s_elements)) != len(s_elements):
                    raise Exception(f'Duplicated symbol in set {s_name}')
                if s_name in self.sets:
                    raise Exception(f'Duplicated set {s_name}')

                self.sets[s_name] = set(s_elements)
            elif machine_regex.match(line):
                match = machine_regex.match(line)

                m_name = match.group(1)
                m_components = (match.group(2), match.group(3), match.group(4), match.group(5),
                                match.group(6), match.group(7), match.group(8))

                if m_name in self.machines:
                    raise Exception(f'Duplicated machine {m_name}')

                self.machines[m_name] = m_components
                self.check_machine(m_name)
            elif list_regex.match(line):
                match = list_regex.match(line)

                l_name = match.group(1)
                l_elements = match.captures(2) + match.captures(3)

                if l_name in self.lists:
                    raise Exception(f'Duplicated list {l_name}')

                self.lists[l_name] = l_elements
            elif line[0] == "!":
                self.run_command(line)
            else:
                raise Exception(f'Unknown command: "{line}"')

    def check_machine(self, m_name: str) -> None:
        n_sigma, n_gamma, n_Q, n_f, B, q0, n_F = self.machines[m_name]

        if n_sigma not in self.sets:
            raise Exception(f'Set {n_sigma} from machine {m_name} not exists')
        sigma = self.sets[n_sigma]
        if n_gamma not in self.sets:
            raise Exception(f'Set {n_gamma} from machine {m_name} not exists')
        gamma = self.sets[n_gamma]
        if n_Q not in self.sets:
            raise Exception(f'Set {n_Q} from machine {m_name} not exists')
        Q = self.sets[n_Q]
        if n_F not in self.sets:
            raise Exception(f'Set {n_F} from machine {m_name} not exists')
        F = self.sets[n_F]
        if n_f not in self.funcs:
            raise Exception(f'Transition function {n_f} from machine {m_name} not exists')
        f = self.funcs[n_f]

        dif = F.difference(Q)
        if len(dif) != 0:
            raise Exception(f'States {dif} from machine {m_name} in final states set {n_F} not in states set {n_Q}')
        inters = Q.intersection(gamma)
        if len(inters) != 0:
            raise Exception(f'Symbols {inters} from machine {m_name} are both Symbol and State')

        if q0 not in Q:
            raise Exception(f'Initial state {q0} from machine {m_name} not in set {n_Q}')

        if len(gamma.union(sigma)) != len(gamma):
            raise Exception(
                f'Sigma set {n_sigma} from machine {m_name} is not gamma' + '\'s' + f' {n_gamma} subset ')
        if B not in gamma:
            raise Exception(
                f'Blank symbol {B} from machine {m_name} not in {n_gamma} or in both {n_gamma} and {n_sigma}')

        for (q, a), (p, b, D) in f.items():
            if D not in ["R", "L"]:
                raise Exception(f'Direction {D} not in ' + '{R, L}')
            if q not in Q:
                raise Exception(f'State {q} from machine {m_name} in transition function {n_f} not in set {n_Q}')
            if p not in Q:
                raise Exception(f'State {p} from machine {m_name} in transition function {n_f} not in set {n_Q}')
            if a not in gamma:
                raise Exception(
                    f'Symbol {a} from machine {m_name} in transition function {n_f} not in set {n_gamma} or {n_sigma}')
            if b not in gamma:
                raise Exception(
                    f'Symbol {b} from machine {m_name} in transition function {n_f} not in set {n_gamma} or {n_sigma}')

        self.machines[m_name] = TuringMachine(sigma, gamma, Q, f, B, q0, F)

    def run_command(self, command: str) -> None:
        run_regex = regex.compile(r"^!run\((\w+),(\w+)\)$")

        if run_regex.match(command):
            match = run_regex.match(command)

            m_name = match.group(1)
            l_name = match.group(2)

            if m_name not in self.machines:
                raise Exception(f'Machine {m_name} from run command "{command}" not exists')
            machine = self.machines[m_name]
            if l_name not in self.lists:
                raise Exception(f'Array {l_name} from run command "{command}" not exists')
            inp = self.lists[l_name]
            for sym in inp:
                if sym not in machine.sigma:
                    raise Exception(f'Symbol {sym} from input array {l_name} in run command "{command}" not in machine {m_name} sigma set')

            print(machine.run(inp))
        else:
            raise Exception(f'Unknown command: "{command}"')
