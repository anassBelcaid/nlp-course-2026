/* Seeded, dependency-free Skip-gram with negative sampling.
 * The browser computes every checkpoint; animation only replays those results.
 * Also usable from Node: require('./word2vec-simulation.js').train().
 */
(function (root) {
  'use strict';
  function random(seed) {
    return () => {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
  const sigmoid = s => 1 / (1 + Math.exp(-s));
  const cosine = (a, b) => dot(a, b) / Math.sqrt(dot(a, a) * dot(b, b));
  function train(seed = 351, epochs = 30) {
    const rng = random(seed);
    const words = ['coffee', 'tea', 'car', 'bus', 'cat', 'dog', 'apple', 'pear',
      'drink', 'warm', 'drive', 'road', 'pet', 'furry', 'fruit', 'sweet'];
    const sentences = [];
    // A deliberately balanced artificial corpus: shared contexts are the only signal.
    for (let repeat = 0; repeat < 12; repeat++) {
      for (let w = 0; w < 8; w++) {
        const first = 8 + 2 * Math.floor(w / 2);
        const context = [first, first + 1];
        if (rng() < 0.5) context.reverse();
        sentences.push([context[0], w, context[1]]);
      }
    }
    const pairs = [], counts = words.map(() => words.map(() => 0));
    const frequencies = words.map(() => 0);
    for (const sentence of sentences) {
      sentence.forEach(w => frequencies[w]++);
      sentence.forEach((w, p) => {
        for (const q of [p - 1, p + 1]) {
          if (q >= 0 && q < sentence.length) {
            pairs.push([w, sentence[q]]); counts[w][sentence[q]]++;
          }
        }
      });
    }
    const weights = frequencies.map(n => n ** 0.75);
    const total = weights.reduce((s, n) => s + n, 0);
    function noise(r) {
      let value = r() * total;
      for (let i = 0; i < words.length; i++) {
        value -= weights[i]; if (value <= 0) return i;
      }
      return words.length - 1;
    }
    const dimensions = 8;
    const v = words.map(() => Array.from({length: dimensions}, () => rng() - 0.5));
    const u = words.map(() => Array.from({length: dimensions}, () => rng() - 0.5));
    // Keep the diagnostic examples fixed across epochs, including noise collisions.
    const diagnosticRng = random(seed + 1), evaluation = [];
    for (const [w, c] of pairs) {
      evaluation.push([w, c, 1]);
      for (let k = 0; k < 3; k++) evaluation.push([w, noise(diagnosticRng), 0]);
    }
    const snapshots = [], trace = [];
    function checkpoint(epoch) {
      const loss = evaluation.reduce((sum, [w, c, y]) => {
        const s = dot(v[w], u[c]);
        return sum + Math.max(s, 0) - y * s + Math.log1p(Math.exp(-Math.abs(s)));
      }, 0) / evaluation.length;
      snapshots.push({epoch, loss, center: v.map(a => [...a]), context: u.map(a => [...a]),
        coffeeTea: cosine(v[0], v[1]), carBus: cosine(v[2], v[3]), coffeeCar: cosine(v[0], v[2]),
        pairCosines: [0, 2, 4, 6].map(i => cosine(v[i], v[i + 1])),
        positiveScore: sigmoid(dot(v[0], u[8])), noiseScore: sigmoid(dot(v[0], u[10]))});
    }
    checkpoint(0);
    for (let epoch = 1; epoch <= epochs; epoch++) {
      const order = pairs.map((_, i) => i);
      for (let i = order.length - 1; i > 0; i--) {
        const j = Math.floor(rng() * (i + 1)); [order[i], order[j]] = [order[j], order[i]];
      }
      const rate = 0.035 * (1 - 0.85 * (epoch - 1) / epochs);
      for (const index of order) {
        const [w, c] = pairs[index];
        const batch = [[w, c, 1]];
        for (let k = 0; k < 3; k++) batch.push([w, noise(rng), 0]);
        if (epoch === 1 && trace.length === 0) trace.push(...batch);
        for (const [a, b, label] of batch) {
          const gradient = sigmoid(dot(v[a], u[b])) - label;
          const old = [...v[a]];
          for (let d = 0; d < dimensions; d++) {
            v[a][d] -= rate * gradient * u[b][d];
            u[b][d] -= rate * gradient * old[d];
          }
        }
      }
      checkpoint(epoch);
    }
    // Fit PCA once to the final eight target vectors; reuse that basis for every epoch.
    const final = snapshots[snapshots.length - 1].center.slice(0, 8);
    const mean = Array.from({length: dimensions}, (_, d) => final.reduce((sum, v) => sum + v[d], 0) / 8);
    const centered = final.map(v => v.map((x, d) => x - mean[d]));
    const covariance = mean.map((_, i) => mean.map((_, j) => centered.reduce((sum, v) => sum + v[i] * v[j], 0) / 8));
    const basis = [];
    for (let component = 0; component < 2; component++) {
      let axis = mean.map((_, d) => Math.sin((d + 1) * (component + 1)));
      for (let iteration = 0; iteration < 200; iteration++) {
        axis = covariance.map(row => dot(row, axis));
        for (const previous of basis) {
          const projection = dot(axis, previous);
          axis = axis.map((x, d) => x - projection * previous[d]);
        }
        const norm = Math.sqrt(dot(axis, axis));
        axis = axis.map(x => x / norm);
      }
      basis.push(axis);
    }
    for (const snapshot of snapshots) snapshot.projected = snapshot.center.slice(0, 8).map(v => basis.map(axis => dot(v.map((x, d) => x - mean[d]), axis)));
    return {seed, words, sentences, pairs, counts, frequencies, trace, snapshots, projection: {mean, basis},
      settings: {dimensions: 8, window: 1, negativesPerPair: 3, epochs,
        noise: 'frequency^0.75; sampled independently, collisions retained',
        diagnostic: 'mean binary cross entropy on a fixed positive/noise sample'}};
  }
  const api = {train, cosine};
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document === 'undefined') return;
  root.Word2VecSimulation = api;
  function mount() {
    if (!document.getElementById('w2v-demo')) return;
    const run = train(), $ = id => document.getElementById(id);
    root.word2vecRun = run;
    const {words, snapshots} = run;
    const groups = ['Drinks', 'Vehicles', 'Pets', 'Fruit'];
    const colors = ['#147d78', '#b54a32', '#6650a5', '#986509'];
    $('w2v-counts').innerHTML = '<thead><tr><th scope="col">Target</th><th scope="col">Context 1</th><th scope="col">Context 2</th></tr></thead><tbody>' +
      words.slice(0, 8).map((w, i) => { const c = 8 + 2 * Math.floor(i / 2); return `<tr><th scope="row" style="border-left:6px solid ${colors[Math.floor(i / 2)]}">${w}</th><td>${words[c]} <b>${run.counts[i][c]}</b></td><td>${words[c + 1]} <b>${run.counts[i][c + 1]}</b></td></tr>`; }).join('') + '</tbody>';
    $('w2v-slider').max = run.settings.epochs;
    let index = 0, timer = null;
    const color = Array.from({length: 8}, (_, i) => colors[Math.floor(i / 2)]);
    const extent = Math.max(...snapshots.flatMap(s => s.projected.flat().map(Math.abs))) * 1.2;
    function scatter(s) {
      const px = v => 350 + v / extent * 260, py = v => 175 - v / extent * 120;
      let svg = '<svg viewBox="0 0 700 350" role="img" aria-label="Eight learned word vectors projected onto a fixed PCA basis"><path d="M50 175H650 M350 30V310" stroke="#c1ced3" stroke-width="2"/><text x="620" y="337">PC 1</text><text x="20" y="28">PC 2</text>';
      const labels = [];
      s.projected.forEach((point, i) => {
        const trail = snapshots.slice(0, index + 1).filter((_, j) => j % 4 === 0 || j === index).map(t => `${px(t.projected[i][0])},${py(t.projected[i][1])}`).join(' ');
        const x = px(point[0]), y = py(point[1]), right = i % 2 === 1;
        const labelX = x + (right ? 16 : -16), width = words[i].length * 17;
        let labelY = y;
        for (const shift of (right ? [24, -18, 56, -50, 88, -82, 120, -114, 152, -146] : [-18, 24, -50, 56, -82, 88, -114, 120, -146, 152])) {
          const candidate = {left: right ? labelX : labelX - width, right: right ? labelX + width : labelX, top: y + shift - 27, bottom: y + shift + 5};
          if (candidate.top < 30 || candidate.bottom > 315) continue;
          if (labels.some(b => candidate.left < b.right + 6 && candidate.right > b.left - 6 && candidate.top < b.bottom + 5 && candidate.bottom > b.top - 5)) continue;
          labelY = y + shift; labels.push(candidate); break;
        }
        svg += `<polyline points="${trail}" fill="none" stroke="${color[i]}" stroke-opacity=".22" stroke-width="3"/><line x1="${x}" y1="${y}" x2="${labelX}" y2="${labelY - 10}" stroke="${color[i]}" stroke-opacity=".55"/><circle cx="${x}" cy="${y}" r="7" fill="${color[i]}"/><text x="${labelX}" y="${labelY}" text-anchor="${right ? 'start' : 'end'}" fill="${color[i]}">${words[i]}</text>`;
      });
      return svg + '</svg>';
    }
    function lossPlot() {
      const visible = snapshots.slice(0, index + 1), max = Math.max(...snapshots.map(s => s.loss)) * 1.1;
      const pts = visible.map(s => `${55 + s.epoch / run.settings.epochs * 610},${125 - s.loss / max * 95}`).join(' ');
      return `<svg viewBox="0 0 700 165" role="img" aria-label="Fixed-sample mean binary loss over training epochs"><path d="M55 20V125H670" fill="none" stroke="#c1ced3" stroke-width="2"/><polyline points="${pts}" fill="none" stroke="#147d78" stroke-width="4"/><text x="4" y="35">${max.toFixed(1)}</text><text x="22" y="131">0</text><text x="50" y="154">0</text><text x="540" y="154">${run.settings.epochs} epochs</text></svg>`;
    }
    function draw() {
      const s = snapshots[index];
      $('w2v-epoch').textContent = `Epoch ${s.epoch} / ${run.settings.epochs}`;
      $('w2v-slider').value = index;
      $('w2v-scatter').innerHTML = scatter(s);
      $('w2v-loss-plot').innerHTML = lossPlot();
      $('w2v-loss').textContent = s.loss.toFixed(3);

    }
    function pause() { clearInterval(timer); timer = null; $('w2v-play').textContent = 'Play training'; }
    $('w2v-play').onclick = () => {
      if (timer) { pause(); return; }
      if (index === snapshots.length - 1) index = 0;
      $('w2v-play').textContent = 'Pause';
      timer = setInterval(() => { index++; draw(); if (index === snapshots.length - 1) pause(); }, 220);
    };
    $('w2v-step').onclick = () => { pause(); index = Math.min(index + 1, snapshots.length - 1); draw(); };
    $('w2v-reset').onclick = () => { pause(); index = 0; draw(); };
    $('w2v-final').onclick = () => { pause(); index = snapshots.length - 1; draw(); };
    $('w2v-slider').oninput = event => { pause(); index = +event.target.value; draw(); };
    // Arrow keys in the slider should change its value, not advance the deck.
    $('w2v-slider').addEventListener('keydown', event => event.stopPropagation());
    document.querySelectorAll('[data-w2v-download]').forEach(button => {
      button.onclick = () => {
        const url = URL.createObjectURL(new Blob([JSON.stringify(run, null, 2)], {type: 'application/json'}));
        const a = document.createElement('a'); a.href = url; a.download = 'word2vec-seed-351.json'; a.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      };
    });
    function attachReveal() {
      if (root.Reveal && root.Reveal.on) root.Reveal.on('slidechanged', pause);
    }
    attachReveal();
    draw();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
  else mount();
})(typeof window === 'undefined' ? globalThis : window);
