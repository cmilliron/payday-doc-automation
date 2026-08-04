import datetime
from pathlib import Path

def setup_weekly_report():
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
    folder_date_str = upcoming_friday.strftime('%Y-%m-%d')
    sunday_date_str = previous_sunday.strftime('%m/%d/%Y') # Using MM/DD/YYYY for content date
    sunday_for_file = previous_sunday.strftime('%Y-%m-%d')

    # 2. Define Folder and File Paths
    # The new folder will be created in the current working directory
    folder_path = Path(folder_date_str)
    cody_file_name = f"Cody Milliron - {sunday_for_file}.txt"
    logan_file_name = f"Logan Sheets - {sunday_for_file}.txt"
    cody_path = folder_path / cody_file_name
    logan_path = folder_path / logan_file_name

    # 3. Create the folder if it does not exist
    try:
        # parents=True allows creating intermediate directories (though not needed here)
        # exist_ok=True prevents an error if the directory already exists
        folder_path.mkdir(exist_ok=True)
        print(f"✅ Folder created/ensured: {folder_path.resolve()}")
    except Exception as e:
        print(f"❌ Error creating directory: {e}")
        return

    # 4. Define the content for the text file
    cody_report_content = f"""Cody Milliron - For Week Ending on {sunday_date_str}
Monday - 7.5
Tuesday - 7.5
Wednesday - 7.5
Thursday - 7.5
Friday - 0
Saturday - 0
Sunday - 0
"""
    logan_report_content = f"""Logan Sheets - For Week Ending on {sunday_date_str}
{(previous_sunday - datetime.timedelta(days=6)).strftime('%Y-%m-%d')} - Monday      - 0.0
{(previous_sunday - datetime.timedelta(days=5)).strftime('%Y-%m-%d')} - Tuesday     - 0.0
{(previous_sunday - datetime.timedelta(days=4)).strftime('%Y-%m-%d')} - Wednesday   - 0.0
{(previous_sunday - datetime.timedelta(days=3)).strftime('%Y-%m-%d')} - Thursday    - 0.0
{(previous_sunday - datetime.timedelta(days=2)).strftime('%Y-%m-%d')} - Friday      - 0.0
{(previous_sunday - datetime.timedelta(days=1)).strftime('%Y-%m-%d')} - Saturday    - 0.0
{previous_sunday.strftime('%Y-%m-%d')} - Sunday     - 0.0
Total
"""

    # 5. Write the content to the text file
    try:
        cody_path.write_text(cody_report_content)
        print(f"✅ Report file created: {cody_path.resolve()}")
        logan_path.write_text(logan_report_content)
        print(f"✅ Report file created: {logan_path.resolve()}")
        print("\n--- Summary ---")
        print(f"Upcoming Friday (Folder Name): {folder_date_str}")
        print(f"Previous Sunday (Report Date): {sunday_date_str}")
    except Exception as e:
        print(f"❌ Error writing file: {e}")

if __name__ == "__main__":
    setup_weekly_report()
