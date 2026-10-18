import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

try:
    from manim_voiceover.services.edge import EdgeService
except (ImportError, ModuleNotFoundError):
    from core.edge_service import EdgeService


class WindCalculus3DLectureV2(ThreeDScene, VoiceoverScene):
    def construct(self):
        # 1. 한국어 AI 성우 설정 (Edge TTS)
        self.set_speech_service(
            EdgeService(voice="ko-KR-InJoonNeural", rate="+0%")
        )
        self.camera.background_color = "#0B1120"  # 깊이감 있는 딥 네이비 배경
        FONT_KR = "Malgun Gothic"

        # 3D 바람 벡터장 (소용돌이치며 완만하게 상승하는 흐름)
        def wind_field(pos):
            x, y, z = pos
            r = np.sqrt(x**2 + y**2) + 0.1
            vx = -y * 0.65 + 0.35
            vy = x * 0.65 + 0.15
            vz = 0.3 * np.sin(0.6 * r) + 0.25
            return np.array([vx, vy, vz])

        # 유선(Streamline) 생성 함수
        def build_streamline(start_pt, steps=70, step_dt=0.06, color="#38BDF8"):
            pts = [start_pt]
            cp = np.array(start_pt, dtype=float)
            for _ in range(steps):
                cp = cp + wind_field(cp) * step_dt
                pts.append(cp.copy())
            curve = VMobject(color=color, stroke_width=3.5)
            curve.set_points_smoothly(pts)
            return curve

        # -----------------------------------------------------------------
        # [Act 1] 보이지 않는 바람과 인식의 문제 (0~14초)
        # -----------------------------------------------------------------
        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            z_range=[-2.0, 2.5, 1],
            x_length=7.0,
            y_length=7.0,
            z_length=4.5,
            axis_config={"color": "#334155", "stroke_width": 1.5},
        )
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.95)
        self.begin_ambient_camera_rotation(rate=0.08)

        title_card = VGroup(
            Text("미적분: 보이지 않는 세상을 보는 눈", font=FONT_KR, font_size=26, color="#F1F5F9"),
            VGroup(
                Text("미분", font=FONT_KR, font_size=18, color="#94A3B8"),
                MathTex(r"\frac{d\vec{r} }{dt}", font_size=26, color="#38BDF8"),
                MathTex(r"\longrightarrow", font_size=26, color="#64748B"),
                Text("적분", font=FONT_KR, font_size=18, color="#94A3B8"),
                MathTex(r"\int \vec{v}\,dt", font_size=26, color="#38BDF8"),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15).to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(title_card)
        self.remove(title_card)

        with self.voiceover(
            text="미분과 적분은 우리가 세상을 인식하는 놀라운 방식을 담고 있습니다. 바람이 부는 날을 상상해 보세요. 실제 바람 자체는 투명해서 우리 눈에 보이지 않습니다."
        ) as tracker:
            self.play(
                Create(axes),
                FadeIn(title_card, shift=DOWN * 0.2),
                run_time=min(3.0, tracker.duration),
            )
            self.wait(max(0.1, tracker.duration - 3.0))

        # -----------------------------------------------------------------
        # [Act 2] 줌인(Zoom-in)과 순간속도 포착 = 미분 (14~34초)
        # -----------------------------------------------------------------
        # 공간에 흩뿌려진 나뭇잎과 작은 벡터들
        field_points = [
            np.array([x, y, z])
            for x in [-2.0, 0.0, 2.0]
            for y in [-2.0, 0.0, 2.0]
            for z in [-1.0, 0.8]
            if not (x == 0 and y == 0)
        ]
        leaves = VGroup(*[Dot3D(point=p, radius=0.065, color="#4ADE80") for p in field_points])
        field_arrows = VGroup(*[
            Arrow(
                start=p,
                end=p + wind_field(p) * 0.45,
                buff=0,
                color="#FACC15",
                stroke_width=2.5,
                max_tip_length_to_length_ratio=0.25,
            )
            for p in field_points
        ])

        # 관찰 대상 나뭇잎 지정
        target_p = np.array([1.6, -1.2, -0.6])
        target_leaf = Dot3D(point=target_p, radius=0.11, color="#22C55E")
        target_vel = wind_field(target_p)
        tangent_arrow = Arrow(
            start=target_p,
            end=target_p + target_vel * 0.85,
            buff=0,
            color="#FACC15",
            stroke_width=5.5,
            max_tip_length_to_length_ratio=0.22,
        )

        sub_act2 = VGroup(
            Text("나뭇잎의 찰나를 확대하면 직선이 된다 : 순간속도(미분)", font=FONT_KR, font_size=23, color="#4ADE80"),
            MathTex(r"\vec{v}(t) = \lim_{\Delta t \to 0} \frac{\Delta \vec{r} }{\Delta t} = \frac{d\vec{r} }{dt}", font_size=32, color="#FACC15"),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act2)
        self.remove(sub_act2)

        with self.voiceover(
            text="하지만 공중에 날리는 나뭇잎을 보면 바람을 알 수 있죠. 카메라를 가까이 당겨 볼까요? 휘어지는 곡선 궤적도 아주 찰나의 순간을 잘라보면 하나의 직선 방향, 즉 순간속도 벡터로 나타납니다. 이것이 바로 미분입니다."
        ) as tracker:
            self.play(
                FadeIn(leaves, scale=0.5),
                LaggedStart(*[GrowArrow(a) for a in field_arrows], lag_ratio=0.04),
                run_time=2.2,
            )
            # 카메라 줌인 & 시선 집중
            self.stop_ambient_camera_rotation()
            self.play(
                leaves.animate.set_opacity(0.18),
                field_arrows.animate.set_opacity(0.18),
                FadeIn(target_leaf, scale=1.5),
                FadeIn(sub_act2, shift=UP * 0.15),
                run_time=1.5,
            )
            self.move_camera(
                phi=70 * DEGREES,
                theta=-25 * DEGREES,
                zoom=1.45,
                run_time=2.2,
            )
            self.play(
                GrowArrow(tangent_arrow),
                target_leaf.animate.set_color("#86EFAC"),
                run_time=max(1.8, tracker.duration - 5.9),
            )

        # -----------------------------------------------------------------
        # [Act 3] 시간 간격을 좁혀가는 이산 빌드업 : Δt → dt (34~54초)
        # -----------------------------------------------------------------
        self.play(
            FadeOut(sub_act2),
            FadeOut(tangent_arrow),
            run_time=0.6,
        )

        # 1단계: 성긴 간격 (dt_coarse = 0.55, 3단계 꺾은선)
        coarse_dt = 0.55
        p_c = target_p.copy()
        coarse_arrows = VGroup()
        for _ in range(3):
            v_step = wind_field(p_c)
            next_c = p_c + v_step * coarse_dt
            coarse_arrows.add(
                Arrow(start=p_c, end=next_c, buff=0, color="#FB923C", stroke_width=4.5)
            )
            p_c = next_c

        # 2단계: 촘촘한 간격 (dt_fine = 0.22, 7단계 꺾은선)
        fine_dt = 0.22
        p_f = target_p.copy()
        fine_arrows = VGroup()
        for _ in range(7):
            v_step = wind_field(p_f)
            next_f = p_f + v_step * fine_dt
            fine_arrows.add(
                Arrow(start=p_f, end=next_f, buff=0, color="#F59E0B", stroke_width=3.5)
            )
            p_f = next_f

        sub_act3 = VGroup(
            Text("시간 간격을 좁힐수록 (Δt → dt) 실제 궤적에 수렴", font=FONT_KR, font_size=23, color="#FB923C"),
            MathTex(r"\Delta \vec{r} = \vec{v}(t) \cdot \Delta t \;\xrightarrow{\Delta t \to 0}\; d\vec{r} = \vec{v}(t)\,dt", font_size=32, color="#FB923C"),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act3)
        self.remove(sub_act3)

        with self.voiceover(
            text="이 순간속도에 시간 delta t를 곱하면 그 찰나의 이동량이 됩니다. 시간 간격을 1초, 0.4초로 점점 좁혀볼까요? 거칠었던 꺾은선이 촘촘해지며 실제 궤적에 부드럽게 가까워집니다."
        ) as tracker:
            self.play(FadeIn(sub_act3), run_time=0.8)
            # 1단계 성긴 꺾은선 진행
            self.play(
                LaggedStart(*[GrowArrow(a) for a in coarse_arrows], lag_ratio=0.25),
                run_time=2.0,
            )
            self.wait(0.5)
            # 2단계 촘촘한 꺾은선으로 변환
            self.play(
                ReplacementTransform(coarse_arrows, fine_arrows),
                run_time=2.2,
            )
            self.wait(max(0.1, tracker.duration - 5.5))

        # -----------------------------------------------------------------
        # [Act 4] 극한과 적분: 매끄러운 바람의 유선(Streamline) (54~80초)
        # -----------------------------------------------------------------
        self.play(FadeOut(sub_act3), run_time=0.5)

        # 카메라 다시 넓게 전체 조망
        self.move_camera(
            phi=65 * DEGREES,
            theta=-50 * DEGREES,
            zoom=1.0,
            run_time=2.0,
        )
        self.begin_ambient_camera_rotation(rate=0.09)

        # 목표 연속 유선
        main_stream = build_streamline(target_p, steps=65, step_dt=0.065, color="#38BDF8")
        surrounding_streams = VGroup(
            build_streamline(np.array([-1.8, -1.2, -0.8]), color="#60A5FA"),
            build_streamline(np.array([1.2, 1.8, -0.4]), color="#818CF8"),
            build_streamline(np.array([-1.2, 2.0, -0.7]), color="#38BDF8"),
            build_streamline(np.array([0.4, -2.0, 0.1]), color="#818CF8"),
            build_streamline(np.array([2.0, 0.5, -0.3]), color="#60A5FA"),
        )

        sub_act4 = VGroup(
            Text("미소 변위들의 무한한 누적 = 적분(전체 흐름)", font=FONT_KR, font_size=23, color="#38BDF8"),
            MathTex(r"\vec{r}(T) - \vec{r}(0) = \lim_{\Delta t \to 0} \sum \vec{v}(t_i)\Delta t = \int_{0}^{T} \vec{v}(t)\,dt", font_size=32, color="#38BDF8"),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act4)
        self.remove(sub_act4)

        with self.voiceover(
            text="시간 간격을 0으로 보내는 극한을 취하면, 시그마는 적분 인테그랄이 되고, 미소 변위들이 완전히 매끄러운 곡선으로 이어집니다. 우리는 매 순간의 미분값을 감각하고, 이를 누적하여 바람의 거대한 흐름을 인식합니다. 미적분은 세상을 꿰뚫어 보는 우리의 수학적 눈입니다."
        ) as tracker:
            self.play(
                FadeIn(sub_act4),
                ReplacementTransform(fine_arrows, main_stream),
                run_time=2.5,
            )
            self.play(
                Create(surrounding_streams),
                field_arrows.animate.set_opacity(0.4),
                leaves.animate.set_opacity(0.4),
                run_time=3.0,
            )

            # 유선을 따라 날아가는 파티클 무리 연출
            stream_dots = VGroup(*[
                Dot3D(color="#4ADE80", radius=0.08)
                for _ in range(len(surrounding_streams))
            ])
            self.play(
                MoveAlongPath(target_leaf, main_stream),
                *[
                    MoveAlongPath(dot, stream)
                    for dot, stream in zip(stream_dots, surrounding_streams)
                ],
                run_time=max(3.0, tracker.duration - 5.5),
                rate_func=linear,
            )

        self.stop_ambient_camera_rotation()
        self.wait(1.5)
