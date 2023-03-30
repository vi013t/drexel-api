from typing import Any

from faculty.as_faculty_generator import generate_as_faculty_data
from faculty.cci_faculty_generator import generate_cci_faculty_data
from faculty.westphal_faculty_generator import generate_westphal_faculty_data
from faculty.lebow_faculty_generator import generate_lebow_faculty_data
from faculty.engineering_faculty_generator import generate_engineering_faculty_data
from faculty.entrepreneurship_faculty_generator import generate_entrepreneurship_faculty_data

def generate_faculty_data(drexel_json: dict[str, list[Any]]) -> None:
    generate_as_faculty_data(drexel_json)
    generate_cci_faculty_data(drexel_json)
    generate_westphal_faculty_data(drexel_json)
    generate_lebow_faculty_data(drexel_json)
    generate_engineering_faculty_data(drexel_json)
    generate_entrepreneurship_faculty_data(drexel_json)