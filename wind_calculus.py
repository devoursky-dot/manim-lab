import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

try:
    from manim_voiceover.services.edge import EdgeService
except (ImportError, ModuleNotFoundError):
    from core.edge_service import EdgeService


class WindCalculus3DLecture(ThreeDScene, VoiceoverScene):
    def construct(self):
        # 1. 무료 한국어 AI 성우 설정 (Microsoft Edge TTS)
        self.set_speech_service(
            EdgeService(voice="ko-KR-InJoonNeural", rate="+0%")
        )
        self.camera.background_color = "#0F172A"  # 세련된 다크 네이비 배경
        FONT_KR = "Malgun Gothic"

        # 3D 벡터장(바람의 속도장) 수학적 정의: 소용돌이치며 상승하는 바람
        def wind_field(pos):
            x, y, z = pos
            vx = -y * 0.6 + 0.4
            vy = x * 0.6 + 0.2
            vz = 0.35 * np.cos(0.5 * x)
            return np.array([vx, vy, vz])

        # ---------------------------------------------------------
        # [Scene 1] 보이지 않는 바람과 3차원 공간 (0~12초)
        # ---------------------------------------------------------
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-2, 3, 1],
            x_length=7,
            y_length=7,
            z_length=4.5,
            axis_config={"color": "#475569", "stroke_width": 1.5},
        )
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.12)

        title_box = VGroup(
            Text("미분과 적분: 세상을 인식하는 방법", font=FONT_KR, font_size=28, color="#F8FAFC"),
            MathTex(r"\frac{d\vec{r} }{dt} \longrightarrow \int \vec{v}(t)\,dt", font_size=32, color="#38BDF8"),
        ).arrange(DOWN, buff=0.15).to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(title_box)
        self.remove(title_box)

        with self.voiceover(
            text="미분은 우리가 세상을 인식하는 방법을 수식화한 것입니다. 바람이 부는 걸 생각해 볼까요? 실제 바람 자체는 우리 눈에 보이지 않습니다."
        ) as tracker:
            self.play(
                Create(axes),
                FadeIn(title_box, shift=DOWN * 0.2),
                run_time=min(3.0, tracker.duration),
            )
            self.wait(max(0.1, tracker.duration - 3.0))

        # ---------------------------------------------------------
        # [Scene 2] 나뭇잎의 움직임과 순간변화율 = 미분 (12~28초)
        # ---------------------------------------------------------
        sample_points = [
            np.array([x, y, z])
            for x in [-2.0, 0.0, 2.0]
            for y in [-2.0, 0.0, 2.0]
            for z in [-1.0, 1.0]
            if not (x == 0 and y == 0)
        ]

        leaves = VGroup()
        velocity_vectors = VGroup()

        for pt in sample_points:
            leaf = Dot3D(point=pt, radius=0.07, color="#4ADE80")
            vel = wind_field(pt)
            vec_arrow = Arrow(
                start=pt,
                end=pt + vel * 0.55,
                buff=0,
                color="#FACC15",
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            )
            leaves.add(leaf)
            velocity_vectors.add(vec_arrow)

        sub_diff = VGroup(
            Text("나뭇잎의 순간 움직임 포착 = 미분(순간변화율)", font=FONT_KR, font_size=24, color="#4ADE80"),
            MathTex(r"\vec{v}(t) = \frac{d\vec{r} }{dt}", font_size=34, color="#FACC15"),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(sub_diff)
        self.remove(sub_diff)

        with self.voiceover(
            text="하지만 우리는 주변에 움직이는 나뭇잎이나 물체들을 보고 바람이 분다고 인식합니다. 여기서 움직이는 물체의 짧은 순간순간의 변화율을 보고 인지하는 것, 이것이 바로 미분입니다."
        ) as tracker:
            self.play(FadeIn(leaves, scale=0.5), FadeIn(sub_diff), run_time=2.5)
            self.play(
                LaggedStart(*[GrowArrow(vec) for vec in velocity_vectors], lag_ratio=0.05),
                run_time=max(2.0, tracker.duration - 2.5),
            )

        # ---------------------------------------------------------
        # [Scene 3] 순간변화율 * 시간 = 순간변화량 (28~42초)
        # ---------------------------------------------------------
        self.play(
            leaves.animate.set_opacity(0.2),
            velocity_vectors.animate.set_opacity(0.2),
            FadeOut(sub_diff),
            run_time=0.8,
        )

        p0 = np.array([1.8, -1.2, -0.8])
        focus_leaf = Dot3D(point=p0, radius=0.1, color="#22C55E")
        dt = 0.35

        step_vectors = VGroup()
        curr_p = p0.copy()
        for _ in range(7):
            v = wind_field(curr_p)
            next_p = curr_p + v * dt
            seg = Arrow(
                start=curr_p,
                end=next_p,
                buff=0,
                color="#FB923C",
                stroke_width=5,
                max_tip_length_to_length_ratio=0.25,
            )
            step_vectors.add(seg)
            curr_p = next_p

        sub_delta = VGroup(
            Text("순간변화율 × 시간 = 순간변화량(미소 변위)", font=FONT_KR, font_size=24, color="#FB923C"),
            MathTex(r"d\vec{r} = \vec{v}(t) \cdot dt", font_size=36, color="#FB923C"),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(sub_delta)
        self.remove(sub_delta)

        with self.voiceover(
            text="이 각각의 순간변화율에 짧은 시간을 곱하면 그 찰나에 이동한 순간변화량이 됩니다."
        ) as tracker:
            self.play(FadeIn(focus_leaf, scale=1.5), FadeIn(sub_delta), run_time=1.2)
            for i in range(3):
                self.play(
                    GrowArrow(step_vectors[i]),
                    focus_leaf.animate.move_to(step_vectors[i].get_end()),
                    run_time=max(0.6, (tracker.duration - 1.2) / 3),
                )

        # ---------------------------------------------------------
        # [Scene 4] 순간변화량의 합(적분) = 바람의 흐름 (42~60초)
        # ---------------------------------------------------------
        self.play(FadeOut(sub_delta), run_time=0.5)

        sub_int = VGroup(
            Text("순간변화량의 누적(적분) = 우리가 인식하는 바람의 흐름", font=FONT_KR, font_size=24, color="#38BDF8"),
            MathTex(r"\vec{r}(T) - \vec{r}(0) = \int_{0}^{T} \vec{v}(t)\,dt", font_size=36, color="#38BDF8"),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(sub_int)
        self.remove(sub_int)

        def build_streamline(start_pt, steps=60, step_dt=0.08, color="#38BDF8"):
            pts = [start_pt]
            cp = start_pt.copy()
            for _ in range(steps):
                cp = cp + wind_field(cp) * step_dt
                pts.append(cp.copy())
            curve = VMobject(color=color, stroke_width=3.5)
            curve.set_points_smoothly(pts)
            return curve

        main_streamline = build_streamline(p0, steps=55, step_dt=0.07, color="#38BDF8")
        bg_streamlines = VGroup(
            build_streamline(np.array([-2.0, -1.5, -1.0]), color="#38BDF8"),
            build_streamline(np.array([1.5, 1.8, -0.5]), color="#818CF8"),
            build_streamline(np.array([-1.5, 2.0, -0.8]), color="#38BDF8"),
            build_streamline(np.array([0.5, -2.2, 0.0]), color="#818CF8"),
        )

        with self.voiceover(
            text="그리고 이 순간변화량들을 차곡차곡 합치면, 즉 적분을 하면 그것이 바람의 전체 흐름일 거라고 생각하는 것입니다. 결국 우리는 매 순간 미분값을 인지하고, 그것들을 누적해서 세상을 인식하고 있습니다."
        ) as tracker:
            self.play(
                FadeIn(sub_int),
                LaggedStart(*[GrowArrow(step_vectors[i]) for i in range(3, 7)], lag_ratio=0.3),
                focus_leaf.animate.move_to(step_vectors[-1].get_end()),
                run_time=2.5,
            )
            self.play(
                ReplacementTransform(step_vectors, main_streamline),
                Create(bg_streamlines),
                velocity_vectors.animate.set_opacity(0.45),
                run_time=3.5,
            )
            moving_dots = VGroup(*[Dot3D(color="#4ADE80", radius=0.08) for _ in range(len(bg_streamlines))])
            self.play(
                MoveAlongPath(focus_leaf, main_streamline),
                *[MoveAlongPath(dot, line) for dot, line in zip(moving_dots, bg_streamlines)],
                run_time=max(2.0, tracker.duration - 6.0),
                rate_func=linear,
            )

        self.stop_ambient_camera_rotation()
        self.wait(1.5)
