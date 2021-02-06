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


# Parse the HTML code for a MyAnimeList entry given its URL; return the English title and MAL score of the entry
def fetch_anime_info(url):
    title_tag = 'class="dark_text">English:</span> '
    title_endpoint = "\n"
    title_tag_alternative = '<meta property="og:title" content="'
    title_endpoint_alternative = '"'
    title_unknown = "entry title unknown"
    score_tag = 'class="score-label score-'
    score_tag_modifiable = 'n">'
    score_endpoint = "<"
    score_unknown = -1
    with urlopen(url) as html:
        data = html.read().decode("utf-8")
        title_start = data.find(title_tag)
        if title_start == -1:
            title_start = data.find(title_tag_alternative)
            if title_start == -1:
                title = title_unknown
            else:
                title_start += len(title_tag_alternative)
                title_stop = data.find(title_endpoint_alternative, title_start)
                if title_stop == -1:
                    title = title_unknown
                else:
                    title = data[title_start:title_stop]
        else:
            title_start += len(title_tag)
            title_stop = data.find(title_endpoint, title_start)
            if title_stop == -1:
                title = title_unknown
            else:
                title = data[title_start:title_stop]
        score_start = data.find(score_tag)
        if score_start == -1:
            score = score_unknown
        else:
            score_start += len(score_tag) + len(score_tag_modifiable)
            score_stop = data.find(score_endpoint, score_start)
            if score_stop == -1:
                score = score_unknown
            else:
                try:
                    score = float(data[score_start:score_stop])
                except ValueError:
                    score = score_unknown
    return title, score


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
    site_tag = 'class="hoverinfo_trigger fl-l ml12 mr8" href="'
    site_endpoint = '"'
    site_unknown = "entry site unknown"
    with urlopen("https://myanimelist.net/topanime.php") as site_html:
        site_data = site_html.read().decode("utf-8")
        top_50_start = [site.start() for site in re.finditer(site_tag, site_data)]
        for site_start in top_50_start:
            if site_start == -1:
                print(site_unknown)
            else:
                site_start += len(site_tag)
                site_stop = site_data.find(site_endpoint, site_start)
                if site_stop == -1:
                    print(site_unknown)
                else:
                    site = site_data[site_start:site_stop]
                    if site[-1] == "°":
                        site = site[:-1]
                    entry_title, entry_score = fetch_anime_info(site)
                    entry_title = entry_title.replace("&#039;", "'")
                    entry_score = format(entry_score, ".2f")
                    print(f"{entry_title}, {entry_score}")
