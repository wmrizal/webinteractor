from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

TARGET_PAGE_HTML = """
<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <title>Feature Toggle Test Target</title>
  </head>
  <body>
    <main>
      <h1 id=\"feature-name\">Checkout flag</h1>
      <p id=\"feature-state\" aria-checked=\"false\">off</p>
      <button id=\"feature-toggle\" type=\"button\">Toggle feature</button>
    </main>
    <script>
      const stateNode = document.getElementById("feature-state");
      const toggleButton = document.getElementById("feature-toggle");
      toggleButton.addEventListener("click", () => {
        const isOn = stateNode.textContent === "on";
        stateNode.textContent = isOn ? "off" : "on";
        stateNode.setAttribute("aria-checked", String(!isOn));
      });
    </script>
  </body>
</html>
"""


@pytest.fixture()
def target_page_file(tmp_path: Path) -> Path:
    page_path = tmp_path / "target-page.html"
    page_path.write_text(textwrap.dedent(TARGET_PAGE_HTML).strip(), encoding="utf-8")
    return page_path


@pytest.fixture()
def target_page_url(target_page_file: Path) -> str:
    return target_page_file.resolve().as_uri()


@pytest.fixture()
def target_page_factory(tmp_path: Path):
  def _build(initial_state: str = "off") -> str:
    normalized_state = "on" if initial_state == "on" else "off"
    aria_checked = "true" if normalized_state == "on" else "false"
    customized_html = textwrap.dedent(TARGET_PAGE_HTML).replace(
      '<p id="feature-state" aria-checked="false">off</p>',
      f'<p id="feature-state" aria-checked="{aria_checked}">{normalized_state}</p>',
    )
    page_path = tmp_path / f"target-page-{normalized_state}.html"
    page_path.write_text(customized_html.strip(), encoding="utf-8")
    return page_path.resolve().as_uri()

  return _build
