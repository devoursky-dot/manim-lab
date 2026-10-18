# 🌬️ manim-lab

> **Interactive Mathematical Visualization & Lecture Laboratory**  
> *Manim과 AI 보이스오버(TTS) 기반의 인터랙티브 수학 시각화 연구소*

[![Manim](https://img.shields.io/badge/Manim-v0.20.0-blue.svg)](https://www.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![Edge-TTS](https://img.shields.io/badge/Voiceover-Edge--TTS-orange.svg)](https://github.com/rany2/edge-tts)

---

## 📽️ Featured Lecture: 3D 바람 벡터장과 미적분의 직관적 이해 (v2)

> **"미분은 세상을 인식하는 방법이고, 적분은 그 순간들을 누적하는 흐름이다."**

눈에 보이지 않는 3차원 바람의 흐름을 통해 미분(순간변화율)과 적분(변화량의 누적)의 직관적 본질을 탐구합니다.  
한국어 AI 신경망 성우(`ko-KR-InJoonNeural`)의 해설 싱크에 맞추어 카메라 앵글과 3D 애니메이션이 정밀하게 동기화됩니다.

![3D 바람 벡터장과 미적분 v2 프리뷰](assets/wind_calculus_v2_preview.gif)

### 📌 수학적 모델링 & v2 교육적 개선점

1. **나뭇잎 줌인(Zoom-in)과 순간속도 포착 (미분)**:
   - 굽이치는 3D 나뭇잎 궤적을 찰나의 순간으로 확대하여 직선 방향의 접선 벡터 $\vec{v}(t) = \frac{d\vec{r}}{dt}$로 수렴함을 시각화
2. **이산($\Delta t$)에서 연속($dt$)으로의 3단계 적분 빌드업**:
   - 거친 꺾은선($\Delta t = 0.55\text{s}$) $\longrightarrow$ 촘촘한 꺾은선($\Delta t = 0.22\text{s}$) $\longrightarrow$ 매끄러운 유선($dt \to 0$)
   - 리만 합의 극한 $\lim_{\Delta t \to 0} \sum \vec{v}(t_i)\Delta t = \int_{0}^{T} \vec{v}(t)\,dt$의 필연성을 직관화
3. **바람의 3차원 연속 유선(Streamline) & 파티클 무리**:
   - 주 유선과 배경 유선들을 따라 흘러가는 다중 파티클을 통해 바람의 입체적 소용돌이 흐름 연출

---

## 🛠️ 설치 및 실행 (Getting Started)

### 1. 저장소 클론 및 패키지 설치
```bash
git clone https://github.com/devoursky-dot/manim-lab.git
cd manim-lab
pip install -r requirements.txt
```

### 2. 렌더링 실행
```bash
# v2 신규 버전 렌더링 (기본 480p15 빠른 모드)
./render.ps1

# v2 고화질 렌더링 (1080p60)
./render.ps1 -Quality qh

# 기존 v1 렌더링 실행
./render.ps1 -Version v1 -Quality qh
```

---

## 📁 디렉토리 구조

```text
manim-lab/
├── assets/                          # README 및 쇼케이스용 GIF / PNG
│   ├── wind_calculus_v2_preview.gif # v2 애니메이션 프리뷰
│   ├── WindCalculus3DLectureV2_final.png
│   ├── wind_calculus_preview.gif    # v1 애니메이션 프리뷰
│   └── WindCalculus3DLecture_final.png
├── core/                            # 공통 유틸리티 (Edge TTS 통합 모듈)
│   ├── __init__.py
│   └── edge_service.py
├── subtitles/                       # 동기화된 SRT 자막 파일
│   ├── WindCalculus3DLectureV2.srt  # v2 자막
│   └── WindCalculus3DLecture.srt    # v1 자막
├── wind_calculus_v2.py              # [v2] 줌인 & 단계적 적분 빌드업 개선 소스
├── wind_calculus.py                 # [v1] 원본 소스 코드 (보존)
├── render.ps1                       # 버전별 간편 렌더링 스크립트
├── requirements.txt                 # 필수 의존성 목록
└── README.md                        # 프로젝트 안내 문서
```

---

## 🔗 연계 프로젝트
- **[manim-app](https://github.com/devoursky-dot/manim-app)**: 웹 기반 인터랙티브 수학 그래프 & 판서 플랫폼
- **[LBWTEST](https://github.com/devoursky-dot/LBWTEST)**: 전자칠판 스마트 수업 드라이브 포털
