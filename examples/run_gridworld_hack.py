"""Run the gridworld reward-hacking demo."""

from rewardhack_probe.toy_envs.gridworld import run_gridworld_demo


def main() -> None:
    honest = run_gridworld_demo(hack=False)
    hack = run_gridworld_demo(hack=True)
    print("honest:", honest)
    print("hack:", hack)


if __name__ == "__main__":
    main()
