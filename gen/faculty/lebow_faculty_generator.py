from utils import *
from typing import cast

def generate_lebow_faculty_data(drexel_json: dict[str, Any]) -> None:
    professors: list[Any] = []
    for page in range(13):
        faculty_html = html(f"https://www.lebow.drexel.edu/faculty-and-research/faculty-directory?title=&field_term_disciplines_target_id=All&page={page}")
        for element in faculty_html.find_all("div", class_="wp grid__item"):
            name = element.find("a", class_="link link--name").decode_contents().strip().split(",")[0]
            print(f"Getting data for Professor {name}")
            title = element.find("p", class_="paragraph paragraph--job-title")
            title = title.decode_contents().strip() if title else "unknown"
            email = element.find("a", class_="link link--email").decode_contents().strip()
            phone_number = element.find("a", class_="link link--tel")
            phone_number = phone_number.decode_contents().strip().replace("(", "").replace(") ", "-") if phone_number else "unknown"
            professors.append({
                "name": name,
                "title": title,
                "email": email,
                "phoneNumber": phone_number
            })

    cast(dict[str, Any], find(lambda college: college["name"] == "LeBow College of Business", drexel_json["colleges"]))["faculty"] = professors