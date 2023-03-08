# cs5293sp23-project0
Name : Rama Dinesh Kumar

OU ID : 113582682

### Project Description:
The objective of this project is to extract information regarding incidents in PDF format from a URL on the Norman Police Department website, and store it into an SQLite database. The PDF contains five columns which include Date/Time, Incident Number, Location, Nature, and Incident ORI. Our task is to extract all rows of incidents, separate the columns, and create a database and table to store the aforementioned five fields. Finally, we will display the list of incident natures and their frequency of occurrence.

![img.png](img.png)

How to install:
1. Create a new directory using the mkdir command followed by the name of the directory. Create a directory called cs5293sp23-project0, run the following command in the terminal: mkdir cs5293sp23-project0.
2. Navigate to the newly created directory using the cd command followed by the directory name. to change to the cs5293sp23-project0 directory, run the following command: cd cs5293sp23-project0.
3. Download project files from a git repository using the git clone command followed by the URL of the git repository. For example, to download a repository from GitHub, run the following command: git clone https://github.com/dk18234/cs5293sp23-project0.
4. Install pipenv using the pip command. To install pipenv globally, run the following command: pip install pipenv.
5. Install the required packages for your project by creating a Pipfile in the project directory with the required packages listed in it, and then running the pip install <packagename> command.

Execution: 
• To execute the main.py we have to the following command:
Pipenv run python3 project0/main.py –incidents <paste the url here>
• To run the py test cases:
 pipenv run python -m pytest

### Functions:

#### Function 1: Function Name: def download_pdf(url):

`def download_pdf(url):

"""Downloads a PDF file from a URL and returns the filename."""`

This is the function definition, it takes one parameter 'url', which is the URL of the PDF file we want to download. It also includes a docstring that briefly explains the function's purpose.

`now = datetime.now()
    filename = f"{now:%Y-%m-%d}_daily_incident_summary.pdf"`

Here, we use the 'datetime.now()' function to get the current date and time. We then format this date and time into a string with the desired format ("%Y-%m-%d" represents the year, month, and day). We append this string to the filename prefix 'daily_incident_summary' and add the '.pdf' extension to create the full filename for the downloaded PDF.

 `urllib.request.urlretrieve(url, filename)`
 
The 'urlretrieve' function from the 'urllib.request' module is called with the provided URL and filename as parameters. This function downloads the file from the URL and saves it to the specified filename on the local filesystem.

 `if os.path.exists(filename):
        print("File downloaded successfully.")
        return filename
    else:
        raise Exception("Error downloading file.")`
 
This checks whether the file was successfully downloaded by checking whether the file exists at the specified filename. If the file exists, it prints a success message to the console and returns the filename. If the file does not exist, it raises an exception with an error message.

Overall, this function takes a URL for a PDF file, downloads it, and returns the filename for the downloaded file. It also includes some error handling to ensure that the file was successfully downloaded before returning the filename.

#### Function 2 : def extract_info_from_pdf(filename):

`def extract_info_from_pdf(filename):`

"""Extracts incident information from a PDF file using regular expressions."""

This function takes a filename as input and returns a list of incident information extracted from the PDF file.

    with open(filename, "rb") as f:
This line opens the PDF file specified by the filename in binary mode for reading.

        p = PyPDF2.PdfReader(f)
This line creates a PyPDF2 PdfReader object from the opened file.

        info = []
This line initializes an empty list called info to store the extracted incident information.

        for page in p.pages:
This line starts a loop over all pages in the PDF file

            page_text = page.extract_text()
            if not page_text:
                continue
This line extracts the text from the current page using the extract_text() method of the PyPDF2 PageObject class. If the extracted text is empty, the loop continues to the next page.

            `lines = page_text.split("\n")
            for line in lines:`

This line splits the page text into lines based on the newline character and starts a loop over each line in the page.

                date_time_match = re.search(r"\d{1,2}/\d{1,2}/\d{4}\s\d{1,2}:\d{2}", line)
                if date_time_match:
                    date_time = date_time_match.group()
                    line = re.sub(date_time, "", line)

This line uses a regular expression to search for a date and time string in the current line. If a match is found, the matched string is stored in the date_time variable and removed from the current line using the re.sub() method. This step is necessary to prevent the date and time string from being included in the location information of the incident.

                incident_number_match = re.search(r"\d{4}-\d{8}", line)
                if incident_number_match:
                    incident_number = incident_number_match.group()
                    line = re.sub(incident_number, "", line)

This line uses another regular expression to search for an incident number string in the current line. If a match is found, the matched string is stored in the incident_number variable and removed from the current line using the re.sub() method.

                nature_match = re.search(r"[A-Z][a-z]+(?:[/ ][A-Za-z]+\s)?", line)
                if nature_match:
                    nature = nature_match.group().strip()
                    line = re.sub(nature, "", line)

This line uses a regular expression to search for a nature string in the current line. If a match is found, the matched string is stored in the nature variable and removed from the current line using the re.sub() method.

                words = line.split()
                if len(words) > 1:
                    ori = words[-1]
                    location = "".join(words[:-1])
                    info.append({
                        "date_time": date_time if date_time_match else "",
                        "incident_number": incident_number if incident_number_match else "",
                        "nature": nature if nature_match else "",
                        "location": location,
                        "origin": ori
                    })

This block of code splits the remaining line of text into words, extracts the last word as the origin of the incident, and concatenates the remaining words as the location of the incident. 


### Database Development:  def insert_info_to_db(info):

This function insert_info_to_db takes a list of dictionaries (called info) and performs the following tasks:

1. Connect to an SQLite database file named "incidents.db" using the sqlite3 module.
2. Drop the table named "incidents" if it already exists.
3. Create a new table named "incidents" with five columns: "date_time", "incident_number", "nature", "location", and "origin". All columns have data type "text".
4. Loop over each dictionary in info, and insert the corresponding data into the "incidents" table using an SQL INSERT statement.
5. Commit the changes to the database.
6. Execute an SQL query that groups the incidents by "nature", counts the number of occurrences for each "nature", and sorts the results in descending order by the count.
7. Print the results of the query to the console in the format "nature | count".

Overall, this function inserts the incident data stored in info into an SQLite database, and then prints a summary of the nature of the incidents and their frequency.

`def insert_info_to_db(info):
    print('Connected')`

This line just prints a message indicating that the function has successfully connected to the database.

    conn = sqlite3.connect('incidents.db')
    cursor = conn.cursor()

These two lines establish a connection to the SQLite database using the connect() method of the sqlite3 module. The connection object conn is then used to create a cursor object cursor, which is used to execute SQL statements on the database.

    cursor.execute('drop table if exists incidents')

This line drops the "incidents" table if it already exists in the database. The if exists clause ensures that the statement does not throw an error if the table doesn't exist

    cursor.execute('''CREATE TABLE incidents
                 (date_time text, incident_number text, nature text, location text, origin text)''')

This line creates a new table named "incidents" with five columns: "date_time", "incident_number", "nature", "location", and "origin". All columns have data type "text"

    for incident in info:
        cursor.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)",(incident['date_time'], incident['incident_number'], incident['nature'], incident['location'], incident['origin']))

This for loop iterates over each dictionary in the info list and inserts its values into the "incidents" table using an SQL INSERT statement. The question marks in the SQL statement are placeholders for the values passed in as a tuple in the second argument of cursor.execute().

    conn.commit()

This line commits the changes made to the database by the INSERT statements.

    cursor.execute('SELECT nature, COUNT() FROM incidents GROUP BY nature ORDER BY COUNT() DESC')
    results = cursor.fetchall()
    for row in results:
        print(row[0], "|", row[1])

This section of the code executes an SQL query that groups the incidents by "nature", counts the number of occurrences for each "nature", and sorts the results in descending order by the count. The results of the query are fetched using cursor.fetchall(), and then printed to the console in the format "nature | count".

Overall, this function connects to an SQLite database, creates a new table, inserts data into it, commits the changes, and then prints a summary of the nature of the incidents and their frequency.


### Assumptions:
1. The PDF file contains incident information in a specific format, including a date and time, incident number, nature of the incident, location, and origin.
2. The regular expressions used to extract the incident information from the PDF file are correct and will capture all relevant information.
3. The incident summary PDF file will be available at the given URL
4. The script will be run on a system with the necessary dependencies installed, including PyPDF2 and SQLite.

### Bugs:
1. The script does not handle exceptions that may occur during the database insertion process, which could result in incomplete or incorrect data being inserted into the database. It would be better to catch these exceptions and handle them appropriately (e.g., by rolling back the transaction or printing an error message)
2. The script assumes that the location field of the incident information is always a single word, but this may not be the case in all situations. A more robust approach would be to split the location field based on a specific delimiter.
3. If the database already contains incident information, the script will drop the incidents table and create a new one, potentially deleting any existing data in the table. A better approach would be to add a check to see if the table already exists and only drop/create the table if necessary.
4. The code assumes that the PDF file will always contain valid incident information in the expected format, but if the PDF file is empty or contains corrupted data, the script may encounter errors or insert incorrect information into the database.




