from urllib.request import urlopen
import re


# Check if an input meets a set of criteria; return the validated input
def validate_input(prompt="Enter a valid input: ", type_=None, range_=None, min_=None, max_=None, default=None):
    sequence = None
    if min_ is not None and max_ is not None and min_ > max_:
        raise ValueError("'min_' is greater than 'max_'")
    if range_ is not None:
        if not range_:
            raise ValueError("'range_' is an empty sequence")
        if isinstance(range_, range):
            if type_ is not None and type_ is not int:
                raise ValueError("one or more elements in 'range_' is not of type 'type_'")
            if min_ is not None and range_.start < min_:
                range_.start = min_
            if max_ is not None and range_.stop - 1 > max_:
                range_.stop = max_ + 1
            sequence = f"between {range_.start} and {range_.stop - 1}"
        else:
            if type_ is not None:
                try:
                    range_ = [type_(element) for element in range_]
                except ValueError as error:
                    raise ValueError("one or more elements in 'range_' is not of type 'type_'") from error
            elements = [str(element) for element in range_]
            if len(range_) < 3:
                sequence = " or ".join(elements)
            else:
                sequence = ", ".join((*elements[:-1], f"or {elements[-1]}"))
    if default is not None:
        if type_ is not None:
            try:
                default = type_(default)
            except ValueError as error:
                raise ValueError("'default' is not of type 'type_'") from error
        if min_ is not None and default < min_:
            raise ValueError("'default_' is less than 'min_'")
        if max_ is not None and default > max_:
            raise ValueError("'default' is greater than 'max_'")
        if range_ is not None and default not in range_:
            raise ValueError("'default' is not an element in 'range_'")
    while True:
        input_ = input(prompt)
        if default is not None and input_ == "":
            input_ = default
        elif type_ is not None:
            try:
                input_ = type_(input_)
            except ValueError:
                print(f"Input must be of type {type_.__name__}.")
                continue
        if range_ is not None and input_ not in range_:
            print(f"Input must be {sequence}.")
        elif min_ is not None and input_ < min_:
            print(f"Input must be greater than or equal to {min_}.")
        elif max_ is not None and input_ > max_:
            print(f"Input must be less than or equal to {max_}.")
        else:
            return input_


# Find an element in HTML code given its start and end tag; return the element content
def find_html_element(html, start_tag, end_tag):
    title_start = html.find(start_tag)
    title_end = html.find(end_tag, title_start + len(start_tag))
    if title_start == -1 or title_end == -1:
        return False
    return html[title_start + len(start_tag):title_end]


# Parse the HTML code for a MyAnimeList entry given its URL; return the English title and MAL score of the entry
def fetch_anime_info(url):
    title_jap_start = '<h1 class="title-name h1_bold_none"><strong>'
    title_jap_end = '</strong>'
    title_eng_start = '<p class="title-english title-inherit">'
    title_eng_end = '</p>'
    title_unknown = "entry title unknown"
    # Actual score tag is '<span itemprop="ratingValue" class="score-label score-n">', where n is 0-9
    score_start = '<span itemprop="ratingValue" class="score-label score-'
    score_end = '</span>'
    score_unknown = 0
    with urlopen(url) as html:
        parsed_html = html.read().decode("utf-8")
        title_jap = find_html_element(parsed_html, title_jap_start, title_jap_end)
        if not title_jap:
            title_jap = title_unknown
        title_eng = find_html_element(parsed_html, title_eng_start, title_eng_end)
        if not title_eng:
            title_eng = title_jap
        score = find_html_element(parsed_html, score_start, score_end)
        if not score:
            score = score_unknown
        else:
            score = float(score[3:])
    return title_jap, title_eng, score


# Generate top 50 anime entries currently on MyAnimeList
def print_top_50():
    site_start = '<a class="hoverinfo_trigger fl-l ml12 mr8" href="'
    site_end = '"'
    site_unknown = "entry site unknown"
    with urlopen("https://myanimelist.net/topanime.php") as site_html:
        site_parsed_html = site_html.read().decode("utf-8")
        top_50 = [site.start() for site in re.finditer(site_start, site_parsed_html)]
        for entry in top_50:
            site = find_html_element(site_parsed_html[entry:], site_start, site_end)
            if not site:
                print(site_unknown)
            else:
                if site[-1] == "°":
                    site = site[:-1]
                entry_title_jap, entry_title_eng, entry_score = fetch_anime_info(site)
                entry_title_jap = entry_title_jap.replace("&#039;", "'")
                entry_title_eng = entry_title_eng.replace("&#039;", "'")
                entry_score = format(entry_score, ".2f")
                print(f"{entry_title_jap} ({entry_title_eng}), {entry_score}")


class List:
    def __init__(self, file_name):
        self.file_name = file_name
        try:
            with open(self.file_name, "r") as file:
                self.catalogue = [entry for entry in file]
        except FileNotFoundError:
            self.catalogue = []

    def add(self, title, score, url):
        self.catalogue.append((title, score, url))

    def remove(self, title):
        if title in [entry[0] for entry in self.catalogue]:
            self.catalogue = [entry for entry in self.catalogue if entry[0] != title]

    def save(self):
        with open(self.file_name, "w") as file:
            file.write("\n".join(f"[{entry[0]}]({entry[2]})" for entry in self.catalogue))

    def sort(self, sort_by_score):
        if sort_by_score:
            self.catalogue.sort(key=lambda entry: entry[1])
        else:
            self.catalogue.sort(key=lambda entry: str.lower(entry[0]))


if __name__ == "__main__":
    while True:
        print("[0] Exit")
        print("[1] Generate the current top 50 anime entries on MyAnimeList")
        print("[2] Generate the information for a MyAnimeList entry")
        selection = validate_input("Please make a selection: ", int, [0, 1, 2])
        print("\n")
        if selection == 1:
            print_top_50()
            print("\n")
        elif selection == 2:
            url = validate_input("Please enter a MyAnimeList link (default is https://myanimelist.net/anime/40591): ",
                                 str, default="https://myanimelist.net/anime/40591")
            title_jap, title_eng, score = fetch_anime_info(url)
            print(f"{title_jap} ({title_eng}), {score}\n")
        else:
            break
