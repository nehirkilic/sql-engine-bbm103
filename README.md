# In-Memory SQL Engine – BBM103 PA3

*Fall 2024 ☕🍂*

This project was developed as part of the **BBM103 – Introduction to Programming Laboratory I** course at Hacettepe University.  
It implements a simplified **SQL interpreter and in-memory relational database engine**, written entirely in Python from scratch — without any external libraries or database backends.

The purpose of this assignment was to simulate core features of a real DBMS (Database Management System), by parsing and executing SQL-like commands provided via an input file.  
All logic, including table storage, filtering, joins, and error handling, is implemented manually using native Python data structures.

---

## 🪄  Key Concepts & Features

- **Custom SQL Parsing Engine**: manually tokenizes and interprets SQL-like statements
- **In-Memory Storage**: each table is modeled with Python lists and dictionaries
- **Relational Operations Supported**:
  - `CREATE_TABLE`, `INSERT`, `SELECT`, `UPDATE`, `DELETE`, `COUNT`, and `JOIN`
- **Single-Column INNER JOIN** support with clean output formatting
- **Exception-Safe Execution**: graceful error handling with `try-except` logic
- **No Global Variables**, PEP-8 compliant modular structure
- **Fully deterministic**: reproducible and tested across multiple datasets

---

## 💻 How to Run

> Requires Python **3.9.18**  
> No external dependencies

From the command line:
```bash
python3 database.py input.txt
```

---

## 📂 I/O Examples

You can find complete example files below:

- [`i1.txt`](./i1.txt) → [`out1.txt`](./out1.txt)
- [`i2.txt`](./i2.txt) → [`out2.txt`](./out2.txt)
- [`i3.txt`](./i3.txt) → [`out3.txt`](./out3.txt)


---

## 🧾 Sample Output
Below are representative snippets for each supported command.
Full outputs can be found in the linked files above.
### CREATE_TABLE
```
###################### CREATE #########################
Table 'students' created with columns: ['id', 'name', 'age', 'major']
#######################################################
```
### INSERT
```
###################### INSERT #########################
Inserted into 'students': ('1', 'John Doe', '20', 'CS')

Table: students
+----+----------+-----+-------+
| id | name     | age | major |
+----+----------+-----+-------+
| 1  | John Doe | 20  | CS    |
+----+----------+-----+-------+
#######################################################
```
### SELECT
```
###################### SELECT #########################
Condition: {'major': 'CS'}
Select result from 'students': [('1', 'John Doe'), ('3', 'Bob Wilson'), ('3', 'Ted Wilson')]
#######################################################
```
### UPDATE
```
###################### UPDATE #########################
Updated 'students' with {'major': 'SE'} where {'name': 'John Doe'}
1 rows updated.

Table: students
+----+------------+-----+-------+
| id | name       | age | major |
+----+------------+-----+-------+
| 1  | John Doe   | 20  | SE    |
| 2  | Jane Smith | 22  | EE    |
| 3  | Bob Wilson | 21  | CS    |
| 3  | Ted Wilson | 21  | CS    |
+----+------------+-----+-------+
#######################################################
```
### DELETE
```
###################### DELETE #########################
Deleted from 'students' where {'age': 22}
1 rows deleted.

Table: students
+----+------------+-----+-------+
| id | name       | age | major |
+----+------------+-----+-------+
| 1  | John Doe   | 20  | SE    |
| 3  | Bob Wilson | 21  | CS    |
| 3  | Ted Wilson | 21  | CS    |
+----+------------+-----+-------+
#######################################################
```
### COUNT
```
###################### COUNT #########################
Count: 2
Total number of entries in 'students' is 2
#######################################################
```
### JOIN
```
####################### JOIN ##########################
Join tables students and courses
Join result (5 rows):

Table: Joined Table
+----+----------------------+-----+-------+-----------+----------------------+
| id | name                 | age | major | course_id | name                 |
+----+----------------------+-----+-------+-----------+----------------------+
| 1  | Intro to Programming | 20  | CS    | 101       | Intro to Programming |
| 1  | Data Structures      | 20  | CS    | 103       | Data Structures      |
| 2  | Circuit Design       | 22  | EE    | 102       | Circuit Design       |
| 3  | Intro to Programming | 21  | CS    | 101       | Intro to Programming |
| 3  | Data Structures      | 21  | CS    | 103       | Data Structures      |
+----+----------------------+-----+-------+-----------+----------------------+
#######################################################
```
---
## ⭐ Notes

This was one of my most intellectually rewarding Python projects.

It allowed me to:
- simulate the **core logic of a real DBMS**, entirely from scratch  
- implement **manual SQL parsing and query execution** without any libraries  
- handle JOIN operations and WHERE conditions with native Python  
- apply robust exception handling and test against multiple input scenarios  
- write code that is modular, deterministic, and fully reproducible

Thanks to this project, I gained a deeper understanding of:
- how databases store and manipulate data internally  
- how SQL queries are interpreted and executed  
- the design of relational operators like SELECT, JOIN, and COUNT  

Overall, it helped me strengthen my problem-solving skills and get more comfortable with database internals using plain Python.
