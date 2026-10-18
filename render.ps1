param(
    [string]$Quality = "ql" # ql (480p15, 빠름), qm (720p30), qh (1080p60, 고화질)
)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🌬️ manim-lab: WindCalculus3DLecture Rendering" -ForegroundColor Cyan
Write-Host "Quality: -$Quality" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

manim -$Quality wind_calculus.py WindCalculus3DLecture
