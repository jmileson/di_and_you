import pytest

from di_and_you.db import make_connection

HTML_BODY = """
<table class="matrix">
<tr xmlns="http://www.w3.org/1999/xhtml">
  <th>Nr.
  </th>
  <th>Name
  </th>
  <th>Spectral Range
  </th>
  <th>Bands
  </th>
  <th>Specific Formula
  </th>
  <th>Calculated
  </th>
  <th>Comment
  </th>
</tr>
<tr xmlns="http://www.w3.org/1999/xhtml">
  <td>1
  </td>
  <td><a href="/db/s-single.php?id=90">AHS</a>
  </td>
  <td>428.5-13140
  </td>
  <td><a href="/db/bs.php?sensor_id=90">80</a>
  </td>
  <td>
    <span class="MathJax_Preview"></span>
      <span class="MJX_Assistive_MathML" role="presentation">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
          <mrow>
            <mrow>
              <mrow>
                <mo>(</mo>
                <mrow>
                  <mrow>
                    <mn>1</mn>
                    <mo>+</mo>
                    <mn>0.16</mn>
                  </mrow>
                </mrow>
                <mo>)</mo>
              </mrow>
              <mo>⁢</mo>
              <mfrac>
                <mrow>
                  <mrow>
                    <mrow>
                      <mi mathcolor="#443399">13</mi>
                      <mo>-</mo>
                      <mi mathcolor="#443399">9</mi>
                    </mrow>
                  </mrow>
                </mrow>
                <mrow>
                  <mrow>
                    <mrow>
                      <mi mathcolor="#443399">13</mi>
                      <mo>+</mo>
                      <mrow>
                        <mi mathcolor="#443399">9</mi>
                        <mo>+</mo>
                        <mn>0.16</mn>
                      </mrow>
                    </mrow>
                  </mrow>
                </mrow>
              </mfrac>
            </mrow>
          </mrow>
        </math>
      </span>
    </span>
  </td>
  <td>Automatic
  </td>
  <td>
  </td>
</tr>
</table>
"""


@pytest.fixture()
def test_conn():
    conn = make_connection(":memory:")
    yield conn
    conn.close()


@pytest.fixture()
def html_body():
    return HTML_BODY
