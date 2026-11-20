# Set up your Windows laptop

This guide sets up a Windows 11 laptop for the whole course.
Everything runs on Windows, and **Git Bash is your terminal**, inside VS Code.
Do Part 1 in week 1 and Part 2 in week 2. After each step, run its check before you go on.

The versions the course uses are in [`VERSIONS.md`](../VERSIONS.md).

## Before you start

- **Windows 11, version 23H2 or newer.** Press Windows+R, type `winver` and press Enter to see your version. Docker Desktop needs 23H2 or newer.
- **At least 8 GB of memory** (16 GB is better) and **25 GB of free disk space**. The course's container images and data need the space.
- **Virtualisation turned on.** Open Task Manager, select Performance, then CPU. It must say `Virtualization: Enabled`. If it says Disabled, ask your mentor to turn on Intel VT-x or AMD SVM in the laptop's BIOS.
- **An administrator account** on the laptop, because the installers change system settings.
- Keep the charger plugged in. If your laptop does not run Windows, ask your mentor for the matching steps.

## Where each tool lives

| Tool | Where it runs | When you install it |
|---|---|---|
| Git and Git Bash | Windows | Week 1 |
| VS Code | Windows | Week 1 |
| uv and Python 3.12 | Windows | Week 1 |
| The course kit | Windows, in your home folder: `~/de-kit` | Week 2 |
| WSL 2 (a Linux system inside Windows) | Windows; Docker Desktop runs on it | Week 2 |
| Docker Desktop | Windows, with the WSL 2 engine | Week 2 |
| PostgreSQL, the S3 emulator, Airflow, Spark, Kafka | Docker containers from the kit's data lab, never installed on Windows | From the map weeks |
| AWS CLI | Windows | P5, from [`datalab/storage/README.md`](../datalab/storage/README.md) |
| k3d and kubectl | Windows | P4, from [`datalab/k3d/README.md`](../datalab/k3d/README.md) |
| Cloud command-line tools (Snowflake, Azure, Google Cloud) and Terraform | Windows | The cloud weeks, from the kit's `cloud/` guides |
| Power BI Desktop | Windows, from the Microsoft Store | P14 |

Run every course command in **Git Bash**, unless a step says PowerShell.

## Part 1, week 1: Git, VS Code, uv and Python

### Step 1: Git for Windows

You installed Git in week 1, from https://git-scm.com/downloads/win with the default options. Those options include Git Bash and Git Credential Manager (for signing in to GitHub).

Check it in Git Bash:

```bash
git --version
```

You see `git version 2.` and more numbers. Any version from 2.45 is fine.

### Step 2: VS Code and its Python extension

1. Install VS Code from https://code.visualstudio.com/download with the default options.
2. Open VS Code, select **Extensions** (Ctrl+Shift+X), search for **Python** and install the extension from Microsoft.

Check it in Git Bash: `code --version` prints a version number.

### Step 3: Make Git Bash the terminal in VS Code

1. In VS Code, press Ctrl+Shift+P and type `Terminal: Select Default Profile`.
2. Choose **Git Bash**.

This is the same as the setting `"terminal.integrated.defaultProfile.windows": "Git Bash"`.

Check it: open a new terminal with Ctrl+`. The prompt shows `MINGW64`, and `uname -s` prints a line that starts with `MINGW64`.

### Step 4: Line endings

Windows ends each line of a text file with two characters (CRLF), and Linux ends it with one (LF).
Linux containers need LF: a script saved with CRLF fails inside a container with errors such as `$'\r': command not found`.

1. In VS Code, open **Settings** (Ctrl+,) and search for `eol`.
2. Set **Files: Eol** to `\n`. This is the setting `"files.eol": "\n"`.

Check it: open a new file. The status bar at the bottom right shows `LF`, not `CRLF`.
Your course repository's `.gitattributes` file keeps Git on LF as well.

### Step 5: uv and Python 3.12

uv installs Python and runs your programs. Run this in **PowerShell**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close every terminal and VS Code, then open Git Bash again and run:

```bash
uv --version
uv python install 3.12
uv python pin --global 3.12
```

The last command makes Python 3.12 uv's default everywhere on your laptop. Without it, uv picks its newest Python, which the course does not use and which Windows may block (see Step 12).

Check it:

```bash
uv run --no-project python --version
```

You see `Python 3.12.` and more numbers. uv's Python is the only Python you need. When a course command says `uv run`, uv starts this Python for you.

Your first uv project comes in week 2. Do Step 12 before it: it checks that Windows lets uv projects run on your laptop. In each new project, pin the version in the project too, right after `uv init`:

```bash
uv init --bare --python 3.12
uv python pin 3.12
```

`uv python pin 3.12` writes a `.python-version` file, which you commit. If a project's `.venv` was made with another Python, delete the `.venv` folder and run `uv sync`.

### Step 6: Python and UTF-8

In Git Bash, Python cannot print characters such as `₹` or `█` through a pipe or into a file, unless UTF-8 mode is on.
Turn it on once, in **PowerShell**:

```powershell
setx PYTHONUTF8 1
```

Then close and reopen VS Code and Git Bash.

Check it in Git Bash:

```bash
uv run --no-project python -c "print('₹1,250.50 █')" | cat
```

You see `₹1,250.50 █`. An error that names `charmap` means the setting is not on yet: reopen VS Code.

## Part 2, week 2: the course kit, WSL 2, Docker Desktop and Smart App Control

### Step 7: Clone the course kit

Clone the kit into your home folder with the `git clone` command in the kit's [`README.md`](../README.md), under "Get the kit". It makes the folder `~/de-kit`, which is `C:\Users\<your name>\de-kit`.
Keep it next to your course repository, never inside it. When a task says so, update it with `git pull` in that folder.

Check it: `ls ~/de-kit` lists `README.md`, `VERSIONS.md`, `setup` and `datalab`.

### Step 8: WSL 2

WSL 2 runs a real Linux system inside Windows. Docker Desktop uses it to run containers.
Open **PowerShell as administrator** (right-click PowerShell and choose "Run as administrator") and run:

```powershell
wsl --install
```

Restart the laptop when it asks. Ubuntu then opens and asks for a user name and a password. Choose a short name, such as `asha`, and a password you will remember. The course does not need Ubuntu, so you can close it after this.

Check it in PowerShell:

```powershell
wsl --version
wsl -l -v
```

`wsl --version` shows `WSL version: 2.` or newer: it must be 2.1.5 or newer. If it is older, run `wsl --update`.
`wsl -l -v` lists Ubuntu with `VERSION 2`.

### Step 9: Limit WSL 2's memory

Docker Desktop runs inside WSL 2, so this limit applies to Docker and every container.
It leaves enough memory for Windows, VS Code and your browser.

In Git Bash, copy the kit's settings file to your Windows user folder:

```bash
cp ~/de-kit/setup/wslconfig.example ~/.wslconfig
cat ~/.wslconfig
```

The file is set for a laptop with **8 GB** of memory: WSL 2 and Docker may use 4 GB, plus 2 GB of swap (disk used as extra memory). On a laptop with **16 GB**, open `~/.wslconfig` in VS Code (`code ~/.wslconfig`), change `memory=4GB` to `memory=8GB` and `swap=2GB` to `swap=4GB`, and save. The file's comments say the same.

Then, in PowerShell, stop WSL so that it starts again with the limit:

```powershell
wsl --shutdown
```

Wait 8 seconds before you start Docker Desktop again. You check the limit in Step 10.

### Step 10: Docker Desktop

Docker Desktop runs containers on Windows, using WSL 2.
**Licence:** Docker Desktop is free under the Personal plan for individual learning. It is also free for small businesses with fewer than 250 employees and less than $10 million in yearly revenue.

1. Download **Docker Desktop for Windows (x86_64)** from https://docs.docker.com/desktop/setup/install/windows-install/.
2. Run the installer. Keep **Use WSL 2 instead of Hyper-V** ticked, then finish. Restart the laptop if it asks.
3. Start **Docker Desktop** from the Start menu.
4. Accept the Docker Subscription Service Agreement. Signing in is optional: you may skip it.
5. Wait until the bottom left of the Docker Desktop window says **Engine running**.

Check it in Git Bash:

```bash
docker run --rm hello-world
docker compose version
docker info | grep "Total Memory"
```

- `docker run --rm hello-world` prints `Hello from Docker!` and a few lines that explain what happened.
- `docker compose version` prints `Docker Compose version` and a number.
- `Total Memory` is about `3.8GiB` with `memory=4GB`, or about `7.7GiB` with `memory=8GB`. If it shows more, run `wsl --shutdown` in PowerShell, wait 8 seconds and start Docker Desktop again.

Docker Desktop must be running whenever you use Docker. Start it from the Start menu after you restart the laptop.

### Step 11: Git Bash and Docker: the path rule

Git Bash changes any word that looks like a Linux path, such as `/etc` or `/tmp/file.sql`, into a Windows path before Docker sees it.
So this command fails, because Docker receives `C:/Program Files/Git/etc`:

```bash
docker run --rm alpine ls /etc
```

When a `docker` or `kubectl` command names a path inside a container, put `MSYS_NO_PATHCONV=1` in front of it. This works:

```bash
MSYS_NO_PATHCONV=1 docker run --rm alpine ls /etc
MSYS_NO_PATHCONV=1 docker run --rm -v "$PWD":/work alpine ls /work
```

- Put `MSYS_NO_PATHCONV=1` in front of one command at a time. Never set it for the whole terminal with `export`: then `uv run ~/file.py` and other commands break.
- With the prefix, give files on your laptop as relative paths, such as `data/stations.sql`, not `~/...`.
- You do not need it for paths inside quotes after `sh -c`, such as `docker exec web sh -c 'ls /tmp'`, or for paths inside a Compose file.
- Interactive commands such as `docker exec -it ...` work in VS Code's terminal. In the separate Git Bash window, put `winpty` in front if you see `the input device is not a TTY`.

### Step 12: Smart App Control

Smart App Control is a Windows 11 security feature. It blocks programs and program parts (DLL files) that Microsoft does not know or that are not signed. A new Windows 11 laptop may have it **On**.

**For this course, Smart App Control must be Off, or you must work in the dev container (Way 2 below).** With it on, every uv project fails: the small `python.exe` that uv puts in each project's `.venv` folder is not signed, so Windows blocks it, and `uv run`, `uv add` and `uv run pytest` stop with `An Application Control policy has blocked this file`. Almost every Python task in the course uses a uv project. It also blocks parts of Python libraries the course uses:

- the `python.exe` in every uv project's `.venv` folder (see above);
- `pyarrow`'s compute and Parquet modules. So `pandas` fails when `pyarrow` is installed, and so do `pandas.read_parquet`, PyIceberg and Delta Lake from Python.
- `psycopg`'s binary driver (`psycopg[binary]`), the PostgreSQL library for Python.
- uv's newest Python (3.15): its `_ctypes` module. Step 5's `uv python pin --global 3.12` avoids it.
- Sometimes `pytest.exe`. Then run tests as `uv run python -m pytest`, which works the same.

**Check whether it is on.** Open **Windows Security**, select **App & browser control**, then **Smart App Control settings**. It says On, Evaluation or Off. Or run this in PowerShell:

```powershell
(Get-MpComputerStatus).SmartAppControlState
```

It prints `On`, `Eval` or `Off`.

**Test it.** Run this in Git Bash (the first run downloads the libraries):

```bash
uv run --python 3.12 --with pandas --with pyarrow --with "psycopg[binary]" python -c "import pandas, pyarrow.parquet, psycopg; print('OK', pandas.__version__)"
```

Success prints `OK` and pandas' version, for example `OK 3.1.1`. If it ends with `ImportError: DLL load failed ... An Application Control policy has blocked this file`, Smart App Control blocks the course's libraries.

**Test a uv project too.** In Git Bash:

```bash
mkdir -p ~/sac-test && cd ~/sac-test && uv init --bare --python 3.12 && uv run python -c "print('project OK')"
cd ~ && rm -r ~/sac-test
```

Success prints `project OK`. If it says `Failed to spawn: python` or `An Application Control policy has blocked this file`, Smart App Control blocks uv projects. If either test fails, choose one of the two ways below, in this order, before you start any project.

**Way 1: turn Smart App Control off on your own laptop.**

1. Open **Windows Security**, then **App & browser control**, then **Smart App Control settings**.
2. Select **Off**. Windows asks for confirmation: confirm.
3. Run the test command again. It prints `OK`.

Do this only on a laptop that is yours. On a laptop that belongs to your centre or employer, ask its owner first.

Can you turn it on again later? Microsoft's page "What is Smart App Control?" says: *"Recent Windows updates allow Smart App Control to be re-enabled without requiring a clean installation."* On older Windows 11 builds, turning it off was permanent until you reset or reinstalled Windows. Keep Windows updated (Settings, Windows Update) before you switch it off, so you can switch it back on after the course. Keep Microsoft Defender Antivirus on either way.

**Way 2: keep it on, and run the course's Python in a container.** The course kit has a dev container (a container that VS Code opens your folder in): Linux, Python 3.12, uv, Docker and the course's tools. Smart App Control does not apply inside it.

- **On your laptop**, with Docker Desktop: install the VS Code extension **Dev Containers** (from Microsoft). Copy the kit's folder into your course repository once, and commit it:

  ```bash
  cp -r ~/de-kit/.devcontainer <your course repository>/
  ```

  Open the repository in VS Code. Press Ctrl+Shift+P and run `Dev Containers: Reopen in Container`. The first time takes 5 to 10 minutes. VS Code's terminal then runs inside the container, and every course command works there. Docker commands in it start a separate Docker inside the container, so start the data lab from that terminal too.
- **In GitHub Codespaces**, if your laptop has 8 GB: see [`codespaces.md`](codespaces.md). Codespaces uses the same `.devcontainer` folder.

For one script, you can also run Python 3.12 in a container without the dev container:

```bash
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W)":/w -w /w ghcr.io/astral-sh/uv:python3.12-bookworm-slim uv run --no-project --with pandas --with pyarrow python your_script.py
```

Inside that container, the data lab's PostgreSQL is `host.docker.internal:5432` and the S3 emulator is `http://host.docker.internal:4566`.

## Final check

Run these in Git Bash, in VS Code's terminal. Compare each line with the "You see" column.

| Command | You see |
|---|---|
| `git --version` | `git version 2.` and more |
| `uv run --no-project python --version` | `Python 3.12.` and more |
| `docker run --rm hello-world` | `Hello from Docker!` |
| `docker info \| grep "Total Memory"` | about `3.8GiB` (or about `7.7GiB` with `memory=8GB`) |
| `cat ~/.wslconfig` | `memory=4GB` and `swap=2GB` (or `8GB` and `4GB`) |
| `ls ~/de-kit` | `README.md`, `VERSIONS.md` and the kit folders |
| The two Step 12 tests | `OK` and a version number, then `project OK` |

## Ubuntu (optional)

`wsl --install` also installed Ubuntu. The course does not need it, because every tool runs on Windows or in a container.
You may use it to practise Linux commands: type `wsl` in PowerShell to open it, and `exit` to leave.

## If something goes wrong

| What you see | What to do |
|---|---|
| `uv`, `code` or `docker` is not recognised | The terminal was open before the install. Close every terminal and VS Code, then open them again. |
| `wsl --install` says that virtualisation is off | Turn on Intel VT-x or AMD SVM in the BIOS. Ask your mentor if you are unsure. |
| Docker Desktop says WSL needs an update | Run `wsl --update` in PowerShell, then start Docker Desktop again. |
| `error during connect` or `Is the docker daemon running?` | Start Docker Desktop and wait for **Engine running**. |
| An error shows a path such as `C:/Program Files/Git/...` | Add `MSYS_NO_PATHCONV=1` in front of the `docker` command (Step 11). |
| `the input device is not a TTY` | Run the command in VS Code's terminal, or put `winpty` in front of it. |
| `UnicodeEncodeError` and `charmap` | Do Step 6, then reopen VS Code. |
| `An Application Control policy has blocked this file`, or `Failed to spawn: python` | Smart App Control blocks it. Do Step 12: turn it off, or work in the dev container. |
| `uv run python --version` shows 3.15 or another version | Run `uv python pin 3.12` in the project, delete `.venv`, then run the command again. |
| `$'\r': command not found` or `bad interpreter` | The file has CRLF line endings. In VS Code, select `CRLF` in the status bar, choose `LF` and save. Then do Step 4. |
| `port is already allocated` for 5432 | Another PostgreSQL runs on your laptop. Stop it in Windows Services, or ask your mentor. |
| The laptop is slow while Docker runs | Check Step 9, and stop the data lab profiles and stacks you are not using. |
