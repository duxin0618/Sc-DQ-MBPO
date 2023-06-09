# Softlearning

Softlearning is a deep reinforcement learning toolbox for training maximum entropy policies in continuous domains. The implementation is fairly thin and primarily optimized for our own development purposes. It utilizes the tf.keras modules for most of the model classes (e.g. policies and value functions). We use Ray for the experiment orchestration. Ray Tune and Autoscaler implement several neat features that enable us to seamlessly run the same experiment scripts that we use for local prototyping to launch large-scale experiments on any chosen cloud service (e.g. GCP or AWS), and intelligently parallelize and distribute training for effective resource allocation.

This implementation uses Tensorflow. For a PyTorch implementation of soft actor-critic, take a look at [rlkit](https://github.com/vitchyr/rlkit).

Softlearning 是一个深度强化学习工具箱，用于在连续领域中训练最大熵策略。该实现相当薄，主要针对我们自己的开发目的进行了优化。它将tf.keras模块用于大多数模型类（例如策略和值函数）。我们使用Ray进行实验编排。Ray Tune和Autoscaler实现了几个简洁的功能，使我们能够无缝地运行用于本地原型的相同实验脚本，以在任何选定的云服务（例如GCP或AWS）上启动大规模实验，并智能地并行化和分发培训，以实现有效的资源分配。

此实现使用Tensorflow。对于soft actor-critic 的PyTorch实现，请查看rlkit。

# Getting Started

## Prerequisites

The environment can be run either locally using conda or inside a docker container. For conda installation, you need to have [Conda](https://conda.io/docs/user-guide/install/index.html) installed. For docker installation you will need to have [Docker](https://docs.docker.com/engine/installation/) and [Docker Compose](https://docs.docker.com/compose/install/) installed. Also, most of our environments currently require a [MuJoCo](https://www.roboti.us/license.html) license.

## Conda Installation

1. [Download](https://www.roboti.us/index.html) and install MuJoCo 1.50 from the MuJoCo website. We assume that the MuJoCo files are extracted to the default location (`~/.mujoco/mjpro150`).

2. Copy your MuJoCo license key (mjkey.txt) to ~/.mujoco/mjkey.txt:

3. Clone `softlearning`
```
git clone https://github.com/rail-berkeley/softlearning.git ${SOFTLEARNING_PATH}
```

4. Create and activate conda environment, install softlearning to enable command line interface.
```
cd ${SOFTLEARNING_PATH}
conda env create -f environment.yml
conda activate softlearning
pip install -e ${SOFTLEARNING_PATH}
```

The environment should be ready to run. See examples section for examples of how to train and simulate the agents.

Finally, to deactivate and remove the conda environment:
```
conda deactivate
conda remove --name softlearning --all
```

## Docker Installation

### docker-compose
To build the image and run the container:
```
export MJKEY="$(cat ~/.mujoco/mjkey.txt)" \
    && docker-compose \
        -f ./docker/docker-compose.dev.cpu.yml \
        up \
        -d \
        --force-recreate
```

You can access the container with the typical Docker [exec](https://docs.docker.com/engine/reference/commandline/exec/)-command, i.e.

```
docker exec -it softlearning bash
```

See examples section for examples of how to train and simulate the agents.

Finally, to clean up the docker setup:
```
docker-compose \
    -f ./docker/docker-compose.dev.cpu.yml \
    down \
    --rmi all \
    --volumes
```

## Examples
### Training and simulating an agent
1. To train the agent
```
softlearning run_example_local examples.development \
    --universe=gym \
    --domain=HalfCheetah \
    --task=v3 \
    --exp-name=my-sac-experiment-1 \
    --checkpoint-frequency=1000  # Save the checkpoint to resume training later
```

2. To simulate the resulting policy:
First, find the path that the checkpoint is saved to. By default (i.e. without specifying the `log-dir` argument to the previous script), the data is saved under `~/ray_results/<universe>/<domain>/<task>/<datatimestamp>-<exp-name>/<trial-id>/<checkpoint-id>`. For example: `~/ray_results/gym/HalfCheetah/v3/2018-12-12T16-48-37-my-sac-experiment-1-0/mujoco-runner_0_seed=7585_2018-12-12_16-48-37xuadh9vd/checkpoint_1000/`. The next command assumes that this path is found from `${SAC_CHECKPOINT_DIR}` environment variable.

```
python -m examples.development.simulate_policy \
    ${SAC_CHECKPOINT_DIR} \
    --max-path-length=1000 \
    --num-rollouts=1 \
    --render-mode=human
```

`examples.development.main` contains several different environments and there are more example scripts available in the  `/examples` folder. For more information about the agents and configurations, run the scripts with `--help` flag: `python ./examples/development/main.py --help`
```
optional arguments:
  -h, --help            show this help message and exit
  --universe {gym}
  --domain {...}
  --task {...}
  --num-samples NUM_SAMPLES
  --resources RESOURCES
                        Resources to allocate to ray process. Passed to
                        `ray.init`.
  --cpus CPUS           Cpus to allocate to ray process. Passed to `ray.init`.
  --gpus GPUS           Gpus to allocate to ray process. Passed to `ray.init`.
  --trial-resources TRIAL_RESOURCES
                        Resources to allocate for each trial. Passed to
                        `tune.run_experiments`.
  --trial-cpus TRIAL_CPUS
                        Resources to allocate for each trial. Passed to
                        `tune.run_experiments`.
  --trial-gpus TRIAL_GPUS
                        Resources to allocate for each trial. Passed to
                        `tune.run_experiments`.
  --trial-extra-cpus TRIAL_EXTRA_CPUS
                        Extra CPUs to reserve in case the trials need to
                        launch additional Ray actors that use CPUs.
  --trial-extra-gpus TRIAL_EXTRA_GPUS
                        Extra GPUs to reserve in case the trials need to
                        launch additional Ray actors that use GPUs.
  --checkpoint-frequency CHECKPOINT_FREQUENCY
                        Save the training checkpoint every this many epochs.
                        If set, takes precedence over
                        variant['run_params']['checkpoint_frequency'].
  --checkpoint-at-end CHECKPOINT_AT_END
                        Whether a checkpoint should be saved at the end of
                        training. If set, takes precedence over
                        variant['run_params']['checkpoint_at_end'].
  --restore RESTORE     Path to checkpoint. Only makes sense to set if running
                        1 trial. Defaults to None.
  --policy {gaussian}
  --env ENV
  --exp-name EXP_NAME
  --log-dir LOG_DIR
  --upload-dir UPLOAD_DIR
                        Optional URI to sync training results to (e.g.
                        s3://<bucket> or gs://<bucket>).
  --confirm-remote [CONFIRM_REMOTE]
                        Whether or not to query yes/no on remote run.
```

### Resume training from a saved checkpoint
In order to resume training from previous checkpoint, run the original example main-script, with an additional `--restore` flag. For example, the previous example can be resumed as follows:

```
softlearning run_example_local examples.development \
    --universe=gym \
    --domain=HalfCheetah \
    --task=v3 \
    --exp-name=my-sac-experiment-1 \
    --checkpoint-frequency=1000 \
    --restore=${SAC_CHECKPOINT_PATH}
```

# References
The algorithms are based on the following papers:

*Soft Actor-Critic Algorithms and Applications*.</br>
Tuomas Haarnoja*, Aurick Zhou*, Kristian Hartikainen*, George Tucker, Sehoon Ha, Jie Tan, Vikash Kumar, Henry Zhu, Abhishek Gupta, Pieter Abbeel, and Sergey Levine.
arXiv preprint, 2018.</br>
[paper](https://arxiv.org/abs/1812.05905)  |  [videos](https://sites.google.com/view/sac-and-applications)

*Latent Space Policies for Hierarchical Reinforcement Learning*.</br>
Tuomas Haarnoja*, Kristian Hartikainen*, Pieter Abbeel, and Sergey Levine.
International Conference on Machine Learning (ICML), 2018.</br>
[paper](https://arxiv.org/abs/1804.02808) | [videos](https://sites.google.com/view/latent-space-deep-rl)

*Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor*.</br>
Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine.
International Conference on Machine Learning (ICML), 2018.</br>
[paper](https://arxiv.org/abs/1801.01290) | [videos](https://sites.google.com/view/soft-actor-critic)

*Composable Deep Reinforcement Learning for Robotic Manipulation*.</br>
Tuomas Haarnoja, Vitchyr Pong, Aurick Zhou, Murtaza Dalal, Pieter Abbeel, Sergey Levine.
International Conference on Robotics and Automation (ICRA), 2018.</br>
[paper](https://arxiv.org/abs/1803.06773) | [videos](https://sites.google.com/view/composing-real-world-policies)

*Reinforcement Learning with Deep Energy-Based Policies*.</br>
Tuomas Haarnoja*, Haoran Tang*, Pieter Abbeel, Sergey Levine.
International Conference on Machine Learning (ICML), 2017.</br>
[paper](https://arxiv.org/abs/1702.08165) | [videos](https://sites.google.com/view/softqlearning/home)

If Softlearning helps you in your academic research, you are encouraged to cite our paper. Here is an example bibtex:
```
@techreport{haarnoja2018sacapps,
  title={Soft Actor-Critic Algorithms and Applications},
  author={Tuomas Haarnoja, Aurick Zhou, Kristian Hartikainen, George Tucker, Sehoon Ha, Jie Tan, Vikash Kumar, Henry Zhu, Abhishek Gupta, Pieter Abbeel, and Sergey Levine},
  journal={arXiv preprint arXiv:1812.05905},
  year={2018}
}
```
