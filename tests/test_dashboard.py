from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_starts_with_committed_snapshot():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=45).run()

    # A clean AppTest run means the page loaded without a Streamlit exception.
    assert len(app.exception) == 0, "\\n".join(
        str(error.value) for error in app.exception
    )
