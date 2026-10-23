// Adds a "Copy" button to every code example. The page works without it.
document.querySelectorAll(".example").forEach((example) => {
  const code = example.querySelector("pre code");
  if (!code || !navigator.clipboard) return;

  const button = document.createElement("button");
  button.className = "copy";
  button.type = "button";
  button.textContent = "Copy";

  button.addEventListener("click", async () => {
    // Copy only the commands: lines starting with "$", without the "$ "
    const lines = code.innerText.split("\n");
    const commands = lines.filter((line) => line.startsWith("$ ")).map((line) => line.slice(2));
    const text = commands.length ? commands.join("\n") : code.innerText;
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = "Copied";
    } catch {
      button.textContent = "Press Ctrl+C";
    }
    setTimeout(() => (button.textContent = "Copy"), 1500);
  });

  example.appendChild(button);
});
