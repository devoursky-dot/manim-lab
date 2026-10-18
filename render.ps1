param(
    [string]$Version = "v2", # v1 또는 v2 선택
    [string]$Quality = "ql"  # ql (480p15), qm (720p30), qh (1080p60)
)

if ($Version -eq "v1") {
    $file = "wind_calculus.py"
    $scene = "WindCalculus3DLecture"
} else {
    $file = "wind_calculus_v2.py"
    $scene = "WindCalculus3DLectureV2"
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🌬️ manim-lab: $scene Rendering ($file)" -ForegroundColor Cyan
Write-Host "Quality: -$Quality" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

manim -$Quality $file $scene
