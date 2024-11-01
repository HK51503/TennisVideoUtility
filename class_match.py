class Match:
    def __init__(self, match_id):
        self.match_id_low = match_id
        self.match_id_high = match_id.upper()
        self.match_id_full = ""
        self.file_list = []
        self.stitched_file = ""
        self.singles_or_doubles = match_id[0]
        self.youtube_upload_title = ""
        self.youtube_upload_description = ""
        self.youtube_upload_file_path = ""
        self.youtube_upload_id = ""

    def is_singles(self):
        if self.singles_or_doubles == "s":
            return True
        else:
            return False

    def get_match_id_full(self):
        return self.match_id_full

    def is_file_selected(self):
        if len(self.file_list) != 0:
            return True
        else:
            return False

    def clear_file_selection(self):
        self.file_list.clear()
        self.stitched_file = ""


class SinglesMatch(Match):
    def __init__(self, match_id):
        super().__init__(match_id)
        self.player_name = ""

    def set_player(self, player_name):
        self.player_name = player_name
        self.match_id_full = self.match_id_high + " " + player_name


class DoublesMatch(Match):
    def __init__(self, match_id):
        super().__init__(match_id)
        self.player_name_1 = ""
        self.player_name_2 = ""

    def set_player(self, player_name_1, player_name_2):
        self.player_name_1 = player_name_1
        self.player_name_2 = player_name_2
        self.match_id_full = self.match_id_high + " " + player_name_1 + " " + player_name_2
