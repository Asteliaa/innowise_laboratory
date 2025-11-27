"""The Student Grade Analyzer"""


from __future__ import annotations


from typing import Optional, TypedDict


class Student(TypedDict):
    """A student record stored in the `students` list."""

    name: str
    grades: list[int]


def find_student(
    students: list[Student], name: str
) -> Optional[Student]:
    """Search for a student in the list by their name.

    The search is case-insensitive and ignores leading/trailing spaces.

    Args:
        students: The collection of student records.
        name: The student's name to look up.

    Returns:
        The student record if found, otherwise None.
    """
    normalized = name.strip().lower()
    return next(
        (s for s in students if s["name"].lower() == normalized), None
    )


def add_new_student(students: list[Student]) -> None:
    """Create and store a new student in the system.

    Ensures the name is valid and not already registered in the list.
    """
    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    if find_student(students, name) is not None:
        print(f"Student '{name}' already exists.")
        return

    students.append({"name": name, "grades": []})
    print(f"Student '{name}' added.")


def add_grades_for_student(students: list[Student]) -> None:
    """Record academic performance scores for a specific student.

    Accepts multiple grades in the range [0, 100].
    User enters 'done' to finish input.
    Validates all entries and shows how many grades were added.
    """
    if not students:
        print("No students found. Please add a student first.")
        return

    name = input("Enter student name: ").strip()
    student = find_student(students, name)

    if student is None:
        print(f"Student '{name}' not found.")
        return

    initial_count = len(student["grades"])

    while True:
        grade_str = input("Enter a grade (or 'done' to finish): ").strip()

        if grade_str.lower() == "done":
            break

        try:
            grade = int(grade_str)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if not 0 <= grade <= 100:
            print("Invalid grade. Please enter a value between 0 and 100.")
            continue

        student["grades"].append(grade)

    grades_added = len(student["grades"]) - initial_count
    print(
        f"Grades updated for '{student['name']}'. "
        f"({grades_added} grade(s) added)"
    )


def show_report(students: list[Student]) -> None:
    """Display a comprehensive summary of all students' performance.

    Shows individual averages for each student and overall statistics.
    Handles cases where students have no grades recorded.
    """
    if not students:
        print("No students to report.")
        return

    print("\n--- Student Report ---")
    averages: list[float] = []

    for student in students:
        grades = student["grades"]

        try:
            student_sum = sum(grades)
            avg = student_sum / len(grades)
        except ZeroDivisionError:
            avg = None

        if avg is None:
            print(f"{student['name']}'s average grade is N/A.")
        else:
            print(f"{student['name']}'s average grade is {avg:.1f}.")
            averages.append(avg)

    # Exit early if no valid grade data exists.
    if not averages:
        print("No grades have been added yet.")
        print("------------------------\n")
        return

    max_avg = max(averages)
    min_avg = min(averages)
    overall_avg = sum(averages) / len(averages)

    print("------------------------")
    print(f"Max Average: {max_avg:.1f}")
    print(f"Min Average: {min_avg:.1f}")
    print(f"Overall Average: {overall_avg:.1f}")
    print("------------------------\n")


def find_top_performer(students: list[Student]) -> None:
    """Identify the student with the best academic performance.

    Compares all students' average grades and displays the top achiever.
    Requires at least one student with recorded grades.
    """
    if not students:
        print("No students found.")
        return

    students_with_grades = [s for s in students if s["grades"]]

    if not students_with_grades:
        print("No grades available to determine top performer.")
        return

    top_student = max(
        students_with_grades,
        key=lambda s: sum(s["grades"]) / len(s["grades"]),
    )
    top_avg = sum(top_student["grades"]) / len(top_student["grades"])

    print(
        f"The student with the highest average is {top_student['name']} "
        f"with a grade of {top_avg:.1f}."
    )


def print_menu() -> None:
    """Output the main menu with all available operations."""
    print("\n--- Student Grade Analyzer ---")
    print("1. Add a new student")
    print("2. Add grades for a student")
    print("3. Generate a full report")
    print("4. Find the top student")
    print("5. Exit program")


def main() -> None:
    """Execute the main application loop.

    Continuously displays the menu and processes user selections
    until the user chooses to exit.
    """
    students: list[Student] = []

    try:
        while True:
            print_menu()
            choice_str = input("Enter your choice: ").strip()

            try:
                choice = int(choice_str)
            except ValueError:
                print("Invalid choice. Please enter a number from 1 to 5.")
                continue

            if choice == 1:
                add_new_student(students)
            elif choice == 2:
                add_grades_for_student(students)
            elif choice == 3:
                show_report(students)
            elif choice == 4:
                find_top_performer(students)
            elif choice == 5:
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Please select a number from 1 to 5.")

    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C) gracefully.
        print("\nExiting program.")


if __name__ == "__main__":
    main()
