from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QActionGroup, QColor, QDesktopServices, QIcon, QKeySequence
from PySide6.QtWidgets import (
    QApplication,
    QDockWidget,
    QFrame,
    QGraphicsDropShadowEffect,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QTextBrowser,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app_paths import app_root
from .calculation_tabs import ExpressionWorkspace, PolynomialWorkspace, RadicalWorkspace


APP_ROOT = app_root()
ICON_DIR = APP_ROOT / "resources" / "icons"
WEBSITE_DIR = APP_ROOT / "website"
WEBSITE_README = WEBSITE_DIR / "README.md"
ORG_URL = "https://github.com/Quick-Red-Tech"


WORKSPACE_GUIDES = {
    "Polynomial": """
        <h3>Polynomial Mode</h3>
        <p>Best for equations built from separate power-rule terms.</p>
        <ul>
            <li>Use it for expressions like <code>4x^3 - 2x + 1</code>.</li>
            <li>Add terms one at a time and let the workspace manage the signs.</li>
            <li>Constants automatically disappear in the derivative.</li>
        </ul>
        <p><b>Shortcut:</b> Ctrl+1 switches here.</p>
    """,
    "Roots": """
        <h3>Root Mode</h3>
        <p>Best for guided square-root and cube-root equations with a linear inside term.</p>
        <ul>
            <li>Use it for expressions like <code>sqrt(x) - 3</code> or <code>cbrt(x + 2)</code>.</li>
            <li>The app rewrites radicals as fractional powers before differentiating.</li>
            <li>The inner slope is included automatically.</li>
        </ul>
        <p><b>Shortcut:</b> Ctrl+2 switches here.</p>
    """,
    "Expressions": """
        <h3>Expressions Mode</h3>
        <p>Best for worksheet-style questions that mix several patterns in one typed expression.</p>
        <ul>
            <li>Use it for <code>4*x - 1/x^2</code>, <code>(x - 1)^5</code>, or <code>2*x^4 + sqrt(x)</code>.</li>
            <li>Supports <code>^</code> or <code>**</code> for powers, plus <code>sqrt(...)</code> and <code>cbrt(...)</code>.</li>
            <li>Only the variable <code>x</code> is supported in this mode.</li>
        </ul>
        <p><b>Shortcut:</b> Ctrl+3 switches here.</p>
    """,
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickRed Tech Differentiator")
        self.resize(1320, 900)
        self.setMinimumSize(1120, 800)
        self.setWindowIcon(self._icon("logo.png"))

        self._setup_ui()
        self._create_status_widgets()
        self._create_help_dock()
        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bar()
        self._connect_events()
        self._apply_styles()
        self._handle_tab_changed(self.tabs.currentIndex())
        self.statusBar().showMessage("Choose a workspace and build a derivative problem.", 5000)

    def _setup_ui(self):
        central = QWidget()
        central.setObjectName("WindowRoot")
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(28, 20, 28, 24)
        root_layout.setSpacing(20)

        header_card = self._build_header_card()
        self._add_shadow(header_card, blur_radius=34, y_offset=14)
        root_layout.addWidget(header_card)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("WorkspaceTabs")

        self.polynomial_tab = PolynomialWorkspace()
        self.radical_tab = RadicalWorkspace()
        self.expression_tab = ExpressionWorkspace()

        self.tabs.addTab(self.polynomial_tab, "Polynomial")
        self.tabs.addTab(self.radical_tab, "Roots")
        self.tabs.addTab(self.expression_tab, "Expressions")

        root_layout.addWidget(self.tabs, 1)

    def _build_header_card(self):
        frame = QFrame()
        frame.setObjectName("HeaderCard")

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        title = QLabel("Differentiation Workspace")
        title.setObjectName("HeroTitle")

        subtitle = QLabel(
            "Version 1 now separates structured polynomial work, guided radical equations, and broader worksheet-style typed expressions."
        )
        subtitle.setObjectName("HeroSubtitle")
        subtitle.setWordWrap(True)

        help_text = QLabel(
            "Use Polynomial for multi-term powers, Roots for guided sqrt/cbrt forms, and Expressions for mixed questions like 4x - 1/x^2, (x - 1)^5, or 2x^4 + sqrt(x)."
        )
        help_text.setObjectName("HeaderHelp")
        help_text.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(help_text)
        return frame

    def _create_status_widgets(self):
        self.workspace_badge = QLabel()
        self.workspace_badge.setObjectName("StatusBadge")
        self.workspace_badge.setMinimumWidth(180)

        self.status_hint = QLabel("Ctrl+Enter solves the current workspace")
        self.status_hint.setObjectName("StatusHint")

        self.statusBar().addPermanentWidget(self.status_hint)
        self.statusBar().addPermanentWidget(self.workspace_badge)

    def _create_help_dock(self):
        self.help_dock = QDockWidget("Workspace Guide", self)
        self.help_dock.setObjectName("GuideDock")
        self.help_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.help_dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetClosable)

        self.guide_browser = QTextBrowser()
        self.guide_browser.setObjectName("GuideBrowser")
        self.guide_browser.setOpenExternalLinks(True)

        self.help_dock.setWidget(self.guide_browser)
        self.addDockWidget(Qt.RightDockWidgetArea, self.help_dock)

    def _create_actions(self):
        self.solve_action = QAction(self._icon("differentiate.png"), "Solve Current Workspace", self)
        self.solve_action.setShortcut(QKeySequence("Ctrl+Return"))
        self.solve_action.triggered.connect(self._solve_current_workspace)

        self.reset_action = QAction(self._icon("add.png"), "Reset Current Workspace", self)
        self.reset_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        self.reset_action.triggered.connect(self._reset_current_workspace)

        self.open_website_folder_action = QAction("Open Website Folder", self)
        self.open_website_folder_action.triggered.connect(self._open_website_folder)

        self.open_website_readme_action = QAction("Open Website README", self)
        self.open_website_readme_action.triggered.connect(self._open_website_readme)

        self.open_quickred_github_action = QAction("Open Quick Red Tech on GitHub", self)
        self.open_quickred_github_action.triggered.connect(self._open_quickred_github)

        self.toggle_guide_action = QAction("Show Workspace Guide", self)
        self.toggle_guide_action.setCheckable(True)
        self.toggle_guide_action.setChecked(True)
        self.toggle_guide_action.setShortcut(QKeySequence("Ctrl+G"))
        self.toggle_guide_action.toggled.connect(self.help_dock.setVisible)

        self.quick_start_action = QAction("Quick Start", self)
        self.quick_start_action.triggered.connect(self._show_quick_start)

        self.supported_inputs_action = QAction("Supported Inputs", self)
        self.supported_inputs_action.triggered.connect(self._show_supported_inputs)

        self.about_action = QAction("About QuickRed Tech Differentiator", self)
        self.about_action.setShortcut(QKeySequence("F1"))
        self.about_action.triggered.connect(self._show_about_dialog)

        self.about_qt_action = QAction("About Qt", self)
        self.about_qt_action.triggered.connect(QApplication.aboutQt)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut(QKeySequence.Quit)
        self.exit_action.triggered.connect(self.close)

        self.tab_action_group = QActionGroup(self)
        self.tab_action_group.setExclusive(True)
        self.workspace_actions = []

        for index, label, shortcut in (
            (0, "Polynomial", "Ctrl+1"),
            (1, "Roots", "Ctrl+2"),
            (2, "Expressions", "Ctrl+3"),
        ):
            action = QAction(label, self)
            action.setCheckable(True)
            action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(lambda checked=False, value=index: self.tabs.setCurrentIndex(value))
            self.tab_action_group.addAction(action)
            self.workspace_actions.append(action)

    def _create_menu_bar(self):
        file_menu = self.menuBar().addMenu("File")
        file_menu.addAction(self.solve_action)
        file_menu.addAction(self.reset_action)
        file_menu.addSeparator()
        file_menu.addAction(self.open_website_folder_action)
        file_menu.addAction(self.open_website_readme_action)
        file_menu.addAction(self.open_quickred_github_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        workspace_menu = self.menuBar().addMenu("Workspace")
        for action in self.workspace_actions:
            workspace_menu.addAction(action)

        view_menu = self.menuBar().addMenu("View")
        view_menu.addAction(self.toggle_guide_action)

        help_menu = self.menuBar().addMenu("Help")
        help_menu.addAction(self.quick_start_action)
        help_menu.addAction(self.supported_inputs_action)
        help_menu.addAction(self.open_quickred_github_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)
        help_menu.addAction(self.about_qt_action)

    def _create_tool_bar(self):
        toolbar = QToolBar("Primary")
        toolbar.setObjectName("PrimaryToolbar")
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        toolbar.addAction(self.solve_action)
        toolbar.addAction(self.reset_action)
        toolbar.addSeparator()
        for action in self.workspace_actions:
            toolbar.addAction(action)
        toolbar.addSeparator()
        toolbar.addAction(self.toggle_guide_action)
        toolbar.addAction(self.about_action)
        toolbar.addAction(self.open_quickred_github_action)

        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def _connect_events(self):
        self.help_dock.visibilityChanged.connect(self.toggle_guide_action.setChecked)
        self.tabs.currentChanged.connect(self._handle_tab_changed)

        for workspace in (self.polynomial_tab, self.radical_tab, self.expression_tab):
            workspace.status_message.connect(self.statusBar().showMessage)

    def _current_workspace(self):
        return self.tabs.currentWidget()

    def _solve_current_workspace(self):
        workspace = self._current_workspace()
        if hasattr(workspace, "solve_workspace"):
            workspace.solve_workspace()

    def _reset_current_workspace(self):
        workspace = self._current_workspace()
        if hasattr(workspace, "reset_workspace"):
            workspace.reset_workspace()
            self.statusBar().showMessage(f"{workspace.workspace_title} workspace reset.", 3500)

    def _handle_tab_changed(self, index: int):
        current_text = self.tabs.tabText(index)

        for action_index, action in enumerate(self.workspace_actions):
            action.setChecked(action_index == index)

        self.workspace_badge.setText(f"Workspace: {current_text}")
        self.guide_browser.setHtml(WORKSPACE_GUIDES.get(current_text, "<p>Select a workspace.</p>"))
        self.statusBar().showMessage(f"Switched to {current_text} workspace.", 2500)

    def _show_quick_start(self):
        QMessageBox.information(
            self,
            "Quick Start",
            (
                "<b>QuickRed Tech Differentiator</b><br><br>"
                "1. Choose a workspace tab based on the problem type.<br>"
                "2. Enter the equation using the guided builder or typed-expression field.<br>"
                "3. Click <b>Solve Current Workspace</b> or press <b>Ctrl+Enter</b>.<br>"
                "4. Review the equation, normalized power-rule form, and derivative result.<br><br>"
                "Use the guide dock on the right for syntax reminders."
            ),
        )

    def _show_supported_inputs(self):
        QMessageBox.information(
            self,
            "Supported Inputs",
            (
                "<b>Polynomial</b><br>"
                "Use separate terms like ax^n, constants, and negative powers.<br><br>"
                "<b>Roots</b><br>"
                "Use guided equations of the form a * root(mx + b) + c.<br><br>"
                "<b>Expressions</b><br>"
                "Supports <code>^</code> or <code>**</code>, <code>sqrt(...)</code>, <code>cbrt(...)</code>, "
                "parentheses, shifted powers, and reciprocal powers with variable <code>x</code>."
            ),
        )

    def _show_about_dialog(self):
        QMessageBox.about(
            self,
            "About QuickRed Tech Differentiator",
            (
                "<b>QuickRed Tech Differentiator</b><br>"
                "Version 1 desktop workspace for teaching and exploring differentiation with the power rule.<br><br>"
                "<b>Included workspaces</b><br>"
                "Polynomial builder, guided radical equations, and mixed typed expressions.<br><br>"
                "<b>Desktop shell</b><br>"
                "Menu bar, toolbar, status bar, workspace guide, and marketing-site companion project."
            ),
        )

    def _open_website_folder(self):
        if not WEBSITE_DIR.exists():
            QDesktopServices.openUrl(QUrl(ORG_URL))
            return

        QDesktopServices.openUrl(QUrl.fromLocalFile(str(WEBSITE_DIR)))

    def _open_website_readme(self):
        if not WEBSITE_README.exists():
            QDesktopServices.openUrl(QUrl(ORG_URL))
            return

        QDesktopServices.openUrl(QUrl.fromLocalFile(str(WEBSITE_README)))

    def _open_quickred_github(self):
        QDesktopServices.openUrl(QUrl(ORG_URL))

    def _icon(self, name: str) -> QIcon:
        path = ICON_DIR / name
        if path.exists():
            return QIcon(str(path))
        return QIcon()

    def _add_shadow(self, widget, blur_radius: int = 26, y_offset: int = 10):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur_radius)
        shadow.setOffset(0, y_offset)
        shadow.setColor(QColor(15, 37, 64, 28))
        widget.setGraphicsEffect(shadow)

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QWidget#WindowRoot {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f4f8fc,
                    stop: 0.52 #ecf3fb,
                    stop: 1 #e2ecf7
                );
            }

            QMenuBar {
                background: rgba(255, 255, 255, 0.88);
                border: 1px solid #d7e1ee;
                border-radius: 12px;
                padding: 4px 8px;
                color: #102a43;
            }

            QMenuBar::item {
                padding: 8px 12px;
                margin: 2px 4px;
                border-radius: 10px;
            }

            QMenuBar::item:selected {
                background: #e6f0fb;
            }

            QMenu {
                background: #ffffff;
                border: 1px solid #d7e1ee;
                border-radius: 14px;
                padding: 8px;
                color: #102a43;
            }

            QMenu::item {
                padding: 8px 16px;
                border-radius: 10px;
            }

            QMenu::item:selected {
                background: #eaf3fc;
            }

            QToolBar#PrimaryToolbar {
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #d7e1ee;
                border-radius: 16px;
                spacing: 10px;
                padding: 8px 10px;
            }

            QToolBar#PrimaryToolbar QToolButton {
                background: transparent;
                border: 1px solid transparent;
                border-radius: 12px;
                padding: 8px 12px;
                color: #102a43;
                font-size: 13px;
                font-weight: 600;
            }

            QToolBar#PrimaryToolbar QToolButton:hover,
            QToolBar#PrimaryToolbar QToolButton:checked {
                background: #e6f0fb;
                border-color: #c5d7ea;
            }

            QFrame#HeaderCard {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #102a43,
                    stop: 0.54 #0f4c81,
                    stop: 1 #1368aa
                );
                border: 1px solid #0b365d;
                border-radius: 28px;
            }

            QFrame#Card {
                background: rgba(255, 255, 255, 0.98);
                border: 1px solid #d7e1ee;
                border-radius: 24px;
            }

            QFrame#PreviewCard {
                background: #f6faff;
                border: 1px solid #dbe6f3;
                border-radius: 18px;
            }

            QScrollArea#ColumnScrollArea,
            QWidget#ScrollColumn {
                background: transparent;
                border: none;
            }

            QLabel {
                color: #102a43;
                font-size: 14px;
            }

            QLabel#HeroTitle {
                color: #f8fbff;
                font-size: 31px;
                font-weight: 700;
            }

            QLabel#HeroSubtitle {
                color: #dbe9f7;
                font-size: 15px;
            }

            QLabel#HeaderHelp {
                color: #f8fbff;
                background: rgba(248, 251, 255, 0.12);
                border: 1px solid rgba(248, 251, 255, 0.16);
                border-radius: 16px;
                padding: 10px 14px;
                font-size: 13px;
            }

            QLabel#CardTitle {
                font-size: 20px;
                font-weight: 700;
                color: #0b2239;
            }

            QLabel#SectionLabel {
                font-size: 13px;
                font-weight: 700;
                color: #486581;
                text-transform: uppercase;
            }

            QLabel#PreviewValue,
            QLabel#ResultValue,
            QTextEdit#PreviewValue,
            QTextEdit#ResultValue {
                background: #fbfdff;
                border: 1px solid #d7e3f0;
                border-radius: 16px;
                padding: 14px 16px;
                color: #0b2239;
                font-size: 15px;
                font-weight: 600;
                font-family: "Cambria Math", "Segoe UI Symbol", "Segoe UI";
            }

            QTextEdit#PreviewValue,
            QTextEdit#ResultValue {
                selection-background-color: #d9e9fb;
                selection-color: #0b2239;
            }

            QLabel#MutedText,
            QLabel#StatusHint {
                color: #627d98;
                font-size: 13px;
            }

            QLabel#StatusBadge {
                background: #d24d2f;
                color: #ffffff;
                border-radius: 12px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 700;
            }

            QLineEdit,
            QComboBox,
            QListWidget,
            QTextEdit {
                background: #f8fbff;
                color: #102a43;
                border: 1px solid #c9d8e6;
                border-radius: 14px;
                padding: 11px 13px;
                selection-background-color: #d9e9fb;
                selection-color: #0b2239;
            }

            QLineEdit:focus,
            QComboBox:focus,
            QListWidget:focus,
            QTextEdit:focus {
                border: 2px solid #0f4c81;
                background: #ffffff;
            }

            QComboBox::drop-down {
                border: none;
                width: 28px;
            }

            QListWidget::item {
                padding: 10px 8px;
                border-bottom: 1px solid #ebf1f7;
            }

            QListWidget::item:selected {
                background: #deebfb;
                color: #0b2239;
                border-radius: 10px;
            }

            QPushButton {
                border-radius: 16px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#PrimaryButton {
                background: #0f4c81;
                color: #ffffff;
                border: 1px solid #0b3c66;
            }

            QPushButton#PrimaryButton:hover {
                background: #0b3c66;
            }

            QPushButton#SecondaryButton {
                background: #edf4fb;
                color: #102a43;
                border: 1px solid #d0dceb;
            }

            QPushButton#SecondaryButton:hover {
                background: #e2edf8;
            }

            QPushButton#DangerButton {
                background: #fff3ec;
                color: #b45309;
                border: 1px solid #f7cbb4;
            }

            QPushButton#DangerButton:hover {
                background: #ffe8dc;
            }

            QPushButton:disabled {
                background: #e8eef5;
                color: #90a4b8;
                border: 1px solid #d7e1ee;
            }

            QTabWidget::pane {
                border: 1px solid #d7e1ee;
                border-radius: 22px;
                background: rgba(255, 255, 255, 0.35);
                top: -1px;
            }

            QTabBar::tab {
                background: rgba(237, 244, 251, 0.92);
                color: #486581;
                border: 1px solid #d0dceb;
                border-bottom: none;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                padding: 12px 22px;
                margin-right: 8px;
                min-width: 140px;
                font-size: 14px;
                font-weight: 600;
            }

            QTabBar::tab:selected {
                background: #ffffff;
                color: #0f4c81;
            }

            QTabBar::tab:hover:!selected {
                background: #e6f0fb;
            }

            QDockWidget {
                color: #102a43;
                font-weight: 700;
            }

            QDockWidget::title {
                background: rgba(255, 255, 255, 0.94);
                border: 1px solid #d7e1ee;
                border-bottom: none;
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                padding: 10px 14px;
            }

            QTextBrowser#GuideBrowser {
                background: rgba(255, 255, 255, 0.97);
                border: 1px solid #d7e1ee;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
                padding: 14px;
                color: #102a43;
                line-height: 1.5;
            }

            QStatusBar {
                background: #102a43;
                color: #f8fbff;
                border-top: 1px solid #0b365d;
            }

            QStatusBar::item {
                border: none;
            }

            QStatusBar QLabel {
                color: #f8fbff;
            }

            QMessageBox {
                background: #fffaf4;
            }

            QMessageBox QLabel {
                color: #102a43;
                min-width: 340px;
            }

            QMessageBox QPushButton {
                min-width: 110px;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 12px;
                margin: 6px 2px 6px 2px;
            }

            QScrollBar::handle:vertical {
                background: #c1d4e8;
                min-height: 28px;
                border-radius: 6px;
            }

            QScrollBar::handle:vertical:hover {
                background: #9fbddb;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical,
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical,
            QScrollBar:horizontal,
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal,
            QScrollBar::add-page:horizontal,
            QScrollBar::sub-page:horizontal {
                background: transparent;
                border: none;
                width: 0px;
                height: 0px;
            }
            """
        )
