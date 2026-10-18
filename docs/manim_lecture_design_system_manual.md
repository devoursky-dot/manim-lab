# manim-lab 강의 시각화 디자인 시스템 & 기술 표준 매뉴얼
*(Manim Lecture Design System & Technical Specification Manual)*

> **문서 버전**: v1.0.0  
> **적용 대상**: `manim-lab` 내 모든 수학 강의 애니메이션 프로젝트  
> **목적**: 3Blue1Brown의 시각적 세련미와 한국 교육과정(평가원/수능)의 엄밀성을 결합하여, 강의 애니메이션의 **시각적 일관성**, **교육적 직관성**, **무결한 기술 안정성**을 보장하는 단일 표준 지침

---

## 1. 한글 표현 표준 (Korean Typography & Text Handling)

Manim은 기본적으로 영문 기반 LaTeX 렌더러를 사용하므로, 한글 텍스트를 다룰 때 가장 많은 컴파일 에러와 시각적 부조화가 발생합니다. 아래 수칙을 반드시 준수합니다.

### 1-1. 한글 폰트 스택 정의
* **기본 폰트**: `"Malgun Gothic"` (윈도우 기본 탑재, 호환성 100%)
* **프리미엄 폰트 (선택)**: `"Pretendard"`, `"Noto Sans KR"` (설치되어 있을 경우 최우선 사용)
* **표준 선언 패턴**:
  ```python
  FONT_KR = "Malgun Gothic"  # 파일 상단 상수 선언
  ```

### 1-2. 🚨 [절대 규칙] `MathTex` 내 한글 직접 입력 금지
* **문제점**: `MathTex(r"\text{미분} \frac{df}{dx}")`처럼 `MathTex` 내부에 한글을 포함하면, LaTeX dvisvgm 컴파일러가 CJK 폰트를 찾지 못해 **`ValueError: latex error converting to dvi`**가 발생하며 렌더링이 중단됩니다.
* **해결 원칙 (텍스트-수식 분리 결합 패턴)**:
  한글은 **`Text`**, 수식은 **`MathTex`**로 명확히 분리한 뒤 **`VGroup`**의 `arrange(RIGHT)`로 결합합니다.

  ```python
  # ❌ 금지 (컴파일 에러 발생)
  bad_title = MathTex(r"\text{순간속도 } \vec{v}(t) = \frac{d\vec{r} }{dt}")

  # ✅ 표준 패턴 (항상 안전하고 완벽한 렌더링)
  good_title = VGroup(
      Text("순간속도", font=FONT_KR, font_size=24, color="#4ADE80"),
      MathTex(r"\vec{v}(t) = \frac{d\vec{r} }{dt}", font_size=32, color="#FACC15"),
  ).arrange(RIGHT, buff=0.2)
  ```

### 1-3. 자막 및 안내 텍스트 레이아웃 표준
* **하단 고정 자막(HUD Subtitle)**:
  ```python
  sub_box = VGroup(
      Text("나뭇잎의 순간 움직임 포착 = 미분(순간변화율)", font=FONT_KR, font_size=22, color="#4ADE80"),
      formula_mobject,
  ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
  ```
* **가독성 확보를 위한 글자 크기 규격**:
  - 메인 타이틀: `font_size=28 ~ 32`
  - 소제목 / 상태 안내: `font_size=22 ~ 24`
  - 부가 설명 / 캡션: `font_size=16 ~ 18`

---

## 2. 수식 표현 표준 (Mathematical Formula & LaTeX Standards)

### 2-1. 🚨 [버그 예방] 연속 닫는 중괄호(`}}`) 공백 규칙
* **문제점**: Manim의 LaTeX 파서에서 분수 끝 중괄호가 닫힐 때(`\frac{d\vec{r}}{dt}}`) 내부 토큰 파싱 에러가 발생할 수 있습니다.
* **해결 원칙**: 분자 분모가 중괄호로 닫힐 때 분자 끝에 반드시 **한 칸 공백**을 둡니다.
  ```python
  # ❌ 잠재적 파싱 버그 위험
  MathTex(r"\frac{d\vec{r}}{dt}")

  # ✅ 표준 패턴 (공백 추가)
  MathTex(r"\frac{d\vec{r} }{dt}")
  ```

### 2-2. 의미론적 색상 결합 (Semantic Color Binding)
3Blue1Brown의 핵심 기법 중 하나는 **"수식의 변수 색상과 화면 속 객체의 색상을 1:1로 일치시키는 것"**입니다.
* 예: 화면의 **속도 화살표가 노란색**이면 수식의 **$\vec{v}(t)$도 노란색**이어야 합니다.
* 예: 화면의 **적분 유선이 하늘색**이면 수식의 **$\int \vec{v}\,dt$도 하늘색**이어야 합니다.

```python
# 수식 내 부분 색상 매핑
formula = MathTex(
    r"d\vec{r}", r"=", r"\vec{v}(t)", r"\cdot", r"dt"
)
formula.set_color_by_tex_to_color_map({
    r"d\vec{r}": "#FB923C",   # 미소 변위 (주황색)
    r"\vec{v}(t)": "#FACC15", # 순간 속도 (노란색)
    r"dt": "#94A3B8",         # 미소 시간 (연회색)
})
```

### 2-3. 기호 전환 표현 규격 ($\lim$, $\sum \to \int$)
이산에서 연속으로의 수렴을 설명할 때는 기호의 진화 과정을 한 줄에 명확히 표기합니다:
$$\Delta \vec{r} = \vec{v}(t) \cdot \Delta t \;\xrightarrow{\Delta t \to 0}\; d\vec{r} = \vec{v}(t)\,dt$$
$$\vec{r}(T) - \vec{r}(0) = \lim_{\Delta t \to 0} \sum \vec{v}(t_i)\Delta t = \int_{0}^{T} \vec{v}(t)\,dt$$

---

## 3. 함수의 그래프 및 좌표평면 표시 표준 (Coordinate Systems & Graphs)

우리 프로젝트는 **두 가지 테마(3b1b 다크 스튜디오 테마 / 수능 평가원 화이트 테마)**를 지원하며, 각 테마별로 엄격한 규격을 적용합니다.

### 3-1. 2D 좌표축 (`Axes`) 표준
* **3b1b 다크 모드**:
  ```python
  axes = Axes(
      x_range=[-4, 4, 1],
      y_range=[-3, 3, 1],
      x_length=8.0,
      y_length=6.0,
      axis_config={
          "color": "#475569",        # 튀지 않는 차분한 슬레이트 그레이
          "stroke_width": 1.5,
          "include_ticks": False,     # 불필요한 눈금 제거로 인지 부하 감소
          "include_tip": True,
          "tip_width": 0.16,
          "tip_height": 0.20,
      }
  )
  ```
* **평가원 시험지 모드**:
  - `camera.background_color = "#FFFFFF"`
  - `axis_config={"color": "#000000", "stroke_width": 2.0, "include_ticks": False}`
  - 원점 표기: `MathTex("O").next_to(axes.c2p(0, 0), DL, buff=0.12)`
  - 축 끝 라벨: $x$는 `axes.x_axis.get_end()`의 `DOWN`, $y$는 `axes.y_axis.get_end()`의 `LEFT`

### 3-2. 3D 좌표축 (`ThreeDAxes`) 표준
* 3D에서는 축이 시각을 방해하지 않도록 색상을 한 톤 낮춥니다 (`"#334155"`).
* 반드시 `set_camera_orientation(phi=65*DEGREES, theta=-45*DEGREES)`로 시작하여 3축($x, y, z$)의 직교 관계가 왜곡 없이 한눈에 들어오게 합니다.

### 3-3. 그래프 및 보조선 규격
* **함수 그래프 곡선**: `stroke_width=3.5` (배경과 뚜렷이 대비되는 굵기)
* **보조 투영 점선 (`DashedLine`)**:
  - 좌표값 투영 시 반드시 점선을 사용합니다.
  - `DashedLine(p_a, axes.c2p(x, 0), stroke_width=1.5, dash_length=0.08, color="#64748B")`
* **좌표 매핑의 철칙**: 모든 기하학적 요소의 위치는 하드코딩된 좌표 대신 항상 **`axes.c2p(x, y)` (Coordinates to Point)** 함수를 사용하여 좌표계와 완벽히 연동시킵니다.

---

## 4. 도형 및 유체역학 기하 객체 표준 (Geometric Shapes & Metaphors)

### 4-1. 화살표(Arrow) 규격
* 화살표 촉이 지나치게 커서 방향을 왜곡하지 않도록 `max_tip_length_to_length_ratio`를 제어합니다:
  ```python
  Arrow(
      start=p0, end=p1,
      buff=0,                      # 시작/끝점 유격 제거
      stroke_width=3.5,
      color="#FACC15",
      max_tip_length_to_length_ratio=0.22,  # 짧아져도 촉이 비대해지지 않음
  )
  ```

### 4-2. 파티클(Particle) 및 나뭇잎 객체
* 2D 점: `Dot(radius=0.06 ~ 0.08)`
* 3D 입자: `Dot3D(radius=0.07 ~ 0.11)`
* 회전 중심점: 패들휠이나 회전체의 중심에는 작은 고정 점(`Dot(radius=0.05, color=RED)`)을 두어 회전 축을 명확히 인지시킵니다.

---

## 5. 최신 트렌드 듀얼 테마 시스템 (Dual Theme Color Tokens)

| 토큰명 (Role) | 🌌 Studio Theme (3b1b 스타일) | 📄 Exam Theme (수능 평가원 스타일) | 의미 및 용도 |
| :--- | :--- | :--- | :--- |
| **`BG_COLOR`** | `"#0B1120"` (Deep Navy) | `"#FFFFFF"` (Pure White) | 배경색 |
| **`AXIS_COLOR`** | `"#334155"` (Muted Slate) | `"#000000"` (Solid Black) | 좌표축 선 |
| **`TEXT_PRIMARY`** | `"#F8FAFC"` (Pure White) | `"#000000"` (Solid Black) | 주 텍스트 / 제목 |
| **`TEXT_MUTED`** | `"#94A3B8"` (Cool Slate) | `"#4B5563"` (Mid Gray) | 설명 자막 / 단위 |
| **`VECTOR_TANGENT`** | `"#FACC15"` (Vibrant Amber) | `"#000000"` (or `#D97706`) | 속도 벡터, 접선, 미분 |
| **`STREAM_LINE`** | `"#38BDF8"` (Electric Cyan) | `"#2563EB"` (Deep Blue) | 유선, 적분 곡선 |
| **`PARTICLE_DOT`** | `"#4ADE80"` (Spring Mint) | `"#059669"` (Dark Green) | 관찰 나뭇잎, 유체 입자 |
| **`ACCENT_ALERT`** | `"#F87171"` (Coral Red) | `"#DC2626"` (Red) | 소용돌이 중심, 경고, 싱크 |

---

## 6. 오디오 싱크 및 3D 카메라 연출 수칙 (Audio Sync & Camera Dynamics)

### 6-1. `tracker.duration` 기반의 완벽한 오디오 싱크 공식
AI 음성 길이는 발음 속도에 따라 가변적이므로, 애니메이션 시간에 하드코딩된 상수를 단독으로 사용하면 음성과 영상이 어긋납니다.
* **표준 싱크 공식**:
  ```python
  with self.voiceover(text="...") as tracker:
      # 1단계: 선행 애니메이션 (전체 음성 길이를 초과하지 않도록 min 사용)
      anim_time = min(2.5, tracker.duration)
      self.play(Create(target), run_time=anim_time)
      
      # 2단계: 음성이 끝날 때까지 남은 시간을 자연스럽게 대기
      remaining_time = max(0.1, tracker.duration - anim_time)
      self.wait(remaining_time)
  ```

### 6-2. 3D 씬에서의 HUD(자막/수식) 고정 필수 수칙
* `ThreeDScene`에서 3D 카메라가 회전할 때, 수식이나 자막이 같이 회전하면 읽을 수 없습니다.
* **해결책**: 화면에 고정되어야 하는 모든 UI는 생성 즉시 `add_fixed_in_frame_mobjects`로 등록합니다.
  ```python
  self.add_fixed_in_frame_mobjects(title_card)
  self.remove(title_card) # 씬 재생 전 숨김 후
  self.play(FadeIn(title_card)) # FadeIn 시 화면 2D 평면에 고정되어 렌더링됨
  ```

### 6-3. 카메라 회전(Ambient Rotation) 제어
* 설명 중: `self.begin_ambient_camera_rotation(rate=0.08)` (아주 천천히)
* 핵심 수식 집중 / 줌인 시: 반드시 `self.stop_ambient_camera_rotation()`으로 정지시켜 시선 흔들림 방지

---

## 7. 개발 및 렌더링 시 주의해야 할 7가지 골든 룰 (Golden Rules Checklist)

1. [ ] **LaTeX 한글 격리**: `MathTex` 안에 한글이 들어있지 않은가? (`Text` + `MathTex` 분리 여부)
2. [ ] **LaTeX 중괄호 공백**: 분수 표기 끝에 공백이 있는가? (`\frac{a }{b}`)
3. [ ] **HUD 고정**: 3D 씬의 수식과 자막이 `add_fixed_in_frame_mobjects`에 등록되었는가?
4. [ ] **의미론적 색상 매핑**: 수식 변수 색상과 그래프/입자 색상이 일치하는가?
5. [ ] **보조선 좌표 연동**: `axes.c2p()`를 사용하여 보조 점선과 라벨이 축과 함께 움직이는가?
6. [ ] **오디오 싱크 방어 코드**: `run_time=min(..., tracker.duration)` 및 `max(0.1, ...)` 처리가 되었는가?
7. [ ] **Git 용량 최적화**: 대용량 비디오(`.mp4`)와 캐시 폴더(`media/`)가 `.gitignore`에 등록되어 깃허브가 가볍게 유지되는가?
8. [ ] **인지적 여백(Soak-in Time)**: 핵심 강조 구간 직후 최소 1.5~2.5초의 시각적 음미 시간이 배정되었는가?

---

## 8. 인지적 여백과 강조 호흡 설계 표준 (Cognitive Pacing & Soak-in Time)

> **"수학적 깨달음(Aha! Moment)은 말이 끝난 뒤 찾아온다."**  
> 3Blue1Brown 영상이 깊은 여운을 남기는 이유는, 핵심 원리가 시각화되는 순간 **화면을 멈추고 시청자가 자신의 뇌로 생각할 수 있는 '인지적 침묵(Soak-in Time)'**을 충분히 주기 때문입니다.

### 8-1. 강조 구간별 필수 대기 시간 규격
1. **국소 선형화(접선 벡터 탄생)**:
   - 굽이치는 곡선이 직선 접선 $\vec{v}(t)$로 펴지는 순간, 나레이션 종료 후 **최소 2.0초간 정지 화면 유지** (`self.wait(2.0)`)
2. **소용돌이(Curl) 패들휠 회전**:
   - 패들휠이 토크를 받아 회전하기 시작할 때, 나레이션과 함께 **최소 3.0초간 오직 회전 움직임만 주시**하도록 카메라 이동 정지
3. **리만 합 $\to$ 연속 유선 변환**:
   - 꺾은선이 녹아내리며 매끄러운 유선 곡선으로 변환되는 순간, 나레이션 종료 후 **최소 2.5초간 침묵 속에서 빛나는 유선만 감상**
4. **시간 설계 공식**:
   ```python
   with self.voiceover(text="핵심 강조 설명...") as tracker:
       self.play(Transform(...), run_time=tracker.duration)
   
   # 🚨 [필수] 음성이 끝난 직후 뇌가 시각 정보를 처리할 인지적 여백 부여
   self.wait(2.0)
   ```

---

## 9. 페어 프로그래밍 피드백 & 매뉴얼 진화 로그 (Living Feedback Log)

사용자와 어시스턴트가 협업하며 도출한 통찰과 규칙들을 누적 기록하여, 매뉴얼을 지속해서 진화시킵니다.

| 날짜 | 피드백 주제 | 사용자 통찰 및 반영 내용 | 기술적 적용 표준 |
| :--- | :--- | :--- | :--- |
| **2026-10-18** | **순수 딥 블랙 배경** | "배경이 검정색일 때 수학 객체와 수식에 집중력이 최고조로 높아진다." | `camera.background_color = "#000000"` (무한 명암비 및 경계 소멸) |
| **2026-10-18** | **버전별 파일 보존** | "기존 코드를 덮어쓰지 말고 `_v1`, `_v2`, `_v3`로 버전화하여 단계별 비교와 롤백이 가능하게 한다." | `wind_calculus.py` 원본 보존, 신규 파일 번호 부여 |
| **2026-10-18** | **3b1b 유체 메타포** | "유체역학의 직관(패들휠, 입자 링, 유선)을 수학 개념과 1:1로 대응시킨다." | Curl=패들휠 회전, Div=방울 팽창, Integral=유선 루프 |
| **2026-10-18** | **인지적 여백(Soak-in Time)** | "강조하는 핵심 구간에서는 보는 사람이 이해하고 소화할 수 있는 충분한 시간을 배정해야 한다." | 핵심 수식/변환 직후 `self.wait(1.5 ~ 2.5)` 필수 적용 (Section 8 추가) |
| **2026-10-18** | **변화량 vs 변화율의 감각적 분리** | "회전(Curl) 등 복잡한 요소를 배제하고, 인간이 바람을 인지할 때 느끼는 것은 '변화량'이 아니라 '변화율'이라는 점에 집중한다." | 찰나를 본 잎($\Delta t=0.1\text{s}$)과 오래 본 잎($\Delta t=0.5\text{s}$)의 서로 다른 변화량이 나눗셈을 통해 동일한 속도 벡터 $\vec{v}$로 수렴하는 대비 애니메이션 구현 |
| **2026-10-18** | **나뭇잎 진동 물리 & 감각 인식론** | "작은 잎은 빠르게 떨리고(고주파/소진폭), 큰 잎은 크게 흔들린다(저주파/대진폭). 진폭($A$)은 달라도 최대 변화율($A\omega$)이 같아 같은 바람으로 인지한다. 또한 원근에 따른 망막 상의 크기 차이 보정, 3D 세계를 2D 단면(미분)으로 보고 3D로 재구성(적분)하는 인간의 뇌 센서 본질을 설명한다." | 조화진동 $A_1\omega_1 = A_2\omega_2 = v_{max}$ 물리 모델링, 원근 망막 투영, 3D $\to$ 2D 슬라이스 미분/적분 시각화 |
| **2026-10-18** | **3Blue1Brown 스타일 비주얼 혁신 (v6)** | "단순 화살표나 허공의 도형은 조잡하게 느껴진다. 조화진동 물리와 실시간 x-t 그래프 및 접선의 기하학적 평행 일치, 3D 투영 시 광학 피라미드와 사파이어 글래스 센서 스크린, 3D 바닥 격자 접지, 글래스모피즘 Pill Badge 시스템을 적용한다." | 실시간 위상 그래프 + 동일 Y축 스케일 접선 기울기 일치, Frustum 투영선, 3D $\to$ 2D 카메라 시점 밀착 전환 |
| *(작업 진행)* | *(피드백 추가)* | *(사용자와 대화하면서 지속해서 실시간 업데이트)* | *(새로운 규칙 반영)* |

---

## 10. 인식론적 미적분 시각화 공식 (Epistemological Calculus Design Principles)

### 10-1. 조화 진동(Harmonic Oscillation)을 통한 미분 직관화
* **수학/물리 공식**:
  $$x(t) = A \sin(\omega t), \quad v(t) = \frac{dx}{dt} = A\omega \cos(\omega t), \quad v_{\max} = A \cdot \omega$$
* **시각화 원칙**:
  - 작은 나뭇잎: 진폭 $A_1 = 0.5\text{ m}$, 각진동수 $\omega_1 = 4.8\text{ rad/s}$ (바르르 빠른 진동)
  - 큰 나뭇잎: 진폭 $A_2 = 1.5\text{ m}$, 각진동수 $\omega_2 = 1.6\text{ rad/s}$ (너울너울 느린 흔들림)
  - 두 나뭇잎의 이동 변위(변화량)는 3배 차이가 나지만, 시간으로 미분한 최고 속도(순간변화율)는 $v_{\max} = 2.4\text{ m/s}$로 정확히 일치함을 시각적 화살표로 증명.

### 10-2. 원근감(Perspective)과 망막 각속도 정규화
* **망막 상의 크기**: 거리가 10배 멀어지면 망막에 맺히는 변위 $\Delta \theta$는 $\frac{1}{10}$로 줄어듭니다.
* **뇌의 미분 센서**:
  $$v \approx d \cdot \frac{d\theta}{dt}$$
  뇌는 시각적 크기(변화량)를 보는 것이 아니라, 거리($d$)와 시간($dt$)을 함께 미분 계산하여 실체 속도를 인지합니다.

### 10-3. 차원의 미분과 적분 (Dimensional Differentiation & Integration)
* **3D $\to$ 2D (미분 단면)**: 3차원 입체 세상을 빛의 단면으로 얇게 잘라 2차원 망막 스크린으로 받아들이는 과정이 곧 공간의 미분($\frac{d}{dz}$)입니다.
* **2D $\to$ 3D (시간 적분)**: 뇌는 시간 축을 따라 흘러 들어오는 무수히 많은 2차원 순간 단면들을 적분($\int dt$)하여 하나의 살아있는 3차원 입체 실체를 머릿속에 복원합니다.

---

## 11. 3Blue1Brown 스타일 프리미엄 그래픽 4대 원칙 (World-Class Visual Standards)

1. **그래프 연동 기하학적 증명 (Geometric Tangent Synchronization)**:
   - 물리적 진동 운동만 보여주지 않고, 옆에 반드시 **실시간 $x(t)$ 위상 곡선**을 그리고, 중심을 통과할 때 **동일한 각도의 접선(Tangent)**이 평행하게 나타나게 하여 미분의 일치를 시각적으로 못 박는다.
2. **공간 접지 그리드 (Grounding Grid)**:
   - 3D 공간에 물체가 둥둥 떠다니는 인상을 방지하기 위해, 바닥($z = -1.8$)에 저투명도(`stroke_opacity=0.4`)의 은은한 `NumberPlane` 그리드를 배치하여 카메라 회전 시 깊이감을 극대화한다.
3. **글래스모피즘 센서 스크린 (Frosted Sensor Glass)**:
   - 3D 투영면은 단순 사각형이 아니라 미세 십자선(Viewfinder)과 반투명 사파이어 색상(`fill_opacity=0.25`)을 지닌 정밀 광학 센서판으로 연출한다.
4. **필 배지 타이포그래피 (Pill Badge Component)**:
   - 허공에 날것의 텍스트를 띄우지 않고, `RoundedRectangle` 기반의 세련된 반투명 배지 안에 텍스트와 수식을 감싸서 시각적 노이즈를 완전히 제거한다.




