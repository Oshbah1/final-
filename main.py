from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import re


@dataclass
class Exam:
    """Represents an exam with all required information"""
    course_id: str  # Format: ABC-123-456
    location: int  # Room number
    date: datetime
    num_students: int


class ExamBookingSystem:
    """
    Exam Booking System using BST for location-based searches
    Requirement [1]: Efficient location range queries
    """

    class Node:
        def __init__(self, exam: Exam):
            self.exam = exam
            self.left = None
            self.right = None
            self.location = exam.location

    def __init__(self):
        """Initialize empty exam booking system"""
        self.root = None
        self.size = 0

    def validate_exam_data(self, exam: Exam) -> bool:
        """Validate exam data before insertion"""
        # Validate course ID format (ABC-123-456)
        if not re.match(r'^[A-Z]{3}-\d{3}-\d{3}$', exam.course_id):
            raise ValueError(f"Invalid course ID format: {exam.course_id}")

        # Validate location
        if not isinstance(exam.location, int) or exam.location <= 0:
            raise ValueError(f"Invalid location: {exam.location}")

        # Validate date
        if not isinstance(exam.date, datetime):
            raise ValueError("Invalid date format")

        # Validate number of students
        if not isinstance(exam.num_students, int) or exam.num_students <= 0:
            raise ValueError(f"Invalid number of students: {exam.num_students}")

        return True

    def book_exam(self, exam: Exam) -> bool:
        """
        Book a new exam (insert into the system)
        Returns True if booked successfully, False if location already occupied
        """
        # Validate exam data
        self.validate_exam_data(exam)

        # Check if location is available for the date
        existing_exam = self.find_exam_by_location_and_date(exam.location, exam.date)
        if existing_exam:
            raise ValueError(f"Room {exam.location} is already booked for {exam.date}")

        # Insert into BST
        if not self.root:
            self.root = self.Node(exam)
            self.size += 1
            return True

        return self._insert_recursive(self.root, exam)

    def _insert_recursive(self, node: Node, exam: Exam) -> bool:
        """Helper method for recursive insertion"""
        if exam.location == node.location:
            return False

        if exam.location < node.location:
            if node.left is None:
                node.left = self.Node(exam)
                self.size += 1
                return True
            return self._insert_recursive(node.left, exam)
        else:
            if node.right is None:
                node.right = self.Node(exam)
                self.size += 1
                return True
            return self._insert_recursive(node.right, exam)

    def find_exams_in_range(self, start_loc: int, end_loc: int) -> List[Exam]:
        """Find all exams with locations in the given range [start_loc, end_loc]"""
        if not (isinstance(start_loc, int) and isinstance(end_loc, int)):
            raise ValueError("Location range must be integers")
        if start_loc > end_loc:
            raise ValueError("Start location must be less than or equal to end location")

        result = []
        self._find_in_range_recursive(self.root, start_loc, end_loc, result)
        return sorted(result, key=lambda x: x.location)

    def _find_in_range_recursive(self, node: Optional[Node], start_loc: int,
                                 end_loc: int, result: List[Exam]) -> None:
        """Helper method for recursive range search"""
        if not node:
            return

        if start_loc <= node.location <= end_loc:
            result.append(node.exam)

        if start_loc < node.location:
            self._find_in_range_recursive(node.left, start_loc, end_loc, result)

        if end_loc > node.location:
            self._find_in_range_recursive(node.right, start_loc, end_loc, result)

    def find_exam_by_location_and_date(self, location: int, date: datetime) -> Optional[Exam]:
        """Helper method to find if an exam exists at a location on a specific date"""
        current = self.root
        while current:
            if location == current.location:
                if current.exam.date.date() == date.date():
                    return current.exam
                return None
            elif location < current.location:
                current = current.left
            else:
                current = current.right
        return None


def run_tests():
    """Comprehensive test cases for the exam booking system"""
    system = ExamBookingSystem()

    # Test Case 1: Basic Booking Operations
    print("Test Case 1: Basic Booking Operations")
    test_exams = [
        Exam("CSE-101-456", 50, datetime(2024, 12, 1, 9, 0), 30),
        Exam("MAT-202-789", 45, datetime(2024, 12, 1, 14, 0), 25),
        Exam("PHY-303-123", 60, datetime(2024, 12, 2, 9, 0), 35),
        Exam("CHE-404-234", 42, datetime(2024, 12, 2, 14, 0), 28),
        Exam("BIO-505-345", 55, datetime(2024, 12, 3, 9, 0), 32)
    ]

    for exam in test_exams:
        try:
            success = system.book_exam(exam)
            print(f"\nBooked exam:")
            print(f"Course: {exam.course_id}")
            print(f"Location: Room {exam.location}")
            print(f"Date: {exam.date}")
            print(f"Students: {exam.num_students}")
        except ValueError as e:
            print(f"Failed to book exam: {e}")

    # Test Case 2: Room Range Search
    print("\nTest Case 2: Room Range Search")
    print("Searching for exams in rooms 40-52:")
    range_results = system.find_exams_in_range(40, 52)
    for exam in range_results:
        print(f"\nRoom {exam.location}:")
        print(f"Course: {exam.course_id}")
        print(f"Date: {exam.date}")
        print(f"Students: {exam.num_students}")

    # Test Case 3: Validation and Error Handling
    print("\nTest Case 3: Validation and Error Handling")

    # Invalid course ID format
    try:
        invalid_exam = Exam("CSE-1-1", 70, datetime(2024, 12, 4, 9, 0), 30)
        system.book_exam(invalid_exam)
    except ValueError as e:
        print(f"Caught invalid course ID: {e}")

    # Duplicate booking attempt
    try:
        duplicate_exam = Exam("ENG-606-567", 50, datetime(2024, 12, 1, 9, 0), 40)
        system.book_exam(duplicate_exam)
    except ValueError as e:
        print(f"Caught duplicate booking: {e}")

    # Invalid number of students
    try:
        invalid_students = Exam("ENG-606-567", 75, datetime(2024, 12, 4, 9, 0), -5)
        system.book_exam(invalid_students)
    except ValueError as e:
        print(f"Caught invalid student count: {e}")


if __name__ == "__main__":
    run_tests()