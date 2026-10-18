# 🌬️ manim-lab

> **Interactive Mathematical Visualization & Lecture Laboratory**  
> *Manim과 AI 보이스오버(TTS) 기반의 인터랙티브 수학 시각화 연구소*

[![Manim](https://img.shields.io/badge/Manim-v0.20.0-blue.svg)](https://www.manim.community/)
[![Python](https://img.shields.io/badge/Python-3.12-brightgreen.svg)](https://www.python.org/)
[![Edge-TTS](https://img.shields.io/badge/Voiceover-Edge--TTS-orange.svg)](https://github.com/rany2/edge-tts)

---

## 📽️ Featured Lecture: 3D 바람 벡터장과 미적분의 직관적 이해

> **"미분은 세상을 인식하는 방법이고, 적분은 그 순간들을 누적하는 흐름이다."**

눈에 보이지 않는 3차원 바람의 흐름을 통해 미분(순간변화율)과 적분(변화량의 누적)의 직관적 본질을 탐구합니다.  
한국어 AI 신경망 성우(`ko-KR-InJoonNeural`)의 해설 싱크에 맞추어 카메라 앵글과 3D 애니메이션이 정밀하게 동기화됩니다.

![3D 바람 벡터장과 미적분 프리뷰](assets/wind_calculus_preview.gif)

### 📌 수학적 모델링 & 시각화 흐름

1. **3차원 비선형 바람 벡터장 (3D Vector Field)**:
   $$\vec{v}(x, y, z) = \begin{pmatrix} -0.6y + 0.4 \\ 0.6x + 0.2 \\ 0.35\cos(0.5x) \end{pmatrix}$$
2. **순간변화율 = 미분**:
   공간에 흩날리는 나뭇잎 파티클의 순간 속도 벡터 $\vec{v}(t) = \frac{d\vec{r}}{dt}$
3. **순간변화량 = 미소 변위**:
   짧은 시간 간격 $dt$ 동안의 위치 변화 $d\vec{r} = \vec{v}(t) \cdot dt$
4. **순간변화량의 누적 = 적분 (유선, Streamline)**:
   미소 변위들의 적분을 통해 전체 바람의 유선 형성 $\vec{r}(T) - \vec{r}(0) = \int_{0}^{T} \vec{v}(t)\,dt$

---

## 🛠️ 설치 및 환경 구성 (Getting Started)

### 1. 저장소 클론 및 패키지 설치
```bash
git clone https://github.com/devoursky-dot/manim-lab.git
cd manim-lab
pip install -r requirements.txt
```

### 2. 렌더링 실행
```bash
# 빠른 미리보기 (480p15)
manim -ql wind_calculus.py WindCalculus3DLecture

# 고화질 렌더링 (1080p60)
manim -qh wind_calculus.py WindCalculus3DLecture

# 원클릭 스크립트 실행 (PowerShell)
./render.ps1 -Quality qh
```

---

## 📁 디렉토리 구조

```text
manim-lab/
├── assets/                  # README 및 쇼케이스용 GIF / PNG
│   ├── wind_calculus_preview.gif
│   └── WindCalculus3DLecture_final.png
├── core/                    # 공통 유틸리티 (Edge TTS 통합 모듈)
│   ├── __init__.py
│   └── edge_service.py
├── subtitles/               # 동기화된 SRT 자막 파일
│   └── WindCalculus3DLecture.srt
├── wind_calculus.py         # 3D 바람과 미적분 강의 메인 소스 코드
├── render.ps1               # 간편 렌더링 스크립트
├── requirements.txt         # 필수 의존성 목록
└── README.md                # 프로젝트 안내 문서
```

---

## 🔗 연계 프로젝트
- **[manim-app](https://github.com/devoursky-dot/manim-app)**: 웹 기반 인터랙티브 수학 그래프 & 판서 플랫폼
- **[LBWTEST](https://github.com/devoursky-dot/LBWTEST)**: 전자칠판 스마트 수업 드라이브 포털
