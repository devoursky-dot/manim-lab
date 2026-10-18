import numpy as np
from manim import *
from manim_voiceover import VoiceoverScene

try:
    from manim_voiceover.services.edge import EdgeService
except (ImportError, ModuleNotFoundError):
    from core.edge_service import EdgeService


class WindCalculus3DLectureV5(ThreeDScene, VoiceoverScene):
    """[v5 Masterpiece] 인간은 세상을 어떻게 미분하는가? : 감각의 인식론

    핵심 교육 철학:
    1. 나뭇잎의 조화진동:
       - 작은 나뭇잎: 고주파수(빠른 떨림), 소진폭 (A1 = 0.4, w1 = 6.0)
       - 큰 나뭇잎: 저주파수(느린 흔들림), 대진폭 (A2 = 1.2, w2 = 2.0)
       - 두 나뭇잎의 진폭(변화량)은 3배나 다르지만, 최대 순간변화율(v_max = A*w = 2.4 m/s)은 완벽히 일치!
    2. 원근의 착시와 뇌의 보정:
       - 가까운 나뭇잎 vs 먼 나뭇잎: 망막에 맺힌 이동거리(각도 변화량)는 10배 차이나지만 같은 바람으로 인지
    3. 차원의 미분과 적분:
       - 3차원 세상을 2차원 평면 이미지(단면 = 미분)로 받아들이고, 뇌 속에서 시간 축으로 적분하여 3차원 세계를 복원
    4. 순수 딥 블랙 (#000000) + 충분한 인지적 여백 (핵심 구간마다 2.0~3.0초 침묵 배정)
    """

    def construct(self):
        # 1. 한국어 AI 성우 및 딥 블랙 캔버스 설정
        self.set_speech_service(
            EdgeService(voice="ko-KR-InJoonNeural", rate="+0%")
        )
        self.camera.background_color = "#000000"
        FONT_KR = "Malgun Gothic"

        # 색상 토큰
        C_VEL = "#FACC15"       # 순간변화율 / 속도 벡터 (Amber Gold)
        C_DISP = "#FB923C"      # 변화량 / 진폭 (Vibrant Orange)
        C_STREAM = "#38BDF8"    # 유선 / 적분 곡선 (Electric Cyan)
        C_LEAF = "#4ADE80"      # 나뭇잎 파티클 (Spring Mint)
        C_AXIS = "#334155"      # 좌표축 (Muted Slate)

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
            curve = VMobject(color=color, stroke_width=3.5)
            curve.set_points_smoothly(pts)
            return curve

        # =================================================================
        # [Act 1] 서론: 바람과 나뭇잎의 진동 (빠른 떨림 vs 큰 흔들림)
        # =================================================================
        # 2D 평면 뷰에서 나뭇잎의 조화진동을 명확하게 관찰
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES, zoom=1.05)

        title_card = VGroup(
            Text("인간은 세상을 어떻게 미분하는가? : 감각의 인식론", font=FONT_KR, font_size=25, color="#F8FAFC"),
            VGroup(
                Text("미분(순간변화율)", font=FONT_KR, font_size=18, color=C_VEL),
                Text(": 변화량이 아닌 변화율을 인지하는 뇌의 센서", font=FONT_KR, font_size=18, color="#94A3B8"),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.15).to_corner(UL, buff=0.4)

        self.add_fixed_in_frame_mobjects(title_card)
        self.remove(title_card)

        # 진동 기준 중심점 및 줄기
        origin_small = np.array([-1.5, 1.2, 0])
        origin_large = np.array([-1.5, -1.2, 0])

        stem_small = Line(origin_small + LEFT * 1.5, origin_small, color=C_AXIS, stroke_width=3)
        stem_large = Line(origin_large + LEFT * 1.5, origin_large, color=C_AXIS, stroke_width=4)

        # 진동 파라미터 (v_max = A * w = 2.4 m/s 로 동일!)
        A_small, w_small = 0.50, 4.8   # 작은 잎: 소진폭, 고주파수 (바르르 떨림)
        A_large, w_large = 1.50, 1.6   # 큰 잎: 대진폭, 저주파수 (너울너울 흔들림)

        t_tracker = ValueTracker(0)

        # 나뭇잎 생성 도우미 함수 (타원 엽신 + 잎맥)
        def make_leaf(scale_val=1.0, color=C_LEAF):
            body = Ellipse(width=0.45 * scale_val, height=0.22 * scale_val, color=color, fill_opacity=0.9, stroke_width=1.5)
            vein = Line(LEFT * 0.22 * scale_val, RIGHT * 0.22 * scale_val, color="#86EFAC", stroke_width=1.2)
            stem = Line(LEFT * 0.35 * scale_val, LEFT * 0.22 * scale_val, color=C_AXIS, stroke_width=2.0)
            return VGroup(body, vein, stem)

        # 동적 나뭇잎 오브젝트
        leaf_small = always_redraw(lambda: make_leaf(scale_val=0.75, color=C_LEAF).move_to(
            origin_small + RIGHT * (A_small * np.sin(w_small * t_tracker.get_value()))
        ))
        leaf_large = always_redraw(lambda: make_leaf(scale_val=2.0, color=C_LEAF).move_to(
            origin_large + RIGHT * (A_large * np.sin(w_large * t_tracker.get_value()))
        ))

        # 진폭(변화량) 구간 표시선
        range_small = DoubleArrow(origin_small + LEFT * A_small, origin_small + RIGHT * A_small, buff=0, color=C_DISP, stroke_width=2.5)
        range_large = DoubleArrow(origin_large + LEFT * A_large, origin_large + RIGHT * A_large, buff=0, color=C_DISP, stroke_width=2.5)

        label_small = VGroup(
            Text("작은 나뭇잎 (빠른 떨림)", font=FONT_KR, font_size=17, color=C_LEAF),
            VGroup(
                Text("변화량(진폭) ", font=FONT_KR, font_size=15, color=C_DISP),
                MathTex(r"A_1 = 0.5\text{ m}", font_size=18, color=C_DISP),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(origin_small, UP, buff=0.25)

        label_large = VGroup(
            Text("큰 나뭇잎 (큰 흔들림)", font=FONT_KR, font_size=17, color=C_LEAF),
            VGroup(
                Text("변화량(진폭) ", font=FONT_KR, font_size=15, color=C_DISP),
                MathTex(r"A_2 = 1.5\text{ m}", font_size=18, color=C_DISP),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(origin_large, UP, buff=0.25)

        with self.voiceover(
            text="바람이 불 때 나뭇잎을 보면, 작은 나뭇잎은 바르르 빠르게 떨리고, 큰 나뭇잎은 너울너울 크게 흔들립니다. 두 나뭇잎이 움직이는 진폭, 즉 변화량은 세 배나 다릅니다. 하지만 우리는 변화량이 달라도 정확히 같은 바람의 세기로 인지합니다. 왜 그럴까요?"
        ) as tracker:
            self.play(FadeIn(title_card, shift=DOWN * 0.2), run_time=1.0)
            self.play(
                Create(stem_small), Create(stem_large),
                FadeIn(label_small), FadeIn(label_large),
                run_time=1.2,
            )
            self.add(leaf_small, leaf_large)
            self.play(Create(range_small), Create(range_large), run_time=1.0)
            # 조화 진동 시작
            self.play(
                t_tracker.animate.set_value(tracker.duration - 3.2),
                run_time=max(2.0, tracker.duration - 3.2),
                rate_func=linear,
            )

        # [인지적 여백 1] 두 나뭇잎의 흔들림 차이 음미
        self.play(t_tracker.animate.set_value(t_tracker.get_value() + 2.0), run_time=2.0, rate_func=linear)

        # =================================================================
        # [Act 2] 변화율의 원리: 주기로 나눈 순간속도 (Aha! Moment)
        # =================================================================
        # 속도 벡터 화살표 (v = A * w * cos(w*t))
        vel_arrow_small = always_redraw(lambda: Arrow(
            start=origin_small + RIGHT * (A_small * np.sin(w_small * t_tracker.get_value())),
            end=origin_small + RIGHT * (A_small * np.sin(w_small * t_tracker.get_value()) + 0.65 * (A_small * w_small * np.cos(w_small * t_tracker.get_value()))),
            buff=0, color=C_VEL, stroke_width=4.5, max_tip_length_to_length_ratio=0.25
        ))
        vel_arrow_large = always_redraw(lambda: Arrow(
            start=origin_large + RIGHT * (A_large * np.sin(w_large * t_tracker.get_value())),
            end=origin_large + RIGHT * (A_large * np.sin(w_large * t_tracker.get_value()) + 0.65 * (A_large * w_large * np.cos(w_large * t_tracker.get_value()))),
            buff=0, color=C_VEL, stroke_width=4.5, max_tip_length_to_length_ratio=0.25
        ))

        sub_act2 = VGroup(
            Text("우리가 인지하는 것은 흔들림의 크기(변화량)가 아니라, '시간당 변화율'이다!", font=FONT_KR, font_size=22, color=C_VEL),
            VGroup(
                Text("최대 순간변화율(속도) ", font=FONT_KR, font_size=18, color=C_VEL),
                MathTex(r"v_{\max} = A \cdot \omega = 2.4\text{ m/s}", font_size=24, color=C_VEL),
                Text(" [두 나뭇잎 완벽히 일치!]", font=FONT_KR, font_size=18, color="#86EFAC"),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act2)
        self.remove(sub_act2)

        with self.voiceover(
            text="우리의 뇌는 단순한 흔들림의 거리, 즉 변화량을 느끼는 것이 아닙니다. 짧은 주기로 나눈 시간당 변화율을 감각하기 때문이죠. 작은 잎의 빠른 떨림이나 큰 잎의 느린 흔들림이나, 시간당 최고 속도인 순간변화율은 초당 2.4미터로 완벽하게 같습니다."
        ) as tracker:
            self.play(FadeIn(sub_act2), run_time=1.0)
            self.add(vel_arrow_small, vel_arrow_large)
            self.play(
                t_tracker.animate.set_value(t_tracker.get_value() + tracker.duration - 1.0),
                run_time=max(2.0, tracker.duration - 1.0),
                rate_func=linear,
            )

        # [인지적 여백 2] 속도 벡터가 최대점에서 똑같이 뻗어나가는 순간 음미
        self.play(t_tracker.animate.set_value(t_tracker.get_value() + 2.5), run_time=2.5, rate_func=linear)

        # =================================================================
        # [Act 3] 원근의 착시: 가까운 잎 vs 먼 잎, 뇌의 미분 센서
        # =================================================================
        # 진동 객체 정리
        self.play(
            FadeOut(leaf_small), FadeOut(leaf_large),
            FadeOut(vel_arrow_small), FadeOut(vel_arrow_large),
            FadeOut(range_small), FadeOut(range_large),
            FadeOut(stem_small), FadeOut(stem_large),
            FadeOut(label_small), FadeOut(label_large),
            FadeOut(sub_act2),
            run_time=1.0,
        )

        # 원근 비교 시각화: 눈(관찰자) -> 1m 앞 나뭇잎 vs 10m 뒤 나뭇잎
        eye = Dot(point=np.array([-4.5, 0, 0]), radius=0.15, color="#38BDF8")
        eye_label = Text("인간의 눈", font=FONT_KR, font_size=16, color="#38BDF8").next_to(eye, DOWN, buff=0.2)

        # 시선 부채꼴 광선
        ray_near = Polygon(np.array([-4.5, 0, 0]), np.array([-1.5, 1.2, 0]), np.array([-1.5, -1.2, 0]), color="#1E293B", fill_opacity=0.3, stroke_width=1.5)
        ray_far = Polygon(np.array([-4.5, 0, 0]), np.array([3.5, 0.4, 0]), np.array([3.5, -0.4, 0]), color="#1E293B", fill_opacity=0.3, stroke_width=1.5)

        leaf_near = Dot(point=np.array([-1.5, 0, 0]), radius=0.12, color=C_LEAF)
        leaf_near_motion = DoubleArrow(np.array([-1.5, -1.0, 0]), np.array([-1.5, 1.0, 0]), buff=0, color=C_DISP, stroke_width=3.5)
        near_tag = VGroup(
            Text("가까운 나뭇잎", font=FONT_KR, font_size=16, color=C_LEAF),
            Text("망막 시각 변화량: 매우 큼", font=FONT_KR, font_size=14, color=C_DISP),
        ).arrange(DOWN, buff=0.06).next_to(leaf_near_motion, UP, buff=0.25)
        dist_near = Text("거리 d = 1m", font=FONT_KR, font_size=13, color="#94A3B8").next_to(leaf_near_motion, DOWN, buff=0.25)

        leaf_far = Dot(point=np.array([3.5, 0, 0]), radius=0.07, color=C_LEAF)
        leaf_far_motion = DoubleArrow(np.array([3.5, -0.3, 0]), np.array([3.5, 0.3, 0]), buff=0, color=C_DISP, stroke_width=2.5)
        far_tag = VGroup(
            Text("먼 나뭇잎", font=FONT_KR, font_size=16, color=C_LEAF),
            Text("망막 시각 변화량: 매우 작음", font=FONT_KR, font_size=14, color=C_DISP),
        ).arrange(DOWN, buff=0.06).next_to(leaf_far_motion, UP, buff=0.25)
        dist_far = Text("거리 d = 10m", font=FONT_KR, font_size=13, color="#94A3B8").next_to(leaf_far_motion, DOWN, buff=0.25)

        sub_act3 = VGroup(
            Text("망막에 맺힌 변화량은 10배 차이나지만, 뇌는 '기준 시간당 변화율'을 인지한다", font=FONT_KR, font_size=21, color="#F8FAFC"),
            Text("즉, 인간은 뇌 속에 '미분을 인지하는 생물학적 센서'를 탑재하고 있다!", font=FONT_KR, font_size=20, color=C_VEL),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act3)
        self.remove(sub_act3)

        with self.voiceover(
            text="나뭇잎을 눈앞에서 볼 때와 저 멀리 숲속에서 볼 때를 생각해 보세요. 망막에 맺히는 상의 움직인 크기, 즉 변화량은 10배 이상 차이가 납니다. 하지만 우리는 저 멀리 부는 바람도 여기와 똑같은 세기라는 것을 즉시 압니다. 우리 뇌는 망막의 변화량에 속지 않고, 기준 거리와 시간으로 나눈 본질적인 변화율을 계산해내기 때문입니다. 인간은 뇌 속에 미분을 인지하는 센서를 탑재하고 태어난 것이죠."
        ) as tracker:
            self.play(FadeIn(sub_act3), run_time=1.0)
            self.play(
                FadeIn(eye), Write(eye_label),
                Create(ray_near), Create(ray_far),
                FadeIn(leaf_near), FadeIn(leaf_far),
                run_time=2.0,
            )
            self.play(
                Create(leaf_near_motion), FadeIn(near_tag), FadeIn(dist_near),
                Create(leaf_far_motion), FadeIn(far_tag), FadeIn(dist_far),
                run_time=max(2.0, tracker.duration - 3.0),
            )

        # [인지적 여백 3] 뇌의 미분 센서 개념 음미
        self.wait(2.5)

        # =================================================================
        # [Act 4] 차원의 미분과 적분: 3D 세상을 2D 단면으로 보다
        # =================================================================
        self.play(
            FadeOut(eye), FadeOut(eye_label),
            FadeOut(ray_near), FadeOut(ray_far),
            FadeOut(leaf_near), FadeOut(leaf_far),
            FadeOut(leaf_near_motion), FadeOut(leaf_far_motion),
            FadeOut(near_tag), FadeOut(far_tag),
            FadeOut(dist_near), FadeOut(dist_far),
            FadeOut(sub_act3),
            run_time=0.8,
        )

        # 3D 공간으로 카메라 전환
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.1, run_time=2.2)

        # 3차원 공간 속 2차원 투영 단면 (망막 스크린)
        retina_screen = Rectangle(
            width=4.5, height=3.5,
            color="#38BDF8", fill_color="#0369A1", fill_opacity=0.22, stroke_width=2.5
        ).shift(OUT * 0.2 + LEFT * 0.5)

        # 3D 입체 궤적 곡선 생성
        t_vals = np.linspace(0, 3.2, 50)
        pts_3d = [np.array([1.3 * np.cos(t) + 0.5, 1.2 * np.sin(t), 0.55 * t - 0.7]) for t in t_vals]
        curve_3d = VMobject(color=C_LEAF, stroke_width=3.5).set_points_smoothly(pts_3d)

        # 망막 단면(z = 0.2 평면)에 투영된 2차원 궤적 (z 좌표를 0.2로 사영)
        pts_2d = [np.array([p[0], p[1], 0.2]) for p in pts_3d]
        curve_2d = VMobject(color=C_VEL, stroke_width=3.0).set_points_smoothly(pts_2d)

        # 3D 동적 입자 및 2D 투영 입자
        dot3d = Dot3D(point=pts_3d[0], radius=0.12, color=C_LEAF)
        dot2d = Dot3D(point=pts_2d[0], radius=0.09, color=C_VEL)
        proj_line = always_redraw(lambda: DashedLine(
            dot3d.get_center(),
            np.array([dot3d.get_center()[0], dot3d.get_center()[1], 0.2]),
            color="#94A3B8", stroke_width=1.5, dash_length=0.08
        ))

        sub_act4 = VGroup(
            Text("3차원 세상을 한 축으로 자른 2차원 단면(이미지)으로 보는 것 = 미분", font=FONT_KR, font_size=21, color=C_STREAM),
            Text("그 단면들을 시간 속에서 다시 엮어 3차원 실체를 복원하는 것 = 적분", font=FONT_KR, font_size=21, color=C_VEL),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.35)

        self.add_fixed_in_frame_mobjects(sub_act4)
        self.remove(sub_act4)

        with self.voiceover(
            text="우리는 눈을 통해 3차원 세계를 바라봅니다. 하지만 생각해보세요. 실제 우리 눈이 받아들이는 것은 오직 2차원의 평면 이미지입니다. 3차원 세상을 빛의 축으로 한 겹 잘라낸 2차원 미분 단면을 보는 것이죠. 그리고 우리의 뇌는 이 미분된 2차원 순간들을 시간 속에서 차곡차곡 적분하여, 3차원의 거대한 입체 세계를 다시 재구성해냅니다."
        ) as tracker:
            self.play(FadeIn(sub_act4), run_time=1.0)
            self.play(
                Create(retina_screen),
                Create(curve_3d),
                Create(curve_2d),
                FadeIn(dot3d),
                FadeIn(dot2d),
                Create(proj_line),
                run_time=2.5,
            )
            # 3D 궤적과 2D 투영면을 따라 동시에 이동하는 파티클 애니메이션
            self.play(
                MoveAlongPath(dot3d, curve_3d),
                MoveAlongPath(dot2d, curve_2d),
                run_time=max(3.5, tracker.duration - 3.5),
                rate_func=linear,
            )

        # [인지적 여백 4] 차원의 미분/적분 개념 음미
        self.wait(2.5)

        # =================================================================
        # [Act 5] 결론: 미적분, 세계를 인식하는 우리의 감각
        # =================================================================
        self.play(
            FadeOut(retina_screen),
            FadeOut(proj_line),
            FadeOut(dot3d),
            FadeOut(dot2d),
            FadeOut(curve_3d),
            FadeOut(curve_2d),
            FadeOut(sub_act4),
            run_time=0.8,
        )

        # 카메라 와이드 줌아웃 & 공전
        self.move_camera(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.95, run_time=2.2)
        self.begin_ambient_camera_rotation(rate=0.08)

        # 전체 공간의 유선 군집
        main_stream = build_streamline(np.array([1.5, -1.0, -0.6]), steps=70, color=C_STREAM)
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
                Text("미분: 찰나의 변화율을 감각하는 센서 (", font=FONT_KR, font_size=17, color=C_VEL),
                MathTex(r"\frac{d\vec{r} }{dt}", font_size=24, color=C_VEL),
                Text(")", font=FONT_KR, font_size=17, color=C_VEL),
                Text("  ·  적분: 세계를 입체적으로 복원하는 뇌 (", font=FONT_KR, font_size=17, color=C_STREAM),
                MathTex(r"\int \vec{v}\,dt", font_size=24, color=C_STREAM),
                Text(")", font=FONT_KR, font_size=17, color=C_STREAM),
            ).arrange(RIGHT, buff=0.1),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)

        self.add_fixed_in_frame_mobjects(final_hud)
        self.remove(final_hud)

        with self.voiceover(
            text="결국 미적분은 책 속에 갇힌 수학 공식이 아닙니다. 찰나의 변화율을 미분하여 감각하고, 이를 누적하여 세계를 적분하는 인간의 가장 위대한 인식 도구입니다."
        ) as tracker:
            self.play(
                FadeIn(final_hud),
                Create(main_stream),
                Create(surrounding_streams),
                run_time=3.0,
            )

            stream_dots = VGroup(*[Dot3D(color=C_LEAF, radius=0.08) for _ in range(len(surrounding_streams) + 1)])
            all_streams = [main_stream] + list(surrounding_streams)
            self.play(
                *[MoveAlongPath(dot, st) for dot, st in zip(stream_dots, all_streams)],
                run_time=max(3.5, tracker.duration - 3.0),
                rate_func=linear,
            )

        # [최종 여운 대기 시간]
        self.wait(3.5)
        self.stop_ambient_camera_rotation()
        self.wait(1.5)
