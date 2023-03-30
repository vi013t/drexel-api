from utils import *
from typing import cast
import re as regex

def generate_westphal_faculty_data(drexel_json: dict[str, Any]) -> None:
    faculty = html("https://drexel.edu/westphal/about/directory/")
    professors: list[Any] = []
    for row in cast(Tag, faculty.find("tbody")).find_all("tr"):
        name = row.find("td").find("a").find("b").decode_contents().strip()
        print(f"Getting data for Professor {name}")
        title = regex.sub(r"\n+", "\n", row.find("td").parent.get_text()).split("\n")
        title = title[1][len(name):]
        email = row.find_all("td")[2].find("a").decode_contents().strip()
        phone_number = regex.sub(r"\n+", "\n", row.find_all("td")[2].get_text().strip()).split("\n")[0]
        phone_number = phone_number[:12].replace(".", "-") if regex.match(r"^\d{3}\.\d{3}\.\d{4}", phone_number) else "unknown"
        professors.append({
            "name": name,
            "title": title,
            "email": email,
            "phoneNumber": phone_number,
        })

    cast(dict[str, Any], find(lambda college: college["name"] == "Antoinette Westphal College of Media Arts & Design", drexel_json["colleges"]))["faculty"] = professors