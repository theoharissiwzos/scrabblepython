import random
import itertools

# Dictionary of Greek letters with their corresponding points
LETTER_POINTS = {
    'Α': 1, 'Β': 8, 'Γ': 4, 'Δ': 4, 'Ε': 1, 'Ζ': 8, 'Η': 1, 'Θ': 8, 
    'Ι': 1, 'Κ': 2, 'Λ': 3, 'Μ': 3, 'Ν': 1, 'Ξ': 10, 'Ο': 1, 'Π': 3, 
    'Ρ': 2, 'Σ': 1, 'Τ': 1, 'Υ': 2, 'Φ': 8, 'Χ': 8, 'Ψ': 10, 'Ω': 3
}

# Class defining the bag of letters
class SakClass:
    def __init__(self):
        self.letters = list(LETTER_POINTS.keys()) * 2  # Initial bag with each letter twice
        random.shuffle(self.letters)
    
    def draw_letters(self, num):
        drawn = random.sample(self.letters, min(num, len(self.letters)))
        for letter in drawn:
            self.letters.remove(letter)
        return drawn

    def return_letters(self, letters):
        self.letters.extend(letters)
        random.shuffle(self.letters)

    def letters_remaining(self):
        return len(self.letters)

# Basic Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.letters = []
        self.score = 0

    def add_letters(self, letters):
        self.letters.extend(letters)

    def remove_letters(self, letters):
        for letter in letters:
            self.letters.remove(letter)

    def calculate_score(self, word):
        return sum(LETTER_POINTS[letter] for letter in word)

# Human player class
class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    def play_word(self, word, dictionary):
        if all(letter in self.letters for letter in word) and word in dictionary:
            self.remove_letters(word)
            score = self.calculate_score(word)
            self.score += score
            return word, score
        else:
            return None, 0

    def swap_letters(self, sak):
        sak.return_letters(self.letters)
        self.letters = sak.draw_letters(7)

# Computer player class
class Computer(Player):
    def __init__(self, name, dictionary):
        super().__init__(name)
        self.dictionary = dictionary

    def find_best_word(self):
        best_word = ""
        best_score = 0
        for L in range(1, len(self.letters) + 1):
            for permutation in itertools.permutations(self.letters, L):
                word = ''.join(permutation)
                if word in self.dictionary:
                    score = self.calculate_score(word)
                    if score > best_score:
                        best_word = word
                        best_score = score
        return best_word, best_score

    def play_word(self):
        word, score = self.find_best_word()
        if word:
            self.remove_letters(word)
            self.score += score
            return word, score
        else:
            return None, 0

    def swap_letters(self, sak):
        sak.return_letters(self.letters)
        self.letters = sak.draw_letters(7)

# Game class managing the game flow
class Game:
    def __init__(self, human_name, dictionary_path):
        self.sak = SakClass()
        self.human = Human(human_name)
        with open(dictionary_path, 'r', encoding='utf-8') as file:
            self.dictionary = {line.strip() for line in file}
        self.computer = Computer("Υπολογιστής", self.dictionary)

    def start_game(self):
        self.human.add_letters(self.sak.draw_letters(7))
        self.computer.add_letters(self.sak.draw_letters(7))

        while True:
            # Human's turn
            print(f"Σειρά του {self.human.name}")
            self.display_letters(self.human.letters)
            print(f"Γράμματα που απομένουν στο σακουλάκι: {self.sak.letters_remaining()}")
            word = input("Εισάγετε μία λέξη ή 'swap' για αλλαγή γραμμάτων ή 'q' για έξοδο: ").strip().upper()

            if word == 'Q':
                print(f"{self.human.name} εγκαταλείπει το παιχνίδι.")
                break
            elif word == 'SWAP':
                self.human.swap_letters(self.sak)
                print(f"{self.human.name} αλλάζει γράμματα και χάνει τη σειρά του.")
            else:
                word, score = self.human.play_word(word, self.dictionary)
                if word:
                    print(f"Παίξατε τη λέξη {word} για {score} πόντους")
                    self.human.add_letters(self.sak.draw_letters(len(word)))
                else:
                    print("Μη έγκυρη λέξη ή η λέξη δεν βρέθηκε στο λεξικό. Η σειρά χάνεται.")

            if self.sak.letters_remaining() == 0:
                break

            # Computer's turn
            print("Σειρά του Υπολογιστή")
            word, score = self.computer.play_word()
            if word:
                print(f"Ο Υπολογιστής έπαιξε τη λέξη {word} για {score} πόντους")
                self.computer.add_letters(self.sak.draw_letters(len(word)))
            else:
                if self.sak.letters_remaining() > 0:
                    self.computer.swap_letters(self.sak)
                    print("Ο Υπολογιστής αλλάζει γράμματα και χάνει τη σειρά του.")
                else:
                    print("Ο Υπολογιστής δεν μπορεί να παίξει λέξη και δεν υπάρχουν γράμματα για αλλαγή.")
                    break

            if self.sak.letters_remaining() == 0:
                break

            print(f"Σκορ: {self.human.name} {self.human.score}, Υπολογιστής {self.computer.score}")

        print("Τέλος παιχνιδιού!")
        if len(self.human.letters) > 0 and len(self.computer.letters) == 0:
            print(f"{self.human.name} κερδίζει γιατί ο Υπολογιστής δεν έχει άλλα γράμματα!")
        elif len(self.computer.letters) > 0 and len(self.human.letters) == 0:
            print(f"Ο Υπολογιστής κερδίζει γιατί ο {self.human.name} δεν έχει άλλα γράμματα!")
        elif self.human.score > self.computer.score:
            print(f"{self.human.name} κερδίζει!")
        else:
            print("Ο Υπολογιστής κερδίζει!")

        print(f"Τελικό σκορ: {self.human.name} {self.human.score}, Υπολογιστής {self.computer.score}")

    def display_letters(self, letters):
        display = [f"{letter}({LETTER_POINTS[letter]})" for letter in letters]
        print("Τα γράμματά σας:", ' '.join(display))

if __name__ == "__main__":
    game = Game("Παίκτης1", 'greek7.txt')
    game.start_game()
