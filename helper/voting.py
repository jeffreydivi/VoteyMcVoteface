import math

class Voting:
    def __init__(self, num_answers):
        super(Voting, self).__init__()
        self.num_voters = 0
        self.num_answers = num_answers
        self.fptp = dict.fromkeys(range(1, num_answers + 1), 0)
        self.borda = dict.fromkeys(range(1, num_answers + 1), 0)
        self.score = dict.fromkeys(range(1, num_answers + 1), 0)
        self.quad = dict.fromkeys(range(1, num_answers + 1), 0)

    # increment whichever answer is chosen by 1
    def fptp_vote(self, answer_index):
        self.fptp[answer_index + 1] += 1

    def borda_vote(self, vote_array):
        for i in range(1, self.num_answers + 1):
            self.borda[i] += vote_array[i - 1]

    # Take the score for each answer and add it
    def score_vote(self, vote_array):
        for i in range(1, self.num_answers + 1):
            self.score[i] += vote_array[i - 1]

    # The n'th vote costs n^2 points out of a fixed pool of points
    # "cost to the voter = (number of votes)^2"
    def quadratic(self, vote_array):
        for i in range(1, self.num_answers + 1):
            self.quad[i] += vote_array[i - 1]

    # Return data in JSON format
    def get_votes(self):
        sorted_fptp = {key: val for key, val in sorted(self.fptp.items(), key = lambda ele: ele[1], reverse = True)}
        sorted_borda = {key: val for key, val in sorted(self.borda.items(), key = lambda ele: ele[1])}
        sorted_score = {key: val for key, val in sorted(self.score.items(), key = lambda ele: ele[1], reverse = True)}
        sorted_quad = {key: val for key, val in sorted(self.quad.items(), key = lambda ele: ele[1], reverse = True)}

        return {
            "fptp": sorted_fptp,
            "borda": sorted_borda,
            "score": sorted_score,
            "quad": sorted_quad
        }


