import subprocess


def run_pytest():
    result = subprocess.run(["pytest"], capture_output=True, text=True)
    print("Output of pytest:")
    print(result.stdout)
    if result.stderr:
        print("Errors in pytest:")
        print(result.stderr)


def run_analyze_data():
    # Importa y ejecuta la función main de tu script AnalyzeData
    from utils.analyze_data import main  # Reemplaza 'tu_script' con el nombre correcto del archivo que contiene la función main
    main()


def main():
    # Ejecuta pytest y espera a que termine
    run_pytest()

    # Ejecuta AnalyzeData después de que pytest haya terminado
    run_analyze_data()


if __name__ == "__main__":
    main()
