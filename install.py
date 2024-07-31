import launch

if not launch.is_installed("sortedcontainers"):
    launch.run_pip("install sortedcontainers", "requirement for Bubble Prompter")