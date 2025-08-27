#!/usr/bin/env python3
def hex_to_srgb(hex: str) -> tuple[float]:
    r = int(hex[1:3], base=16) / 255.0
    g = int(hex[3:5], base=16) / 255.0
    b = int(hex[5:7], base=16) / 255.0
    return r, g, b

def rgb_to_srgb(rgb: tuple[float]) -> tuple[float]:
    r, g, b = rgb
    return r / 255.0, g / 255.0, b / 255.0

def rgb_to_hex(color: str | tuple[float]) -> str:
    if isinstance(color, str):
        return color
    else:
        r, g, b = color
        return '#{:02x}{:02x}{:02x}'.format(round(r), round(g), round(h))
    
def adjust_srgb(color: str | tuple[float]) -> tuple[float]:
    r, g, b = hex_to_srgb(color) if isinstance(color, str) else rgb_to_srgb(color)
    r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
    return r, g, b

def relative_luminance(color: str | tuple[float]) -> float:
    r, g, b = adjust_srgb(color)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(color_1: str | tuple[float], color_2: str | tuple[float]) -> float:
    l_1 = relative_luminance(color_1)
    l_2 = relative_luminance(color_2)
    return (max(l_1, l_2) + 0.05) / (min(l_1, l_2) + 0.05)

def wcag_compliance(color_1: str | tuple[float], color_2: str | tuple[float]) -> None:
    ratio = contrast_ratio(color_1, color_2)
    print('Contrast checker with inputs', rgb_to_hex(color_1), 'and', rgb_to_hex(color_2))
    print('- Non-bold text < 18pt OR bold text < 14pt')
    print('  - WCAG AA (>= 4.5:1)', '✓' if ratio >= 4.5 else '✗')
    print('  - WCAG AAA (>= 7:1)', '✓' if ratio >= 7 else '✗')
    print('- Non-bold text >= 18pt OR bold text >= 14pt')
    print('  - WCAG AA (>= 3:1)', '✓' if ratio >= 3 else '✗')
    print('  - WCAG AAA (>= 4.5:1)', '✓' if ratio >= 4.5 else '✗')