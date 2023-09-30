#!/usr/bin/env python3

import subprocess
import json

releases = json.loads(subprocess.check_output("gh api -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' /repos/rameshvarun/openfst-python/releases", shell=True))

with open("index.html", "w") as output:
    output.write("""<!DOCTYPE html>
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
<body>
""")
                 
    for release in releases:
        output.write(f"<h1>{release['tag_name']}</h1>\n")
        output.write(f"<ul>\n")
        for asset in release["assets"]:
            url = asset["browser_download_url"]
            name = asset["name"]
            if url.endswith(".whl"):
                output.write(f"<li><a href='{url}'>{name}</a></li>\n")
        output.write(f"</ul>\n")

    output.write("""</body>
</html>""")