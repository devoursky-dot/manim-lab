param(
    [string]$Version = "v3", # v1, v2 또는 v3 선택 (기본: v3 Masterpiece)
    [string]$Quality = "ql"  # ql (480p15), qm (720p30), qh (1080p60)
)

if ($Version -eq "v1") {
    $file = "wind_calculus.py"
    $scene = "WindCalculus3DLecture"
} elseif ($Version -eq "v2") {
    $file = "wind_calculus_v2.py"
    $scene = "WindCalculus3DLectureV2"
} else {
    $file = "wind_calculus_v3.py"
    $scene = "WindCalculus3DLectureV3"
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🌬️ manim-lab: $scene Rendering ($file)" -ForegroundColor Cyan
Write-Host "Quality: -$Quality" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

manim -$Quality $file $scene
