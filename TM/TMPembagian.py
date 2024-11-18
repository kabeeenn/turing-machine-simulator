class TMPembagian:
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
                '+': {'write': 'B', 'R': 'q1'},
                '-': {'write': 'B', 'R': 'q2'}
            },
            'q1': {
                '0': {'R': 'q1'},
                '1': {'R': 'q1'},
                '+': {'R': 'q3'},
                '-': {'R': 'q6'}
            },
            'q2': {
                '0': {'R': 'q2'},
                '1': {'R': 'q2'},
                '+': {'R': 'q6'},
                '-': {'R': 'q3'}
            },
            'q3': {
                '0': {'R': 'q3'},
                '1': {'R': 'q3'},
                'B': {'write': '+', 'L': 'q5'}
            },
            'q5': {
                '0': {'L': 'q5'},
                '1': {'L': 'q5'},
                '+': {'L': 'q5'},
                '-': {'L': 'q5'},
                'B': {'R': 'q8'}
            },
            'q6': {
                '0': {'R': 'q6'},
                '1': {'R': 'q6'},
                'B': {'write': '-', 'L': 'q5'}
            },
            'q8': {
                '0': {'write': 'X', 'R': 'q9'},
                '1': {'R': 'q19'}
            },
            'q9': {
                '0': {'R': 'q9'},
                '1': {'R': 'q10'}
            },
            'q10': {
                'X': {'R': 'q10'},
                '+': {'R': 'q10'},
                '-': {'R': 'q10'},
                '0': {'write': 'X', 'L': 'q11'},
                '1': {'write': 'B', 'L': 'q17'}
            },
            'q11': {
                'X': {'L': 'q11'},
                '+': {'L': 'q11'},
                '-': {'L': 'q11'},
                '1': {'L': 'q12'}
            },
            'q12': {
                '0': {'L': 'q12'},
                'X': {'R': 'q8'}
            },
            'q13': {
                'X': {'R': 'q13'},
                '0': {'R': 'q13'},
                '1': {'R': 'q13'},
                '+': {'R': 'q13'},
                '-': {'R': 'q13'},
                'B': {'write': '0', 'L': 'q14'}
            },
            'q14': {
                '0': {'L': 'q14'},
                '+': {'L': 'q14'},
                '-': {'L': 'q14'},
                '1': {'L': 'q15'}
            },
            'q15': {
                '0': {'L': 'q15'},
                'X': {'L': 'q15'},
                '+': {'L': 'q15'},
                '-': {'L': 'q15'},
                '1': {'L': 'q16'}
            },
            'q16': {
                'X': {'write': '0', 'L': 'q16'},
                'B': {'R': 'q8'}
            },
            'q17': {
                '0': {'write': 'B', 'L': 'q17'},
                '1': {'write': 'B', 'L': 'q17'},
                'X': {'write': 'B', 'L': 'q17'},
                '+': {'write': 'B', 'L': 'q17'},
                '-': {'write': 'B', 'L': 'q17'},
                'B': {'R': 'q18'}
            },
            'q18': {
                'B': {'R': 'q18'},
                '+': {'write': 'B', 'R': 'q21'},
                '-': {'write': 'B', 'R': 'q21'}
            },
            'q19': {
                '+': {'R': 'q20'},
                '-': {'R': 'q20'}
            },
            'q20': {
                'X': {'R': 'q13'},
                '0': {'L': 'q20'},
                '1': {'L': 'q20'},
                '+': {'L': 'q20'},
                'B': {'R': 'q22'}
            },
            'q21': {},
            'q22': {
                '1': {'write': 'B', 'R': 'q22'},
                '0': {'write': 'B', 'R': 'q22'},
                '+': {'write': 'B', 'R': 'q22'},
                'B': {'write': 'Y', 'R': 'q21'}
            }
        }
        
        return table.get(state, {}).get(symbol)

    def run(self):
        while self.state != 'halt':
            self.step()

    def get_tape(self):
        return ''.join(self.tape).strip(self.blank_symbol)

# Example:
# input_tape = '+001+00001'
# tm = TMPembagian(tape=input_tape)
# tm.run()
# print(tm.get_tape())
