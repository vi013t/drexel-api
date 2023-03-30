import sys
sys.dont_write_bytecode = True

import re as regex
import json

from utils import *
from faculty_generator import *
from course_generator import *
from organization_generator import *
from modifier import *

drexel_json: dict[str, list[Any]] = { "colleges": [] }
generate_course_data(drexel_json)
generate_organization_data(drexel_json)
generate_faculty_data(drexel_json)
modify(drexel_json)

json_data = regex.sub(r"\\u\d+", "'", json.dumps(drexel_json, indent=4))

print("Data generation complete. Writing to file...")
open("src/data/drexel.json", "w").write(json_data)
print("Data written.")