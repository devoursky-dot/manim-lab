import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

try:
    from manim_voiceover.services.edge import EdgeService
except (ImportError, ModuleNotFoundError):
    from core.edge_service import EdgeService


class WindCalculus3DLectureV3(ThreeDScene, VoiceoverScene):
    """[v3 Masterpiece] 3Blue1Brown 스타일 바람과 미적분 심층 시각화 강의

    설계 원칙 (Design Standards):
    1. 캔버스: 완전한 순수 딥 블랙 (#000000)
    2. 3b1b 유체 메타포: 국소 선형화 접선 + 회전(Curl) 패들휠 + 리만 합 유선 승화
    3. 인지적 여백 (Cognitive Soak-in Time): 핵심 깨달음 구간마다 2.0~3.0초의 시각적 음미 시간 배정
    4. 텍스트 분리 철칙: Text("한글") + MathTex("수식") 분리 VGroup 결합
    """

    def construct(self):
        # 1. 한국어 AI 성우 및 순수 딥 블랙 캔버스 설정
        self.set_speech_service(
            EdgeService(voice="ko-KR-InJoonNeural", rate="+0%")
        )
        self.camera.background_color = "#000000"  # 3b1b 딥 블랙 베이스
        FONT_KR = "Malgun Gothic"

        # 색상 디자인 토큰 (Semantic Color Binding)
        C_VEL = "#FACC15"       # 순간속도 벡터 / 미분 (Amber Gold)
        C_STREAM = "#38BDF8"    # 유선 / 적분 (Electric Cyan)
        C_LEAF = "#4ADE80"      # 나뭇잎 / 관찰 입자 (Spring Mint)
        C_DISP = "#FB923C"      # 미소 변위 (Vibrant Orange)
        C_CURL = "#F43F5E"      # 국소 회전 / 소용돌이 중심 (Rose Red)
        C_AXIS = "#334155"      # 은은한 좌표축 (Muted Slate)

        # 3D 비선형 소용돌이 바람 벡터장 정의
        def wind_field(pos):
            x, y, z = pos
            r = np.sqrt(x**2 + y**2) + 0.1
            vx = -y * 0.70 + 0.30
            vy = x * 0.70 + 0.15
            vz = 0.32 * np.sin(0.55 * r) + 0.22
            return np.array([vx, vy, vz])

        # 유선(Streamline) 생성 헬퍼 함수
        def build_streamline(start_pt, steps=75, step_dt=0.06, color=C_STREAM):
            pts = [start_pt]
            cp = np.array(start_pt, dtype=float)
            for _ in range(steps):
                cp = cp + wind_field(cp) * step_dt
                pts.append(cp.copy())
            curve = VMobject(color=color, stroke_width=3.5)
            curve.set_points_smoothly(pts)
            return curve

        # =================================================================
        # [Act 1] 서론: 보이지 않는 유체와 인식의 시작 (0:00 ~ 0:30)
        # =================================================================
        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            z_range=[-2.0, 2.5, 1],
            x_length=7.0,
            y_length=7.0,
            z_length=4.5,
            axis_config={"color": C_AXIS, "stroke_width": 1.4},
        )
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.95)
        self.begin_ambient_camera_rotation(rate=0.07)

        title_card = VGroup(
            Text("바람과 미적분: 보이지 않는 흐름을 보는 눈", font=FONT_KR, font_size=26, color="#F8FAFC"),
            VGroup(
                Text("순간 포착 (미분)", font=FONT_KR, font_size=18, color="#94A3B8"),
                MathTex(r"\frac{d\vec{r} }{dt}", font_size=26, color=C_VEL),
                MathTex(r"\;\longrightarrow\;", font_size=24, color="#64748B"),
                Text("흐름 누적 (적분)", font=FONT_KR, font_size=18, color="#94A3B8"),
                MathTex(r"\int \vec{v}\,dt", font_size=26, color=C_STREAM),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15).to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(title_card)
        self.remove(title_card)

        with self.voiceover(
            text="바람은 눈에 보이지 않습니다. 하지만 우리는 나뭇잎이 흔들리고 날리는 것을 보며 바람이 존재함을 알죠. 미분과 적분은 바로 이 보이지 않는 세계의 흐름을 꿰뚫어 보는 수학적 언어입니다."
        ) as tracker:
            self.play(
                Create(axes),
                FadeIn(title_card, shift=DOWN * 0.2),
                run_time=min(3.5, tracker.duration),
            )
            self.wait(max(0.1, tracker.duration - 3.5))

        # [인지적 여백 1] 첫 인상 음미
        self.wait(1.5)

        # =================================================================
        # [Act 2] 미분(순간변화율): 초근접 줌인과 국소 선형화 (0:30 ~ 1:05)
        # =================================================================
        field_points = [
            np.array([x, y, z])
            for x in [-2.0, 0.0, 2.0]
            for y in [-2.0, 0.0, 2.0]
            for z in [-1.0, 0.8]
            if not (x == 0 and y == 0)
        ]
        leaves = VGroup(*[Dot3D(point=p, radius=0.065, color=C_LEAF) for p in field_points])
        field_arrows = VGroup(*[
            Arrow(
                start=p,
                end=p + wind_field(p) * 0.45,
                buff=0,
                color="#64748B",
                stroke_width=2.0,
                max_tip_length_to_length_ratio=0.25,
            )
            for p in field_points
        ])

        target_p = np.array([1.6, -1.2, -0.6])
        target_leaf = Dot3D(point=target_p, radius=0.12, color=C_LEAF)
        target_vel = wind_field(target_p)
        tangent_arrow = Arrow(
            start=target_p,
            end=target_p + target_vel * 0.90,
            buff=0,
            color=C_VEL,
            stroke_width=6.0,
            max_tip_length_to_length_ratio=0.22,
        )

        sub_act2 = VGroup(
            Text("찰나의 순간을 무한히 확대하면 직선이 된다 : 국소 선형화", font=FONT_KR, font_size=23, color=C_LEAF),
            MathTex(r"\vec{v}(t) = \lim_{\Delta t \to 0} \frac{\Delta \vec{r} }{\Delta t} = \frac{d\vec{r} }{dt}", font_size=32, color=C_VEL),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act2)
        self.remove(sub_act2)

        with self.voiceover(
            text="공중에 날리는 나뭇잎을 가까이 당겨 볼까요? 휘어지는 나뭇잎의 복잡한 궤적도, 아주 찰나의 순간을 무한히 확대하면 하나의 완벽한 직선 접선 벡터가 됩니다. 이것이 미분의 본질인 국소적 선형화입니다."
        ) as tracker:
            self.play(
                FadeIn(leaves, scale=0.5),
                LaggedStart(*[GrowArrow(a) for a in field_arrows], lag_ratio=0.04),
                run_time=2.5,
            )
            # 카메라 초근접 줌인 및 시선 집중
            self.stop_ambient_camera_rotation()
            self.play(
                leaves.animate.set_opacity(0.15),
                field_arrows.animate.set_opacity(0.15),
                FadeIn(target_leaf, scale=1.5),
                FadeIn(sub_act2, shift=UP * 0.15),
                run_time=1.8,
            )
            self.move_camera(
                phi=72 * DEGREES,
                theta=-22 * DEGREES,
                zoom=1.65,
                run_time=2.2,
            )
            self.play(
                GrowArrow(tangent_arrow),
                target_leaf.animate.set_color("#86EFAC"),
                run_time=max(2.0, tracker.duration - 6.5),
            )

        # [인지적 여백 2] 직선으로 펴진 미분 접선 벡터 음미 시간
        self.wait(2.2)

        # =================================================================
        # [Act 3] 소용돌이와 회전(Curl): 패들휠로 감지하는 미세 토크 (1:05 ~ 1:40)
        # =================================================================
        # 3Blue1Brown 시그니처: 유체 속 떠다니는 회전 패들휠(바람개비)
        paddle_center = target_p + np.array([0.0, 0.0, 0.4])
        paddle_blade1 = Line3D(start=paddle_center + LEFT * 0.35, end=paddle_center + RIGHT * 0.35, color=C_VEL, thickness=0.035)
        paddle_blade2 = Line3D(start=paddle_center + DOWN * 0.35, end=paddle_center + UP * 0.35, color=C_VEL, thickness=0.035)
        paddle_axis = Dot3D(point=paddle_center, radius=0.06, color=C_CURL)
        paddle_group = VGroup(paddle_blade1, paddle_blade2, paddle_axis)

        sub_curl = VGroup(
            Text("속도 차이가 만드는 국소 소용돌이 : 회전 (Curl)", font=FONT_KR, font_size=23, color=C_CURL),
            VGroup(
                MathTex(r"\text{Curl}(\vec{v}) = \nabla \times \vec{v} \;\propto\; \omega", font_size=30, color=C_VEL),
                Text("(패들휠 회전 각속도)", font=FONT_KR, font_size=18, color="#94A3B8"),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_curl)
        self.remove(sub_curl)

        with self.voiceover(
            text="바람은 앞으로만 불지 않고 소용돌이칩니다. 공간 속 나뭇잎의 위쪽과 아래쪽 속도 차이가 작은 회전 토크를 만들어내죠. 미분은 전진하는 속도뿐 아니라, 공간의 미세한 비틀림과 회전, 즉 컬까지 측정해 냅니다."
        ) as tracker:
            self.play(
                FadeOut(sub_act2),
                FadeIn(paddle_group, scale=1.4),
                FadeIn(sub_curl),
                run_time=2.0,
            )

            # 패들휠 실시간 회전 업데이터 등록
            def update_paddle_spin(group, dt):
                group.rotate(1.8 * dt, axis=OUT, about_point=paddle_center)

            paddle_group.add_updater(update_paddle_spin)
            self.wait(max(2.0, tracker.duration - 2.0))

        # [인지적 여백 3] 패들휠이 빙글빙글 도는 소용돌이 물리 현상 음미 시간
        self.wait(2.5)
        paddle_group.remove_updater(update_paddle_spin)

        # =================================================================
        # [Act 4] 적분: 리만 합에서 연속 유선으로의 승화 (1:40 ~ 2:25)
        # =================================================================
        self.play(
            FadeOut(paddle_group),
            FadeOut(sub_curl),
            FadeOut(tangent_arrow),
            run_time=0.8,
        )

        # 1단계: 성긴 간격 (dt=0.6, 3단계 꺾은선)
        coarse_dt = 0.60
        p_c = target_p.copy()
        coarse_arrows = VGroup()
        for _ in range(3):
            v_step = wind_field(p_c)
            next_c = p_c + v_step * coarse_dt
            coarse_arrows.add(
                Arrow(start=p_c, end=next_c, buff=0, color=C_DISP, stroke_width=4.5)
            )
            p_c = next_c

        # 2단계: 촘촘한 간격 (dt=0.22, 7단계 꺾은선)
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

        main_stream = build_streamline(target_p, steps=70, step_dt=0.065, color=C_STREAM)

        sub_act4 = VGroup(
            Text("미소 변위들의 무한한 누적 = 적분 (리만 합의 극한)", font=FONT_KR, font_size=23, color=C_STREAM),
            MathTex(r"\vec{r}(T) - \vec{r}(0) = \lim_{\Delta t \to 0} \sum \vec{v}(t_i)\Delta t = \int_{0}^{T} \vec{v}(t)\,dt", font_size=32, color=C_STREAM),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act4)
        self.remove(sub_act4)

        with self.voiceover(
            text="이 찰나의 순간변위들을 차곡차곡 누적해 볼까요? 시간 간격을 좁힐수록 거친 꺾은선은 부드러워지고, 마침내 시그마는 적분 인테그랄이 되어 완전히 매끄러운 유선이 됩니다."
        ) as tracker:
            self.play(FadeIn(sub_act4), run_time=0.8)
            # 1단계 성긴 꺾은선
            self.play(
                LaggedStart(*[GrowArrow(a) for a in coarse_arrows], lag_ratio=0.25),
                run_time=2.2,
            )
            self.wait(0.6)
            # 2단계 촘촘한 꺾은선으로 변환
            self.play(
                ReplacementTransform(coarse_arrows, fine_arrows),
                run_time=2.2,
            )
            self.wait(0.6)
            # 3단계 연속 유선으로 승화
            self.play(
                ReplacementTransform(fine_arrows, main_stream),
                run_time=2.5,
            )
            self.wait(max(0.1, tracker.duration - 8.9))

        # [인지적 여백 4] 단 하나의 아름다운 유선 곡선이 맺히는 순간 음미
        self.wait(2.2)

        # =================================================================
        # [Act 5] 결론: 3차원 유체장과 우주의 조망 (2:25 ~ 3:00)
        # =================================================================
        self.play(FadeOut(sub_act4), run_time=0.6)

        # 카메라 원위치 줌아웃 & 서서히 공전 재개
        self.move_camera(
            phi=65 * DEGREES,
            theta=-50 * DEGREES,
            zoom=1.0,
            run_time=2.5,
        )
        self.begin_ambient_camera_rotation(rate=0.08)

        # 전체 공간을 채우는 3b1b 스타일의 유선 군집
        surrounding_streams = VGroup(
            build_streamline(np.array([-1.8, -1.2, -0.8]), color="#60A5FA"),
            build_streamline(np.array([1.2, 1.8, -0.4]), color="#818CF8"),
            build_streamline(np.array([-1.2, 2.0, -0.7]), color=C_STREAM),
            build_streamline(np.array([0.4, -2.0, 0.1]), color="#818CF8"),
            build_streamline(np.array([2.0, 0.5, -0.3]), color="#60A5FA"),
        )

        final_hud = VGroup(
            Text("미적분: 보이지 않는 세계의 질서를 감각하는 수학적 눈", font=FONT_KR, font_size=24, color="#F8FAFC"),
            VGroup(
                Text("찰나의 미분", font=FONT_KR, font_size=18, color=C_VEL),
                MathTex(r"\vec{v} = \frac{d\vec{r} }{dt}", font_size=26, color=C_VEL),
                Text("를 감각하고, 누적된 적분", font=FONT_KR, font_size=18, color="#94A3B8"),
                MathTex(r"\int \vec{v}\,dt", font_size=26, color=C_STREAM),
                Text("으로 흐름을 완성한다", font=FONT_KR, font_size=18, color=C_STREAM),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(final_hud)
        self.remove(final_hud)

        with self.voiceover(
            text="우리는 매 순간의 미분값을 감각하고, 뇌 속에서 그것을 적분하여 바람의 거대한 흐름을 인식합니다. 미적분은 단순한 계산 공식이 아니라, 보이지 않는 세계의 질서를 감각하는 우리의 수학적 눈입니다."
        ) as tracker:
            self.play(
                FadeIn(final_hud),
                Create(surrounding_streams),
                field_arrows.animate.set_opacity(0.4),
                leaves.animate.set_opacity(0.4),
                run_time=3.5,
            )

            # 유선을 타고 유영하는 다중 파티클 무리
            stream_dots = VGroup(*[
                Dot3D(color=C_LEAF, radius=0.08)
                for _ in range(len(surrounding_streams))
            ])
            self.play(
                MoveAlongPath(target_leaf, main_stream),
                *[
                    MoveAlongPath(dot, stream)
                    for dot, stream in zip(stream_dots, surrounding_streams)
                ],
                run_time=max(3.5, tracker.duration - 3.5),
                rate_func=linear,
            )

        # [최종 여운 대기 시간]
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.5)
