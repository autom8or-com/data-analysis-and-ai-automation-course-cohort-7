# =====================================================================
# Olist SQL Setup — runs on BOTH Google Colab and a local machine.
# Run this cell FIRST. It loads the 8 Olist tables into a SQLite
# database and connects the %%sql magic to it. You should not need to
# edit anything unless auto-detection fails (see the two knobs below).
#
# Design notes:
# - We teach SQL with the %%sql cell magic (jupysql), not pd.read_sql().
# - jupysql opens its OWN connection, so the DB must be a real FILE
#   (a :memory: DB would be invisible to it).
# - We use jupysql (the maintained SQL magic). On Colab we install it,
#   because Colab ships the legacy ipython-sql, which (a) can't take a
#   connection by engine variable and (b) renders every result through
#   prettytable.__dict__[style], crashing on modern prettytable with
#   KeyError 'DEFAULT'/'SINGLE_BORDER'. jupysql fixes both.
# - autopandas=True makes every %%sql result a pandas DataFrame, which
#   lets the self-check cells assert on .iloc/.shape directly.
# =====================================================================
import os, glob, sqlite3, tempfile, zipfile
import pandas as pd

# --- Optional knobs (leave blank; only set if auto-detect fails) ------
LOCAL_DATA_DIR = ""   # local run: folder that holds olist_orders_dataset.csv
DRIVE_ZIP_PATH = ""   # Colab: full path to phase-2-python-sql.zip in your Drive
# ---------------------------------------------------------------------

# Detect Colab (google.colab only imports there). Outside Colab — including
# the content-pipeline validator — this falls through to the local branch.
try:
    from google.colab import drive
    drive.mount("/content/drive")
    ON_COLAB = True
except ModuleNotFoundError:
    ON_COLAB = False


def _colab_find_zip():
    """Locate phase-2-python-sql.zip in Drive WITHOUT a full recursive scan
    (globbing '/content/drive/MyDrive/**' walks the entire Drive over the
    network and can hang for many minutes). Try explicit paths first, then a
    depth- and count-bounded breadth-first search that prints progress."""
    if DRIVE_ZIP_PATH:
        if os.path.exists(DRIVE_ZIP_PATH):
            return DRIVE_ZIP_PATH
        raise FileNotFoundError(f"DRIVE_ZIP_PATH is set but not found: {DRIVE_ZIP_PATH}")

    target = "phase-2-python-sql.zip"
    # Fast, instant checks of the most likely spots (top of Drive + course folder).
    for cand in (
        f"/content/drive/MyDrive/{target}",
        f"/content/drive/MyDrive/Data Analysis and AI Automation Course Cohort 7/Dataset/{target}",
        f"/content/{target}",
    ):
        if os.path.exists(cand):
            return cand

    # Bounded BFS: depth <= 4, at most ~600 folders, skipping hidden dirs.
    print("Searching your Google Drive for phase-2-python-sql.zip ...")
    root, queue, scanned = "/content/drive/MyDrive", [("/content/drive/MyDrive", 0)], 0
    while queue:
        d, depth = queue.pop(0)
        hit = os.path.join(d, target)
        if os.path.exists(hit):
            return hit
        if depth >= 4:
            continue
        try:
            for e in os.scandir(d):
                if e.is_dir() and not e.name.startswith("."):
                    queue.append((e.path, depth + 1))
        except OSError:
            continue
        scanned += 1
        if scanned % 50 == 0:
            print(f"  ...scanned {scanned} folders")
        if scanned >= 600:
            break

    raise FileNotFoundError(
        "Could not quickly find phase-2-python-sql.zip in your Drive. Put the zip at the "
        "TOP of your Drive (My Drive) and re-run, or set DRIVE_ZIP_PATH at the top of this "
        "cell to its exact path.")


def _find_csv_dir():
    """Return the folder that actually contains olist_orders_dataset.csv."""
    roots = []
    env_dir = os.environ.get("OLIST_DATA_PATH", "")   # set by the pipeline validator
    if env_dir:
        roots.append(env_dir)
    if LOCAL_DATA_DIR:
        roots.append(LOCAL_DATA_DIR)

    if ON_COLAB:
        extract_path = "/content/olist_data"
        # unzip only the first time; reuse the extracted CSVs afterwards
        if not glob.glob(f"{extract_path}/**/olist_orders_dataset.csv", recursive=True):
            zip_path = _colab_find_zip()
            os.makedirs(extract_path, exist_ok=True)
            print(f"Unzipping {os.path.basename(zip_path)} ...")
            with zipfile.ZipFile(zip_path) as z:
                z.extractall(extract_path)
        roots.append(extract_path)
    else:
        # Local: search cwd (recursively) + a few common spots — never the whole
        # home dir (that recursive walk can be very slow). Set LOCAL_DATA_DIR if
        # your CSVs live elsewhere.
        roots += [os.getcwd(),
                  os.path.expanduser("~/Downloads"),
                  os.path.expanduser("~/Desktop"),
                  os.path.expanduser("~/olist")]

    for root in roots:
        if os.path.exists(os.path.join(root, "olist_orders_dataset.csv")):
            return root
        hits = glob.glob(os.path.join(root, "**", "olist_orders_dataset.csv"), recursive=True)
        if hits:
            return os.path.dirname(hits[0])

    raise FileNotFoundError(
        "Olist CSVs not found. Set LOCAL_DATA_DIR (local) or DRIVE_ZIP_PATH (Colab) at "
        "the top of this cell.")


DATA_DIR = _find_csv_dir()
print("Data folder:", DATA_DIR)

# Build a file-based SQLite DB shared by pandas (loading) and jupysql (querying).
DB_PATH = os.environ.get("OLIST_DB_PATH") or (
    "/content/olist.db" if ON_COLAB else os.path.join(tempfile.gettempdir(), "olist.db"))

tables = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product_category_translation": "product_category_name_translation.csv",
}

conn = sqlite3.connect(DB_PATH)
for table_name, filename in tables.items():
    df = pd.read_csv(os.path.join(DATA_DIR, filename))
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {table_name}: {len(df):,} rows")
conn.close()
print("\nDatabase ready.")

# On Colab, install jupysql so `%load_ext sql` loads it instead of the legacy
# ipython-sql (see header). Off Colab (local / pipeline validator) jupysql is
# already installed, so we skip the install and stay offline-safe.
if ON_COLAB:
    get_ipython().run_line_magic("pip", "install --quiet --upgrade jupysql")

get_ipython().run_line_magic("load_ext", "sql")

# Guard: if the legacy ipython-sql was already loaded earlier THIS session (e.g.
# an older cell ran first), the freshly installed jupysql cannot hot-swap in — a
# runtime restart is the only fix. jupysql exposes sql.connection.ConnectionManager;
# ipython-sql does not. Stop with a clear instruction instead of a later cryptic
# prettytable KeyError.
import sql.connection as _sqlconn
if not hasattr(_sqlconn, "ConnectionManager"):
    raise RuntimeError(
        "Legacy ipython-sql is active, not jupysql. On Colab: Runtime -> Restart session, "
        "then run THIS setup cell first (before any other cell). Locally: "
        "pip install --upgrade jupysql and restart the kernel."
    )

# Connect the %%sql magic to the SAME database file. autopandas=True is REQUIRED
# (see header). We connect with run_line_magic (not a literal `%sql` line) so the
# computed DB_PATH is interpolated correctly. Do NOT set SqlMagic.style.
get_ipython().run_line_magic("config", "SqlMagic.autopandas = True")
get_ipython().run_line_magic("config", "SqlMagic.feedback = 0")
get_ipython().run_line_magic("sql", f"sqlite:///{DB_PATH}")

# Verify (expected row counts — do not alter without re-running against data):
#   orders 99,441 | customers 99,441 | order_items 112,650 | order_payments 103,886
#   order_reviews 99,224 | products 32,951 | sellers 3,095 | product_category_translation 71
