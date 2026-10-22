from database.db import init_db
from ui.movimiento_form import FinanzasApp


def main():
    init_db()
    FinanzasApp().run()


if __name__ == "__main__":
    main()