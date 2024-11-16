function AddAnimatedCircle() {
  const circle = document.getElementById('circleId');
  document.addEventListener('mousemove', (e) => {
    requestAnimationFrame(() => {
      circle.style.left = `${e.clientX}px`;
      circle.style.top = `${e.clientY}px`;
    });
  });
}

AddAnimatedCircle();