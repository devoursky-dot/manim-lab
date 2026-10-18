# 🌬️ manim-lab

> **Interactive Mathematical Visualization & Lecture Laboratory**  
> *3Blue1Brown 스타일과 엄밀한 수학 교육을 결합한 인터랙티브 수학 시각화 연구소*

[![Manim](https://img.shields.io/badge/Manim-v0.20.0-blue.svg)](https://www.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![Edge-TTS](https://img.shields.io/badge/Voiceover-Edge--TTS-orange.svg)](https://github.com/rany2/edge-tts)

---

## 📽️ Featured Lecture: 3D 바람 벡터장과 미적분의 직관적 이해 (v3 Masterpiece)

> **"미분은 세상을 인식하는 방법이고, 적분은 그 순간들을 누적하는 흐름이다."**

눈에 보이지 않는 3차원 바람의 흐름을 통해 미분(순간변화율, 국소 선형화), 회전(Curl, 소용돌이 패들휠), 적분(미소 변위의 누적, 연속 유선)의 직관적 본질을 탐구합니다.  
한국어 AI 신경망 성우(`ko-KR-InJoonNeural`)의 해설 싱크에 맞추어 카메라 앵글과 3D 애니메이션이 정밀하게 동기화됩니다.

![3D 바람 벡터장과 미적분 v3 프리뷰](assets/wind_calculus_v3_preview.gif)

### 📌 v3 핵심 시각화 및 교육적 특징

1. **순수 딥 블랙 캔버스 (`#000000`)**:
   - 모니터 경계를 허물고 무한한 명암비로 발광하는 수학 객체와 수식에 최고의 집중도 제공
2. **소용돌이를 감지하는 회전 패들휠 (Paddlewheel for Curl)**:
   - 바람의 유속 차이가 만드는 토크로 인해 실시간 회전하는 패들휠을 통해 공간의 회전($\text{Curl}(\vec{v}) = \nabla \times \vec{v}$)을 직관화
3. **국소 선형화 (Local Linearization)**:
   - 복잡하게 굽이치는 나뭇잎 궤적을 찰나의 순간($\Delta t \to 0$)으로 줌인하여 직선 접선 벡터 $\vec{v}(t) = \frac{d\vec{r}}{dt}$로 수렴함을 시각화
4. **리만 합에서 연속 유선으로의 3단계 승화**:
   - 거친 꺾은선($\Delta t = 0.60\text{s}$) $\longrightarrow$ 촘촘한 꺾은선($\Delta t = 0.22\text{s}$) $\longrightarrow$ 매끄러운 유선($dt \to 0$)
5. **충분한 인지적 여백 (Cognitive Soak-in Time)**:
   - 서두르지 않고 핵심 수식과 전환마다 2.0 ~ 3.0초의 침묵과 음미 시간을 배정 (총 101초 러닝타임, 26개 시퀀스)

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
# v3 마스터피스 렌더링 (기본 480p15 빠른 모드)
./render.ps1

# v3 고화질 렌더링 (1080p60)
./render.ps1 -Quality qh

# 이전 버전 실행 (v1, v2)
./render.ps1 -Version v2 -Quality qh
./render.ps1 -Version v1 -Quality qh
```

---

## 📁 디렉토리 구조

```text
manim-lab/
├── assets/                          # README 및 쇼케이스용 GIF / PNG
│   ├── wind_calculus_v3_preview.gif # 🌟 v3 마스터피스 프리뷰
│   ├── WindCalculus3DLectureV3_final.png
│   ├── wind_calculus_v2_preview.gif # v2 프리뷰
│   ├── wind_calculus_preview.gif    # v1 프리뷰
│   └── fluid_3b1b_preview.gif       # 3b1b 유체역학 프로토타입 프리뷰
├── core/                            # 공통 유틸리티 (Edge TTS 통합 모듈)
│   ├── __init__.py
│   └── edge_service.py
├── docs/                            # 공식 설계 시스템 및 매뉴얼
│   ├── manim_lecture_design_system_manual.md # 강의 시각화 표준 & 피드백 로그
│   └── 3b1b_fluid_visualization_manual.md   # 3b1b 유체역학 시각화 매뉴얼
├── subtitles/                       # 동기화된 SRT 자막 파일
│   ├── WindCalculus3DLectureV3.srt  # 🌟 v3 자막
│   ├── WindCalculus3DLectureV2.srt  # v2 자막
│   └── WindCalculus3DLecture.srt    # v1 자막
├── wind_calculus_v3.py              # 🌟 [v3] 마스터피스 소스 코드 (블랙 캔버스, 패들휠, 인지적 여백)
├── wind_calculus_v2.py              # [v2] 줌인 & 단계적 수렴 소스 코드 (보존)
├── wind_calculus.py                 # [v1] 초기 원본 소스 코드 (보존)
├── fluid_mechanics_sample.py        # 3b1b 유체역학 프로토타입 코드
├── render.ps1                       # 버전별 간편 렌더링 스크립트
├── requirements.txt                 # 필수 의존성 목록
└── README.md                        # 프로젝트 안내 문서
```

---

## 🔗 연계 프로젝트
- **[manim-app](https://github.com/devoursky-dot/manim-app)**: 웹 기반 인터랙티브 수학 그래프 & 판서 플랫폼
- **[LBWTEST](https://github.com/devoursky-dot/LBWTEST)**: 전자칠판 스마트 수업 드라이브 포털
