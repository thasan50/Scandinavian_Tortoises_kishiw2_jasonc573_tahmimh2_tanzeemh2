# Scenario 1: Tater Tots by Swedish_Fish
## Roster:
* Kishi Wijaya (PM, Linking, CSS)
* Jason Chao (Account details, login, CSS)
* Tahmim Hassan (Database with edit permissions, user data and IDS)
* Tanzeem Hasan (Individual story data, edit status, votes, version history)
## Description of Project:
Tater Tots is a collaborative storytelling website. Prospective authors create accounts in order to begin a new story, or add an edit on top of an ongoing one. New edits on a story are voted on by other authors who have already contributed to the story (to prevent new authors from creating tons of alt accounts to vote for themselves). Edits with the most votes are accepted after a certain period of time or after obtaining a majority of votes. Authors can vote on possible edits multiple times. Stories are presented on the front page of the website, and can be sorted by latest edit or other tags. User IDS will be associated with information containing their previous edits across stories. After a user has successfully edited a story, their permission levels are changed from read and write to read and vote.
## Install guide:
### Prerequisites:
Must have Git and Python installed beforehand.
1. Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
2. Python: https://www.python.org/downloads/
3. Using Git: https://novillo-cs.github.io/apcsa/tools/
^Referenced Jobless_Monkeys for prerequisites

### Procedure:
1. Locate green <>Code button on main page of project repository
2. Copy the HTTPS URL
3. Open the terminal on your local machine and navigate to the desired directory
4. Clone the repository in the corresponding directory:
```
git clone https://github.com/thasan50/SwedishFish__kishiw2_jasonc573_tahmimh2_tanzeemh2.git
```
5. Setup a virtual environment
```
python3 -m venv <name>
```
6. Activate virtual environment
```
. <name>/bin/activate
```
7. cd into the repo, ```
cd SwedishFish__kishiw2_jasonc573_tahmimh2_tanzeemh2.git.```

8. Install required packages
```
pip install -r requirements.txt
```
## Launch codes:
1. Navigate to project directory
```cd stuff/SwedishFish__kishiw2_jasonc573_tahmimh2_tanzeemh2```
2. Run app
```python3 app.py```
3. Open firefox and go to the given link
```http://127.0.0.1:5000```
