from pathlib import Path
import re
from html import escape

# --------------------------------------------------
# Settings
# --------------------------------------------------

ISSUES_DIR = Path("issues")
OUTPUT_FILE = Path("index.html")


# --------------------------------------------------
# Find all newspaper issues
# --------------------------------------------------

issues = []

for pdf in ISSUES_DIR.glob("*.pdf"):
    match = re.search(r"(\d+)", pdf.stem)

    if match:
        number = int(match.group(1))
    else:
        number = 0

    issues.append({
        "number": number,
        "filename": pdf.name
    })


# Newest issue first
issues.sort(key=lambda x: x["number"], reverse=True)


# --------------------------------------------------
# Determine latest issue
# --------------------------------------------------

if issues:
    latest = issues[0]
else:
    latest = None


# --------------------------------------------------
# Create an issue card
# --------------------------------------------------

def issue_card(issue):
    return f"""
    <div class="issue">
        <h3>Issue #{issue["number"]}</h3>

        <a href="issues/{escape(issue["filename"])}">
            Read Issue
        </a>
    </div>
    """


# --------------------------------------------------
# Build Latest Issue section
# --------------------------------------------------

if latest:

    # Everything except the newest issue
    previous_issues = issues[1:]

    # Create cards for previous issues
    previous_html = "\n".join(
        issue_card(issue)
        for issue in previous_issues
    )

    # Display the newest PDF on the homepage
    # Desktop: show PDF
    # Mobile: show an "Open Issue" button
    latest_html = f"""
    <section class="latest">

        <h2>Latest Issue</h2>

        <h3>Issue #{latest["number"]}</h3>

        <div class="pdf-viewer">

            <iframe
                src="issues/{escape(latest["filename"])}"
                title="The News Weekly - Issue #{latest["number"]}">
            </iframe>

            <div class="mobile-pdf-message">

                <p>
                    Reading on a phone?
                </p>

                <a
                    class="button"
                    href="issues/{escape(latest["filename"])}"
                    target="_blank">
                    Open Issue #{latest["number"]}
                </a>

            </div>

        </div>

        <p class="desktop-open-button">
            <a
                class="button"
                href="issues/{escape(latest["filename"])}"
                target="_blank">
                Open Full Issue
            </a>
        </p>

    </section>
    """

else:

    latest_html = """
    <section class="latest">

        <h2>Latest Issue</h2>

        <p>
            The first issue will be published soon.
        </p>

    </section>
    """

    previous_html = ""


# --------------------------------------------------
# Create the complete website
# --------------------------------------------------

html = f"""<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0">

    <title>The News Weekly</title>

    <style>

        /* ------------------------------------------
           Page
           ------------------------------------------ */

        body {{
            max-width: 900px;
            margin: auto;
            padding: 40px 20px;
            font-family: Georgia, serif;
            background: #f7f3ea;
            color: #222;
        }}


        /* ------------------------------------------
           Header
           ------------------------------------------ */

        header {{
            text-align: center;
            border-bottom: 4px solid #222;
            padding-bottom: 20px;
        }}

        h1 {{
            font-size: 3rem;
            margin-bottom: 5px;
        }}

        header p {{
            font-style: italic;
        }}


        /* ------------------------------------------
           Sections
           ------------------------------------------ */

        section {{
            margin-top: 40px;
        }}


        /* ------------------------------------------
           Latest Issue
           ------------------------------------------ */

        .latest {{
            text-align: center;
            padding: 35px;
            border: 2px solid #222;
            background: white;
        }}


        /* ------------------------------------------
           PDF Viewer
           ------------------------------------------ */

        .pdf-viewer {{
            margin-top: 25px;
            width: 100%;
        }}

        .pdf-viewer iframe {{
            width: 100%;
            height: 900px;
            border: 1px solid #ccc;
            background: white;
        }}


        /* ------------------------------------------
           Buttons
           ------------------------------------------ */

        .button {{
            display: inline-block;
            padding: 12px 20px;
            background: #222;
            color: white;
            text-decoration: none;
            margin-top: 10px;
        }}


        /* ------------------------------------------
           Mobile PDF Message
           ------------------------------------------ */

        .mobile-pdf-message {{
            display: none;
        }}


        /* ------------------------------------------
           Previous Issues
           ------------------------------------------ */

        .issues {{
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
        }}

        .issue {{
            background: white;
            border: 1px solid #ccc;
            padding: 20px;
        }}

        .issue h3 {{
            margin-top: 0;
        }}

        .issue a {{
            color: #222;
        }}


        /* ------------------------------------------
           Footer
           ------------------------------------------ */

        footer {{
            margin-top: 60px;
            text-align: center;
            border-top: 1px solid #ccc;
            padding-top: 20px;
        }}


        /* ------------------------------------------
           Mobile Layout
           ------------------------------------------ */

        @media (max-width: 700px) {{

            body {{
                padding: 25px 15px;
            }}

            h1 {{
                font-size: 2.3rem;
            }}

            .latest {{
                padding: 20px;
            }}

            /* Hide PDF viewer on phones */
            .pdf-viewer iframe {{
                display: none;
            }}

            /* Show mobile message */
            .mobile-pdf-message {{
                display: block;
                padding: 30px 10px;
            }}

            /* Hide desktop button on phones */
            .desktop-open-button {{
                display: none;
            }}

            /* One issue per row */
            .issues {{
                grid-template-columns: 1fr;
            }}

        }}

    </style>

</head>


<body>

    <!-- Header -->

    <header>

        <h1>The News Weekly</h1>

        <p>
            Our neighborhood's weekly newspaper
        </p>

    </header>


    <!-- Latest Issue -->

    {latest_html}


    <!-- Previous Issues -->

    <section>

        <h2>Previous Issues</h2>

        <div class="issues">

            {previous_html}

        </div>

    </section>


    <!-- Footer -->

    <footer>

        <p>
            The News Weekly
        </p>

    </footer>

</body>

</html>
"""


# --------------------------------------------------
# Write index.html
# --------------------------------------------------

OUTPUT_FILE.write_text(
    html,
    encoding="utf-8"
)


# --------------------------------------------------
# Show information in GitHub Actions
# --------------------------------------------------

print("======================================")
print("Website generated successfully!")
print("======================================")

print(f"Found {len(issues)} issue(s).")

if latest:
    print(
        f"Latest issue: #{latest['number']} "
        f"({latest['filename']})"
    )
else:
    print("No issues found.")

print(f"Created: {OUTPUT_FILE}")
