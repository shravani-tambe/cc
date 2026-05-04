import time
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich.align import Align
from rich import box
from rich.style import Style
from rich.prompt import Prompt, IntPrompt
from rich.traceback import install

install()
console = Console()
QUEEN = "♛"

# ─────────────────────────────────────────────────────────────
#  SOLVER  —  board[row] = col  of queen placed in that row
# ─────────────────────────────────────────────────────────────
class NQueensSolver:
    def __init__(self, n):
        self.n           = n
        self.board       = [-1] * n
        self.solutions   = []
        self.nodes_explored = 0
        self.backtracks  = 0
        self.pruned      = 0
        self.cols_used   = 0
        self.diag1_used  = 0   # row + col
        self.diag2_used  = 0   # row - col + n-1
        self.history     = []

    def is_safe(self, row, col):
        return not (
            (self.cols_used  >> col)                     & 1 or
            (self.diag1_used >> (row + col))             & 1 or
            (self.diag2_used >> (row - col + self.n-1))  & 1
        )

    def place(self, row, col):
        self.board[row]   = col
        self.cols_used   |= 1 << col
        self.diag1_used  |= 1 << (row + col)
        self.diag2_used  |= 1 << (row - col + self.n-1)

    def remove(self, row, col):
        self.board[row]   = -1
        self.cols_used   &= ~(1 << col)
        self.diag1_used  &= ~(1 << (row + col))
        self.diag2_used  &= ~(1 << (row - col + self.n-1))

    def bound_violated(self, next_row):
        """B&B bound: prune if any future row has no safe column."""
        for r in range(next_row, self.n):
            for c in range(self.n):
                if self.is_safe(r, c):
                    break
            else:
                return True
        return False

    def solve(self, row=0, record=False):
        if row == self.n:
            self.solutions.append(self.board[:])
            if record:
                self.history.append({"type":"solution","board":self.board[:],"sol_num":len(self.solutions)})
            return

        self.nodes_explored += 1

        for col in range(self.n):
            if self.is_safe(row, col):
                self.place(row, col)
                if record:
                    self.history.append({"type":"place","board":self.board[:],"row":row,"col":col})

                if self.bound_violated(row + 1):
                    self.pruned += 1
                    if record:
                        self.history.append({"type":"prune","board":self.board[:],"row":row,"col":col})
                else:
                    self.solve(row + 1, record)

                self.remove(row, col)
                self.backtracks += 1
                if record:
                    self.history.append({"type":"backtrack","board":self.board[:],"row":row,"col":col})

# ─────────────────────────────────────────────────────────────
#  RENDERING
# ─────────────────────────────────────────────────────────────
def render_board(board, n, hi_row=-1, hi_col=-1, ev=""):
    tbl = Table(show_header=False, show_lines=False, padding=0, box=None, expand=False)
    for _ in range(n):
        tbl.add_column(width=3, justify="center", no_wrap=True)
    for r in range(n):
        cells = []
        for c in range(n):
            light = (r+c) % 2 == 0
            bg_base = "grey30" if light else "grey11"
            if board[r] == c:
                if r == hi_row and c == hi_col and ev in ("prune","backtrack"):
                    cells.append(Text(f" {QUEEN} ", style=Style(color="bright_red", bgcolor="dark_red", bold=True)))
                elif ev == "solution":
                    cells.append(Text(f" {QUEEN} ", style=Style(color="bright_yellow", bgcolor="dark_green", bold=True)))
                else:
                    cells.append(Text(f" {QUEEN} ", style=Style(color="bright_yellow", bgcolor=bg_base, bold=True)))
            else:
                cells.append(Text("   ", style=Style(bgcolor=bg_base)))
        tbl.add_row(*cells)
    return tbl

def render_solution(board, n, idx):
    tbl = Table(show_header=False, show_lines=False, padding=0, box=None, expand=False)
    for _ in range(n):
        tbl.add_column(width=3, justify="center", no_wrap=True)
    for r in range(n):
        cells = []
        for c in range(n):
            light = (r+c) % 2 == 0
            bg = "grey30" if light else "grey11"
            if board[r] == c:
                cells.append(Text(f" {QUEEN} ", style=Style(color="bright_yellow", bgcolor="dark_green", bold=True)))
            else:
                cells.append(Text("   ", style=Style(bgcolor=bg)))
        tbl.add_row(*cells)
    notation = " ".join(str(board[r]+1) for r in range(n))
    return Panel(Align.center(tbl), title=f"[bold bright_cyan]#{idx}[/]",
                 subtitle=f"[grey50]{notation}[/]", border_style="cyan", padding=(0,1))

def stats_panel(solver, step, total, ev):
    labels = {
        "place":     "[bright_yellow]▶  PLACE[/]",
        "backtrack": "[bright_red]◀  BACKTRACK[/]",
        "prune":     "[bold red]✂  PRUNED (B&B)[/]",
        "solution":  "[bold bright_green]★  SOLUTION![/]",
    }
    t = Text()
    t.append(" Event    ", style="grey50 bold"); t.append_text(Text.from_markup(labels.get(ev, ev)))
    t.append(f"\n Step     ", style="grey50 bold"); t.append(f"{step}/{total}", style="bright_cyan")
    t.append(f"\n Nodes    ", style="grey50 bold"); t.append(f"{solver.nodes_explored}", style="bright_white")
    t.append(f"\n Pruned   ", style="grey50 bold"); t.append(f"{solver.pruned}", style="bright_red")
    t.append(f"\n B-tracks ", style="grey50 bold"); t.append(f"{solver.backtracks}", style="yellow")
    t.append(f"\n Solns    ", style="grey50 bold"); t.append(f"{len(solver.solutions)}", style="bright_green")
    return Panel(t, title="[bold magenta]── Stats ──[/]", border_style="magenta", padding=(0,1))

def clear_lines(n):
    sys.stdout.write(f"\033[{n}A\033[J")
    sys.stdout.flush()

def animate(solver, delay, max_steps):
    n = solver.n
    history = solver.history
    total = min(len(history), max_steps)

    legend = Table(show_header=False, box=None, padding=(0,3))
    for _ in range(4): legend.add_column()
    legend.add_row(Text("▶ PLACE",style="bright_yellow"), Text("◀ BACKTRACK",style="bright_red"),
                   Text("✂ PRUNED",style="bold red"), Text("★ SOLUTION",style="bright_green"))
    console.print(Align.center(legend))
    console.print()
    time.sleep(0.3)

    last_sol = 0
    for i, step in enumerate(history[:total]):
        ev     = step["type"]
        brd    = step["board"]
        hi_r   = step.get("row", -1)
        hi_c   = step.get("col", -1)
        grid   = Table.grid(padding=(0,2))
        grid.add_column(); grid.add_column()
        grid.add_row(render_board(brd, n, hi_r, hi_c, ev), stats_panel(solver, i+1, total, ev))
        console.print(Align.center(grid))
        sol_n = step.get("sol_num", 0)
        if ev == "solution" and sol_n != last_sol:
            last_sol = sol_n
            time.sleep(delay * 8)
        else:
            time.sleep(delay)
        clear_lines(n + 3)

    # Final frame
    last = history[total - 1]
    grid = Table.grid(padding=(0,2))
    grid.add_column(); grid.add_column()
    grid.add_row(render_board(last["board"], n, ev="solution"), stats_panel(solver, total, total, last["type"]))
    console.print(Align.center(grid))

def show_all_solutions(solver, limit=16):
    console.print()
    console.print(Rule("[bold magenta]  ALL SOLUTIONS  [/]", style="magenta"))
    console.print()
    panels = [render_solution(sol, solver.n, i+1) for i, sol in enumerate(solver.solutions[:limit])]
    if len(solver.solutions) > limit:
        console.print(Align.center(Text(f"  Showing {limit} of {len(solver.solutions)} solutions  ", style="grey50 on grey15")))
        console.print()
    chunk = max(1, min(4, 36 // max(solver.n * 3 + 2, 1)))
    for s in range(0, len(panels), chunk):
        console.print(Columns(panels[s:s+chunk], equal=True, align="center"))
        console.print()

def show_summary(solver, elapsed):
    n = solver.n
    tbl = Table(title=f"[bold bright_cyan]  Performance Report — {n}-Queens  [/]",
                box=box.DOUBLE_EDGE, border_style="cyan", header_style="bold magenta",
                show_lines=True, expand=False)
    tbl.add_column("Metric", style="bold grey70", justify="right", min_width=26)
    tbl.add_column("Value",  style="bold bright_white", justify="left", min_width=20)
    tbl.add_row("Board size",          f"{n} × {n}")
    tbl.add_row("Total solutions",     f"[bright_green]{len(solver.solutions)}[/]")
    tbl.add_row("Nodes explored",      f"[bright_cyan]{solver.nodes_explored:,}[/]")
    tbl.add_row("B&B pruned branches", f"[bright_red]{solver.pruned:,}[/]")
    tbl.add_row("Backtracks",          f"[yellow]{solver.backtracks:,}[/]")
    tbl.add_row("Solve time",          f"{elapsed*1000:.2f} ms")
    tbl.add_row("Algorithm",           "[dim]Backtracking + Branch & Bound (bitmask)[/]")
    tbl.add_row("Bound",               "[dim]Prune when any future row has 0 safe columns[/]")
    console.print()
    console.print(Align.center(tbl))
def show_explainer():
    t = Text()
    t.append("  Backtracking\n", style="bold bright_cyan")
    t.append("  Try placing a queen in each column of the current row.\n"
             "  If a placement is invalid, undo (backtrack) and try the next.\n\n", style="grey80")
    t.append("  Branch & Bound  (speedup)\n", style="bold bright_yellow")
    t.append("  After placing a queen, check all remaining rows (the bound).\n"
             "  If any future row has zero safe columns, prune the entire\n"
             "  subtree — it cannot lead to a valid solution.\n\n", style="grey80")
    t.append("  Bitmask O(1) conflict detection\n", style="bold bright_green")
    t.append("  Three integers track occupied columns, '/' and '\\' diagonals.\n"
             "  Checking safety is a single bitwise AND operation.", style="grey80")
    console.print(Panel(t, title="[bold magenta]── How it works ──[/]", border_style="grey30", padding=(1,2)))

def main():
    console.clear()
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ♛  N - Q U E E N S   S O L V E R                             ║
║      Branch & Bound  +  Backtracking  (CSP)                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝"""
    console.print(Text(banner, style="bold bright_cyan"))
    console.print()
    show_explainer()
    console.print()

    n = IntPrompt.ask("[bold bright_cyan]  Enter N[/] [grey50](board size, 4–15)[/]", default=8)
    n = max(4, min(n, 15))

    speed = Prompt.ask(
        "[bold bright_cyan]  Animation speed[/] [grey50](fast / medium / slow)[/]",
        choices=["fast","medium","slow"], default="medium"
    )
    delay     = {"fast":0.025, "medium":0.065, "slow":0.15}[speed]
    max_steps = {"fast":800,   "medium":600,   "slow":400 }[speed]

    console.print()
    console.print(Rule(style="grey30"))

    solver = NQueensSolver(n)
    with console.status("[bold cyan]Solving…[/]", spinner="aesthetic"):
        t0 = time.perf_counter()
        solver.solve(0, record=True)
        elapsed = time.perf_counter() - t0

    console.print(f"  [bold bright_green]✓[/] Found [bold bright_cyan]{len(solver.solutions)}[/] solutions"
                  f"  ·  [grey50]{len(solver.history)} steps, replaying {min(len(solver.history), max_steps)}[/]")
    console.print(Rule(style="grey30"))
    console.print()

    animate(solver, delay, max_steps)
    show_summary(solver, elapsed)

    if solver.solutions:
        ans = Prompt.ask("\n[bold bright_cyan]  Show all solutions?[/]", choices=["y","n"], default="y")
        if ans == "y":
            show_all_solutions(solver)

    console.print()
    console.print(Align.center(Text("  ♛  Done!  ♛  ", style="bold black on bright_cyan")))
    console.print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[grey50]  Exited.[/]")
