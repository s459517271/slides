#!/usr/bin/env python3
"""
Generate YC Introduction Demo Images for all 11 styles
Uses nanobanana2 2k model via inference.sh CLI
"""

import subprocess
import json
from pathlib import Path

# YC content for slides
YC_CONTENT = {
    "title_en": "What is Y Combinator?",
    "title_cn": "什么是 Y Combinator？",
    "subtitle_en": "The World's Most Famous Startup Accelerator",
    "subtitle_cn": "全球最著名的创业加速器",
    "stats": "Founded 2005 • 4000+ Companies • $600B+ Valuation",
    "stats_cn": "2005 年成立 • 4000+ 公司 • $600B+ 估值",
}

# All 11 styles with their prompts
STYLES = [
    {
        "name": "retro-pop",
        "display": "Retro Pop Art",
        "prompt": """
Retro pop art style PPT slide, 1970s magazine aesthetic,
flat design with thick 3px black outlines,
cream beige background #F5F0E6,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Stats cards: "2005" "4000+" "$600B+",
Salmon pink #FF6B6B, sky blue #4ECDC4, mustard yellow #FFD93D, mint green #6BCB77,
Geometric decorations: quarter circles, concentric rings, star bursts,
Bold sans-serif typography,
Clean grid layout, no gradients, no shadows,
Professional PPT slide, presentation design,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "minimal",
        "display": "Minimalist Clean",
        "prompt": """
Minimalist clean design PPT slide,
White background #FFFFFF, generous whitespace,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Stats: "2005 • 4000+ • $600B+",
Subtle gray accents #F8F9FA, #343A40, blue #007BFF,
Thin 1px lines, clean sans-serif typography,
Inter / Helvetica font style,
Professional corporate aesthetic,
Simple data cards, elegant layout,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "cyberpunk",
        "display": "Cyberpunk Neon",
        "prompt": """
Cyberpunk neon style PPT slide,
Dark background #0D0D1A,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Neon glow text effects,
Neon colors: magenta #FF00FF, cyan #00FFFF, yellow #FFFF00,
Tech grid patterns, circuit decorations,
Holographic data panels, glow effects,
Futuristic UI elements, scanlines,
Digital presentation aesthetic,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "neo-brutalism",
        "display": "Neo-Brutalism",
        "prompt": """
Neo-brutalism style PPT slide, raw design,
Cream background #FFF8E7,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Bold primary colors: red #FF4D4D, blue #4D94FF, yellow #FFD93D,
Thick 4px black outlines, hard shadows,
Brutalist frames, bold typography,
Stark contrast, unpolished aesthetic,
Archivo Black font style,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "acid-graphics",
        "display": "Acid Graphics Y2K",
        "prompt": """
Acid graphics Y2K style PPT slide,
Light gray background #E8E8E8,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Metallic chrome elements, holographic accents,
Colors: purple #B185FF, pink #FF6EC7, mint #7BFFCB, gold #FFD700,
Liquid shapes, star sparkles, mesh gradients,
Y2K aesthetic, futuristic design,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "modern-minimal-pop",
        "display": "Modern Minimal Pop",
        "prompt": """
Modern minimal pop art PPT slide, Instagram aesthetic,
Dark charcoal #1A1A1A or pastel background,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Pastel colors: mint #A8E6C8, cream #FFF4BD, coral #FF8B7A, purple #8B7AFF,
Star burst graphics, thin line circles,
Tilted color blocks, small L-shaped arrows,
Clean sans-serif typography, lowercase style,
Swiss design influence, contemporary,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "swiss-international",
        "display": "Swiss International",
        "prompt": """
Swiss international style PPT slide, brutalist graphic design,
Light gray background #E5E5E5,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Bold geometric color blocks, diagonal typography,
High saturation: blue #007AFF, green #00994D, yellow #FFF066, purple #9966FF, pink #FF3399, orange #FF8800,
Helvetica style clean sans-serif,
Asymmetric composition, Japanese contemporary design,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "dark-editorial",
        "display": "Dark Editorial",
        "prompt": """
Dark editorial PPT slide, New York Times Sunday Review style,
Black background #0A0A0F with white dot grid pattern,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
White text, orange accent #E85D2A,
Minimalist wireframe illustrations,
Serif typography, Georgia style,
Dramatic negative space, sophisticated,
Newspaper supplement aesthetic,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "design-blueprint",
        "display": "Design Blueprint",
        "prompt": """
Design blueprint PPT slide, Figma documentation style,
White background, cyan grid lines #66B8CC,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Figma selection boxes with control points,
Annotation lines, numbered labels,
Technical UI/UX mockup aesthetic,
Clean sans-serif Inter font,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "neo-brutalist-ui",
        "display": "Neo-Brutalist UI",
        "prompt": """
Neo-brutalist UI PPT slide, dashboard interface,
Cream background #F5F0E6,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Pastel panels: mint #A8E4CF, yellow #FFD93D, lavender #E5B3FF,
Thick 3px black outlines #1A1A1A,
Card-based layout, flat colors,
Bold typography, stat cards,
Contemporary SaaS dashboard aesthetic,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
    {
        "name": "y2k-pixel-retro",
        "display": "Y2K Pixel Retro",
        "prompt": """
Y2K pixel retro PPT slide, 90s aesthetic,
Dark background #2D2D2D with noise texture,
Title: "{title_en}" / "{title_cn}",
Subtitle: "{subtitle}",
Bright colors: yellow #FFD700, orange #FF8C00, green #4A7C4E,
Pixel art computer icons, CRT monitor graphics,
Isometric tech illustrations,
VT323 / pixel font style,
Vintage 1990s design,
--ar 16:9 --style raw --v 6 --q 2
""".strip(),
    },
]


def generate_image(style_data, output_dir, lang="en"):
    """Generate image using inference.sh CLI"""
    prompt = style_data["prompt"].format(
        title_en=YC_CONTENT["title_en"] if lang == "en" else YC_CONTENT["title_cn"],
        title_cn=YC_CONTENT["title_cn"],
        subtitle=YC_CONTENT["subtitle_en"] if lang == "en" else YC_CONTENT["subtitle_cn"],
    )

    output_path = output_dir / f"{style_data['name']}_{lang}.png"

    # Use inference.sh / nanobanana2
    cmd = [
        "infsh",
        "gen",
        "--model", "nanobanana2",
        "--prompt", prompt,
        "--aspect", "16:9",
        "--quality", "2",
        "--output", str(output_path)
    ]

    print(f"\n🎨 Generating: {style_data['display']} ({lang})")
    print(f"Output: {output_path}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ Success: {output_path}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    output_dir = Path("/Users/ajtoy/retro-pop-ppt/demos/yc-intro/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("YC Introduction Demo Generator")
    print("11 Styles × 2 Languages = 22 Images")
    print("=" * 60)

    # Generate for both English and Chinese
    for lang in ["en", "cn"]:
        print(f"\n>>> Language: {'English' if lang == 'en' else '中文'}")

        for style in STYLES:
            generate_image(style, output_dir, lang)

    print("\n" + "=" * 60)
    print("Generation Complete!")
    print(f"Output directory: {output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
