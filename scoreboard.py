def get_scoreboard(path):
    try:
        with open(path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return ""


def update_scoreboard(scoreboard_file, time, difficulty):
    try:
        with open(scoreboard_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        content = "===EASY===\n\n===MEDIUM===\n\n===HARD===\n"

    sections = {"EASY": [], "MEDIUM": [], "HARD": []}
    current_section = None

    for line in content.split('\n'):
        if line.startswith("==="):
            current_section = line.strip("= \n")
        elif line and current_section:
            sections[current_section].append(line.split(') ')[1])

    sections[difficulty].append(format_time(time))
    sorted_times = quicksort(sections[difficulty])

    new_content = ""
    for diff in ["EASY", "MEDIUM", "HARD"]:
        new_content += f"==={diff}===\n" + format_section(sorted_times if diff == difficulty else sections[diff]) + "\n"

    with open(scoreboard_file, 'w') as f:
        f.write(new_content.strip())


def format_time(time):
    minutes, seconds = divmod(time, 60)
    seconds, milliseconds = divmod(seconds, 1)
    return f"{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds * 100):02d}"


def format_section(times):
    return '\n'.join(f"{i + 1}) {time}" for i, time in enumerate(times))