const S=require('./sim.js'), D=require('./data.json'); const C=S.makeCircuit(D); let ok=0; const A=(c,m)=>{ if(!c){console.error('FAIL:',m); process.exit(1);} ok++; };
// 1. shapes, signs, 5% sparse code
A(C.NK===2045&&C.NG===65&&C.NM===49,'shapes'); const w0=new S.World(C,0); const rng=new S.RNG(1); const P=C.P0;
const code=S.kcCode(C,w0.odors[0],P,rng); A(code.length===102,'5% code');
// 2. initial valence 0 for every circuit
for(const kind of ['real','shuffled','random','real_binary']){ const Pk=S.makeP(C,kind,new S.RNG(2)); const mb=new S.MB(C,0.15); for(const o of w0.odors){ A(Math.abs(mb.valence(S.kcCode(C,o,Pk,rng)))<1e-6,'initial valence '+kind);} }
// 3. learning direction + generalisation to the similar odour (shares 4/6) more than to a dissimilar one
let mb=new S.MB(C,0.15); const cA=S.kcCode(C,w0.odors[0],P,rng),cA2=S.kcCode(C,w0.odors[1],P,rng),cB=S.kcCode(C,w0.odors[3],P,rng);
for(let i=0;i<30;i++) mb.update(cA,1-mb.valence(cA)); const vA=mb.valence(cA),vA2=mb.valence(cA2),vB=mb.valence(cB); A(vA>0.3&&vA2>vB+0.02&&vA>vA2,`generalisation ${vA} ${vA2} ${vB}`);
for(let i=0;i<30;i++) mb.update(cA,-1-mb.valence(cA)); A(mb.valence(cA)<0,'reversal');
// 4. lesions
mb=new S.MB(C,0.15); mb.blocked.fill(1); for(let i=0;i<20;i++) mb.update(cA,1); A(Math.abs(mb.valence(cA))<1e-6,'plasticity block');
mb=new S.MB(C,0.15); for(let i=0;i<20;i++) mb.update(cA,1); mb.silenced.fill(1); A(Math.abs(mb.valence(cA))<1e-6,'silencing');
// 5. determinism
const run=(kind,seed,T,conflict)=>{ const w=new S.World(C,seed,{conflict}); const f=new S.Fly(C,w,kind,5000+seed); let tot=0; for(let t=0;t<T;t++) tot+=f.step(t); return tot; };
A(run('real',3,1500)===run('real',3,1500),'determinism');
// 6. statistical parity with the Python preregistered evaluation (200 worlds): Python means consistent: real +44.0, linear +46.2, none +0.5 ; conflict: real +35.9, linear +31.5
const N=60, mean=(kind,conflict)=>{ let s=0; for(let k=0;k<N;k++) s+=run(kind,100+k,6000,conflict); return s/N; };
const res={ real_c:mean('real',false), lin_c:mean('linear',false), none_c:mean('none',false), real_x:mean('real',true), lin_x:mean('linear',true), rand_c:mean('random',false) };
console.log('JS means over',N,'worlds:',JSON.stringify(Object.fromEntries(Object.entries(res).map(([k,v])=>[k,+v.toFixed(1)]))));
A(Math.abs(res.real_c-44.0)<7,'parity real consistent'); A(Math.abs(res.lin_c-46.2)<7,'parity linear consistent'); A(Math.abs(res.none_c-0.5)<4,'parity none'); A(Math.abs(res.real_x-35.9)<7,'parity real conflict'); A(Math.abs(res.lin_x-31.5)<8,'parity linear conflict');
// 7. ants: Python 20-world pilot gave ~ +174 (consistent) per colony of 20
let as=0; const NA=12; for(let k=0;k<NA;k++){ const w=new S.World(C,100+k); const a=new S.Ants(w,20,5000+k); for(let t=0;t<6000;t++) a.step(t); as+=a.reward; } console.log('JS ants mean over',NA,'worlds:',(as/NA).toFixed(1)); A(Math.abs(as/NA-174)<30,'parity ants');
console.log('test_sim.js passed ('+ok+' checks)');
