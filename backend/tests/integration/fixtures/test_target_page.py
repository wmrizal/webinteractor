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
