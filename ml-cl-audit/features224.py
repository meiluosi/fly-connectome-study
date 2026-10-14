import torch, torch.nn as nn, torchvision, numpy as np, time
dev="mps" if torch.backends.mps.is_available() else "cpu"; torch.manual_seed(0)
rn=torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1); rn.fc=nn.Identity(); rn=rn.to(dev).eval()
mean=torch.tensor([0.485,0.456,0.406],device=dev).view(1,3,1,1); std=torch.tensor([0.229,0.224,0.225],device=dev).view(1,3,1,1); t0=time.time()
def enc(ds):
    X=torch.tensor(ds.data).permute(0,3,1,2).float().div(255); fs=[]
    with torch.no_grad():
        for i in range(0,len(X),250):
            b=nn.functional.interpolate(X[i:i+250].to(dev),size=224,mode="bilinear",align_corners=False); fs.append(rn((b-mean)/std).cpu().numpy())
            if (i//250)%40==0: print(i,len(X),round(time.time()-t0),"s",flush=True)
    return np.concatenate(fs),np.array(ds.targets)
a=enc(torchvision.datasets.CIFAR100("data",train=True)); b=enc(torchvision.datasets.CIFAR100("data",train=False))
np.savez("data/features/cifar100_224.npz",Xtr=a[0],ytr=a[1],Xte=b[0],yte=b[1]); print("saved",a[0].shape,round(time.time()-t0),"s")
