
# Dude, Don't Let Your Treehouse Floor Go 'D'oh!' – Bending Stress Edition<br>친구, 트리하우스 바닥이 '으악' 하지 않게 조심해! – 굽힘 응력 편

* Ever dreamt of building the raddest treehouse? Well, before you start hammering away, let's make sure that floor isn't gonna send you crashing down like a gnarly wipeout.  This assignment will teach you how to use numerical methods to calculate the bending stress on your treehouse floor supports.<br>나무 위에 멋진 놀이방을 만들어 보는 건 어떨까요? 공사를 시작하기 전에, 바닥이 무너지지 않을지 확인해야 합니다. 이 과제에서는 수치적 방법을 사용하여 아늑한 휴식처의 바닥을 지지하는 보의 굽힘 응력을 계산하는 방법을 알아봅시다.

![Tree House](https://github.com/kangwonlee/beam_section/assets/17876446/051577ce-2f31-4ade-ac67-78122132a538)
Can I use Simpson formula to do this?<br>심슨 공식으로 할 수 있을까요?

## Learning Objectives<br>학습 목표

* Master numerical integration techniques like the Trapezoidal and Simpson's Rule to calculate section properties.<br>사다리꼴 공식이나 심슨 수치적분의 달인이 되어 단면 특성을 계산해 봅시다.

$$
\begin{align}
    \bar{y} &= \frac{1}{A}\int y dA \\
    I &= \int y^2 dA \\
\end{align}
$$

* Become a bending stress expert by using the flexure formula to analyze your treehouse floor supports.<br>굽힘 공식으로 바닥 지지보를 해석해 봅시다.

$$
σ = \frac{My}{I}
$$

* Level up your Python skills to create functions that automate those calculations.<br>이러한 여러 계산을 자동화하는 함수를 만들어 보면서 파이썬 역량을 한 단계 향상시켜 봅시다.
* Write clean, well-organized code that even Linus Torvalds would approve of.<br>리누스 토발즈도 인정할 만한 깔끔하고 잘 정리된 코드를 작성해 봅시다.

<a href="https://github.com/torvalds"><img alt="Torvalds's avatar" src="https://avatars.githubusercontent.com/u/1024025?v=4" width="120" height="120"></a>
<br>Linus Torvalds, Linux Foundation (Let's aim for code so good, even Linus might crack a smile!)<br>리누스 토발즈, 리눅스 재단 (목표는 리누스씨 마음에도 흡족할 만큼 훌륭한 코드를 작성하는 겁니다!)

## Your Mission, Should You Choose to Accept It:<br>다음 함수를 구현해 보세요:

<img alt="section dimensions" src="https://github.com/kangwonlee/beam_section/assets/17876446/2ae07371-9a3d-45d7-9c73-421de6640252" style="max-width: 50%;">

* In `beam_analysis.py`, implement the following Python functions to calculate the area, centroid, moment of inertia, and bending stress of a T-beam cross-section.<br>`beam_analysis.py` 파일에 아래 파이썬 함수를 구현하여 T형 단면의 면적, 중심, 관성 모멘트, 그리고 굽힘 응력을 계산하시오.

| function | description |
|:--------:|:-----------:|
| `area(w0, h0, w1, h1, w2, h2):` | The total area of the T-beam cross-section.<br> T형 단면의 전체 면적 |
| `centroid_y(w0, h0, w1, h1, w2, h2):` | The vertical distance from the bottom of the section to the neutral axis (centroid).<br> 단면의 하단으로부터 단면의 중립축(중심축)까지의 수직 거리 |
| `moment_of_inertia(w0, h0, w1, h1, w2, h2):` | The moment of inertia (I) of the T-beam cross-section.<br>T형 단면의 관성 모멘트(I) |
| `bending_stress(M, w0, h0, w1, h1, w2, h2):` | The maximum bending stress (σ) at the top or bottom fibers of the T-beam.<br> T형 단면의 상단 또는 하단에서의 최대 굽힘 응력(σ) |

* All arguments and return values would be `float`<br>모든 매개변수와 반환값은 `float`.
* All units of length are in meters.<br>길이의 단위는 미터.
* All units of force are in Newtons.<br>힘의 단위는 뉴턴.

## Grading: Totally Tubular Rubric<br>평가기준

| Criteria<br>기준	| Points<br>배점 |
|:---------:|:------:|
| Python Grammar<br>파이썬 문법	| 1 |
| Coding Style<br>모든 코드는 함수 안에	| 1 |
| Intermediate Results<br>중간 결과	| 1 |
| Final Result<br>최종 결과	| 2 |

* Make sure your code passes all the tests in GitHub Actions – it's like getting a thumbs-up! 👍<br>코드를 commit 한 후 저장소 Actions 에서 테스트를 모두 통과 하는지 확인 바랍니다. 👍

## Need a Hand?<br>힌트가 필요하다면

* Check out the `sample.py` file for some righteous examples on how to use your functions.<br>함수 사용 예는 `sample.py` 파일을 참고하세요.

```python
import matplotlib.pyplot as plt
import numpy as np
import beam_analysis as beam

w0_m, h0_m = 50e-3, 12e-3
w1_m, h1_m = 7.5e-3, 70e-3
w2_m, h2_m = 90e-3, 10e-3

area_m2 = beam.area(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)
centroid_m = beam.centroid_y(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)
moment_m4 = beam.moment_of_inertia(w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)
bending_stress_max_pa = beam.bending_stress(100, w0_m, h0_m, w1_m, h1_m, w2_m, h2_m)

print(f'T-beam area: {area_m2:.6f} m^2')
print(f'T-beam centroid: {centroid_m:.6f} m')
print(f'T-beam moment of inertia: {moment_m4:.6f} m^4')
print(f'T-beam max bending stress: {bending_stress_max_pa:.6f} Pa')

plt.fill_between([(-0.5) * w0_m, (0.5) * w0_m], [0, 0], [h0_m, h0_m], color='blue', alpha=0.5)
plt.fill_between([(-0.5) * w1_m, (0.5) * w1_m], [h0_m, h0_m], [h1_m+h0_m, h1_m+h0_m], color='blue', alpha=0.5)
plt.fill_between([(-0.5) * w2_m, (0.5) * w2_m], [h1_m+h0_m, h1_m+h0_m], [h2_m+h1_m+h0_m, h2_m+h1_m+h0_m], color='blue', alpha=0.5)
plt.axhline(y=centroid_m, color='red', linestyle='--')
plt.grid(True)
plt.show()
```

 So, what are you waiting for? Let's build a treehouse that's so epic! 🍕<br>이제 나무 위에 역대급 놀이방을 만들어 봅시다!
