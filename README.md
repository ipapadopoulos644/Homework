# Console Task Manager

A small command-line application for keeping a persistent to-do list. It can:

- add tasks;
- display all tasks with their completion status;
- mark tasks as completed;
- delete tasks;
- save the list between runs in `tasks.json`.

## Extra improvement

The application rejects empty task titles, including titles that contain only spaces.

## Requirements

- Python 3.8 or newer
- No third-party packages

## Installation and launch

Clone the repository, enter its directory, and run the application:

```bash
git clone <repository-url>
cd console-task-manager
python main.py
```

Depending on the operating system, the Python command may be `python3` instead:

```bash
python3 main.py
```

The application creates `tasks.json` automatically on its first run. This file is kept out of Git because it contains the local user's task data.

## Example

```text
1. Add a task
2. Show tasks
3. Complete a task
4. Delete a task
5. Exit

Choose an action: 1
Enter the task: Finish the homework
Task added.

Choose an action: 2
1. [ ] Finish the homework

Choose an action: 3
1. [ ] Finish the homework
Enter the task number: 1
Task completed.

Choose an action: 2
1. [x] Finish the homework
```

## Tests

Run the automated tests with:

```bash
python -m unittest -v
```

