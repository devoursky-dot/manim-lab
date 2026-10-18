import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

try:
    from manim_voiceover.services.edge import EdgeService
except (ImportError, ModuleNotFoundError):
    from core.edge_service import EdgeService


class WindCalculus3DLectureV6(ThreeDScene, VoiceoverScene):
    """
    [v6 Masterpiece] 인간은 세상을 어떻게 미분하는가? : 감각의 인식론
    
    3Blue1Brown 스타일 비주얼 개편:
    1. 조화진동 물리 + 실시간 x(t) 위상 그래프 & 원점 접선(Tangent) 기울기(2.4 m/s) 완전 일치 기하학적 증명
    2. 세련된 광학계 다이어그램: 눈 렌즈 + 망막 각속도 보정 Pill Badge
    3. 3D 투영의 혁신:
       - 미세 좌표 그리드가 새겨진 반투명 사파이어 글래스 센서 스크린
       - 3D 입체 궤적과 관찰자 사이를 잇는 빛의 광추(Projection Ray Frustum)
       - 3D 공간에서 2D 센서 스크린 정면으로 카메라가 날아와 밀착하는 시점 전환 (3B1B Signature)
    4. 글래스모피즘 Pill Badge 시스템 및 슬레이트 3D 바닥 접지 그리드
    """

    def construct(self):
        # 1. 한국어 AI 성우 및 딥 블랙 캔버스 설정
        self.set_speech_service(
            EdgeService(voice="ko-KR-InJoonNeural", rate="+0%")
        )
        self.camera.background_color = "#000000"
        FONT_KR = "Malgun Gothic"

        # 정제된 큐레이티드 컬러 팔레트 (Tailwind Slate / Emerald / Amber / Sky)
        C_VEL = "#FACC15"       # 순간변화율 / 속도 벡터 / 접선 (Amber Gold)
        C_DISP = "#FB923C"      # 변화량 / 진폭 (Vibrant Orange)
        C_STREAM = "#38BDF8"    # 유선 / 적분 곡선 (Electric Cyan)
        C_LEAF = "#4ADE80"      # 나뭇잎 (Spring Mint)
        C_AXIS = "#475569"      # 기준축 (Slate Gray)
        C_GRID = "#1E293B"      # 바닥 그리드 (Dark Slate)
        C_GLASS = "#0284C7"     # 센서 글래스 (Sapphire Blue)

        # -------------------------------------------------------------
        # UI 도우미: 글래스모피즘 필 배지 (Pill Badge)
        # -------------------------------------------------------------
        def make_badge(content, fill_color="#090D16", stroke_color="#334155", stroke_width=1.2, fill_opacity=0.88, buff=0.15):
            box = RoundedRectangle(
                corner_radius=0.14,
                width=content.width + buff * 2.2,
                height=content.height + buff * 1.8,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                stroke_color=stroke_color,
                stroke_width=stroke_width,
            )
            content.move_to(box.get_center())
            return VGroup(box, content)

        # -------------------------------------------------------------
        # 나뭇잎 형태 생성 도우미
        # -------------------------------------------------------------
        def make_leaf_mobject(scale_val=1.0, color=C_LEAF):
            body = Ellipse(width=0.45 * scale_val, height=0.22 * scale_val, color=color, fill_opacity=0.9, stroke_width=1.5)
            vein = Line(LEFT * 0.20 * scale_val, RIGHT * 0.20 * scale_val, color="#A7F3D0", stroke_width=1.2)
            stem = Line(LEFT * 0.32 * scale_val, LEFT * 0.18 * scale_val, color=C_AXIS, stroke_width=2.0)
            return VGroup(body, vein, stem)

        # 3D 바람 벡터장 정의
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
            curve = VMobject(color=color, stroke_width=3.2)
            curve.set_points_smoothly(pts)
            return curve

        # =================================================================
        # [Act 1 & 2] 조화진동 물리 + 실시간 x(t) 위상 그래프 & 미분 접선 일치
        # =================================================================
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.0)

        # 헤더 타이틀 배지
        title_raw = VGroup(
            Text("인간은 세상을 어떻게 미분하는가? : 감각의 인식론", font=FONT_KR, font_size=20, color="#F8FAFC"),
            VGroup(
                Text("미분(순간변화율)", font=FONT_KR, font_size=15, color=C_VEL),
                Text(": 변화량이 아닌 변화율(접선 기울기)을 인지하는 뇌", font=FONT_KR, font_size=15, color="#94A3B8"),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        header_badge = make_badge(title_raw, stroke_color="#38BDF8", buff=0.16).to_corner(UL, buff=0.35)

        self.add_fixed_in_frame_mobjects(header_badge)
        self.remove(header_badge)

        # -------------------------------------------------------------
        # 좌측: 물리 진동 공간 / 우측: 실시간 x-t 그래프 공간
        # -------------------------------------------------------------
        # 1. 작은 나뭇잎 (위)
        origin_small = np.array([-4.5, 1.3, 0])
        stem_small = Line(origin_small + LEFT * 1.2, origin_small, color=C_AXIS, stroke_width=2.5)
        A_small, w_small = 0.50, 4.8   # v_max = 0.5 * 4.8 = 2.4 m/s

        # 2. 큰 나뭇잎 (아래)
        origin_large = np.array([-4.5, -1.3, 0])
        stem_large = Line(origin_large + LEFT * 1.2, origin_large, color=C_AXIS, stroke_width=3.5)
        A_large, w_large = 1.50, 1.6   # v_max = 1.5 * 1.6 = 2.4 m/s (완벽 일치)

        t_tracker = ValueTracker(0)

        # 동적 나뭇잎
        leaf_small = always_redraw(lambda: make_leaf_mobject(scale_val=0.75, color=C_LEAF).move_to(
            origin_small + RIGHT * (A_small * np.sin(w_small * t_tracker.get_value()))
        ))
        leaf_large = always_redraw(lambda: make_leaf_mobject(scale_val=1.8, color=C_LEAF).move_to(
            origin_large + RIGHT * (A_large * np.sin(w_large * t_tracker.get_value()))
        ))

        # 좌측 물리 라벨 배지
        lbl_s_raw = VGroup(
            Text("작은 잎 (바르르 빠른 떨림)", font=FONT_KR, font_size=13, color=C_LEAF),
            Text("진폭(변화량) A1 = 0.5m", font=FONT_KR, font_size=12, color=C_DISP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        lbl_badge_s = make_badge(lbl_s_raw, stroke_color=C_DISP, buff=0.1).next_to(origin_small, UP, buff=0.25)

        lbl_l_raw = VGroup(
            Text("큰 잎 (너울너울 큰 흔들림)", font=FONT_KR, font_size=13, color=C_LEAF),
            Text("진폭(변화량) A2 = 1.5m", font=FONT_KR, font_size=12, color=C_DISP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        lbl_badge_l = make_badge(lbl_l_raw, stroke_color=C_DISP, buff=0.1).next_to(origin_large, UP, buff=0.25)

        # 우측: 3Blue1Brown 스타일 실시간 x(t) 위상 그래프 좌표축 (동일한 Y축 스케일로 접선 기울기 직관 비교)
        graph_origin_s = np.array([0.5, 1.3, 0])
        axes_s = Axes(
            x_range=[0, 3.5, 1.0], y_range=[-1.8, 1.8, 1.0],
            x_length=4.8, y_length=1.6,
            axis_config={"color": "#475569", "stroke_width": 1.5},
            tips=False,
        ).move_to(graph_origin_s)
        axes_s_lbl = Text("시간-변위 그래프 x₁(t) [소진폭 0.5m]", font=FONT_KR, font_size=12, color="#94A3B8").next_to(axes_s, UP, buff=0.1)

        graph_origin_l = np.array([0.5, -1.3, 0])
        axes_l = Axes(
            x_range=[0, 3.5, 1.0], y_range=[-1.8, 1.8, 1.0],
            x_length=4.8, y_length=1.6,
            axis_config={"color": "#475569", "stroke_width": 1.5},
            tips=False,
        ).move_to(graph_origin_l)
        axes_l_lbl = Text("시간-변위 그래프 x₂(t) [대진폭 1.5m]", font=FONT_KR, font_size=12, color="#94A3B8").next_to(axes_l, UP, buff=0.1)

        # 실시간 그려지는 사인 곡선
        def get_sin_curve_s():
            t_curr = min(3.5, t_tracker.get_value())
            if t_curr < 0.05:
                t_curr = 0.05
            return axes_s.plot(lambda t: A_small * np.sin(w_small * t), x_range=[0, t_curr], color=C_LEAF, stroke_width=2.5)

        def get_sin_curve_l():
            t_curr = min(3.5, t_tracker.get_value())
            if t_curr < 0.05:
                t_curr = 0.05
            return axes_l.plot(lambda t: A_large * np.sin(w_large * t), x_range=[0, t_curr], color=C_LEAF, stroke_width=2.5)

        curve_s_dynamic = always_redraw(get_sin_curve_s)
        curve_l_dynamic = always_redraw(get_sin_curve_l)

        # 원점을 통과하는 순간의 접선(Tangent) 기울기 표시선 (기울기 dx/dt = 2.4 m/s 완벽 평행 일치!)
        tangent_s = Line(
            axes_s.c2p(-0.35, -0.35 * 2.4),
            axes_s.c2p(0.35, 0.35 * 2.4),
            color=C_VEL, stroke_width=4.0
        )
        tangent_l = Line(
            axes_l.c2p(-0.35, -0.35 * 2.4),
            axes_l.c2p(0.35, 0.35 * 2.4),
            color=C_VEL, stroke_width=4.0
        )

        # 하단 설명 배지 (Act 1)
        sub_act1_raw = VGroup(
            Text("두 나뭇잎의 진폭(변화량)은 3배나 다르지만, 우리는 정확히 같은 바람 세기로 인지한다", font=FONT_KR, font_size=16, color="#F8FAFC"),
            Text("왜 뇌는 서로 다른 흔들림의 크기 속에서 동일한 바람을 알아챌 수 있을까?", font=FONT_KR, font_size=15, color="#94A3B8"),
        ).arrange(DOWN, buff=0.08)
        sub_act1_badge = make_badge(sub_act1_raw, stroke_color="#334155", buff=0.15).to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(sub_act1_badge)
        self.remove(sub_act1_badge)

        with self.voiceover(
            text="바람이 불 때 나뭇잎을 유심히 관찰해 보세요. 작은 나뭇잎은 바르르 빠르게 떨리고, 큰 나뭇잎은 너울너울 크게 요동칩니다. 두 나뭇잎이 움직이는 진폭, 즉 변화량은 세 배나 차이가 납니다. 하지만 우리는 변화량이 달라도 정확히 같은 바람의 세기로 인지합니다. 왜 그럴까요?"
        ) as tracker:
            self.play(FadeIn(header_badge, shift=DOWN * 0.2), FadeIn(sub_act1_badge), run_time=1.0)
            self.play(
                Create(stem_small), Create(stem_large),
                FadeIn(lbl_badge_s), FadeIn(lbl_badge_l),
                Create(axes_s), Create(axes_l),
                Write(axes_s_lbl), Write(axes_l_lbl),
                run_time=1.4,
            )
            self.add(leaf_small, leaf_large, curve_s_dynamic, curve_l_dynamic)
            # 조화 진동 및 실시간 그래프 생성
            self.play(
                t_tracker.animate.set_value(2.8),
                run_time=max(2.5, tracker.duration - 2.6),
                rate_func=linear,
            )

        # [인지적 여백 1] 두 그래프의 진동 차이 음미
        self.wait(1.8)

        # -------------------------------------------------------------
        # [Act 2 Climax] 접선(Tangent) 등장: 기울기(순간변화율) 2.4 m/s 완전 일치
        # -------------------------------------------------------------
        sub_act2_raw = VGroup(
            Text("뇌는 '흔들림의 크기(변화량)'가 아니라, '그래프의 순간 접선 기울기(변화율)'를 본다!", font=FONT_KR, font_size=17, color=C_VEL),
            VGroup(
                Text("최고 순간속도(미분계수) ", font=FONT_KR, font_size=15, color=C_VEL),
                MathTex(r"v_{\max} = A_1 \cdot \omega_1 = A_2 \cdot \omega_2 = 2.4\text{ m/s}", font_size=20, color=C_VEL),
                Text(" [완벽 평행 일치!]", font=FONT_KR, font_size=15, color="#86EFAC"),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.08)
        sub_act2_badge = make_badge(sub_act2_raw, stroke_color=C_VEL, fill_color="#181303", buff=0.16).to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(sub_act2_badge)
        self.remove(sub_act2_badge)

        with self.voiceover(
            text="우리의 뇌는 단순한 진폭의 거리, 즉 변화량을 느끼는 것이 아닙니다. 짧은 주기로 나눈 시간당 변화율, 바로 이 그래프의 접선 기울기를 감각하기 때문입니다. 작은 잎의 촘촘한 파형이나 큰 잎의 완만한 파형이나, 중심을 지나는 순간의 최고 속도인 접선 기울기는 초당 2.4미터로 완벽하게 같습니다!"
        ) as tracker:
            self.play(
                ReplacementTransform(sub_act1_badge, sub_act2_badge),
                run_time=0.8,
            )
            # 접선 화살표 번쩍이며 강조
            self.play(
                GrowFromCenter(tangent_s),
                GrowFromCenter(tangent_l),
                run_time=1.2,
            )
            self.play(
                tangent_s.animate.set_stroke(color="#FEF08A", width=5.5),
                tangent_l.animate.set_stroke(color="#FEF08A", width=5.5),
                run_time=0.8,
            )
            self.play(
                tangent_s.animate.set_stroke(color=C_VEL, width=4.0),
                tangent_l.animate.set_stroke(color=C_VEL, width=4.0),
                run_time=max(1.0, tracker.duration - 2.8),
            )

        # [인지적 여백 2] 접선 기울기가 동일함을 깊이 있게 소화
        self.wait(2.5)

        # =================================================================
        # [Act 3] 원근의 착시: 가까운 잎 vs 먼 잎, 뇌의 미분 보정 센서
        # =================================================================
        self.play(
            FadeOut(leaf_small), FadeOut(leaf_large),
            FadeOut(curve_s_dynamic), FadeOut(curve_l_dynamic),
            FadeOut(stem_small), FadeOut(stem_large),
            FadeOut(lbl_badge_s), FadeOut(lbl_badge_l),
            FadeOut(axes_s), FadeOut(axes_l),
            FadeOut(axes_s_lbl), FadeOut(axes_l_lbl),
            FadeOut(tangent_s), FadeOut(tangent_l),
            FadeOut(sub_act2_badge),
            run_time=0.8,
        )

        # 3Blue1Brown 스타일 세련된 광학 다이어그램
        eye_center = np.array([-5.0, 0, 0])
        eye_lens = Arc(radius=0.45, start_angle=-PI / 3, angle=2 * PI / 3, color="#38BDF8", stroke_width=3.0).shift(eye_center)
        eye_pupil = Dot(point=eye_center, radius=0.08, color="#F8FAFC")
        eye_tag_raw = Text("관찰자의 눈 (미분 센서)", font=FONT_KR, font_size=13, color="#38BDF8")
        eye_badge = make_badge(eye_tag_raw, stroke_color="#38BDF8", buff=0.1).next_to(eye_lens, DOWN, buff=0.25)

        # 1m 앞 가까운 나뭇잎 vs 10m 뒤 먼 나뭇잎
        pos_near = np.array([-1.5, 0, 0])
        pos_far = np.array([4.0, 0, 0])

        leaf_near_obj = make_leaf_mobject(scale_val=1.2, color=C_LEAF).move_to(pos_near)
        leaf_far_obj = make_leaf_mobject(scale_val=0.5, color=C_LEAF).move_to(pos_far)

        # 광선 (시선 DashedLine)
        ray_top_near = DashedLine(eye_center, pos_near + UP * 1.0, color="#64748B", stroke_width=1.5, dash_length=0.1)
        ray_bot_near = DashedLine(eye_center, pos_near + DOWN * 1.0, color="#64748B", stroke_width=1.5, dash_length=0.1)
        motion_near = DoubleArrow(pos_near + DOWN * 1.0, pos_near + UP * 1.0, buff=0, color=C_DISP, stroke_width=3.0)

        ray_top_far = DashedLine(eye_center, pos_far + UP * 0.35, color="#475569", stroke_width=1.2, dash_length=0.1)
        ray_bot_far = DashedLine(eye_center, pos_far + DOWN * 0.35, color="#475569", stroke_width=1.2, dash_length=0.1)
        motion_far = DoubleArrow(pos_far + DOWN * 0.35, pos_far + UP * 0.35, buff=0, color=C_DISP, stroke_width=2.2)

        # 망막 상의 각도 표시 호
        retina_arc_near = Arc(radius=1.2, start_angle=-0.32, angle=0.64, arc_center=eye_center, color=C_DISP, stroke_width=3.0)
        retina_arc_far = Arc(radius=1.8, start_angle=-0.06, angle=0.12, arc_center=eye_center, color="#94A3B8", stroke_width=2.5)

        near_card_raw = VGroup(
            Text("가까운 나뭇잎 (거리 d = 1m)", font=FONT_KR, font_size=13, color=C_LEAF),
            Text("망막 각도 변화량: 매우 큼 (Δθ₁)", font=FONT_KR, font_size=12, color=C_DISP),
        ).arrange(DOWN, buff=0.04)
        near_card = make_badge(near_card_raw, stroke_color=C_LEAF, buff=0.1).next_to(motion_near, UP, buff=0.2)

        far_card_raw = VGroup(
            Text("먼 나뭇잎 (거리 d = 10m)", font=FONT_KR, font_size=13, color=C_LEAF),
            Text("망막 각도 변화량: 매우 작음 (Δθ₂)", font=FONT_KR, font_size=12, color="#94A3B8"),
        ).arrange(DOWN, buff=0.04)
        far_card = make_badge(far_card_raw, stroke_color="#475569", buff=0.1).next_to(motion_far, UP, buff=0.2)

        sub_act3_raw = VGroup(
            Text("망막의 변화량은 10배 차이나지만, 뇌는 거리와 시간을 나눈 '변화율'을 계산한다", font=FONT_KR, font_size=16, color="#F8FAFC"),
            VGroup(
                Text("뇌의 미분 연산: ", font=FONT_KR, font_size=15, color=C_VEL),
                MathTex(r"v \approx d \cdot \frac{d\theta}{dt} = 2.4\text{ m/s}", font_size=18, color=C_VEL),
                Text(" [모든 거리에서 동일한 바람 속도로 정규화]", font=FONT_KR, font_size=14, color="#86EFAC"),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.08)
        sub_act3_badge = make_badge(sub_act3_raw, stroke_color=C_VEL, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(sub_act3_badge)
        self.remove(sub_act3_badge)

        with self.voiceover(
            text="나뭇잎을 눈앞에서 볼 때와 저 멀리 숲속에서 볼 때를 생각해 보세요. 망막에 맺히는 상의 움직인 크기, 즉 변화량은 10배 이상 차이가 납니다. 하지만 우리는 저 멀리 부는 바람도 여기와 똑같은 세기라는 것을 즉시 압니다. 우리 뇌는 망막의 변화량에 속지 않고, 거리와 시간으로 나눈 본질적인 변화율을 계산해내기 때문입니다. 인간은 뇌 속에 미분을 인지하는 센서를 탑재하고 태어난 것이죠."
        ) as tracker:
            self.play(FadeIn(sub_act3_badge), run_time=0.8)
            self.play(
                Create(eye_lens), FadeIn(eye_pupil), FadeIn(eye_badge),
                FadeIn(leaf_near_obj), FadeIn(leaf_far_obj),
                run_time=1.6,
            )
            self.play(
                Create(ray_top_near), Create(ray_bot_near), Create(motion_near),
                Create(retina_arc_near), FadeIn(near_card),
                Create(ray_top_far), Create(ray_bot_far), Create(motion_far),
                Create(retina_arc_far), FadeIn(far_card),
                run_time=max(2.0, tracker.duration - 2.5),
            )

        # [인지적 여백 3] 뇌의 미분 센서 원리 음미
        self.wait(2.5)

        # =================================================================
        # [Act 4] 차원의 미분과 적분: 3D 세상을 2D 망막 센서로 자르다 (Slicing)
        # =================================================================
        self.play(
            FadeOut(eye_lens), FadeOut(eye_pupil), FadeOut(eye_badge),
            FadeOut(leaf_near_obj), FadeOut(leaf_far_obj),
            FadeOut(ray_top_near), FadeOut(ray_bot_near), FadeOut(motion_near),
            FadeOut(ray_top_far), FadeOut(ray_bot_far), FadeOut(motion_far),
            FadeOut(retina_arc_near), FadeOut(retina_arc_far),
            FadeOut(near_card), FadeOut(far_card),
            FadeOut(sub_act3_badge),
            run_time=0.8,
        )

        # 3D 공간으로 카메라 전환 (아이소메트릭 입체 뷰)
        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=1.1, run_time=2.0)

        # 3D 공간의 안정적 접지를 위한 슬레이트 바닥 격자판
        ground_grid = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-4, 4, 1],
            x_length=10, y_length=8,
            background_line_style={"stroke_color": C_GRID, "stroke_width": 1.0, "stroke_opacity": 0.4},
            axis_config={"stroke_color": "#334155", "stroke_width": 1.2, "stroke_opacity": 0.6},
        ).shift(OUT * -1.8)

        # 3D 관찰자 눈 (초점)
        eye_3d = Dot3D(point=np.array([-3.8, -1.8, 0]), radius=0.16, color="#38BDF8")

        # -------------------------------------------------------------
        # 세련된 반투명 사파이어 글래스 센서 스크린 (2차원 망막 단면)
        # -------------------------------------------------------------
        screen_center = np.array([-1.2, -0.6, 0.2])
        screen_glass = Rectangle(
            width=3.6, height=2.6,
            color=C_STREAM, fill_color="#0369A1", fill_opacity=0.25, stroke_width=2.5
        ).move_to(screen_center)

        grid_h = DashedLine(screen_center + LEFT * 1.7, screen_center + RIGHT * 1.7, color="#38BDF8", stroke_width=1.0, stroke_opacity=0.5)
        grid_v = DashedLine(screen_center + DOWN * 1.2, screen_center + UP * 1.2, color="#38BDF8", stroke_width=1.0, stroke_opacity=0.5)
        screen_group = VGroup(screen_glass, grid_h, grid_v)

        # 3D 공간을 관통하는 입체 바람/나뭇잎 나선 궤적 (입체 실체)
        t_samples = np.linspace(0, 3.4, 60)
        pts_3d = [np.array([1.5 * np.cos(t) + 0.8, 1.4 * np.sin(t) + 0.4, 0.65 * t - 0.9]) for t in t_samples]
        curve_3d_real = VMobject(color=C_LEAF, stroke_width=4.0).set_points_smoothly(pts_3d)

        # 2차원 글래스 센서 평면에 투영된 사영 궤적 (Screen Coordinate 사영)
        pts_2d_proj = [np.array([-1.2 + 0.65 * (p[0] - 0.8), -0.6 + 0.55 * (p[1] - 0.4), 0.2]) for p in pts_3d]
        curve_2d_proj = VMobject(color=C_VEL, stroke_width=3.2).set_points_smoothly(pts_2d_proj)

        # 3D 입자 및 2D 투영 입자
        dot_3d_real = Dot3D(point=pts_3d[0], radius=0.14, color=C_LEAF)
        dot_2d_proj = Dot3D(point=pts_2d_proj[0], radius=0.10, color=C_VEL)

        # 3D 실체 -> 2D 스크린을 잇는 빛의 투영 광선 (Projection Ray)
        ray_frustum = always_redraw(lambda: DashedLine(
            dot_3d_real.get_center(),
            dot_2d_proj.get_center(),
            color="#FEF08A", stroke_width=1.8, dash_length=0.08
        ))

        sub_act4_raw = VGroup(
            Text("3차원 세상을 빛의 축으로 자른 2차원 평면 이미지로 보는 것 = 공간의 미분(d/dz)", font=FONT_KR, font_size=16, color=C_STREAM),
            Text("그리고 뇌가 시간 속에서 이 단면들을 적분하여 3차원 입체 세상을 복원하는 것 = 적분(∫ dt)", font=FONT_KR, font_size=16, color=C_VEL),
        ).arrange(DOWN, buff=0.08)
        sub_act4_badge = make_badge(sub_act4_raw, stroke_color=C_STREAM, buff=0.16).to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(sub_act4_badge)
        self.remove(sub_act4_badge)

        with self.voiceover(
            text="우리는 눈을 통해 3차원 세계를 바라봅니다. 하지만 생각해보세요. 실제 우리 눈이 받아들이는 것은 오직 2차원의 평면 이미지입니다. 3차원 세상을 빛의 축으로 한 겹 잘라낸 2차원 미분 단면을 보는 것이죠. 그리고 우리의 뇌는 이 미분된 2차원 순간들을 시간 속에서 차곡차곡 적분하여, 3차원의 거대한 입체 세계를 다시 재구성해냅니다."
        ) as tracker:
            self.play(FadeIn(sub_act4_badge), run_time=0.8)
            self.play(
                Create(ground_grid),
                FadeIn(eye_3d),
                Create(screen_group),
                Create(curve_3d_real),
                Create(curve_2d_proj),
                FadeIn(dot_3d_real),
                FadeIn(dot_2d_proj),
                Create(ray_frustum),
                run_time=2.4,
            )

            # 동시 이동 애니메이션: 3D 실체와 2D 투영면 위의 상이 함께 흐름
            self.play(
                MoveAlongPath(dot_3d_real, curve_3d_real),
                MoveAlongPath(dot_2d_proj, curve_2d_proj),
                run_time=max(3.0, tracker.duration - 3.4),
                rate_func=linear,
            )

        # -------------------------------------------------------------
        # [3Blue1Brown 시그니처 시점 전환] 센서 스크린 정면으로 카메라 줌인 밀착
        # "이것이 바로 눈에 맺히는 2차원 미분 단면입니다"
        # -------------------------------------------------------------
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.45, frame_center=screen_center, run_time=2.2)
        self.wait(1.8)

        # 다시 3D 와이드 뷰로 빠져나오며 적분의 입체 공간 조망
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=0.95, frame_center=ORIGIN, run_time=2.2)

        # [인지적 여백 4] 차원의 미적분 개념 음미
        self.wait(2.2)

        # =================================================================
        # [Act 5] 결론: 미적분, 보이지 않는 세계를 감각하는 수학적 눈
        # =================================================================
        self.play(
            FadeOut(ground_grid),
            FadeOut(eye_3d),
            FadeOut(screen_group),
            FadeOut(curve_3d_real),
            FadeOut(curve_2d_proj),
            FadeOut(dot_3d_real),
            FadeOut(dot_2d_proj),
            FadeOut(ray_frustum),
            FadeOut(sub_act4_badge),
            run_time=0.8,
        )

        # 카메라 부드러운 공전 시작
        self.begin_ambient_camera_rotation(rate=0.07)

        # 다층 유선 필드 (적분된 3차원 유체 공간)
        main_stream = build_streamline(np.array([1.5, -1.0, -0.6]), steps=70, color=C_STREAM)
        surrounding_streams = VGroup(
            build_streamline(np.array([-1.8, -1.2, -0.8]), color="#60A5FA"),
            build_streamline(np.array([1.2, 1.8, -0.4]), color="#818CF8"),
            build_streamline(np.array([-1.2, 2.0, -0.7]), color=C_STREAM),
            build_streamline(np.array([0.4, -2.0, 0.1]), color="#818CF8"),
            build_streamline(np.array([2.0, 0.5, -0.3]), color="#60A5FA"),
        )

        final_raw = VGroup(
            Text("미적분: 보이지 않는 세계의 질서를 감각하는 가장 우아한 인간의 센서", font=FONT_KR, font_size=18, color="#F8FAFC"),
            VGroup(
                Text("미분: 찰나의 변화율을 인지하는 생물학적 센서 (", font=FONT_KR, font_size=14, color=C_VEL),
                MathTex(r"\frac{d\vec{r} }{dt}", font_size=20, color=C_VEL),
                Text(")", font=FONT_KR, font_size=14, color=C_VEL),
                Text("  ·  적분: 단면들을 엮어 실체를 복원하는 뇌 (", font=FONT_KR, font_size=14, color=C_STREAM),
                MathTex(r"\int \vec{v}\,dt", font_size=20, color=C_STREAM),
                Text(")", font=FONT_KR, font_size=14, color=C_STREAM),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.08)
        final_badge = make_badge(final_raw, stroke_color=C_VEL, buff=0.16).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(final_badge)
        self.remove(final_badge)

        with self.voiceover(
            text="결국 미적분은 책 속에 갇힌 수학 공식이 아닙니다. 찰나의 변화율을 미분하여 감각하고, 이를 누적하여 세계를 적분하는 인간의 가장 위대한 인식 도구입니다."
        ) as tracker:
            self.play(
                FadeIn(final_badge),
                Create(main_stream),
                Create(surrounding_streams),
                run_time=2.8,
            )

            stream_dots = VGroup(*[Dot3D(color=C_LEAF, radius=0.08) for _ in range(len(surrounding_streams) + 1)])
            all_streams = [main_stream] + list(surrounding_streams)
            self.play(
                *[MoveAlongPath(dot, st) for dot, st in zip(stream_dots, all_streams)],
                run_time=max(3.5, tracker.duration - 2.8),
                rate_func=linear,
            )

        # [최종 여운 및 감상 대기 시간]
        self.wait(3.5)
        self.stop_ambient_camera_rotation()
        self.wait(1.5)
