const S=require('./sim.js'), D=require('./data.json'); const C=S.makeCircuit(D);
// regression: the single-fly path must be unchanged (determinism and the same mean as before)
const run=(kind,seed)=>{ const w=new S.World(C,seed); const f=new S.Fly(C,w,kind,5000+seed); let tot=0; for(let t=0;t<6000;t++) tot+=f.step(t); return tot; };
let a=0; for(let k=0;k<20;k++) a+=run('real',100+k); a/=20; console.log('single fly mean over 20 worlds',a.toFixed(1),'(earlier JS check: ~44)'); if(Math.abs(a-44)>9) { console.error('FAIL single-fly regression'); process.exit(1); }
// swarm parity with the Python preregistered evaluation (100 worlds; consistent): independent +274.2, attract +211.0, observe +353.5, broadcast +411.6
const N=12, mean=(mode)=>{ let s=0; for(let k=0;k<N;k++){ const w=new S.World(C,100+k); const sw=new S.FlySwarm(C,w,20,mode,8000+k); for(let t=0;t<6000;t++) sw.step(t); s+=sw.reward; } return s/N; };
const py={independent:274.2,attract:211.0,observe:353.5,broadcast:411.6}; const out={};
for(const m of Object.keys(py)){ out[m]=mean(m); console.log(m,'JS mean over',N,'worlds:',out[m].toFixed(1),'| Python (100 worlds):',py[m]); }
for(const m of Object.keys(py)) if(Math.abs(out[m]-py[m])>0.2*py[m]){ console.error('FAIL parity',m); process.exit(1); }
if(!(out.broadcast>out.observe && out.observe>out.independent && out.independent>out.attract)){ console.error('FAIL ordering'); process.exit(1); }
console.log('test_swarm.js passed (means within 20% of Python and the ordering broadcast > observe > independent > attract holds)');
