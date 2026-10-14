/* Fly foraging bench: simulation core (browser + Node). A line-by-line port of forage.py.
 * REAL: PN->KC wiring, KC top-5% code, KC->MBON wiring and neurotransmitter signs, MBON types/compartments (MaleCNS v1.0, right hemisphere).
 * HAND-WRITTEN: odour field, steering rule, reward schedule, bounded delta learning rule, ant colony rules. */
(function (root) {
  'use strict';
  const ARENA = 100;
  function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  class RNG {
    constructor(seed) { this.f = mulberry32(seed >>> 0); this.sp = null; }
    rand() { return this.f(); }
    int(n) { return Math.floor(this.f() * n); }
    uniform(a, b) { return a + (b - a) * this.f(); }
    normal() {
      if (this.sp !== null) { const v = this.sp; this.sp = null; return v; }
      let u = 0; while (u === 0) u = this.f(); const v = this.f(); const m = Math.sqrt(-2 * Math.log(u));
      this.sp = m * Math.sin(2 * Math.PI * v); return m * Math.cos(2 * Math.PI * v);
    }
    choice(n, k) { const a = Array.from({ length: n }, (_, i) => i); for (let i = 0; i < k; i++) { const j = i + this.int(n - i);[a[i], a[j]] = [a[j], a[i]]; } return a.slice(0, k); }
  }
  const clip = (x, lo, hi) => Math.min(hi, Math.max(lo, x));

  function makeCircuit(D) {
    const C = { NK: D.NK, NG: D.NG, NM: D.NM, signs: Int8Array.from(D.signs), nRow: Int32Array.from(D.nRow), nMbon: Int32Array.from(D.nMbon), nW: Float32Array.from(D.nW),
      mbonType: D.mbonType, mbonComp: D.mbonComp, gls: D.gls, kcType: D.kcType };
    C.P0 = { row: Int32Array.from(D.pRow), glom: Int32Array.from(D.pGlom), count: Float32Array.from(D.pCount) };
    return C;
  }
  /* PN->KC wiring variants. real | shuffled (per-KC glomerulus identities re-drawn, in-degree and counts kept) | random (6 random inputs, weight 1) | real_binary (real topology, counts=1) */
  function makeP(C, kind, rng) {
    const P0 = C.P0, NK = C.NK, NG = C.NG;
    if (kind === 'real') return P0;
    if (kind === 'real_binary') return { row: P0.row, glom: P0.glom, count: new Float32Array(P0.count.length).fill(1) };
    if (kind === 'shuffled') {
      const glom = new Int32Array(P0.glom.length);
      for (let k = 0; k < NK; k++) { const n = P0.row[k + 1] - P0.row[k]; const g = rng.choice(NG, n); for (let j = 0; j < n; j++) glom[P0.row[k] + j] = g[j]; }
      return { row: P0.row, glom, count: P0.count };
    }
    if (kind === 'random') {
      const row = new Int32Array(NK + 1), glom = new Int32Array(NK * 6), count = new Float32Array(NK * 6).fill(1);
      for (let k = 0; k < NK; k++) { row[k + 1] = (k + 1) * 6; const g = rng.choice(NG, 6); for (let j = 0; j < 6; j++) glom[k * 6 + j] = g[j]; }
      return { row, glom, count };
    }
    throw new Error('unknown circuit ' + kind);
  }
  /* top-5% KCs by summed input; ties broken with tiny random jitter (as in forage.py) */
  function kcCode(C, odorGloms, P, rng) {
    const mask = new Uint8Array(C.NG); for (const g of odorGloms) mask[g] = 1;
    const psi = new Float64Array(C.NK);
    for (let k = 0; k < C.NK; k++) { let s = 0; for (let e = P.row[k]; e < P.row[k + 1]; e++) if (mask[P.glom[e]]) s += P.count[e]; psi[k] = s + 1e-6 * rng.rand(); }
    const k5 = Math.floor(0.05 * C.NK); const idx = Array.from({ length: C.NK }, (_, i) => i); idx.sort((a, b) => psi[b] - psi[a]);
    return Int32Array.from(idx.slice(0, k5));
  }
  /* mushroom-body valence learner on the real KC->MBON edges. q in [0,1], q0 = 0.5. */
  class MB {
    constructor(C, eta) { this.C = C; this.eta = eta; this.q = new Float32Array(C.nW.length).fill(0.5); this.silenced = new Uint8Array(C.NM); this.blocked = new Uint8Array(C.NM); }
    valence(code) {
      const C = this.C; let b = 0, b0 = 0, sc = 0;
      for (let i = 0; i < code.length; i++) { const k = code[i];
        for (let e = C.nRow[k]; e < C.nRow[k + 1]; e++) { const m = C.nMbon[e]; if (this.silenced[m]) continue; const w = C.nW[e], s = C.signs[m]; b += w * this.q[e] * s; b0 += 0.5 * w * s; sc += 0.5 * w; } }
      return clip((b - b0) / Math.max(sc, 1e-9), -1, 1);
    }
    update(code, delta) {
      const C = this.C, g = this.eta * Math.abs(delta);
      for (let i = 0; i < code.length; i++) { const k = code[i];
        for (let e = C.nRow[k]; e < C.nRow[k + 1]; e++) { const m = C.nMbon[e]; if (this.blocked[m]) continue; const pot = delta * C.signs[m] > 0; const q = this.q[e]; this.q[e] = q + g * (pot ? (1 - q) : -q); } }
    }
  }
  class LinearValence {
    constructor(NG, eta) { this.w = new Float64Array(NG); this.eta = eta; }
    valence(x) { let s = 0, n = 0; for (const g of x) { s += this.w[g]; n++; } return clip(s / Math.max(n, 1), -1, 1); }
    update(x, delta) { const n = Math.max(x.length, 1); for (const g of x) this.w[g] += this.eta * delta / n * 3; }
  }
  class NoLearning { valence() { return 0; } update() { } }

  /* world: 6 sources in two odour families (variants share 4 of 6 glomeruli); a family's reward sign flips every `rev` ticks (plus manual flips) */
  class World {
    constructor(C, seed, opts) {
      opts = opts || {}; const r = new RNG(seed); this.C = C; this.rev = opts.rev || 3000; this.lam = 14; this.conflict = !!opts.conflict; this.flip = 0; this.rEat = 3;
      const odor = () => r.choice(C.NG, 6).sort((a, b) => a - b);
      const variant = (b) => { const keep = new Set(r.choice(6, 4).map(i => b[i])); while (keep.size < 6) keep.add(r.int(C.NG)); return Array.from(keep).sort((a, b) => a - b); };
      const A = odor(), B = odor(); this.odors = [A, variant(A), variant(A), B, variant(B), variant(B)];
      this.family = this.conflict ? [0, 1, 0, 1, 0, 1] : [0, 0, 0, 1, 1, 1];
      this.pos = []; let guard = 0;
      while (this.pos.length < 6 && guard++ < 10000) { const p = [r.uniform(10, ARENA - 10), r.uniform(10, ARENA - 10)]; if (this.pos.every(q => Math.hypot(p[0] - q[0], p[1] - q[1]) > 22)) this.pos.push(p); }
      this.refr = new Float64Array(6);
    }
    rewardValue(i, t) { const ph = (Math.floor(t / this.rev) + this.flip) % 2; return ((this.family[i] === 0) === (ph === 0)) ? 1 : -1; }
    conc(x, y, out) { for (let i = 0; i < 6; i++) out[i] = Math.exp(-Math.hypot(this.pos[i][0] - x, this.pos[i][1] - y) / this.lam); return out; }
    clone() { const w = Object.create(World.prototype); Object.assign(w, this); w.refr = new Float64Array(6); return w; }
  }
  function reflect(a) { for (let ax = 0; ax < 2; ax++) { if (a.pos[ax] < 0) { a.pos[ax] = -a.pos[ax]; a.th = ax === 0 ? Math.PI - a.th : -a.th; } if (a.pos[ax] > ARENA) { a.pos[ax] = 2 * ARENA - a.pos[ax]; a.th = ax === 0 ? Math.PI - a.th : -a.th; } } }

  /* the fly. kind: real | shuffled | random | real_binary | linear | none */
  class Fly {
    constructor(C, world, kind, seed, params) {
      this.C = C; this.w = world; this.kind = kind; this.r = new RNG(seed); this.prm = Object.assign({ gInn: 0.3, sigma: 0.12, speed: 1 }, params || {});
      const isMB = ['real', 'shuffled', 'random', 'real_binary'].includes(kind);
      if (isMB) { this.P = makeP(C, kind, new RNG(seed + 777)); this.learner = new MB(C, 0.4); this.gLearn = 2; this.kTurn = 1.4; this.codes = world.odors.map(o => kcCode(C, o, this.P, this.r)); }
      else if (kind === 'linear') { this.learner = new LinearValence(C.NG, 1.0); this.gLearn = 2; this.kTurn = 1.4; this.codes = world.odors; }
      else { this.learner = new NoLearning(); this.gLearn = 0; this.kTurn = 0.45; this.codes = world.odors; }
      this.pos = [ARENA / 2 + 5 * this.r.normal(), ARENA / 2 + 5 * this.r.normal()]; this.th = this.r.uniform(0, 2 * Math.PI);
      this.val = this.codes.map(c => this.learner.valence(c)); this.cL = new Float64Array(6); this.cR = new Float64Array(6); this.events = []; this.reward = 0;
    }
    refreshValence() { this.val = this.codes.map(c => this.learner.valence(c)); }
    step(t, skipRefr, social) {
      const w = this.w, p = this.prm, hx = Math.cos(this.th), hy = Math.sin(this.th);
      w.conc(this.pos[0] - 1.5 * hy, this.pos[1] + 1.5 * hx, this.cL); w.conc(this.pos[0] + 1.5 * hy, this.pos[1] - 1.5 * hx, this.cR);
      let dl = 0, dr = 0; for (let i = 0; i < 6; i++) { const wt = p.gInn + this.gLearn * this.val[i]; dl += this.cL[i] * wt; dr += this.cR[i] * wt; }
      if (social) { const sc = social(this, [this.pos[0] - 1.5 * hy, this.pos[1] + 1.5 * hx], [this.pos[0] + 1.5 * hy, this.pos[1] - 1.5 * hx]); dl += sc[0]; dr += sc[1]; }
      this.th += this.kTurn * (dl - dr) / (Math.abs(dl) + Math.abs(dr) + 0.02) + p.sigma * this.r.normal();
      this.pos[0] += p.speed * Math.cos(this.th); this.pos[1] += p.speed * Math.sin(this.th); reflect(this);
      if (!skipRefr) for (let i = 0; i < 6; i++) w.refr[i] = Math.max(w.refr[i] - 1, 0);
      let rt = 0;
      for (let i = 0; i < 6; i++) {
        if (Math.hypot(w.pos[i][0] - this.pos[0], w.pos[i][1] - this.pos[1]) < w.rEat && w.refr[i] === 0) {
          const rv = w.rewardValue(i, t); rt += rv; w.refr[i] = 30; this.learner.update(this.codes[i], rv - this.val[i]); this.refreshValence(); this.events.push({ t, i, rv });
        }
      }
      this.reward += rt; return rt;
    }
  }
  /* ant colony: stigmergy only (no odour sensing); a pheromone field on a 50x50 grid; ants return food to the nest depositing pheromone; touching a punishing source costs 1 and sends the ant home */
  class Ants {
    constructor(world, n, seed, params) {
      this.w = world; this.r = new RNG(seed); this.n = n; this.prm = Object.assign({ rho: 0.01, Q: 1, alpha: 3, cell: 2 }, params || {}); this.G = Math.floor(ARENA / this.prm.cell);
      this.tau = new Float64Array(this.G * this.G); this.nest = [ARENA / 2, ARENA / 2]; this.pos = []; this.th = []; this.carry = []; this.reward = 0;
      for (let a = 0; a < n; a++) { this.pos.push([this.nest[0] + this.r.normal(), this.nest[1] + this.r.normal()]); this.th.push(this.r.uniform(0, 2 * Math.PI)); this.carry.push(false); }
    }
    cellOf(p) { const c = this.prm.cell, G = this.G; return Math.min(G - 1, Math.max(0, Math.floor(p[0] / c))) * G + Math.min(G - 1, Math.max(0, Math.floor(p[1] / c))); }
    step(t) {
      const w = this.w, pr = this.prm, r = this.r; let rt = 0;
      for (let i = 0; i < this.tau.length; i++) this.tau[i] *= (1 - pr.rho);
      for (let i = 0; i < 6; i++) w.refr[i] = Math.max(w.refr[i] - 1, 0);
      for (let a = 0; a < this.n; a++) {
        const o = { pos: this.pos[a], th: this.th[a] };
        if (this.carry[a]) {
          const vx = this.nest[0] - o.pos[0], vy = this.nest[1] - o.pos[1]; o.th = Math.atan2(vy, vx) + 0.15 * r.normal();
          o.pos[0] += Math.cos(o.th); o.pos[1] += Math.sin(o.th); this.tau[this.cellOf(o.pos)] += pr.Q;
          if (Math.hypot(this.nest[0] - o.pos[0], this.nest[1] - o.pos[1]) < 4) { this.carry[a] = false; rt += 1; }
        } else {
          const cand = [-0.5, 0, 0.5].map(d => o.th + d); const ph = cand.map(c => this.tau[this.cellOf([o.pos[0] + 4 * Math.cos(c), o.pos[1] + 4 * Math.sin(c)])] + 0.05);
          const pw = ph.map(x => Math.pow(x, pr.alpha)); const s = pw[0] + pw[1] + pw[2]; let u = r.rand() * s, j = 0; while (j < 2 && u > pw[j]) { u -= pw[j]; j++; }
          o.th = cand[j] + 0.25 * r.normal(); o.pos[0] += Math.cos(o.th); o.pos[1] += Math.sin(o.th); reflect(o);
          for (let i = 0; i < 6; i++) {
            if (Math.hypot(w.pos[i][0] - o.pos[0], w.pos[i][1] - o.pos[1]) < w.rEat && w.refr[i] === 0) {
              const rv = w.rewardValue(i, t); w.refr[i] = 30;
              if (rv > 0) this.carry[a] = true; else { rt += rv; o.pos[0] = this.nest[0] + r.normal(); o.pos[1] = this.nest[1] + r.normal(); }
              break;
            }
          }
        }
        this.th[a] = o.th;
      }
      this.reward += rt; return rt;
    }
  }

  /* fly swarm: n flies, each with its OWN mushroom body (real wiring), sharing one world (shared depletion = competition).
   * mode: independent | attract (hand-written social attraction) | observe (nearby flies get a smaller prediction-error update) | broadcast (everyone; ant-like shared memory, NOT biological) */
  class FlySwarm {
    constructor(C, world, n, mode, seed, opts) {
      this.C = C; this.w = world; this.n = n; this.mode = mode; this.o = Object.assign({ gSoc: 0.5, Robs: 20, alphaObs: 0.5 }, opts || {}); this.reward = 0;
      this.flies = []; for (let i = 0; i < n; i++) this.flies.push(new Fly(C, world, 'real', seed + 101 * i + 1));
      this.social = mode === 'attract' ? (self, pl, pr) => { let sl = 0, sr = 0; for (const f of this.flies) { if (f === self) continue; const dl = Math.hypot(pl[0] - f.pos[0], pl[1] - f.pos[1]), dr = Math.hypot(pr[0] - f.pos[0], pr[1] - f.pos[1]); sl += 1 / (1 + (dl / 8) * (dl / 8)); sr += 1 / (1 + (dr / 8) * (dr / 8)); } return [this.o.gSoc * sl * 0.1, this.o.gSoc * sr * 0.1]; } : null;
    }
    step(t) {
      const w = this.w; for (let i = 0; i < 6; i++) w.refr[i] = Math.max(w.refr[i] - 1, 0); let tot = 0;
      for (const f of this.flies) {
        const before = f.events.length; tot += f.step(t, true, this.social);
        if ((this.mode === 'observe' || this.mode === 'broadcast') && f.events.length > before) {
          for (let e = before; e < f.events.length; e++) { const ev = f.events[e];
            for (const g of this.flies) { if (g === f) continue;
              if (this.mode === 'broadcast' || Math.hypot(g.pos[0] - f.pos[0], g.pos[1] - f.pos[1]) < this.o.Robs) { g.learner.update(g.codes[ev.i], this.o.alphaObs * (ev.rv - g.val[ev.i])); g.refreshValence(); } } }
        }
        if (f.events.length > 64) f.events.splice(0, 32);
      }
      this.reward += tot; return tot;
    }
  }
  const api = { ARENA, RNG, makeCircuit, makeP, kcCode, MB, LinearValence, NoLearning, World, Fly, Ants, FlySwarm, clip };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.FlySim = api;
})(typeof self !== 'undefined' ? self : this);
