"""Tests for the toy reward-hacking environments."""

from rewardhack_probe.toy_envs.gridworld import run_gridworld_demo
from rewardhack_probe.toy_envs.text_game import run_text_game_demo


def test_gridworld_hack_detected() -> None:
    honest = run_gridworld_demo(hack=False)
    hacked = run_gridworld_demo(hack=True)
    assert honest.actual_success is True
    assert honest.hack_detected is False
    assert hacked.reward == 1.0
    assert hacked.actual_success is False
    assert hacked.hack_detected is True


def test_text_game_hack_detected() -> None:
    honest = run_text_game_demo(hack=False)
    hacked = run_text_game_demo(hack=True)
    assert honest.actual_success is True
    assert honest.hack_detected is False
    assert hacked.reward == 1.0
    assert hacked.actual_success is False
    assert hacked.hack_detected is True
