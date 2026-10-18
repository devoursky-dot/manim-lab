# 🌬️ manim-lab

> **Interactive Mathematical Visualization & Lecture Laboratory**  
> *3Blue1Brown 스타일과 엄밀한 수학 교육을 결합한 인터랙티브 수학 시각화 연구소*

[![Manim](https://img.shields.io/badge/Manim-v0.20.0-blue.svg)](https://www.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![Edge-TTS](https://img.shields.io/badge/Voiceover-Edge--TTS-orange.svg)](https://github.com/rany2/edge-tts)

---

## 📽️ Featured Lecture: 바람과 미적분 (v4: 변화량이 아닌 변화율을 보다)

> **"우리가 느끼는 것은 변화량이 아니라, 시간에 따른 '변화율'이다!"**

눈에 보이지 않는 3차원 바람의 흐름을 통해 미분(순간변화율, 국소 선형화)과 적분(변화량의 누적, 유선)의 직관적 본질을 탐구합니다.  
찰나를 본 나뭇잎($0.2\text{m}$ 이동)과 오래 본 나뭇잎($1.0\text{m}$ 이동)의 이동거리가 5배나 다른데도 왜 같은 바람으로 인지하는지, 시간 나눗셈을 통해 동일한 속도 벡터 $\vec{v}$로 일치하는 과정을 직관적으로 증명합니다.

![3D 바람 벡터장과 미적분 v4 프리뷰](assets/wind_calculus_v4_preview.gif)

### 📌 v4 핵심 교육 혁신

1. **변화량(Amount) vs 변화율(Rate)의 감각적 분리**:
   - 나뭇잎이 얼마나 멀리 갔는가(변화량)가 아니라, 얼마나 빠르게 변하는가(변화율)를 감각하는 인간의 인지 원리를 규명
2. **시간 나눗셈을 통한 속도 벡터 일치 연출 (Aha! Moment)**:
   - 길이가 5배 다르던 두 주황색 변화량 화살표가 각자의 시간($\Delta t$)으로 나누어지는 순간, 정확히 동일한 크기의 황금빛 순간속도 벡터($\vec{v} = 2\text{m/s}$)로 일치
3. **순수 딥 블랙 캔버스 (`#000000`) & 인지적 여백 (Soak-in Time)**:
   - 핵심 깨달음 구간마다 2.0 ~ 2.5초의 시각적 음미 시간을 두어 시청자의 완전한 인지 흡수 유도 (약 2분 풀버전)
4. **리만 합에서 연속 유선으로의 자연스러운 승화**:
   - 순간변화율들을 모아 전체 흐름을 완성하는 적분($\int \vec{v}\,dt$)으로 완벽한 스토리라인 종결

---

## 🛠️ 설치 및 실행 (Getting Started)

### 1. 저장소 클론 및 패키지 설치
```bash
git clone https://github.com/devoursky-dot/manim-lab.git
cd manim-lab
pip install -r requirements.txt
```

### 2. 원클릭 렌더링 실행
```bash
# v4 최신 버전 렌더링 (기본 480p15 빠른 모드)
./render.ps1

# v4 고화질 렌더링 (1080p60)
./render.ps1 -Quality qh

# 이전 버전 실행 (v1, v2, v3)
./render.ps1 -Version v3 -Quality qh
./render.ps1 -Version v2 -Quality qh
./render.ps1 -Version v1 -Quality qh
```

---

## 📁 디렉토리 구조

```text
manim-lab/
├── assets/                          # README 및 쇼케이스용 GIF / PNG
│   ├── wind_calculus_v4_preview.gif # 🌟 v4 변화량 vs 변화율 혁신 프리뷰
│   ├── WindCalculus3DLectureV4_final.png
│   ├── wind_calculus_v3_preview.gif # v3 프리뷰
│   ├── wind_calculus_v2_preview.gif # v2 프리뷰
│   └── wind_calculus_preview.gif    # v1 프리뷰
├── core/                            # 공통 유틸리티 (Edge TTS 통합 모듈)
│   ├── __init__.py
│   └── edge_service.py
├── docs/                            # 공식 설계 시스템 및 매뉴얼
│   ├── manim_lecture_design_system_manual.md # 강의 시각화 표준 & 피드백 로그
│   └── 3b1b_fluid_visualization_manual.md   # 3b1b 유체역학 시각화 매뉴얼
├── subtitles/                       # 동기화된 SRT 자막 파일
│   ├── WindCalculus3DLectureV4.srt  # 🌟 v4 자막
│   ├── WindCalculus3DLectureV3.srt  # v3 자막
│   └── WindCalculus3DLecture.srt    # v1 자막
├── wind_calculus_v4.py              # 🌟 [v4] 변화량 vs 변화율 핵심 직관화 완성본
├── wind_calculus_v3.py              # [v3] 블랙 캔버스 & 3D 유체 마스터피스 (보존)
├── wind_calculus_v2.py              # [v2] 줌인 & 단계적 수렴 소스 (보존)
├── wind_calculus.py                 # [v1] 초기 원본 소스 (보존)
├── render.ps1                       # 버전별 간편 렌더링 스크립트
├── requirements.txt                 # 필수 의존성 목록
└── README.md                        # 프로젝트 안내 문서
```

---

## 🔗 연계 프로젝트
- **[manim-app](https://github.com/devoursky-dot/manim-app)**: 웹 기반 인터랙티브 수학 그래프 & 판서 플랫폼
- **[LBWTEST](https://github.com/devoursky-dot/LBWTEST)**: 전자칠판 스마트 수업 드라이브 포털
