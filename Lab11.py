import matplotlib.pyplot as plt

# Load data from files
def load_students(filepath):
    students = {}
    with open(filepath, 'r') as f:
        for line in f:
            student_id = line[:3]
            name = line[3:].strip()
            students[name] = student_id
    return students

def load_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        for i in range(0, len(lines), 3):
            name = lines[i]
            assignment_id = lines[i+1]
            points = int(lines[i+2])
            assignments[name] = {'id': assignment_id, 'points': points}
    return assignments

def load_submissions(filepath):
    submissions = {}
    with open(filepath, 'r') as f:
        for line in f:
            student_id, assignment_id, percent = line.strip().split('|')
            submissions[(student_id, assignment_id)] = float(percent)
    return submissions

# Helper functions
def calculate_student_grade(student_name, students, assignments, submissions):
    if student_name not in students:
        return None
    student_id = students[student_name]
    total_score = 0
    for name, info in assignments.items():
        assignment_id = info['id']
        points = info['points']
        percent = submissions.get((student_id, assignment_id), 0)
        total_score += (percent / 100) * points
    return round((total_score / 1000) * 100)

def get_assignment_scores(assignment_name, assignments, submissions):
    if assignment_name not in assignments:
        return None
    assignment_id = assignments[assignment_name]['id']
    scores = [percent for (sid, aid), percent in submissions.items() if aid == assignment_id]
    return {
        'min': round(min(scores)),
        'avg': round(sum(scores) / len(scores)),
        'max': round(max(scores)),
        'scores': scores
    }

def show_histogram(scores):
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.xlabel('Score Ranges')
    plt.ylabel('Number of Students')
    plt.title('Assignment Score Distribution')
    plt.show()

# Main menu
def main():
    students = load_students('data/students.txt')
    assignments = load_assignments('data/assignments.txt')
    submissions = load_submissions('data/6a1d33e0-174d-4ea4-bb39-7383974acc54.txt')

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("\nEnter your selection: ")

    if choice == '1':
        name = input("What is the student's name: ")
        grade = calculate_student_grade(name, students, assignments, submissions)
        if grade is None:
            print("Student not found")
        else:
            print(f"{grade}%")

    elif choice == '2':
        name = input("What is the assignment name: ")
        stats = get_assignment_scores(name, assignments, submissions)
        if stats is None:
            print("Assignment not found")
        else:
            print(f"Min: {stats['min']}%")
            print(f"Avg: {stats['avg']}%")
            print(f"Max: {stats['max']}%")

    elif choice == '3':
        name = input("What is the assignment name: ")
        stats = get_assignment_scores(name, assignments, submissions)
        if stats is None:
            print("Assignment not found")
        else:
            show_histogram(stats['scores'])

if __name__ == '__main__':
    main()
