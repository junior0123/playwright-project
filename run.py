import subprocess


def run_pytest():
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    print("Output of pytest:")
    print(result.stdout)
    if result.stderr:
        print("Errors in pytest:")
        print(result.stderr)


def run_analyze_data():
    from utils.analyze_data import main
    main()


def main():
    run_pytest()
    run_analyze_data()


if __name__ == "__main__":
    main()
