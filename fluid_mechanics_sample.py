import numpy as np
from manim import *


class FluidMechanics3B1BStyle(Scene):
    """3Blue1Brown 스타일의 유체역학 및 벡터장 핵심 시각화 씬

    주요 구현:
    1. StreamLines 연속 유선 루프 애니메이션
    2. 국소 회전(Curl)을 시각화하는 회전 패들휠(Paddlewheel)
    3. 유체 팽창/수축(Divergence)을 감지하는 추적 입자 고리(Particle Ring)
    """

    def construct(self):
        # 1. 3b1b 시그니처 딥 다크 배경
        self.camera.background_color = "#0B1120"
        FONT_KR = "Malgun Gothic"

        # 비선형 와류(소용돌이) 유체 속도장 정의
        def velocity_field(pos):
            x, y, _ = pos
            r2 = x**2 + y**2 + 0.1
            # 소용돌이 성분 + 중심 회전
            vx = -y * 0.8 / np.sqrt(r2) + 0.3
            vy = x * 0.8 / np.sqrt(r2) - 0.1 * y
            return np.array([vx, vy, 0])

        # 2. 제목 타이틀
        title = VGroup(
            Text("유체역학적 벡터장 해석 (3Blue1Brown 스타일)", font=FONT_KR, font_size=28, color="#F8FAFC"),
            Text("StreamLines · Curl (회전) · Divergence (발산)", font=FONT_KR, font_size=18, color="#38BDF8"),
        ).arrange(DOWN, buff=0.15).to_corner(UL, buff=0.4)

        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1.0)

        # -------------------------------------------------------------
        # Part 1: 살아 숨 쉬는 연속 유선 (StreamLines)
        # -------------------------------------------------------------
        stream_lines = StreamLines(
            velocity_field,
            x_range=[-4.5, 4.5, 0.45],
            y_range=[-3.0, 3.0, 0.45],
            stroke_width=2.5,
            virtual_time=2.5,
            color=color_gradient([BLUE_E, BLUE_C, TEAL, YELLOW], 80),
        )

        self.play(Create(stream_lines), run_time=1.8)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.4)
        self.wait(2.0)

        # -------------------------------------------------------------
        # Part 2: Curl(회전)의 시각화 - 떠다니는 패들휠 (Paddlewheel)
        # -------------------------------------------------------------
        # 십자 모양의 패들휠 생성
        paddle_center = np.array([0.0, 0.5, 0])
        paddle = VGroup(
            Line(LEFT * 0.35, RIGHT * 0.35, color="#FACC15", stroke_width=4),
            Line(DOWN * 0.35, UP * 0.35, color="#FACC15", stroke_width=4),
            Dot(color="#EF4444", radius=0.08),
        ).move_to(paddle_center)

        curl_label = VGroup(
            Text("국소 회전 (Curl : ∇ × v)", font=FONT_KR, font_size=20, color="#FACC15"),
            Text("유체 속 물체의 회전 속도 = Curl", font=FONT_KR, font_size=14, color="#94A3B8"),
        ).arrange(DOWN, buff=0.1).next_to(paddle, UR, buff=0.3)

        self.play(FadeIn(paddle, scale=1.5), FadeIn(curl_label), run_time=1.0)

        # 패들휠을 유체의 컬(Curl) 각속도에 맞춰 회전시키는 업데이터
        def update_paddle(p, dt):
            # 소용돌이 중심에서 시계 반대 방향 회전
            p.rotate(2.0 * dt, about_point=p[2].get_center())

        paddle.add_updater(update_paddle)
        self.wait(3.0)
        paddle.remove_updater(update_paddle)

        # -------------------------------------------------------------
        # Part 3: Divergence(발산)의 시각화 - 유체 방울(입자 링)의 변형
        # -------------------------------------------------------------
        self.play(FadeOut(paddle), FadeOut(curl_label), run_time=0.6)

        bubble_center = np.array([-2.5, -1.0, 0])
        num_particles = 24
        angles = np.linspace(0, 2 * np.pi, num_particles, endpoint=False)
        radius = 0.45

        particles = VGroup(*[
            Dot(
                point=bubble_center + np.array([radius * np.cos(a), radius * np.sin(a), 0]),
                radius=0.06,
                color="#4ADE80",
            )
            for a in angles
        ])
        bubble_outline = Circle(radius=radius, color="#4ADE80", stroke_width=2).move_to(bubble_center)

        div_label = VGroup(
            Text("면적 변화 (Divergence : ∇ · v)", font=FONT_KR, font_size=20, color="#4ADE80"),
            Text("유체 방울이 흐르며 면적이 팽창/수축하는 율", font=FONT_KR, font_size=14, color="#94A3B8"),
        ).arrange(DOWN, buff=0.1).to_edge(DOWN, buff=0.4)

        self.play(Create(bubble_outline), FadeIn(particles), FadeIn(div_label), run_time=1.0)

        # 입자들이 유속장에 따라 개별적으로 흘러가며 방울이 늘어나고 변형되는 애니메이션
        def update_bubble_particles(group, dt):
            for dot in group:
                v = velocity_field(dot.get_center())
                dot.shift(v * dt * 1.2)

        particles.add_updater(update_bubble_particles)
        self.play(FadeOut(bubble_outline), run_time=0.5)
        self.wait(3.5)
        particles.remove_updater(update_bubble_particles)

        # 마무리 정리
        stream_lines.end_animation()
        self.wait(1.0)
