import datetime, sys
from pathlib import Path
from config import output_folder, employees, cody_default_hours


def get_hours_by_employee(employee: str, prev_sunday: datetime.date):
    """
    Gets the number of hours the employee works each day. 
    It returns an array of hours with index 0 = Monday
    """
    print(f"Please enter your time for {employee}")
    work_week = []
    for i in range(1, 8):
        day = prev_sunday - datetime.timedelta(days=(7-i))
        current_day = f"{day.strftime('%Y-%m-%d')} - {day.strftime("%A")}: "
        hours = input(current_day)
        work_week.append(float(hours))
    return work_week

def create_folder(dest_folder: Path):
    try:
        # parents=True allows creating intermediate directories (though not needed here)
        # exist_ok=True prevents an error if the directory already exists
        dest_folder.mkdir(exist_ok=True)
        print(f"✅ Folder created/ensured: {dest_folder.resolve()}")
    except Exception as e:
        sys.exit(f"❌ Error creating directory: {e}")


def write_file(employee: str, prev_sunday: str, paydate: str, content: str) -> None:
    file_name = f"{employee} - {prev_sunday}.txt"
    subfolder = Path(paydate)
    dest_path = Path(output_folder) / subfolder
    dest_file = dest_path / file_name
    create_folder(dest_path)
    dest_file.write_text(content)
    print(f"✅ Report file created: {dest_file.resolve()}")


def process_workweek(work_week, employee, prev_sunday) -> str:
    output = f"{employee} - For Week Ending on {prev_sunday.strftime('%m/%d/%Y')}\n\n"
    total = 0
    for ind, hours in enumerate(work_week, 1):
        day = prev_sunday - datetime.timedelta(days=(7-ind))
        current_day = f"{day.strftime('%Y-%m-%d')} - {day.strftime("%A") + ":":15} {hours:>4.2f}\n"
        total += hours
        output += current_day
    output += f"{"Work Week totals:":28} {total:>5.2f}"
    return output



def process_payroll():
    """
    Calculates the date of the upcoming Friday and the previous Sunday,
    creates a folder named after the Friday date, and creates a text file
    inside it with the weekly report template, dated for the previous Sunday.
    """
    # 1. Calculate the necessary dates
    today = datetime.date.today()

    # Calculate Upcoming Friday's Date (4 represents Friday's weekday index)
    # The formula ensures we get the next Friday, or today if today is Friday.
    days_to_friday = (4 - today.weekday() + 7) % 7
    upcoming_friday = today + datetime.timedelta(days=days_to_friday)

    # Calculate Previous Sunday's Date (Sunday's index is 6, or -1 relative to today's week start)
    # The formula ensures we get the most recent Sunday (0 days ago if today is Sunday, 1 if Monday, etc.)
    days_since_sunday = (today.weekday() + 1) % 7
    previous_sunday = today - datetime.timedelta(days=days_since_sunday)

    # Format the dates for use in paths and content
    paydate_formated = upcoming_friday.strftime('%Y-%m-%d')
    sunday_date_str = previous_sunday.strftime('%m/%d/%Y') # Using MM/DD/YYYY for content date
    prev_sunday_string = previous_sunday.strftime('%Y-%m-%d')

    for employee in employees:
        hours = []
        if employee == "Cody Milliron":
            hours = cody_default_hours
        else:
            hours = get_hours_by_employee(employee=employee, prev_sunday=previous_sunday)
        content = process_workweek(hours, employee, previous_sunday)
        write_file(employee, prev_sunday_string, paydate_formated, content)

    done = False
    while (not done):
        cont = input("Do you have any more employees to add (yes/no): ")
        if cont.lower() == "n" or cont.lower() == "no":
            done = True
            continue
        employee = input("What is the name of the employee: ")
        hours = get_hours_by_employee(employee=employee, prev_sunday=previous_sunday)
        content = process_workweek(hours, employee, previous_sunday)
        write_file(employee, prev_sunday_string, paydate_formated, content)

    print("--Done--")
