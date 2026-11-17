# Run a lab in GitHub Codespaces

GitHub Codespaces gives you a Linux machine in the cloud, with VS Code in your browser or in VS Code on your laptop. Use it when a task's "Before you start" says your 8 GB laptop needs it: P8 EditStream (Kafka with Spark) and P13 CareLine (the incident drill). It also helps in P4 if your laptop is slow with k3d. A 16 GB laptop does not need it.

Every course command works the same in a codespace, in its terminal. The codespace uses the kit's dev container: Linux with Docker, uv and Python 3.12, the AWS CLI, kubectl and the GitHub CLI.

## What it costs: the free hours

Facts from GitHub's page "About billing for GitHub Codespaces", read on 13 November 2026:

- A personal GitHub Free account gets **120 core hours** of compute and **15 GB-months** of storage free every month.
- A core hour is one processor core for one hour. A 2-core machine uses 2 core hours per hour, so the free quota is **60 hours a month on a 2-core machine**, or 30 hours on a 4-core machine.
- Without a payment method on your GitHub account, Codespaces stops when the quota is used up. It does not bill you. Do not add a payment method for the course.
- Storage counts while a codespace exists, even when it is stopped. Delete a codespace when its project is done.

## Which machine

| Machine | Memory | Use it for |
|---|---|---|
| **2-core** | 8 GB | Every course lab in its `lite` profile, including Kafka with Spark. Choose this one |
| 4-core | 16 GB | Only if a `full` profile is needed. It uses the free hours twice as fast |

The whole 8 GB is for Linux and Docker: no Windows, no browser. That is why a lab that does not fit an 8 GB laptop fits a 2-core codespace.

## 1. Add the dev container to your course repository (once)

On your laptop, in Git Bash:

```bash
cp -r ~/de-kit/.devcontainer <your course repository>/
cd <your course repository>
git add .devcontainer
git commit -m "Add the course dev container"
git push
```

## 2. Create the codespace

1. Open your course repository on github.com.
2. Select **Code**, then the **Codespaces** tab, then **...** (more actions), then **New with options**.
3. Choose your branch and the machine type **2-core**, then **Create codespace**.

The first start builds the dev container and takes 5 to 10 minutes. Later starts take about one minute.

With the GitHub CLI, the same is `gh codespace create --repo <your-user>/<your-repository> --machine basicLinux32gb`. List the machine names with `gh codespace create --repo <your-user>/<your-repository>` and the arrow keys.

To work in VS Code on your laptop instead of the browser, install the extension **GitHub Codespaces** and run `Codespaces: Connect to Codespace` from the Command Palette (Ctrl+Shift+P).

## 3. Set up the codespace (once per codespace)

In the codespace's terminal:

1. Clone the kit with the `git clone` command in the kit's `README.md`, under "Get the kit". It makes `~/de-kit`, as on your laptop.
2. Check the tools:

   ```bash
   uv run --no-project python --version
   docker version --format '{{.Server.Version}}'
   ```

   The first prints `Python 3.12.` and more numbers. The second prints the Docker engine's version.
3. Airflow only: Airflow needs your user number to write to your product folder. In the product folder, run `echo "AIRFLOW_UID=$(id -u)" >> .env` once.

Then follow your task as written: `docker compose --profile core up -d` in `~/de-kit/datalab`, `docker compose --profile lite up -d` in the product folder, and so on. `MSYS_NO_PATHCONV=1` is not needed in a codespace, but it does no harm.

## 4. Open the web pages: forwarded ports

When a container publishes a port, such as Airflow's 8080 or Spark's 4040, the codespace forwards it to you:

- In VS Code on your laptop, open `http://localhost:8080` as usual.
- In the browser, open the **PORTS** tab (next to TERMINAL), find the port, and select the globe icon. The address looks like `https://<name>-8080.app.github.dev`. Only you can open it: it asks you to sign in to GitHub.

The kit's dev container names the course's ports in the PORTS tab: PostgreSQL 5432, the S3 emulator 4566, Airflow 8080, Kafka 9092, Kafka Connect 8083, the Spark UI 4040, the Spark history server 18080 and the Spark master 8081.

## 5. Stop it, every time

A codespace uses your free hours while it runs, even when you do nothing in it.

- **Stop it when you finish**: on github.com/codespaces, select **...** next to the codespace, then **Stop codespace**. In VS Code, run `Codespaces: Stop Current Codespace` from the Command Palette. With the GitHub CLI: `gh codespace stop`.
- GitHub stops a codespace by itself after **30 minutes** without activity. You can change this between 5 and 240 minutes: your profile picture, **Settings**, **Codespaces**, **Default idle timeout**. A shorter time saves hours.
- A stopped codespace keeps your files and Docker volumes. Start it again from github.com/codespaces.
- **Commit and push your work before you stop.** A codespace is not a backup.
- **Delete it when the project is over**: **...**, then **Delete**. Its storage then stops counting.

## Troubleshooting

- **The codespace does not start, and GitHub says the quota is used up**: wait for next month's quota, and work on the laptop with the `lite` profile. Ask your mentor.
- **`docker: command not found`** or **`Cannot connect to the Docker daemon`**: the codespace was made without the kit's dev container. Check that `.devcontainer/devcontainer.json` is in your repository, then run `Codespaces: Rebuild Container` from the Command Palette.
- **`uv run python --version` shows another version**: run `uv python pin 3.12` in the project folder, delete `.venv`, and run the command again.
- **A web page does not open**: check the **PORTS** tab. If the port is not listed, select **Forward a Port** and type its number.
- **`Permission denied`** when Airflow or Spark writes to `data/`: see "Codespaces and Linux" in the kit's Airflow or Spark README.
