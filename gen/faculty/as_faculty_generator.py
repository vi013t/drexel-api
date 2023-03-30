from utils import *
from typing import cast
import re as regex

def generate_as_faculty_data(drexel_json: dict[str, Any]) -> None:
    as_professors: list[Any]= []
    professor_html = html("https://drexel.edu/coas/faculty-research/faculty-directory/")

    for element in professor_html.find_all("div", class_="fname"):
        professor_name = regex.sub(r"\s+", " ", element.find("h3").find("a").decode_contents().strip())
        print(f"Getting data for Professor {professor_name}")
        professor_role = regex.sub(r"\n+", "\n", element.parent.get_text().strip().replace("\r", "")).split("\n")[1].strip()
        
        professor_email = cast(Tag, find(lambda elem: elem["href"].startswith("mailto:"), element.parent.find_all("a"))).decode_contents().strip()
        professor_department = element.parent.parent.parent.find_all("td")[1].find("li").decode_contents().strip()
        professor_department = professor_department if professor_department else "unknown"
        professor_email = professor_email if professor_email else "unknown"

        # professor_interests = element.parent.parent.parent.find_all("td")[2].find("p")
        # professor_interests: list[str] = list(map(lambda x: x.strip(), professor_interests.decode_contents().strip().split(";"))) if professor_interests else []

        phone_number = regex.sub(r"\n+", "\n", element.parent.get_text().strip().replace("\r", "")).split("\n")
        phone_number = phone_number[len(phone_number) - 1].strip()
        phone_number = phone_number.replace(".", "-") if regex.match(r"^\d{3}\.\d{3}\.\d{4}$", phone_number) else "unknown"

        as_professors.append({
            "name": professor_name,
            "title": professor_role,
            "email": professor_email,
            "phoneNumber": phone_number,
        })

    cast(dict[str, Any], find(lambda college: college["name"] == "College of Arts and Sciences", drexel_json["colleges"]))["faculty"] = as_professors