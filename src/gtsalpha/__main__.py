"""Entry point for ``python -m gtsalpha``."""

from gtsalpha.gui.app import App


def main() -> None:
    """Launch the GtsAlpha Caption Pro GUI."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
