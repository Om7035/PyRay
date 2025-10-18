# Web Deployment (Pyodide / WebAssembly)

PyRay targets web via Pyodide (Python in WebAssembly). This guide outlines the approach and current recommendations.

## Status

- Direct real-time game loops in the browser require careful integration. Phase 4 will include templates and examples.

## Approach Overview

- Bundle your Python code with a minimal HTML shell.
- Load Pyodide and install (or bundle) dependencies.
- Use a canvas element to draw; for pygame, this may require a specific backend.

## Current Recommendation

- For now, export gameplay footage as GIF/MP4 for web presentation.
- Follow updates in the Phase 4 roadmap for full in-browser runtime support.

## Resources

- https://pyodide.org/
- https://emscripten.org/
