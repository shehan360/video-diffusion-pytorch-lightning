import torch
import argparse
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from video_diffusion_pytorch import Unet3D, GaussianDiffusion
import torch.optim.lr_scheduler as lr_scheduler
from data import VideoData
from matplotlib import pyplot as plt
from matplotlib import animation
from VideoDiffusion import VideoDiffusion



pl.seed_everything(1234)

parser = argparse.ArgumentParser()
parser = pl.Trainer.add_argparse_args(parser)
parser.add_argument('--resolution', type=int, default=64)
parser.add_argument('--sequence_length', type=int, default=16)
parser.add_argument('--timesteps', type=int, default=1000)
parser.add_argument('--loss', type=str, default='l1')
parser.add_argument('--batch_size', type=int, default=8)
parser.add_argument('--num_workers', type=int, default=8)
parser.add_argument('--lr', type=float, default=2e-5)
parser.add_argument('--ckpt_path', type=str)
args = parser.parse_args()

kwargs = {'args': args}
model = VideoDiffusion.load_from_checkpoint(checkpoint_path='epoch=0-step=94217.ckpt', **kwargs)



videos = model.diffusion.sample(batch_size=4)

videos = ((videos + 0.5) * 255).cpu().numpy().astype('uint8')

fig = plt.figure()
plt.title('real (left), reconstruction (right)')
plt.axis('off')
im = plt.imshow(videos[0, :, :, :])

def init():
    im.set_data(videos[0, :, :, :])

def animate(i):
    im.set_data(videos[i, :, :, :])
    return im

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=videos.shape[0], interval=40)  # 200ms = 5 fps
plt.show()
