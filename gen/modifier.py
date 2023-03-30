from typing import Any

def modify(data: Any):
    for college in data["colleges"]:
        for major in college["majors"]:
            major["collegeName"] = college["name"]
