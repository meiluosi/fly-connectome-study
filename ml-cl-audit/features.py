"""Extract frozen features: MNIST-20 via LeNet5 trained on KMNIST (84-d); CIFAR-100 via ImageNet ResNet18 penultimate (512-d, native 32x32)."""
import torch, torch.nn as nn, torchvision, numpy as np, time, os
torch.manual_seed(0); np.random.seed(0); dev="mps" if torch.backends.mps.is_available() else "cpu"; os.makedirs("data/features",exist_ok=True); T=torchvision.transforms
class LeNet5(nn.Module):
    def __init__(s):
        super().__init__(); s.c=nn.Sequential(nn.Conv2d(1,6,5,padding=2),nn.BatchNorm2d(6),nn.ReLU(),nn.MaxPool2d(2),nn.Conv2d(6,16,5),nn.BatchNorm2d(16),nn.ReLU(),nn.MaxPool2d(2))
        s.f1=nn.Sequential(nn.Linear(400,120),nn.ReLU(),nn.Linear(120,84),nn.ReLU()); s.out=nn.Linear(84,10)
    def feats(s,x): return s.f1(s.c(x).flatten(1))
    def forward(s,x): return s.out(s.feats(x))
def tens(ds): return ds.data.float().div(255).unsqueeze(1), ds.targets.long()
t0=time.time(); kt=torchvision.datasets.KMNIST("data",train=True); X,y=tens(kt); X,y=X.to(dev),y.to(dev); net=LeNet5().to(dev); opt=torch.optim.Adam(net.parameters(),1e-3)
for ep in range(25):
    perm=torch.randperm(len(X),device=dev); net.train(); tot=0
    for i in range(0,len(X),64):
        idx=perm[i:i+64]; loss=nn.functional.cross_entropy(net(X[idx]),y[idx]); opt.zero_grad(); loss.backward(); opt.step(); tot+=loss.item()*len(idx)
    if ep%5==4: print("LeNet5 epoch",ep+1,"loss %.4f"%(tot/len(X)),round(time.time()-t0),"s",flush=True)
net.eval(); kte=torchvision.datasets.KMNIST("data",train=False); Xt,yt=tens(kte)
with torch.no_grad(): print("KMNIST test acc %.4f"%(net(Xt.to(dev)).argmax(1).cpu()==yt).float().mean().item())
def enc(ds):
    X,y=tens(ds)
    with torch.no_grad(): return net.feats(X.to(dev)).cpu().numpy(), y.numpy()
out={}
for name,cls,off in [("mnist",torchvision.datasets.MNIST,0),("fmnist",torchvision.datasets.FashionMNIST,10)]:
    for tr in (True,False): f,l=enc(cls("data",train=tr)); out[f"{name}_{'train' if tr else 'test'}"]=(f,l+off)
np.savez("data/features/mnist20.npz",Xtr=np.concatenate([out["mnist_train"][0],out["fmnist_train"][0]]),ytr=np.concatenate([out["mnist_train"][1],out["fmnist_train"][1]]),Xte=np.concatenate([out["mnist_test"][0],out["fmnist_test"][0]]),yte=np.concatenate([out["mnist_test"][1],out["fmnist_test"][1]]))
print("mnist20 saved; feature dim",out["mnist_train"][0].shape[1],"nonneg:",bool((out["mnist_train"][0]>=0).all()))
rn=torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1); rn.fc=nn.Identity(); rn=rn.to(dev).eval()
mean=torch.tensor([0.485,0.456,0.406],device=dev).view(1,3,1,1); std=torch.tensor([0.229,0.224,0.225],device=dev).view(1,3,1,1)
def cenc(ds):
    X=torch.tensor(ds.data).permute(0,3,1,2).float().div(255); fs=[]
    with torch.no_grad():
        for i in range(0,len(X),500): fs.append(rn((X[i:i+500].to(dev)-mean)/std).cpu().numpy())
    return np.concatenate(fs),np.array(ds.targets)
a=cenc(torchvision.datasets.CIFAR100("data",train=True)); b=cenc(torchvision.datasets.CIFAR100("data",train=False)); np.savez("data/features/cifar100.npz",Xtr=a[0],ytr=a[1],Xte=b[0],yte=b[1]); print("cifar100 saved",a[0].shape,round(time.time()-t0),"s")
