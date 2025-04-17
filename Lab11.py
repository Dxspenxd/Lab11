import matplotlib.pyplot as plt
import os

# File paths
STUDENTS_FILE = "data/students.txt"
ASSIGNMENTS_FILE = "data/assignments.txt"
SUBMISSIONS_FILE = "data/submissions.txt"

# Load data
def load_students():
    students = {}
    try:
        with open(STUDENTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                student_id = parts[0]
                name = " ".join(parts[1:])
                students[name] = student_id
    except FileNotFoundError:
        print(f"Error: {STUDENTS_FILE} not found. Please ensure the file exists in the 'data' directory.")
        return {}
    return students

def load_assignments():
    assignments = {}
    id_to_name = {}
    try:
        with open(ASSIGNMENTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 3:
                    continue  # skip lines that are too short
                assignment_id = parts[0]
                try:
                    point_value = int(parts[1])
                except ValueError:
                    continue  # skip lines where point value isn't a number
                name = " ".join(parts[2:])
                assignments[name] = (assignment_id, point_value)
                id_to_name[assignment_id] = name
    except FileNotFoundError:
        print(f"Error: {ASSIGNMENTS_FILE} not found. Please ensure the file exists in the 'data' directory.")
        return {}, {}
    return assignments, id_to_name

def load_submissions():
    submissions = []
    try:
        with open(SUBMISSIONS_FILE, "r") as f:
            for line in f:
                student_id, assignment_id, percent = line.strip().split()
                submissions.append((student_id, assignment_id, float(percent)))
    except FileNotFoundError:
        print(f"Error: {SUBMISSIONS_FILE} not found. Please ensure the file exists in the 'data' directory.")
        return []
    return submissions

# Menu functions
def student_grade(student_name, students, assignments, submissions):
    if student_name not in students:
        print("Student not found")
        return
    student_id = students[student_name]
    total_earned = 0
    for aid, (assign_id, point_val) in assignments.items():
        for sub in submissions:
            if sub[0] == student_id and sub[1] == assign_id:
                earned = (sub[2] / 100) * point_val
                total_earned += earned
                break
    percent = round((total_earned / 1000) * 100)
    print(f"{percent}%")

def assignment_stats(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assign_id, _ = assignments[assignment_name]
    scores = [sub[2] for sub in submissions if sub[1] == assign_id]
    if not scores:
        print("No submissions found.")
        return
    print(f"Min: {int(min(scores))}%")
    print(f"Avg: {int(sum(scores)/len(scores))}%")
    print(f"Max: {int(max(scores))}%")

def assignment_graph(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        print("Assignment not found")
        return
    assign_id, _ = assignments[assignment_name]
    scores = [sub[2] for sub in submissions if sub[1] == assign_id]
    if not scores:
        print("No submissions found.")
        return
    plt.hist(scores, bins=[0, 25, 50, 75, 100], edgecolor='black')
    plt.title(f"Score Distribution: {assignment_name}")
    plt.xlabel("Percentage")
    plt.ylabel("Number of Students")
    plt.show()

# Main program
def main():
    print("Current working directory:", os.getcwd())  # Debug: Show working directory
    students = load_students()
    assignments, id_to_name = load_assignments()
    submissions = load_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("\nEnter your selection: ")

    if choice == "1":
        name = input("What is the student's name: ")
        student_grade(name, students, assignments, submissions)
    elif choice == "2":
        name = input("What is the assignment name: ")
        assignment_stats(name, assignments, submissions)
    elif choice == "3":
        name = input("What is the assignment name: ")
        assignment_graph(name, assignments, submissions)

if __name__ == "__main__":
    main()