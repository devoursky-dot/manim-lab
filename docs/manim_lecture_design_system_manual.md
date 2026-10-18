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
