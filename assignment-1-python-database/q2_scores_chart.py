"""Q2: Fetch student scores from an API, compute average, draw bar chart."""
import requests, statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

API = "https://example.com/api/students/scores"   # assumption: returns [{"name":..,"score":..}]
SAMPLE = [{"name": n, "score": s} for n, s in
          [("Aarav", 78), ("Diya", 92), ("Karthik", 65), ("Meera", 88), ("Rohan", 71), ("Sneha", 95), ("Vikram", 59)]]

def fetch_scores():
    try:
        r = requests.get(API, timeout=10); r.raise_for_status(); return r.json()
    except Exception as e:
        print(f"[warn] using sample data ({e.__class__.__name__})"); return SAMPLE

def main():
    data = [d for d in fetch_scores() if isinstance(d.get("score"), (int, float))]  # validate
    names, scores = [d["name"] for d in data], [d["score"] for d in data]
    avg = statistics.mean(scores)
    print(f"Students: {len(scores)} | Average: {avg:.2f} | Max: {max(scores)} | Min: {min(scores)}")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = ["#2e7d32" if s >= avg else "#c62828" for s in scores]
    bars = ax.bar(names, scores, color=colors)
    ax.axhline(avg, ls="--", color="#1565c0", label=f"Average = {avg:.1f}")
    ax.bar_label(bars, padding=2)
    ax.set(title="Student Test Scores", ylabel="Score", ylim=(0, 105)); ax.legend()
    plt.tight_layout(); plt.savefig("scores_chart.png", dpi=160)

if __name__ == "__main__":
    main()
