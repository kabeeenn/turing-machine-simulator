class TMFaktorial:
    def __init__(self, tape, blank_symbol='B'):
        self.tape = list(tape) + [blank_symbol]  
        self.head = 0
        self.state = 'q0'
        self.blank_symbol = blank_symbol

    def step(self):
        current_symbol = self.tape[self.head]
        action = self.get_action(self.state, current_symbol)
        
        if action is not None:
            self.tape[self.head] = action.get('write', current_symbol)
            self.head += 1 if 'R' in action else -1
            self.state = action.get('R', action.get('L'))
            if self.head == len(self.tape):
                self.tape.append(self.blank_symbol)  
            elif self.head < 0:
                self.tape.insert(0, self.blank_symbol)  
                self.head = 0 
        else:
            self.state = 'halt'

    def get_action(self, state, symbol):
        table = {
            'q0': {
                '0': {'write': 'X', 'R': 'q1'},
                '1': {'write': '1', 'R': 'q4'}
            },
            'q1': {
                '0': {'write': '0', 'R': 'q1'},
                '1': {'write': '1', 'R': 'q2'}
            },
            'q2': {
                '0': {'write': '0', 'R': 'q2'},
                'B': {'write': '0', 'L': 'q3'}
            },
            'q3': {
                '0': {'write': '0', 'L': 'q3'},
                '1': {'write': '1', 'L': 'q3'},
                'X': {'write': 'X', 'R': 'q0'}
            },
            'q4': {
                '0': {'write': '0', 'R': 'q4'},
                'B': {'write': '1', 'L': 'q5'}
            },
            'q5': {
                '0': {'write': '0', 'L': 'q5'},
                '1': {'write': '1', 'L': 'q5'},
                'X': {'write': 'X', 'L': 'q5'},
                'B': {'write': 'B', 'R': 'q6'}
            },
            'q6': {
                'X': {'write': 'B', 'R': 'q7'},
                '1': {'write': '0', 'R': 'f0'}
            },
            'f0': {
                '1': {'write': 'B', 'L': 'q25'}
            },
            'q7': {
                'X': {'write': '0', 'R': 'q8'},
                '1': {'write': 'B', 'R': 'q25'}
            },
            'q8': {
                'X': {'write': 'X', 'R': 'q8'},
                '1': {'write': '1', 'R': 'q9'}
            },
            'q9': {
                '0': {'write': 'X', 'R': 'q10'},
                '1': {'write': '1', 'L': 'q12'}
            },
            'q10': {
                '0': {'write': '0', 'R': 'q10'},
                '1': {'write': '1', 'R': 'q10'},
                'B': {'write': '0', 'L': 'q11'}
            },
            'q11': {
                '0': {'write': '0', 'L': 'q11'},
                '1': {'write': '1', 'L': 'q11'},
                'X': {'write': 'X', 'R': 'q9'}
            },
            'q12': {
                'X': {'write': '0', 'L': 'q12'},
                '1': {'write': '1', 'L': 'q13'}
            },
            'q13': {
                'X': {'write': 'X', 'L': 'q14'},
                '0': {'write': '0', 'L': 'q15'}
            },
            'q14': {
                'X': {'write': 'X', 'L': 'q14'},
                '0': {'write': '0', 'R': 'q7'}
            },
            'q15': {
                '0': {'write': '0', 'L': 'q15'},
                'B': {'write': 'B', 'R': 'q16'}
            },
            'q16': {
                '0': {'write': 'B', 'R': 'q17'}
            },
            'q17': {
                '0': {'write': '0', 'R': 'q17'},
                '1': {'write': '1', 'R': 'q18'}
            },
            'q18': {
                '0': {'write': '0', 'R': 'q18'},
                'X': {'write': 'X', 'R': 'q18'},
                '1': {'write': '1', 'L': 'q19'}
            },
            'q19': {
                'X': {'write': 'X', 'L': 'q19'},
                '0': {'write': 'X', 'L': 'q20'}
            },
            'q20': {
                '0': {'write': '0', 'L': 'q20'},
                '1': {'write': '1', 'L': 'q26'},
                'B': {'write': 'B', 'R': 'q21'}
            },
            'q21': {
                '0': {'write': 'B', 'R': 'q21'},
                '1': {'write': 'B', 'R': 'q21'},
                'X': {'write': 'B', 'R': 'q22'}
            },
            'q22': {
                'X': {'write': 'X', 'R': 'q23'},
                '1': {'write': 'B', 'R': 'q25'}
            },
            'q23': {
                'X': {'write': 'X', 'R': 'q23'},
                '0': {'write': '0', 'R': 'q23'},
                '1': {'write': '1', 'R': 'q23'},
                'B': {'write': '1', 'L': 'q24'}
            },
            'q24': {
                'X': {'write': 'X', 'L': 'q24'},
                '0': {'write': '0', 'L': 'q24'},
                '1': {'write': '1', 'L': 'q24'},
                'B': {'write': 'B', 'R': 'q7'}
            },
            'q25': {
                '0': {'R': 'q25'},
                '1': {'write': 'B', 'L': 'q25'}
            },
            'q26': {
                '0': {'write': '0', 'L': 'q15'},
                'B': {'write': 'B', 'R': 'q21'}
            }
        }
        
        return table.get(state, {}).get(symbol)

    def run(self):
        while self.state != 'halt':
            self.step()

    def get_tape(self):
        return ''.join(self.tape).strip(self.blank_symbol)

# Example:
# input_tape = '001'
# tm = TMFaktorial(tape=input_tape)
# tm.run()
# print(tm.get_tape())
