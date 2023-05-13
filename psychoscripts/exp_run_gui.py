# Here we define a GUI for running experiments using the scripts defined in utils.py.

import os
from pathlib import Path

from PyQt5.QtWidgets import (
    QComboBox,
    QGridLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QWidget,
)


class ExperimentRunner(QWidget):
    """GUI for running experiments defined in utils.py."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._available_experiments = self.look_for_experiments()

        self._initUI()

    def _initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Grid layout is a 2x2 grid, with the top row being the mouse name and experiment name,
        # and the bottom row being the run button.

        # Add a text box for the mouse name:
        self.mouse_label = QLabel("Mouse:")
        self.grid.addWidget(self.mouse_label, 0, 0)

        self.mouse_id_edit = QTextEdit("Mouse")
        self.grid.addWidget(self.mouse_id_edit, 0, 1)

        self.exp_label = QLabel("Experiment:")
        self.grid.addWidget(self.exp_label, 1, 0)

        self.exp_combo = QComboBox()
        self.exp_combo.addItems(self._available_experiments.keys())
        self.grid.addWidget(self.exp_combo, 1, 1)

        self.run_button = QPushButton("Run")
        self.grid.addWidget(self.run_button, 2, 0, 1, 2)

        self.run_button.clicked.connect(self.run_exp)

        self.show()

    def run_exp(self) -> None:
        """Run the experiment selected in the combobox."""
        exp_name = self.exp_combo.currentText()
        exp_script = self._available_experiments[exp_name]

        # Run the experiment with the mouse name as an argument
        mouse_id = self.mouse_id_edit.toPlainText()
        term_line = f"MOUSE_ID={mouse_id} python {exp_script}"
        os.system(term_line)

    def look_for_experiments(self) -> dict:
        """Find all runnable .py scripts in bricks.

        Returns:
            dict: Dictionary of experiment names and paths to the scripts.
        """

        experiments = dict()
        utils_location = Path(__file__).parent / "bricks"

        for f in utils_location.glob("*.py"):
            if f.stem != "__init__":
                experiments[f.stem] = f
        return experiments


if __name__ == "__main__":
    import sys

    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ex = ExperimentRunner()
    sys.exit(app.exec_())
