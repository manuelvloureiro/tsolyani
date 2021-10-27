from random import randint, sample


class Table(dict):

    def __init__(self, dict_with_iterables):

        super().__init__()
        for k, v in dict_with_iterables.items():
            if not hasattr(k, '__iter__'):
                k = [k]
            for o in k:
                if self.get(o):
                    raise KeyError("Key is overrepresented")
                self[o] = v

        self.min = min(self.keys())
        self.max = max(self.keys())

        for o in range(self.min, self.max + 1):
            if not self.get(o):
                raise KeyError("Key is underrepresented")

    def roll(self, min_=None, max_=None):
        k = randint(min_ or self.min, max_ or self.max)
        must_roll = isinstance(self[k], Table) or \
                    (isinstance(self[k], type) and issubclass(self[k], Table))
        return self[k].roll() if must_roll else self[k]


shape = Table({
    range(1, 11): 'VCV',
    range(11, 21): 'VCVC',
    range(21, 31): 'VCVCV',
    range(31, 41): 'CVC',
    range(41, 71): 'CVCV',
    range(71, 91): 'CVCVC',
    range(91, 96): 'CVCVCV',
    range(96, 101): 'CVCVCVC',
})

C = Table({
    range(1, 3): Table({1: 'p', 2: 'b', 3: 'm', 4: 'f', 5: 'v', 6: 'w', 7: 't',
                        8: 'd', 9: 'n', 10: 'th'}),
    range(3, 5): Table({1: 'dh', 2: 'ch', 3: 'l', 4: 'y', 5: 'k', 6: 'g',
                        7: 'kh', 8: Table({1: 'gh', 2: "'"}), 9: 'q', 10: 'h'}),
    range(5, 7): Table({1: 'w', 2: 'ts', 3: 'tl', 4: 's', 5: 'sh', 6: 'z',
                        7: Table({1: 'zh', 2: "ss"}), 8: 'r', 9: 'l', 10: 'hl'})
})

last_consonant_in_a_cluster = Table(
    {1: 'm', 2: 'n', 3: 'ng', 4: 'r', 5: 'l', 6: 'y', 7: 's', 8: 'sh', 9: 'ss',
     10: Table({1: 'tl', 2: 'sh'})})


class CC(Table):

    @classmethod
    def roll(cls, **kwargs):
        first = C.roll()
        if first == 'n':
            second = last_consonant_in_a_cluster.roll()
        else:
            second = last_consonant_in_a_cluster.roll(
                max_=last_consonant_in_a_cluster.max - 1)
        return first + second


class CCC(Table):

    @classmethod
    def roll(cls, **kwargs):
        return C.roll() + CC.roll()


first_consonant_cluster = Table({
    range(1, 51): C,
    range(51, 96): CC,
})

consonant_clusters = Table({
    range(1, 51): C,
    range(51, 96): CC,
    range(96, 101): CCC,
})

final_consonant = Table(
    {1: 'm', 2: 'n', 3: 'ng', 4: 'r', 5: 'l', 6: 'kh', 7: 'k', 8: 's', 9: 'hl',
     10: Table({1: 'tl', 2: 'sh'})})


class Dipthong(Table):
    diphthong = {0: '_', 1: 'i', 2: 'a', 3: 'o', 4: 'u', 5: 'y', 6: 'e'}

    @classmethod
    def roll(cls, **kwargs):
        return ''.join(map(cls.diphthong.get, sample(range(1, 7), 2)))


vowel = Table({1: 'i', 2: 'a', 3: 'o', 4: 'u', 5: 'y', 6: 'e', 7: 'au', 8: 'ai',
               9: 'oi', 10: Dipthong})


def generate_name():
    name = shape.roll()
    for i in reversed(range(1, len(name) - 1)):
        if name[i] == 'C':
            name = name[:i] + consonant_clusters.roll() + name[i + 1:]
    if name[0] == 'C':
        name = first_consonant_cluster.roll() + name[1:]
    if name[-1] == 'C':
        name = name[:-1] + final_consonant.roll()
    for i in reversed(range(len(name))):
        if name[i] == 'V':
            name = name[:i] + vowel.roll() + name[i + 1:]
    return name[:2].title() + name[2:]


if __name__ == '__main__':
    for _ in range(10):
        print(generate_name())
