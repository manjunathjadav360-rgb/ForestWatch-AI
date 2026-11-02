from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def test_dashboard_starts_with_committed_snapshot():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=45).run()

    assert not app.exception, "\n".join(
        str(error.value) for error in app.exception
    )
    assert any(
        "ForestWatch AI" in str(element.value)
        for element in app.title
    )
    assert any(
        "Review tool, not an enforcement verdict" in str(element.value)
        for element in app.markdown
    )
