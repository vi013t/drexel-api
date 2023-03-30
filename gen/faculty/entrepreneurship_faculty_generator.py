from utils import *
from typing import cast

def generate_entrepreneurship_faculty_data(drexel_json: dict[str, Any]):
    professors: list[Any] = []
    faculty_html = html("https://drexel.edu/close/about/staff/")
    i = 0
    for element in faculty_html.find_all("div", class_="clearfix"):
        name = element.find("h2").decode_contents().strip()
        print(f"Getting data for Professor {name}")
        title = element.find_all("h2")[1].get_text().strip()
        email = cast(Tag, find(lambda x: x["href"].startswith("mailto"), element.find_all("a"))).decode_contents().strip()
        phone_number = list(filter(lambda x: len(x) > 0, cast(Tag, cast(Tag, find(lambda x: x["href"].startswith("mailto"), element.find_all("a"))).parent).get_text().split("\n")))[-2 if i != 0 else -3].strip().replace(".", "-")

        professors.append({
            "name": name,
            "title": title,
            "email": email,
            "phoneNumber": phone_number
        })

        i += 1
    
    cast(dict[str, Any], find(lambda college: college["name"] == "Close School of Entrepreneurship-3145", drexel_json["colleges"]))["faculty"] = professors