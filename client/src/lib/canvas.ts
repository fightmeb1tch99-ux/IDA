export function drawCanvasGrid(
  context: CanvasRenderingContext2D,
  canvas: HTMLCanvasElement,
  spacing = 40,
): void {
  context.strokeStyle = "rgba(6, 182, 212, 0.05)";
  context.lineWidth = 1;

  for (let x = 0; x < canvas.width; x += spacing) {
    context.beginPath();
    context.moveTo(x, 0);
    context.lineTo(x, canvas.height);
    context.stroke();
  }

  for (let y = 0; y < canvas.height; y += spacing) {
    context.beginPath();
    context.moveTo(0, y);
    context.lineTo(canvas.width, y);
    context.stroke();
  }
}
