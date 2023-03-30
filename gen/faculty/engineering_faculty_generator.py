from utils import *
from typing import cast

def generate_engineering_faculty_data(drexel_json: dict[str, Any]) -> None:
    professors: list[Any] = []
    for page in range(22):
        page_html = html(f"https://drexel.edu/engineering/about/faculty-staff/?q&sortBy=relevance&sortOrder=asc&page={page + 1}")
        for section in page_html.find_all("section", class_="directory-result is-visible"):
            name = section.find("div", class_="directory-result__name").decode_contents().strip()
            title = section.find("div", class_="directory-result__title").decode_contents().strip()
            email = section.find("ul", class_="directory-result__contact-card").find("a").decode_contents().strip()
            phone = section.find("ul", class_="directory-result__contact-card").find_all("a")
            phone = phone[1].decode_contents().strip().replace(".", "-") if len(phone) > 1 else "unknown"
            
            professors.append({
                "name": name,
                "title": title,
                "email": email,
                "phone": phone
            })

    cast(dict[str, Any], find(lambda college: college["name"] == "College of Engineering", drexel_json["colleges"]))["faculty"] = professors