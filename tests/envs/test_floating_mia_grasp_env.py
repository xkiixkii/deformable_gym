import pytest
from deformable_gym.envs.floating_mia_grasp_env import FloatingMiaGraspEnv


@pytest.fixture
def env():
    return FloatingMiaGraspEnv(
        gui=False,
        verbose=True,
        horizon=10,
        object_name="insole_on_conveyor_belt/back",
        observable_object_pos=True,
        difficulty_mode="hard")


action_space_dims_expected = 10


def test_action_space_dims(env):
    action_space = env.action_space
    assert action_space.shape[0] == action_space_dims_expected


def test_obs_space_dims(env):
    if env._observable_object_pos:
        obs_space_dims_expected = 19
    else:
        obs_space_dims_expected = 16

    obs_space = env.observation_space
    assert obs_space.shape[0] == obs_space_dims_expected


def test_initial_obs(env):
    obs, info = env.reset()
    if env._observable_object_pos:
        obs_space_dims_expected = 19
    else:
        obs_space_dims_expected = 16
    assert len(obs) == obs_space_dims_expected


def test_eps_done(env):
    if env._observable_object_pos:
        obs_space_dims_expected = 19
    else:
        obs_space_dims_expected = 16

    for t in range(9):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)

        assert len(obs) == obs_space_dims_expected
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert not terminated

    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    assert terminated