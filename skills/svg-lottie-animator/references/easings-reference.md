# Easing Function Reference (easings.net)

This document provides definitive cubic-bezier values for all standard easing functions from [easings.net](https://easings.net/zh-cn), optimized for Lottie's `o` (out) and `i` (in) properties.

## Lottie Easing Usage
In Lottie JSON, cubic-bezier points are split between keyframes:
- `o`: The outgoing tangent of the *current* keyframe.
- `i`: The incoming tangent of the *next* keyframe.
- Value format: `{"x": [cp1x], "y": [cp1y]}` etc.

---

## Ease Tables

| Easing Name | Out (o) `[x, y]` | In (i) `[x, y]` | Visual Description |
| :--- | :--- | :--- | :--- |
| **easeInSine** | `[0.12, 0]` | `[0.39, 0]` | Start very slowly, linear-like end |
| **easeOutSine** | `[0.61, 1]` | `[0.88, 1]` | Smoothly decelerates at the very end |
| **easeInOutSine** | `[0.37, 0]` | `[0.63, 1]` | Balanced and subtle |
| **easeInQuad** | `[0.11, 0]` | `[0.5, 0]` | Acceleration proportional to t^2 |
| **easeOutQuad** | `[0.5, 1]` | `[0.89, 1]` | Deceleration proportional to t^2 |
| **easeInOutQuad** | `[0.45, 0]` | `[0.55, 1]` | Good all-rounder |
| **easeInCubic** | `[0.32, 0]` | `[0.67, 0]` | Stronger acceleration |
| **easeOutCubic** | `[0.33, 1]` | `[0.68, 1]` | Clear deceleration |
| **easeInOutCubic** | `[0.65, 0]` | `[0.35, 1]` | Smooth start and end |
| **easeInQuart** | `[0.5, 0]` | `[0.75, 0]` | Powerful rush out |
| **easeOutQuart** | `[0.25, 1]` | `[0.5, 1]` | Sudden ease into rest |
| **easeInOutQuart** | `[0.76, 0]` | `[0.24, 1]` | Sharp middle transition |
| **easeInQuint** | `[0.64, 0]` | `[0.78, 0]` | Extreme acceleration |
| **easeOutQuint** | `[0.22, 1]` | `[0.36, 1]` | Extremely smooth rest |
| **easeInOutQuint** | `[0.83, 0]` | `[0.17, 1]` | High contrast movement |
| **easeInExpo** | `[0.7, 0]` | `[0.84, 0]` | Instant burst |
| **easeOutExpo** | `[0.16, 1]` | `[0.3, 1]` | Snap into place |
| **easeInOutExpo** | `[0.87, 0]` | `[0.13, 1]` | Dramatic "teleport" effect |
| **easeInCirc** | `[0.55, 0]` | `[1, 0.45]` | Slow start, sudden end |
| **easeOutCirc** | `[0, 0.55]` | `[0.45, 1]` | Sudden start, slow end |
| **easeInOutCirc** | `[0.85, 0]` | `[0.15, 1]` | Symmetric circular curve |
| **easeInBack** | `[0.36, 0]` | `[0.66, -0.56]` | Pulls back before moving |
| **easeOutBack** | `[0.34, 1.56]` | `[0.64, 1]` | Over shoots then settles |
| **easeInOutBack** | `[0.68, -0.6]` | `[0.32, 1.6]` | Pulls back AND overshoots |

---

## Complex Easings (Approximation)

These cannot be represented by a single cubic-bezier. Use these multi-point strategies:

### Bounce (easeOutBounce)
Use a 4-keyframe sequence:
1. `t:0, s:0, o:[0.33, 0], i:[0.67, 1]`
2. `t:12, s:1, o:[0.33, 0], i:[0.67, 1]` (Impact)
3. `t:18, s:0.92, o:[0.33, 0], i:[0.67, 1]` (Small bounce)
4. `t:24, s:1` (Rest)

### Elastic (easeOutElastic)
Requires 5-7 keyframes of damped oscillation.
Recommended: Use the `Damped Oscillation` pattern in [bezier-easing.md](file:///Users/user/Desktop/Skill%E4%B8%93%E7%94%A8/AI%20Lottie%E5%B7%A5%E5%85%B7/references/bezier-easing.md).
