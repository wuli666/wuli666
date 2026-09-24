"""Render the "Contributing to" cards into assets/cards/, dark and light."""
import json
import os
import urllib.request
from html import escape

CARDS = [
    # repo, accent, one-liner, what I worked on
    ("vllm-project/vllm-omni", "#7aa2f7", "Omni-modality inference on vLLM",
     ["Step-Audio2", "Triton kernels", "Quantization"]),
    ("vllm-project/semantic-router", "#bb9af7", "Mixture-of-Models router for LLM inference",
     ["CPU inference", "Integration tests"]),
    ("google/langextract", "#9ece6a", "Structured extraction with LLMs",
     ["vLLM provider"]),
    ("NousResearch/hermes-agent", "#ff9e64", "The agent that grows with you",
     ["Feishu voice", "Kanban", "Aux client"]),
]
THEMES = {
    "": {"bg": "#1a1b27", "border": "none", "name": "#c0caf5", "text": "#a9b1d6", "muted": "#737aa2"},
    "-light": {"bg": "#ffffff", "border": "#d0d7de", "name": "#1f2328", "text": "#424a53", "muted": "#6e7781"},
}


def stars(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        n = json.load(resp)["stargazers_count"]
    return f"{n / 1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def card(repo, accent, blurb, tags, star_text, t):
    org, name = repo.split("/")
    x, chips = 24, []
    for tag in tags:
        w = 7.2 * len(tag) + 20
        chips.append(
            f'<rect x="{x}" y="86" width="{w:.0f}" height="22" rx="11" fill="{accent}" fill-opacity="0.16"/>'
            f'<text x="{x + w / 2:.0f}" y="101" class="chip" fill="{accent}">{escape(tag)}</text>'
        )
        x += w + 8

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="128" viewBox="0 0 420 128">
<style>
text{{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}}
.org{{font-size:12px;fill:{t['muted']}}} .name{{font-size:20px;font-weight:700;fill:{t['name']}}}
.blurb{{font-size:13px;fill:{t['text']}}} .meta{{font-size:12px;fill:{t['muted']}}}
.chip{{font-size:12px;font-weight:600;text-anchor:middle}}
.card{{animation:rise .6s ease-out both}} @keyframes rise{{from{{opacity:0;transform:translateY(6px)}}}}
</style>
<g class="card">
<rect x="0.5" y="0.5" width="419" height="127" rx="12" fill="{t['bg']}" stroke="{t['border']}"/>
<rect x="0.5" y="16" width="4" height="96" rx="2" fill="{accent}"/>
<text x="24" y="30" class="org">{escape(org)}</text>
<text x="24" y="54" class="name">{escape(name)}</text>
<text x="396" y="30" class="meta" text-anchor="end">★ {star_text}</text>
<text x="24" y="74" class="blurb">{escape(blurb)}</text>
{''.join(chips)}
</g>
</svg>
"""


os.makedirs("assets/cards", exist_ok=True)
for repo, *rest in CARDS:
    star_text = stars(repo)
    for suffix, theme in THEMES.items():
        with open(f"assets/cards/{repo.split('/')[1]}{suffix}.svg", "w") as f:
            f.write(card(repo, *rest, star_text, theme))
