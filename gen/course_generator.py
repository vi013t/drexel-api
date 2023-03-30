from utils import *
import re as regex
from typing import cast, TypedDict

class Token(TypedDict):
    type: str
    value: str

def tokenize_prereqs(prereq_string: str) -> list[Token] | list[str]:
    prereq_string = regex.sub(r"([A-Z])\s(\d+)", r"\1-\2", prereq_string)
    token_types = {
        "class": r"^[A-Z]+\-\d+",
        "whitespace": r"^\s+",
        "grade": r"^\[Min Grade: (.+?)\]",
        "and": r"^and\b",
        "or": r"^or\b",
        "left parentheses": r"^\(",
        "right parentheses": r"^\)"
    }
    tokens: list[Token] = []
    remaining_string = prereq_string
    while(remaining_string):
        match_found = False
        for type_, regexp in token_types.items():
            match = regex.match(regexp, remaining_string)
            if match:
                if type_ == "grade": tokens.append({ "type": type_, "value": match.group(1) })
                elif type_ != "whitespace": tokens.append({ "type": type_, "value": match.group(0) })
                remaining_string = remaining_string[len(match.group(0)):]
                match_found = True
                break
        if not match_found: return [remaining_string]
    
    return tokens

# Somehow every project I do ends up with me writing a parser
def parse_prereqs(prereq_string: str) -> list[Any]:
    """Parses a string of prerequisites into a prerequisite array object."""
    

    # Tokenize 
    tokens = tokenize_prereqs(prereq_string)
    if type(tokens[0]) is str: return tokens
    tokens = cast(list[Token], tokens)
    tokens_to_parse = tokens.copy()


    def next(type_: str | None) -> Any:
        """
        Removes and returns the next token.
        
        ### Parameters
        - `type` &mdash; The type of token that should be next. If the type is incorrect an error is raised.
        ### Returns
        The removed token.
        """
        if len(tokens_to_parse) == 0: return False
        if type_ and tokens_to_parse[0]["type"] != type_: raise Exception("Expected type " + type_ + " but found " + tokens_to_parse[0]['type'] + " in\n" + "\n".join(map(lambda token : str(token), tokens)))
        return tokens_to_parse.pop(0)


    def next_is(type_: str) -> bool:
        """Returns whether or not the next token is of the specified type."""
        return tokens_to_parse[0]["type"] == type_ if len(tokens_to_parse) > 0 else False


    def parse_and_or(left: dict[str, Any]) -> dict[str, Any]:
        """Parses an "and" or "or" expression. """
        while next_is("and"):
            next("and")
            expr = parse_expr()
            if type(expr) is list and type(left) is list: left = cast(Any, [*cast(list[Any], left), *cast(list[Any], expr)])
            elif type(expr) is list: left = cast(Any, [left, *cast(list[Any], expr)])
            elif type(left) is list: left = cast(Any, [*cast(list[Any], left), expr])
            else: left = cast(Any, [left, expr])
        while next_is("or"):
            next("or")
            expr = parse_expr()
            if "oneOf" in expr: left = { "oneOf": [left, *cast(list[Any], expr.get("oneOf"))] }
            else: left = { "oneOf": [left, expr] }
        return left


    def parse_expr() -> dict[str, Any]:
        """Parses an expression."""
        if next_is("left parentheses"):
            next("left parentheses")
            expr = parse_expr()
            next("right parentheses")
            if (next_is("and") or next_is("or")): return parse_and_or(expr)
            return expr
        if next_is("class"):
            course_name = cast(dict[str, Any], next("class"))["value"]
            grade = "Any"
            if next_is("grade"): grade = cast(dict[str, Any], next("grade"))["value"]
            return parse_and_or({
                "codeName": course_name,
                "minimumGrade": grade
            })
        raise Exception("Unexpected token: " + str(tokens_to_parse[0]))


    # Parse the prerequisites
    prerequisites: list[Any] = []
    while next_is("or") or next_is("and"): next(None)
    while(tokens_to_parse): prerequisites.append(parse_expr())

    # Return the parsed prerequisites
    if len(prerequisites) == 1 and type(prerequisites[0]) is list: return cast(list[Any], prerequisites[0])
    return prerequisites


def generate_course_data(drexel_json: dict[str, Any]) -> None:
    ugSoup = html("https://catalog.drexel.edu/coursedescriptions/quarter/undergrad")
    for element in ugSoup.find_all("a"):
        text_contents = element.decode_contents()
        if "(" in text_contents and ")" in text_contents:
            href = element.get("href")
            major_soup = html("https://catalog.drexel.edu" + href)
            major_name = text_contents[:text_contents.index("(") - 1].replace("&amp;", "&")
            print("Getting stats for " + major_name)
    
            for course_block in major_soup.find_all("div", class_="courseblock"):
                
                # Proper name + Code name
                title = course_block.find_all("span", class_="cdspacing")
    
                # Code name
                code = regex.sub(r"[^\w]", "-", title[0].decode_contents()[:-2])
    
                # Proper name
                name = title[1].decode_contents().replace("&amp;", "&")
    
                # Credits
                credits = title[2].previous_sibling.strip()
                if "-" in credits: credits = credits[credits.index("-") + 1:].strip()
                credits = int(float(credits))
    
                # Prequisites
                prereqs = course_block.find_all("b")[-1]
                prereq_list = []
                if prereqs and not "credit" in prereqs.next_sibling: prereq_list = parse_prereqs(prereqs.next_sibling.strip())
    
                # College 
                college = course_block.find("b").next_sibling.strip()
    
                # Get college object
                college_object = cast(dict[str, Any], find(lambda x: x.get("name") == college, cast(list[Any], drexel_json["colleges"])))
                if not college_object:  
                    college_object: dict[str, Any] = { "name": college, "majors": [] }
                    cast(list[Any], drexel_json["colleges"]).append(college_object)
    
                # Get major object
                major_object = cast(dict[str, Any], find(lambda major: major["name"] == major_name, college_object["majors"]))
                if not major_object:
                    major_object: dict[str, Any] = { "name": major_name, "courses": [] }
                    college_object["majors"].append(major_object)
    
                # Get class Object
                class_object = {
                    "codeName": code,
                    "properName": name,
                    "credits": credits,
                    "majorName": major_name,
                    "prerequisites": prereq_list if prereq_list else []
                }
                cast(list[Any], major_object["courses"]).append(class_object)
