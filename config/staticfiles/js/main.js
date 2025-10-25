const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

// function toggleMusic() {
//   const music = document.getElementById('holiday-music');
//   music.paused ? music.play() : music.pause();
// }

// #const canvas = document.getElementById('confetti-canvas');
// #const ctx = canvas.getContext('2d');
// canvas.width = window.innerWidth;
// canvas.height = window.innerHeight;

// const confetti = Array.from({ length: 100 }, () => ({
//   x: Math.random() * canvas.width,
//   y: Math.random() * canvas.height,
//   r: Math.random() * 6 + 4,
//   color: `hsl(${Math.random() * 360}, 100%, 70%)`,
//   speed: Math.random() * 2 + 1
// }));

// function draw() {
//   ctx.clearRect(0, 0, canvas.width, canvas.height);
//   confetti.forEach(p => {
//     ctx.beginPath();
//     ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
//     ctx.fillStyle = p.color;
//     ctx.fill();
//     p.y += p.speed;
//     if (p.y > canvas.height) p.y = -10;
//   });
//   requestAnimationFrame(draw);
// }
// draw();

// const countdown = document.getElementById('countdown');
// const targetDate = new Date('December 25, 2025 00:00:00').getTime();

// setInterval(() => {
//   const now = new Date().getTime();
//   const distance = targetDate - now;
//   const days = Math.floor(distance / (1000 * 60 * 60 * 24));
//   countdown.innerHTML = `🎄 ${days} days until Christmas! 🎄`;
// }, 1000);

