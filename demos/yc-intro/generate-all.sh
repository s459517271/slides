#!/bin/bash
# YC Introduction Demo - Generate all 11 styles
# Run this after: infsh login

set -e

OUTPUT_DIR="/Users/ajtoy/retro-pop-ppt/demos/yc-intro/images"
mkdir -p "$OUTPUT_DIR"

echo "=========================================="
echo "YC Introduction Demo Generator"
echo "11 Styles × 2 Languages = 22 Images"
echo "=========================================="

# Function to generate image
generate() {
    local style=$1
    local lang=$2
    local title=$3
    local subtitle=$4
    local extra=$5
    local output="$OUTPUT_DIR/${style}-${lang}.png"

    echo ""
    echo "🎨 Generating: $style ($lang)"

    infsh app run falai/flux-dev-lora --input "{
  \"prompt\": \"$style style PPT slide, 16:9 aspect ratio, Title: $title, Subtitle: $subtitle, $extra, Professional presentation design\",
  \"aspect_ratio\": \"16:9\"
}" --save "${output%.png}.json"

    echo "✅ Done: $output"
}

# English content
TITLE_EN="What is Y Combinator"
SUBTITLE_EN="The Worlds Most Famous Startup Accelerator"
STATS_EN="2005 founded | 4000+ companies | \$600B+ valuation"

# Chinese content
TITLE_CN="什么是 Y Combinator"
SUBTITLE_CN="全球最著名的创业加速器"
STATS_CN="2005 年成立 | 4000+ 公司 | \$600B+ 估值"

echo ""
echo ">>> Starting English versions..."

# 1. Retro Pop
generate "retro-pop-art" "en" "$TITLE_EN" "$SUBTITLE_EN" "cream background, thick black outlines, salmon pink sky blue mustard yellow accents, geometric decorations quarter circles star bursts, 1970s magazine aesthetic"

# 2. Minimal
generate "minimalist-clean" "en" "$TITLE_EN" "$SUBTITLE_EN" "white background, generous whitespace, thin lines, subtle gray and blue accents, Inter Helvetica font, corporate aesthetic"

# 3. Cyberpunk
generate "cyberpunk-neon" "en" "$TITLE_EN" "$SUBTITLE_EN" "dark background #0D0D1A, neon glow effects, magenta cyan yellow neon colors, tech grid patterns, circuit decorations, holographic panels, futuristic UI"

# 4. Neo-Brutalism
generate "neo-brutalism" "en" "$TITLE_EN" "$SUBTITLE_EN" "cream background, bold primary colors red blue yellow, thick 4px black outlines, hard shadows, brutalist frames, Archivo Black font"

# 5. Acid Graphics
generate "acid-graphics-Y2K" "en" "$TITLE_EN" "$SUBTITLE_EN" "light gray background, metallic chrome elements, holographic accents, purple pink mint gold colors, liquid shapes, star sparkles, mesh gradients"

# 6. Modern Minimal Pop
generate "modern-minimal-pop" "en" "$TITLE_EN" "$SUBTITLE_EN" "pastel background, mint coral cream purple colors, star burst graphics, thin line circles, tilted color blocks, small arrows, Swiss design influence"

# 7. Swiss International
generate "Swiss-international" "en" "$TITLE_EN" "$SUBTITLE_EN" "light gray background, bold geometric color blocks, diagonal typography, high saturation blue green yellow purple pink orange, Helvetica font, asymmetric composition"

# 8. Dark Editorial
generate "dark-editorial" "en" "$TITLE_EN" "$SUBTITLE_EN" "black background with white dot grid pattern, white text, orange accent, minimalist wireframe, serif typography Georgia style, dramatic negative space, newspaper aesthetic"

# 9. Design Blueprint
generate "design-blueprint-Figma" "en" "$TITLE_EN" "$SUBTITLE_EN" "white background, cyan grid lines, Figma selection boxes with control points, annotation lines, numbered labels, technical UI mockup aesthetic"

# 10. Neo-Brutalist UI
generate "neo-brutalist-UI" "en" "$TITLE_EN" "$SUBTITLE_EN" "cream background, pastel panels mint yellow lavender, thick 3px black outlines, card-based layout, flat colors, stat cards, SaaS dashboard aesthetic"

# 11. Y2K Pixel Retro
generate "Y2K-pixel-retro-90s" "en" "$TITLE_EN" "$SUBTITLE_EN" "dark background with noise texture, bright yellow orange green colors, pixel art computer icons, CRT monitor graphics, isometric tech, VT323 pixel font, vintage 1990s"

echo ""
echo ">>> Starting Chinese versions..."

generate "retro-pop-art" "cn" "$TITLE_CN" "$SUBTITLE_CN" "cream background, thick black outlines, salmon pink sky blue mustard yellow accents, geometric decorations, 1970s magazine aesthetic"

generate "minimalist-clean" "cn" "$TITLE_CN" "$SUBTITLE_CN" "white background, generous whitespace, thin lines, subtle gray and blue accents, Inter Helvetica font, corporate aesthetic"

generate "cyberpunk-neon" "cn" "$TITLE_CN" "$SUBTITLE_CN" "dark background, neon glow effects, magenta cyan yellow neon colors, tech grid patterns, circuit decorations, holographic panels"

generate "neo-brutalism" "cn" "$TITLE_CN" "$SUBTITLE_CN" "cream background, bold primary colors, thick 4px black outlines, hard shadows, brutalist frames"

generate "acid-graphics-Y2K" "cn" "$TITLE_CN" "$SUBTITLE_CN" "light gray background, metallic chrome elements, holographic accents, liquid shapes, star sparkles, mesh gradients"

generate "modern-minimal-pop" "cn" "$TITLE_CN" "$SUBTITLE_CN" "pastel background, mint coral cream purple colors, star burst graphics, thin line circles, Swiss design influence"

generate "Swiss-international" "cn" "$TITLE_CN" "$SUBTITLE_CN" "light gray background, bold geometric color blocks, diagonal typography, high saturation colors, Helvetica font"

generate "dark-editorial" "cn" "$TITLE_CN" "$SUBTITLE_CN" "black background with white dot grid, white text, orange accent, minimalist wireframe, serif typography, newspaper aesthetic"

generate "design-blueprint-Figma" "cn" "$TITLE_CN" "$SUBTITLE_CN" "white background, cyan grid lines, Figma selection boxes, annotation lines, technical UI mockup"

generate "neo-brutalist-UI" "cn" "$TITLE_CN" "$SUBTITLE_CN" "cream background, pastel panels, thick 3px black outlines, card-based layout, stat cards"

generate "Y2K-pixel-retro-90s" "cn" "$TITLE_CN" "$SUBTITLE_CN" "dark background with noise, bright colors, pixel art computers, CRT monitors, vintage 1990s design"

echo ""
echo "=========================================="
echo "✅ Generation Complete!"
echo "Output: $OUTPUT_DIR"
echo "=========================================="
