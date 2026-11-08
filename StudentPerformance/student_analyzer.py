
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# 1. Load the dataset
def load_data(filename):

    try:
        df = pd.read_csv(filename)

        print("\nDataset loaded successfully!")

        return df

    except FileNotFoundError:
        print("CSV file not found!")
        return None


# 2. Analyse student performance
def analyse_students(df):

    subjects = [
        "Maths",
        "Physics",
        "Chemistry",
        "Computer_Science",
        "English"
    ]

    # Calculate total and average
    df["Total"] = df[subjects].sum(axis=1)

    df["Average"] = df[subjects].mean(axis=1).round(2)

    # Check pass or fail
    df["Result"] = np.where(
        (df[subjects] >= 35).all(axis=1),
        "Pass",
        "Fail"
    )

    # Assign grades
    conditions = [
        df["Average"] >= 90,
        df["Average"] >= 80,
        df["Average"] >= 70,
        df["Average"] >= 60,
        df["Average"] >= 50,
        df["Average"] >= 35
    ]

    grades = ["A+", "A", "B", "C", "D", "E"]

    df["Grade"] = np.select(
        conditions,
        grades,
        default="F"
    )

    return df


# 3. Display overall statistics
def display_statistics(df):

    subjects = [
        "Maths",
        "Physics",
        "Chemistry",
        "Computer_Science",
        "English"
    ]

    print("\n===== OVERALL STATISTICS =====")

    print("Total students:", len(df))

    print("Class average:", round(df["Average"].mean(), 2))

    print("Highest average:", df["Average"].max())

    print("Lowest average:", df["Average"].min())

    print("\n===== SUBJECT-WISE AVERAGES =====")

    print(df[subjects].mean().round(2))

    print("\n===== PASS / FAIL COUNT =====")

    print(df["Result"].value_counts())

    print("\n===== GRADE DISTRIBUTION =====")

    print(df["Grade"].value_counts())


# 4. Display top performers
def display_top_students(df):

    print("\n===== TOP 5 STUDENTS =====")

    top_students = df.sort_values(
        by="Average",
        ascending=False
    ).head(5)

    print(
        top_students[
            ["Student_ID", "Name", "Total", "Average", "Grade"]
        ].to_string(index=False)
    )


# 5. Create visualisations
def create_charts(df):

    subjects = [
        "Maths",
        "Physics",
        "Chemistry",
        "Computer_Science",
        "English"
    ]

    subject_averages = df[subjects].mean()

    # Chart 1: Subject-wise average
    plt.figure(figsize=(9, 5))

    subject_averages.plot(kind="bar")

    plt.title("Average Marks by Subject")
    plt.xlabel("Subjects")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=30)
    plt.tight_layout()

    plt.savefig("subject_averages.png")
    plt.show()

    # Chart 2: Grade distribution
    grade_counts = df["Grade"].value_counts()

    plt.figure(figsize=(7, 5))

    grade_counts.plot(kind="bar")

    plt.title("Student Grade Distribution")
    plt.xlabel("Grades")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.savefig("grade_distribution.png")
    plt.show()


# 6. Save analysed data
def save_results(df):

    df.to_csv(
        "student_analysis_results.csv",
        index=False
    )

    print("\nAnalysis saved to student_analysis_results.csv")


# 7. Main function
def main():

    print("===== STUDENT PERFORMANCE ANALYZER =====")

    df = load_data("students.csv")

    if df is None:
        return

    print("\n===== ORIGINAL DATASET =====")

    print(df.to_string(index=False))

    df = analyse_students(df)

    print("\n===== ANALYSED DATASET =====")

    print(df.to_string(index=False))

    display_statistics(df)

    display_top_students(df)

    create_charts(df)

    save_results(df)

    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
