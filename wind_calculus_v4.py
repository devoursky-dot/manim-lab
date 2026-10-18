import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

try:
    from manim_voiceover.services.edge import EdgeService
except (ImportError, ModuleNotFoundError):
    from core.edge_service import EdgeService


class WindCalculus3DLectureV4(ThreeDScene, VoiceoverScene):
    """[v4 Masterpiece] 바람과 미적분: 변화량이 아닌 변화율을 감각하는 수학

    핵심 교육 철학:
    1. 미분 = 잘게 쪼개어(微分) 찰나의 작은 구간을 관찰하는 것
    2. 변화량 vs 변화율의 감각적 분리:
       - 찰나를 본 잎(0.1초 관찰) = 작은 이동 거리 (변화량 작음)
       - 오래 본 잎(0.5초 관찰) = 큰 이동 거리 (변화량 큼)
       - 이동거리가 5배나 다른데 왜 같은 바람인가? -> 시간에 대한 '변화율'이 같기 때문!
    3. 순수 딥 블랙 (#000000) + 인지적 여백 (핵심 구간마다 2.0~2.5초 침묵 배정)
    4. 적분으로의 자연스러운 승화: 순간변화율의 누적 = 바람의 전체 유선
    """

    def construct(self):
        # 1. 한국어 AI 성우 및 딥 블랙 캔버스 설정
        self.set_speech_service(
            EdgeService(voice="ko-KR-InJoonNeural", rate="+0%")
        )
        self.camera.background_color = "#000000"
        FONT_KR = "Malgun Gothic"

        # 색상 토큰 (Semantic Color Binding)
        C_VEL = "#FACC15"       # 순간변화율 / 속도 벡터 (Amber Gold)
        C_DISP = "#FB923C"      # 변화량 / 이동 거리 (Vibrant Orange)
        C_STREAM = "#38BDF8"    # 유선 / 적분 곡선 (Electric Cyan)
        C_LEAF = "#4ADE80"      # 나뭇잎 파티클 (Spring Mint)
        C_AXIS = "#334155"      # 좌표축 (Muted Slate)

        # 3D 바람 벡터장 정의 (완만하게 상승하는 소용돌이)
        def wind_field(pos):
            x, y, z = pos
            r = np.sqrt(x**2 + y**2) + 0.1
            vx = -y * 0.65 + 0.35
            vy = x * 0.65 + 0.15
            vz = 0.30 * np.sin(0.55 * r) + 0.22
            return np.array([vx, vy, vz])

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
        # [Act 1] 서론: 작게 쪼개어 보는 미분(微分)의 시작 (0:00 ~ 0:30)
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
        self.begin_ambient_camera_rotation(rate=0.06)

        title_card = VGroup(
            Text("바람과 미적분: 변화량이 아닌 변화율을 보다", font=FONT_KR, font_size=26, color="#F8FAFC"),
            VGroup(
                Text("미분(微分)", font=FONT_KR, font_size=18, color=C_VEL),
                Text(": 작게 쪼개어 순간변화율을 감각하다", font=FONT_KR, font_size=18, color="#94A3B8"),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.15).to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(title_card)
        self.remove(title_card)

        with self.voiceover(
            text="미분은 한자 그대로 작게 나눈다는 뜻입니다. 바람이 불 때 우리는 전체 흐름을 한눈에 보려 하지 않고, 나뭇잎이 흔들리는 찰나의 작은 구간을 떼어내어 관찰합니다."
        ) as tracker:
            self.play(
                Create(axes),
                FadeIn(title_card, shift=DOWN * 0.2),
                run_time=min(3.5, tracker.duration),
            )
            self.wait(max(0.1, tracker.duration - 3.5))

        # [인지적 여백 1]
        self.wait(1.5)

        # =================================================================
        # [Act 2] 변화량의 역설: 거리가 다른데 왜 같은 바람인가? (0:30 ~ 1:05)
        # =================================================================
        # 3D 회전을 잠시 멈추고 2D 비교 모드로 전환
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.1, run_time=1.8)

        # Leaf A: 0.1초 동안 0.2m 이동
        pA_start = np.array([-3.2, 0.8, 0])
        pA_end = np.array([-2.4, 0.8, 0])
        leafA = Dot(point=pA_start, radius=0.10, color=C_LEAF)
        arrowA = Arrow(pA_start, pA_end, buff=0, color=C_DISP, stroke_width=4.5, max_tip_length_to_length_ratio=0.25)

        cardA = VGroup(
            Text("나뭇잎 A (찰나의 관찰)", font=FONT_KR, font_size=18, color=C_LEAF),
            VGroup(
                Text("시간 ", font=FONT_KR, font_size=15, color="#94A3B8"),
                MathTex(r"\Delta t_A = 0.1\text{ s}", font_size=20, color="#94A3B8"),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("이동 거리(변화량) ", font=FONT_KR, font_size=16, color=C_DISP),
                MathTex(r"\Delta r_A = 0.2\text{ m}", font_size=22, color=C_DISP),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(pA_start, UP, buff=0.35)

        # Leaf B: 0.5초 동안 1.0m 이동
        pB_start = np.array([-3.2, -1.2, 0])
        pB_end = np.array([0.8, -1.2, 0])
        leafB = Dot(point=pB_start, radius=0.10, color=C_LEAF)
        arrowB = Arrow(pB_start, pB_end, buff=0, color=C_DISP, stroke_width=4.5, max_tip_length_to_length_ratio=0.15)

        cardB = VGroup(
            Text("나뭇잎 B (더 긴 관찰)", font=FONT_KR, font_size=18, color=C_LEAF),
            VGroup(
                Text("시간 ", font=FONT_KR, font_size=15, color="#94A3B8"),
                MathTex(r"\Delta t_B = 0.5\text{ s}", font_size=20, color="#94A3B8"),
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                Text("이동 거리(변화량) ", font=FONT_KR, font_size=16, color=C_DISP),
                MathTex(r"\Delta r_B = 1.0\text{ m}", font_size=22, color=C_DISP),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(pB_start, UP, buff=0.35)

        sub_act2 = VGroup(
            Text("변화량(이동 거리)이 5배나 다른데, 왜 우리는 같은 바람이라고 느낄까?", font=FONT_KR, font_size=22, color="#F8FAFC"),
        ).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(sub_act2)
        self.remove(sub_act2)

        with self.voiceover(
            text="여기 같은 바람을 맞고 있는 두 나뭇잎이 있습니다. 찰나를 본 나뭇잎은 0.2미터를 움직였고, 더 오래 본 나뭇잎은 1미터를 움직였죠. 움직인 거리, 즉 변화량이 5배나 다른데 바람의 세기도 다를까요? 아닙니다. 우리는 본능적으로 같은 바람이라고 느낍니다."
        ) as tracker:
            self.play(FadeIn(sub_act2), run_time=1.0)
            self.play(
                FadeIn(leafA), FadeIn(cardA),
                FadeIn(leafB), FadeIn(cardB),
                run_time=1.5,
            )
            # 두 나뭇잎의 이동
            self.play(
                GrowArrow(arrowA), leafA.animate.move_to(pA_end),
                GrowArrow(arrowB), leafB.animate.move_to(pB_end),
                run_time=max(2.0, tracker.duration - 2.5),
            )

        # [인지적 여백 2] 변화량의 차이를 눈으로 응시하는 시간
        self.wait(2.2)

        # =================================================================
        # [Act 3] 시각적 도약: 시간으로 나누어 일치하는 변화율 (1:05 ~ 1:45)
        # =================================================================
        # 시간으로 나눈 속도 벡터 (동일한 길이: 2.0m/s -> 2.5 단위 길이로 표현)
        rateA_end = pA_start + RIGHT * 2.5
        rateB_end = pB_start + RIGHT * 2.5

        rate_arrowA = Arrow(pA_start, rateA_end, buff=0, color=C_VEL, stroke_width=5.5, max_tip_length_to_length_ratio=0.20)
        rate_arrowB = Arrow(pB_start, rateB_end, buff=0, color=C_VEL, stroke_width=5.5, max_tip_length_to_length_ratio=0.20)

        rate_cardA = VGroup(
            Text("나뭇잎 A의 변화율", font=FONT_KR, font_size=18, color=C_VEL),
            MathTex(r"\frac{\Delta r_A}{\Delta t_A} = \frac{0.2}{0.1} = 2\text{ m/s}", font_size=24, color=C_VEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(pA_start, UP, buff=0.35)

        rate_cardB = VGroup(
            Text("나뭇잎 B의 변화율", font=FONT_KR, font_size=18, color=C_VEL),
            MathTex(r"\frac{\Delta r_B}{\Delta t_B} = \frac{1.0}{0.5} = 2\text{ m/s}", font_size=24, color=C_VEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(pB_start, UP, buff=0.35)

        sub_act3 = VGroup(
            Text("우리가 느끼는 것은 변화량이 아니라, 시간에 따른 '변화율'이다!", font=FONT_KR, font_size=23, color=C_VEL),
            VGroup(
                Text("순간변화율(속도) ", font=FONT_KR, font_size=20, color=C_VEL),
                MathTex(r"\vec{v} = \frac{\Delta \vec{r} }{\Delta t} = 2\text{ m/s}", font_size=28, color=C_VEL),
                Text(" (완벽히 일치!)", font=FONT_KR, font_size=20, color="#86EFAC"),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act3)
        self.remove(sub_act3)

        with self.voiceover(
            text="우리의 감각은 나뭇잎이 얼마나 멀리 갔는지, 그 단순한 변화량을 느끼는 것이 아닙니다. 이동한 거리를 시간으로 나눈 변화율을 느끼는 것이죠. 0.2미터를 0.1초 만에 간 것이나, 1미터를 0.5초 만에 간 것이나 시간당 변화율은 1초에 2미터로 완벽하게 같습니다."
        ) as tracker:
            self.play(FadeOut(sub_act2), FadeIn(sub_act3), run_time=1.0)
            # 길이가 다르던 두 주황색 화살표가 같은 길이의 황금빛 벡터로 수렴!
            self.play(
                ReplacementTransform(cardA, rate_cardA),
                ReplacementTransform(cardB, rate_cardB),
                ReplacementTransform(arrowA, rate_arrowA),
                ReplacementTransform(arrowB, rate_arrowB),
                leafA.animate.move_to(pA_start),
                leafB.animate.move_to(pB_start),
                run_time=max(2.5, tracker.duration - 1.0),
            )

        # [인지적 여백 3] 두 벡터가 완벽히 같아지는 마법의 순간 음미
        self.wait(2.5)

        # =================================================================
        # [Act 4] 극한: 순간변화율 = 미분의 탄생 (1:45 ~ 2:20)
        # =================================================================
        self.play(
            FadeOut(rate_cardA), FadeOut(rate_cardB),
            FadeOut(rate_arrowA), FadeOut(rate_arrowB),
            FadeOut(leafA), FadeOut(leafB),
            FadeOut(sub_act3),
            run_time=0.8,
        )

        # 다시 3D 뷰로 복귀
        self.move_camera(phi=70 * DEGREES, theta=-25 * DEGREES, zoom=1.5, run_time=2.0)

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

        sub_act4 = VGroup(
            Text("관찰 시간을 극한으로 줄인 순간의 변화율 = 미분", font=FONT_KR, font_size=23, color=C_LEAF),
            MathTex(r"\vec{v}(t) = \lim_{\Delta t \to 0} \frac{\Delta \vec{r} }{\Delta t} = \frac{d\vec{r} }{dt}", font_size=32, color=C_VEL),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act4)
        self.remove(sub_act4)

        with self.voiceover(
            text="이 관찰 시간 delta t를 무한히 0으로 줄인 극한, 그것이 바로 미분입니다. 우리가 바람이 세다, 약하다고 느낄 때 그것은 나뭇잎의 위치를 시간에 대해 미분한 순간변화율을 뇌가 실시간으로 감각하고 있는 것입니다."
        ) as tracker:
            self.play(
                FadeIn(target_leaf, scale=1.5),
                GrowArrow(tangent_arrow),
                FadeIn(sub_act4),
                run_time=min(3.0, tracker.duration),
            )
            self.wait(max(0.1, tracker.duration - 3.0))

        # [인지적 여백 4] 찰나의 순간변화율(미분) 음미
        self.wait(2.2)

        # =================================================================
        # [Act 5] 적분: 순간변화율을 다시 모아 흐름을 완성하다 (2:20 ~ 3:00)
        # =================================================================
        self.play(
            FadeOut(sub_act4),
            FadeOut(tangent_arrow),
            run_time=0.6,
        )

        # 3단계 적분 빌드업: 꺾은선 -> 촘촘한 꺾은선 -> 매끄러운 유선
        p_c = target_p.copy()
        coarse_arrows = VGroup()
        for _ in range(3):
            v_step = wind_field(p_c)
            next_c = p_c + v_step * 0.60
            coarse_arrows.add(Arrow(start=p_c, end=next_c, buff=0, color=C_DISP, stroke_width=4.5))
            p_c = next_c

        p_f = target_p.copy()
        fine_arrows = VGroup()
        for _ in range(7):
            v_step = wind_field(p_f)
            next_f = p_f + v_step * 0.22
            fine_arrows.add(Arrow(start=p_f, end=next_f, buff=0, color="#F59E0B", stroke_width=3.5))
            p_f = next_f

        main_stream = build_streamline(target_p, steps=70, step_dt=0.065, color=C_STREAM)

        # 카메라 전체 줌아웃 & 서서히 공전
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=0.95, run_time=2.2)
        self.begin_ambient_camera_rotation(rate=0.08)

        surrounding_streams = VGroup(
            build_streamline(np.array([-1.8, -1.2, -0.8]), color="#60A5FA"),
            build_streamline(np.array([1.2, 1.8, -0.4]), color="#818CF8"),
            build_streamline(np.array([-1.2, 2.0, -0.7]), color=C_STREAM),
            build_streamline(np.array([0.4, -2.0, 0.1]), color="#818CF8"),
            build_streamline(np.array([2.0, 0.5, -0.3]), color="#60A5FA"),
        )

        final_hud = VGroup(
            Text("미적분: 순간변화율을 느끼고, 누적하여 세상을 보다", font=FONT_KR, font_size=24, color="#F8FAFC"),
            VGroup(
                Text("순간변화율(미분) ", font=FONT_KR, font_size=18, color=C_VEL),
                MathTex(r"\vec{v} = \frac{d\vec{r} }{dt}", font_size=26, color=C_VEL),
                Text("을 모아 전체 유선(적분) ", font=FONT_KR, font_size=18, color="#94A3B8"),
                MathTex(r"\int \vec{v}\,dt", font_size=26, color=C_STREAM),
                Text("을 완성한다", font=FONT_KR, font_size=18, color=C_STREAM),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(final_hud)
        self.remove(final_hud)

        with self.voiceover(
            text="그리고 이 순간변화율들을 다시 차곡차곡 누적하는 것, 그것이 적분입니다. 우리는 매 찰나의 미분값을 감각하고, 뇌 속에서 이를 적분하여 바람의 전체 흐름을 인식합니다. 미적분은 세상을 인식하는 우리의 감각입니다."
        ) as tracker:
            self.play(FadeIn(final_hud), run_time=1.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in coarse_arrows], lag_ratio=0.2), run_time=1.8)
            self.play(ReplacementTransform(coarse_arrows, fine_arrows), run_time=1.8)
            self.play(
                ReplacementTransform(fine_arrows, main_stream),
                Create(surrounding_streams),
                run_time=2.5,
            )

            stream_dots = VGroup(*[Dot3D(color=C_LEAF, radius=0.08) for _ in range(len(surrounding_streams))])
            self.play(
                MoveAlongPath(target_leaf, main_stream),
                *[MoveAlongPath(dot, stream) for dot, stream in zip(stream_dots, surrounding_streams)],
                run_time=max(3.0, tracker.duration - 7.1),
                rate_func=linear,
            )

        # [최종 여운 대기 시간]
        self.wait(3.0)
        self.stop_ambient_camera_rotation()
        self.wait(1.5)
