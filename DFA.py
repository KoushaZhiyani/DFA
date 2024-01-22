##########################################################
##        1.generate n string                           ##
##        2.string check                                ##
##        3.check have loop                             ##
##        4.check finite state machine                  ##
##########################################################

class State:
    def __init__(self, label):
        self.label = label
        self.links = {}

    def set_link(self, alph, state_f):
        self.links[alph] = state_f


class DFA:
    def __init__(self, states, alphabet, initial, acceptance):
        self.all_states = []
        self.all_alphabet = []
        self.path = []
        self.wayTrue = []
        self.wayFalse = []
        self.loop = []
        c = 0
        for i in range(len(states)):
            self.all_states.append(State(states[i]))
            if initial == self.all_states[i].label:
                self.startG = self.all_states[i]
                c = c + 1
            if acceptance == self.all_states[i].label:
                self.endG = self.all_states[i].label
                c = c + 1

        else:
            if c != 2:
                print("we have problem in initial or acceptance")
                exit()

        self.endG = acceptance

        for i in alphabet:
            self.all_alphabet.append(i)

    def connection(self, state_s, alph, state_f):
        states = [i.label for i in self.all_states]
        if state_s in states and state_f in states and alph in self.all_alphabet:
            start_index = states.index(state_s)

        else:
            print("state_s or alph or state_f error")
            exit()

        self.all_states[start_index].set_link(alph, state_f)

    def string_check(self, text, check=1):
        copy_text = text
        text = list(text)
        copy_startG = self.startG

        while text:
            letter = int(text.pop(0))
            index = self.startG.links
            if letter in index:
                res = self.startG.links[letter]
                for i in range(len(self.all_states)):
                    if self.all_states[i].label == res:
                        self.startG = self.all_states[i]
            else:
                if letter not in index and check == 1:
                    print("unaccepted")
                self.startG = copy_startG
                return

        if self.startG.label == self.endG and check == 1:
            print("accepted")
        elif self.startG.label == self.endG and check == 0:
            self.wayTrue.append(copy_text)
        elif self.startG.label != self.endG and check == 0:
            self.wayFalse.append(copy_text)

        self.startG = copy_startG

    def generate(self, n, check=0):
        for i in range(1, n + 1):
            for j in range(2 ** i):
                sample = str(bin(j)).replace("0b", "")
                sample = sample[::-1]
                sample = self.convertor(sample, i)
                sample = sample[::-1]

                self.path.append(sample)
        print(self.path)
        if check == 1:
            return self.path
        for i in self.path:
            self.string_check(i, check=0)
        print("accepted list :", self.wayTrue)
        print("unaccepted list :", self.wayFalse)

    def convertor(self, sample, n):
        while len(sample) - n < 0:
            sample += "0"
        return sample

    def have_loop(self):
        copy_g = self.startG
        self.loop.append(self.startG.label)
        if self.check_have_loop() == 1:
            exit()

        index = self.startG.links
        if 0 in index:
            res = self.startG.links[0]

            for i in range(len(self.all_states)):
                if self.all_states[i].label == res:
                    self.startG = self.all_states[i]
                    self.have_loop()
                    self.startG = copy_g
        if 1 in index:
            res = self.startG.links[1]

            for i in range(len(self.all_states)):
                if self.all_states[i].label == res:
                    self.startG = self.all_states[i]
                    self.have_loop()
                    self.startG = copy_g

        self.loop.remove(self.startG.label)

        if len(self.loop) == 0:
            print("Finite state machine!")
            return 0

    def check_have_loop(self):

        for i in range(len(self.loop)):
            for j in range(i + 1, len(self.loop)):
                if self.loop[i] == self.loop[j]:
                    print("find loop!")
                    return 1

    def finite_state(self):

        pos = self.have_loop()
        if pos == 0:
            self.generate(len(self.all_states) - 1)


##########################TEST###########################################
a = DFA(['q0', 'q1', 'q2', 'q3', 'q4'], [0, 1], 'q0', 'q3')

a.connection('q0', 0, 'q1')
a.connection('q1', 1, 'q2')
a.connection('q2', 1, 'q3')
# a.connection('q1', 0, 'q0')
# a.connection('q4', 1, 'q3')
# a.connection('q3', 1, 'q3')
# a.string_check("011")
# a.finite_state()
# a.have_loop()


