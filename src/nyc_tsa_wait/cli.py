import argparse
import sys
from collections import defaultdict

from rich.console import Console
from rich.table import Table
from rich import box

from .api import fetch_wait_times, AIRPORTS

console = Console()


def _wait_color(minutes: int, queue_open: bool, available: bool) -> str:
    if not queue_open or not available:
        return "dim"
    if minutes <= 10:
        return "green"
    if minutes <= 20:
        return "yellow"
    return "red"


def _fmt_wait(minutes: int, status: str, queue_open: bool, available: bool) -> str:
    if not queue_open:
        return "[dim]Closed[/dim]"
    if not available or status.upper() in ("N/A", "-", ""):
        return "[dim]N/A[/dim]"
    color = _wait_color(minutes, queue_open, available)
    label = f"{minutes} min" if minutes else "< 1 min"
    return f"[{color}]{label}[/{color}]"


def show_airport(code: str) -> bool:
    info = AIRPORTS[code]
    try:
        data = fetch_wait_times(code)
    except Exception as exc:
        console.print(f"[red]Error fetching {code}:[/red] {exc}")
        return False

    # Group entries by terminal, then by queue type (Reg / TSAPre)
    # Each entry: terminal, checkPoint, queueType, timeInMinutes, queueOpen, isWaitTimeAvailable, status, updateTimeText
    terminals: dict[str, dict] = defaultdict(lambda: {"Reg": None, "TSAPre": None, "updated": ""})
    for entry in data:
        t = entry.get("title", entry.get("terminal", "—"))
        qt = entry.get("queueType", "Reg")
        terminals[t][qt] = entry
        terminals[t]["updated"] = entry.get("updateTimeText", "")

    updated_sample = next(iter(terminals.values()), {}).get("updated", "")
    title = f"[bold]{code}[/bold] — {info['name']}  [dim](updated {updated_sample})[/dim]"

    table = Table(
        title=title,
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        title_justify="left",
    )
    table.add_column("Terminal", style="bold")
    table.add_column("Standard", justify="center")
    table.add_column("TSA PreCheck", justify="center")

    if not terminals:
        table.add_row("—", "[dim]No data[/dim]", "[dim]No data[/dim]")
    else:
        for terminal, queues in sorted(terminals.items()):
            reg = queues.get("Reg")
            pre = queues.get("TSAPre")

            def fmt(entry):
                if entry is None:
                    return "[dim]—[/dim]"
                return _fmt_wait(
                    entry.get("timeInMinutes", 0),
                    entry.get("status", ""),
                    entry.get("queueOpen", False),
                    entry.get("isWaitTimeAvailable", False),
                )

            table.add_row(terminal, fmt(reg), fmt(pre))

    console.print(table)
    console.print()
    return True


def main():
    parser = argparse.ArgumentParser(
        prog="tsa-wait",
        description="Show live TSA security wait times at NYC-area airports.",
    )
    parser.add_argument(
        "airports",
        nargs="*",
        metavar="AIRPORT",
        default=list(AIRPORTS.keys()),
        help="Airport codes to check (default: JFK LGA EWR)",
    )
    args = parser.parse_args()

    codes = [a.upper() for a in args.airports]
    unknown = [c for c in codes if c not in AIRPORTS]
    if unknown:
        console.print(f"[red]Unknown airport(s):[/red] {', '.join(unknown)}")
        console.print(f"Supported: {', '.join(AIRPORTS)}")
        sys.exit(1)

    ok = all(show_airport(code) for code in codes)
    sys.exit(0 if ok else 1)
