from utils import *
from typing import cast
import re as regex

def generate_cci_faculty_data(drexel_json: dict[str, list[Any]]) -> None:
    cci_faculty_html = html("https://drexel.edu/cci/academics/computer-science-department/faculty/")
    cci_faculty: list[Any] = []
    for row in cci_faculty_html.find_all("div", class_="row")[1:]:
     
        # Name
        name = " ".join(reversed(row.find("div", class_="cell").find("a").decode_contents().strip().split(", ")))
        print(f"Getting data for Professor {name}")
        
        # Interests
        # interests = row.find_all("div", class_="cell")[1].find("p").decode_contents().strip().split(", ")
        
        # Email
        email = cast(Tag, find(lambda elem: elem["href"].startswith("mailto:"), row.find_all("div", class_="cell")[2].find_all("a"))).decode_contents().strip()

        # Phone Number
        ps = row.find_all("div", class_="cell")[2].find_all("p")
        is_phone_number: Callable[[Tag], bool] = lambda p: bool(regex.match(r"^\d{3}\.\d{3}\.\d{4}$", p.decode_contents().strip()))
        phone_number = find(is_phone_number, ps)
        phone_number = phone_number.decode_contents().strip().replace(".", "-") if phone_number else "unknown"

        # Title
        title = row.find("div", class_="cell").find("a").parent.find("em").get_text().strip().replace("\n", ". ")

        # Register
        cci_faculty.append({
            "name": name,
            "title": title,
            "email": email,
            "phoneNumber": phone_number,
        })
    
    cast(dict[str, Any], find(lambda college: college["name"] == "College of Computing and Informatics", drexel_json["colleges"]))["faculty"] = cci_faculty