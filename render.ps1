param(
    [string]$Version = "v4", # v1, v2, v3, v4 선택 (기본: v4 변화량 vs 변화율 혁신 버전)
    [string]$Quality = "ql"  # ql (480p15), qm (720p30), qh (1080p60)
)

if ($Version -eq "v1") {
    $file = "wind_calculus.py"
    $scene = "WindCalculus3DLecture"
} elseif ($Version -eq "v2") {
    $file = "wind_calculus_v2.py"
    $scene = "WindCalculus3DLectureV2"
} elseif ($Version -eq "v3") {
    $file = "wind_calculus_v3.py"
    $scene = "WindCalculus3DLectureV3"
} else {
    $file = "wind_calculus_v4.py"
    $scene = "WindCalculus3DLectureV4"
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "🌬️ manim-lab: $scene Rendering ($file)" -ForegroundColor Cyan
Write-Host "Quality: -$Quality" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

manim -$Quality $file $scene
