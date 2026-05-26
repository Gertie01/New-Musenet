def validate_midi_params(bpm, grid, time_sig):
    if not (75 <= bpm <= 160):
        return False
    if grid not in ["1/3", "1/4", "1/6"]:
        return False
    if time_sig not in ["4/4", "3/4"]:
        return False
    return True