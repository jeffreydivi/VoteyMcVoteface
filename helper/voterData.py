import math

class VoterData:
    def __init__(self, num_answers):
        self.num_answers = num_answers
        self.fptp = -1
        self.borda = [0] * num_answers
        self.score = [0] * num_answers
        self.quad = [0] * num_answers

    # first past the poll (pole?) post
    def score_fptp(self, answer_index):
        self.fptp = answer_index

    # the way we implement ranked-choice makes it a borda count
    def score_borda(self, vote_array):
        for i in range(self.num_answers):
            self.borda[i] = vote_array[i]
        #need to convert the raw votes into a score depending on size
        #ex: if vote_array = [10, 4, 8] -> ranked_array = [1, 3, 2]

    # unweighted votes
    def score_score(self, vote_array):
        for i in range(self.num_answers):
            self.score[i] = vote_array[i]

    # quadratic scoring
    def score_quad(self, vote_array):
        for i in range(self.num_answers):
            self.quad[i] = math.sqrt(vote_array[i])

    def get_votes(self):
        return {
            "fptp": self.fptp,
            "borda": self.borda,
            "score": self.score,
            "quad": self.quad
        }
