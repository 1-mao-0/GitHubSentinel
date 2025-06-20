import argparse
from core.hn_analyzer import HNAnalyzer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=24, help="分析时间范围")
    args = parser.parse_args()

    report = HNAnalyzer().generate_daily_report(args.hours)
    print(report)

if __name__ == "__main__":
    main()
