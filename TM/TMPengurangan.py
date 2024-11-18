class TMPengurangan:
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
                '0': {'write': 'B', 'R': 'q1'},
                '1': {'write': 'B', 'R': 'q6'}
            },
            'q1': {
                '0': {'R': 'q1'},
                '1': {'R': 'q2'}
            },
            'q2': {
                '1': {'R': 'q2'},
                '0': {'write': '1', 'L': 'q3'},
                'B': {'L': 'q4'}
            },
            'q3': {
                '1': {'L': 'q3'},
                '0': {'L': 'q3'},
                'B': {'R': 'q0'}
            },
            'q4': {
                '1': {'write': 'B', 'L': 'q4'},
                '0': {'L': 'q4'},
                'B': {'write': '0', 'R': 'q5'}
            },
            'q5': {},  
            'q6': {
                '1': {'write': 'B', 'R': 'q6'},
                '0': {'write': 'B', 'R': 'q6'},
                'B': {'R': 'q5'}
            }
        }
        
        return table.get(state, {}).get(symbol)

    def run(self):
        while self.state != 'halt':
            self.step()

    def get_tape(self):
        return ''.join(self.tape).strip(self.blank_symbol)

# Example:
# input_tape = '000000100000'  
# tm = TMPengurangan(tape=input_tape)
# tm.run()
# print(tm.get_tape())  
