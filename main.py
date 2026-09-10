import argparse
import json
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    marks: list[int]

parser = argparse.ArgumentParser()
parser.add_argument("--name")
parser.add_argument("--marks")
args = parser.parse_args()

marks_text = args.marks
marks_list = marks_text.split(",")
marks_numbers = [int(m) for m in marks_list]

try:
    student = Student(name=args.name, marks=marks_numbers)
    print("Sab theek hai!")
    print(student)
    result = {"name": student.name, "marks": student.marks}
    with open("result.json", "w") as f:
        json.dump(result, f)
    print("Result save ho gaya result.json mein!")
except Exception as e:
    print("Kuch galat data diya gaya:", e)