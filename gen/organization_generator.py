from utils import *
import re as regex

def generate_organization_data(drexel_json: dict[str, list[Any]]):
    clubs_html = BeautifulSoup(open("data_generation/pages/clubs.html").read(), features = "html.parser")
    clubs = clubs_html.find_all("div", class_="MuiPaper-root MuiCard-root MuiPaper-elevation3 MuiPaper-rounded")

    organizations: list[dict[str, Any]] = []

    for club_element in clubs:
        club_div = club_element.find("div").find("span").find("div").find("div")
        club_name = regex.sub(r"\s+", " ", club_div.find("div", attrs={"alt": None}).decode_contents()).strip()
        print(f"Getting data for student organization \"{club_name}\"")
        club_desc = regex.sub(r"\s+", " ", club_div.find("p").decode_contents()).strip()
        link = club_element.parent["href"]

        organizations.append({
            "name": club_name,
            "description": club_desc,
            "link": link
        })

    drexel_json["studentOrganizations"] = organizations