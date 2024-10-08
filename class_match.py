class Match:
    def __init__(self, match_id):
        self.match_id_low = match_id
        self.match_id_high = match_id.upper()
        self.file_list = []
        self.stitched_file = ""
        self.singles_or_doubles = match_id[0]
        self.player_1 = ""
        self.player_2 = ""