mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose"
});

document$.subscribe(() => {
  mermaid.run();
});
